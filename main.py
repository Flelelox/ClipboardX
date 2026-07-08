import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow

BASE_DIR = Path(__file__).resolve().parent


def load_stylesheet(app: QApplication) -> None:
    """Подключает общий QSS-стиль приложения."""

    qss_path = BASE_DIR / "ui" / "style.qss.css"

    try:
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print(f"Стиль не найден: {qss_path}")


def main():
    app = QApplication(sys.argv)

    app.setApplicationName("ClipboardX")
    app.setApplicationVersion("5.0")

    load_stylesheet(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()