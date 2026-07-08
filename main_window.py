from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea
)

from PySide6.QtCore import (
    Qt,
    QPropertyAnimation,
    QEasingCurve,
    QRect
)

import pyperclip

from core.clipboard import ClipboardManager
from core.settings import Settings

from ui.sidebar import Sidebar
from ui.card_widget import ClipboardCard


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.settings = Settings()
        self.manager = ClipboardManager(self.settings)

        self.setWindowTitle("ClipboardX Pro")

        self.setMinimumSize(720, 480)

        self.resize(
            self.settings.get("window_width", 1100),
            self.settings.get("window_height", 700)
        )

        self.build_ui()

        self.manager.new_item.connect(
            self.on_new_item
        )

        self.load_history()

        self.update_sidebar()

        self.animate_show()

    # --------------------------------------------------

    def copy_text(self, text):

        try:

            pyperclip.copy(text)

            self.status.setText("📋 Текст скопирован")

        except Exception as e:

            self.status.setText(f"⚠️ Не удалось скопировать: {e}")

    # --------------------------------------------------

    def delete_item(self, record_id, widget):

        try:

            self.manager.delete(record_id)

        except Exception:

            pass

        widget.deleteLater()

        self.update_status()

        self.update_sidebar()

        self.update_empty_state()

    # --------------------------------------------------

    def toggle_favorite(self, row, card):
        """Переключает избранное точечно, без перерисовки всего списка."""

        value = not bool(row.get("favorite", False))

        self.manager.favorite(
            row["id"],
            value
        )

        row["favorite"] = value

        card.set_favorite(value)

        self.update_sidebar()

    # --------------------------------------------------

    def clear_history(self):

        from PySide6.QtWidgets import QMessageBox

        answer = QMessageBox.question(
            self,
            "ClipboardX",
            "Удалить всю историю? Это действие необратимо.",
            QMessageBox.Yes | QMessageBox.No
        )

        if answer != QMessageBox.Yes:
            return

        self.manager.clear()

        self.load_history()

        self.update_sidebar()

    # --------------------------------------------------

    def on_new_item(self, row):

        if self.search.text().strip():
            return

        self.add_card(row)

        self.update_status()

        self.update_sidebar()

        self.update_empty_state()

    # --------------------------------------------------

    def export_history(self):

        from PySide6.QtWidgets import QFileDialog

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Экспорт истории",
            "clipboard.txt",
            "Text (*.txt)"
        )

        if not filename:
            return

        self.manager.db.export_txt(filename)

        self.status.setText("✅ История экспортирована")

    # --------------------------------------------------

    def clear_cards(self):
        """Удаляет все карточки."""

        while self.cardsLayout.count() > 1:

            item = self.cardsLayout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

    # --------------------------------------------------

    def load_history(self):
        """Загрузить историю из базы."""

        self.clear_cards()

        rows = self.manager.get_history()

        for row in rows:
            self.add_card(row)

        self.update_status()

        self.update_empty_state()

    # --------------------------------------------------

    def add_card(self, row):

        card = ClipboardCard(row)

        self.cardsLayout.insertWidget(0, card)

        card.copyButton.clicked.connect(
            lambda _, text=row["text"]:
            self.copy_text(text)
        )

        card.deleteButton.clicked.connect(
            lambda _, rid=row["id"], w=card:
            self.delete_item(rid, w)
        )

        card.favoriteButton.clicked.connect(
            lambda _, r=row, c=card:
            self.toggle_favorite(r, c)
        )

    # --------------------------------------------------

    def search_items(self):

        text = self.search.text().strip()

        self.clear_cards()

        if text:
            rows = self.manager.search(text)
        else:
            rows = self.manager.get_history()

        for row in rows:
            self.add_card(row)

        self.update_status()

        self.update_empty_state(is_search=bool(text))

    # --------------------------------------------------

    def update_status(self):

        total = len(self.manager.get_history())

        self.status.setText(
            f"📋 Записей: {total}"
        )

    # --------------------------------------------------

    def update_empty_state(self, is_search=False):
        """Показывает подсказку, когда список карточек пуст."""

        has_cards = self.cardsLayout.count() > 1

        if has_cards:
            self.emptyState.hide()
            return

        if is_search:
            self.emptyState.setText("🔍 Ничего не найдено")
        else:
            self.emptyState.setText(
                "📋 История пуста\nСкопируйте что-нибудь — запись появится здесь"
            )

        self.emptyState.show()

    # --------------------------------------------------

    def update_sidebar(self):

        rows = self.manager.get_history()

        stats = {
            "total": len(rows)
        }

        for row in rows:

            tag = row.get("tag", "📄 Text")

            stats[tag] = stats.get(tag, 0) + 1

        self.sidebar.update_stats(stats)

    # --------------------------------------------------

    def build_ui(self):

        root = QHBoxLayout(self)

        root.setContentsMargins(0, 0, 0, 0)

        root.setSpacing(0)

        # ---------- Sidebar ----------

        self.sidebar = Sidebar()

        root.addWidget(self.sidebar)

        # ---------- Content ----------

        content = QWidget()

        root.addWidget(content, 1)

        layout = QVBoxLayout(content)

        layout.setContentsMargins(28, 24, 28, 20)

        layout.setSpacing(16)

        # ---------- Header ----------

        title = QLabel("ClipboardX Pro")
        title.setStyleSheet("font-size:28px; font-weight:700;")

        subtitle = QLabel("История буфера обмена")
        subtitle.setObjectName("MutedLabel")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # ---------- Top ----------

        top = QHBoxLayout()
        top.setSpacing(10)

        self.search = QLineEdit()

        self.search.setPlaceholderText("🔍 Поиск по истории...")

        self.search.setClearButtonEnabled(True)

        self.search.textChanged.connect(
            self.search_items
        )

        self.exportButton = QPushButton("⬇ Экспорт")

        self.exportButton.clicked.connect(
            self.export_history
        )

        self.clearButton = QPushButton("🗑 Очистить")

        self.clearButton.setObjectName("DangerButton")

        self.clearButton.clicked.connect(
            self.clear_history
        )

        top.addWidget(self.search, 1)
        top.addWidget(self.exportButton)
        top.addWidget(self.clearButton)

        layout.addLayout(top)

        # ---------- Scroll ----------

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(True)

        self.scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.container = QWidget()

        self.cardsLayout = QVBoxLayout(
            self.container
        )

        self.cardsLayout.setSpacing(12)

        self.cardsLayout.addStretch()

        self.scroll.setWidget(
            self.container
        )

        layout.addWidget(
            self.scroll,
            1
        )

        # ---------- Empty state ----------

        self.emptyState = QLabel("")
        self.emptyState.setObjectName("EmptyState")
        self.emptyState.setAlignment(Qt.AlignCenter)
        self.emptyState.hide()

        layout.addWidget(self.emptyState)

        # ---------- Status ----------

        self.status = QLabel()
        self.status.setObjectName("StatusLabel")

        layout.addWidget(
            self.status
        )

    # --------------------------------------------------

    def animate_show(self):
        """Мягкое появление окна при старте приложения."""

        self.setWindowOpacity(0)

        geo = self.geometry()

        start = QRect(
            geo.x(),
            geo.y() + 16,
            geo.width(),
            geo.height()
        )

        self.moveAnim = QPropertyAnimation(
            self,
            b"geometry"
        )

        self.moveAnim.setDuration(260)

        self.moveAnim.setStartValue(start)

        self.moveAnim.setEndValue(geo)

        self.moveAnim.setEasingCurve(
            QEasingCurve.OutCubic
        )

        self.fadeAnim = QPropertyAnimation(
            self,
            b"windowOpacity"
        )

        self.fadeAnim.setDuration(260)

        self.fadeAnim.setStartValue(0)

        self.fadeAnim.setEndValue(1)

        self.moveAnim.start()

        self.fadeAnim.start()