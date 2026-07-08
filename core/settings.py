import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings:

    DEFAULTS = {
        "theme": "dark",
        "language": "ru",
        "clipboard_interval": 500,
        "max_history": 1000,
        "auto_start": False,
        "minimize_to_tray": True,
        "show_notifications": True,
        "save_duplicates": False,
        "window_width": 1100,
        "window_height": 700
    }

    def __init__(self):

        self.config_dir = BASE_DIR / "config"
        self.config_dir.mkdir(exist_ok=True)

        self.file = self.config_dir / "settings.json"

        self.data = {}

        self.load()

    def load(self):

        if not self.file.exists():

            self.data = self.DEFAULTS.copy()

            self.save()

            return

        try:

            with open(self.file, "r", encoding="utf-8") as f:

                self.data = json.load(f)

        except Exception:

            self.data = self.DEFAULTS.copy()

            self.save()

        # Добавляем новые параметры, если их нет
        for key, value in self.DEFAULTS.items():

            if key not in self.data:

                self.data[key] = value

        self.save()

    def save(self):

        with open(self.file, "w", encoding="utf-8") as f:

            json.dump(
                self.data,
                f,
                indent=4,
                ensure_ascii=False
            )

    def get(self, key, default=None):

        return self.data.get(key, default)

    def set(self, key, value):

        self.data[key] = value

        self.save()

    def reset(self):

        self.data = self.DEFAULTS.copy()

        self.save()

    @property
    def theme(self):
        return self.get("theme")

    @property
    def interval(self):
        return self.get("clipboard_interval")

    @property
    def max_history(self):
        return self.get("max_history")

    @property
    def notifications(self):
        return self.get("show_notifications")