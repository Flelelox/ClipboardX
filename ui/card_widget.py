from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QSizePolicy
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor


class ClipboardCard(QFrame):

    def __init__(self, data):
        super().__init__()

        self.data = data

        self.build_ui()

    def build_ui(self):

        self.setObjectName("Card")

        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Minimum
        )

        layout = QHBoxLayout(self)

        layout.setContentsMargins(18, 18, 18, 18)

        layout.setSpacing(15)

        # ----------------------------

        left = QVBoxLayout()
        left.setSpacing(8)

        top = QHBoxLayout()

        self.tag = QLabel(self.data["tag"])
        self.tag.setObjectName("CardTag")

        top.addWidget(self.tag)

        top.addStretch()

        created = self.data.get("created", "")

        self.date = QLabel(created)
        self.date.setObjectName("CardDate")

        top.addWidget(self.date)

        left.addLayout(top)

        # ----------------------------

        text = self.data["text"]

        if len(text) > 400:
            text = text[:400] + "…"

        self.text = QLabel(text)
        self.text.setObjectName("CardText")

        self.text.setWordWrap(True)

        self.text.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )

        left.addWidget(self.text)

        layout.addLayout(left)

        # ----------------------------

        right = QVBoxLayout()
        right.setSpacing(8)

        self.favoriteButton = QPushButton()
        self.favoriteButton.setObjectName("IconButton")
        self.favoriteButton.setFixedSize(38, 38)
        self.favoriteButton.setToolTip("В избранное")
        self._update_favorite_icon()

        self.copyButton = QPushButton("📋")
        self.copyButton.setObjectName("IconButton")
        self.copyButton.setFixedSize(38, 38)
        self.copyButton.setToolTip("Скопировать")

        self.deleteButton = QPushButton("🗑")
        self.deleteButton.setObjectName("IconButton")
        self.deleteButton.setProperty("danger", "true")
        self.deleteButton.setFixedSize(38, 38)
        self.deleteButton.setToolTip("Удалить")

        right.addWidget(self.favoriteButton)
        right.addWidget(self.copyButton)
        right.addWidget(self.deleteButton)

        right.addStretch()

        layout.addLayout(right)

    def _update_favorite_icon(self):
        """Обновляет вид кнопки избранного в зависимости от состояния."""

        is_favorite = bool(self.data.get("favorite"))

        self.favoriteButton.setText("⭐" if is_favorite else "☆")
        self.favoriteButton.setProperty("active", "true" if is_favorite else "false")
        self.favoriteButton.style().unpolish(self.favoriteButton)
        self.favoriteButton.style().polish(self.favoriteButton)

    def set_favorite(self, value: bool):
        """Синхронизирует визуальное состояние избранного с данными."""

        self.data["favorite"] = value
        self._update_favorite_icon()