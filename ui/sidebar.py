from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QFrame
)


class StatCard(QFrame):

    def __init__(self, icon: str, title: str):
        super().__init__()

        self.setObjectName("StatCard")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(4)

        self.title = QLabel(f"{icon} {title}")
        self.title.setObjectName("StatTitle")

        self.value = QLabel("0")
        self.value.setObjectName("StatValue")

        layout.addWidget(self.title)
        layout.addWidget(self.value)


class Sidebar(QWidget):

    def __init__(self):
        super().__init__()

        self.setObjectName("Sidebar")
        self.setFixedWidth(260)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 24, 20, 20)
        layout.setSpacing(10)

        title = QLabel("ClipboardX")
        title.setObjectName("SidebarTitle")

        subtitle = QLabel("Статистика")
        subtitle.setObjectName("SidebarSubtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(12)

        self.total = StatCard("📋", "Всего")
        self.urls = StatCard("🌐", "URL")
        self.emails = StatCard("📧", "Email")
        self.python = StatCard("🐍", "Python")
        self.json = StatCard("📦", "JSON")
        self.text = StatCard("📄", "Текст")

        layout.addWidget(self.total)
        layout.addWidget(self.urls)
        layout.addWidget(self.emails)
        layout.addWidget(self.python)
        layout.addWidget(self.json)
        layout.addWidget(self.text)

        layout.addStretch()

    def update_stats(self, stats: dict):
        """Обновление статистики."""

        self.total.value.setText(str(stats.get("total", 0)))
        self.urls.value.setText(str(stats.get("🌐 URL", 0)))
        self.emails.value.setText(str(stats.get("📧 Email", 0)))
        self.python.value.setText(str(stats.get("🐍 Python", 0)))
        self.json.value.setText(str(stats.get("📦 JSON", 0)))
        self.text.value.setText(str(stats.get("📄 Text", 0)))