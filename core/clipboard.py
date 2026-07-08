from datetime import datetime

from PySide6.QtCore import QObject, Signal, QTimer
import pyperclip

from core.database import Database
from core.settings import Settings
from core.tags import detect


class ClipboardManager(QObject):
    """
    Менеджер буфера обмена.

    Отслеживает изменения буфера Windows,
    автоматически определяет тип данных,
    сохраняет историю в SQLite.
    """

    new_item = Signal(dict)

    def __init__(self, settings: Settings = None):
        super().__init__()

        self.settings = settings or Settings()
        self.db = Database()

        self.last_text = ""

        self.timer = QTimer()
        self.timer.setInterval(self.settings.get("clipboard_interval", 500))
        self.timer.timeout.connect(self.check_clipboard)
        self.timer.start()

    def check_clipboard(self):
        """Проверка буфера обмена."""

        try:
            text = pyperclip.paste()

            if not isinstance(text, str):
                return

            text = text.strip()

            if not text:
                return

            if text == self.last_text:
                return

            self.last_text = text

            tag = detect(text)

            item_id = self.db.add_item(text, tag)

            item = {
                "id": item_id,
                "text": text,
                "tag": tag,
                "favorite": False,
                "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            self.new_item.emit(item)

        except Exception as e:
            print("Clipboard error:", e)

    def get_history(self):
        """Получить историю."""

        return self.db.load_items()

    def search(self, query):
        """Поиск."""

        return self.db.search(query)

    def clear(self):
        """Очистить историю."""

        self.db.clear()

    def delete(self, item_id):
        """Удалить запись."""

        self.db.delete_item(item_id)

    def favorite(self, item_id, value=True):
        """Добавить в избранное."""

        self.db.favorite(item_id, int(value))