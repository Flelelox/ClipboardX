from PySide6.QtWidgets import (
    QMessageBox,
    QFileDialog,
    QInputDialog
)


class Dialogs:

    @staticmethod
    def confirm(parent, title, text):

        return QMessageBox.question(
            parent,
            title,
            text,
            QMessageBox.Yes | QMessageBox.No
        ) == QMessageBox.Yes

    @staticmethod
    def info(parent, title, text):

        QMessageBox.information(
            parent,
            title,
            text
        )

    @staticmethod
    def warning(parent, title, text):

        QMessageBox.warning(
            parent,
            title,
            text
        )

    @staticmethod
    def error(parent, title, text):

        QMessageBox.critical(
            parent,
            title,
            text
        )

    @staticmethod
    def save_file(parent,
                  title="Сохранить",
                  default="clipboard.txt"):

        filename, _ = QFileDialog.getSaveFileName(
            parent,
            title,
            default,
            "Text (*.txt)"
        )

        return filename

    @staticmethod
    def input(parent,
              title,
              label,
              default=""):

        text, ok = QInputDialog.getText(
            parent,
            title,
            label,
            text=default
        )

        if ok:
            return text

        return None