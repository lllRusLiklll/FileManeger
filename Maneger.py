import sys
import os
import shutil
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtWidgets import QMessageBox, QLabel, QInputDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QCoreApplication, Qt


def human_read_format(size):
    if size >= 1024 ** 3:
        return '{}ГБ'.format(round(size / (1024 ** 3)))
    elif size >= 1024 ** 2:
        return '{}МБ'.format(round(size / (1024 ** 2)))
    elif size >= 1024:
        return '{}КБ'.format(round(size / 1024))
    else:
        return '{}Б'.format(size)


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('FileManeger.ui', self)

        self.label_2 = QLabel(self)
        frame = QtWidgets.QFrame.Box
        self.scrollArea.setFrameShape(frame)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.label_2)
        scroll_layout = QtWidgets.QVBoxLayout(self)
        scroll_layout.addWidget(self.scrollArea)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(scroll_layout)

        self.openButton.clicked.connect(self.open)
        self.deleteButton.clicked.connect(self.delete)
        self.copyButton.clicked.connect(self.copy)
        self.cutButton.clicked.connect(self.cut)
        self.renameButton.clicked.connect(self.rename)
        self.cleanButton.clicked.connect(self.clean)
        self.exitButton.clicked.connect(self.exit)

    def open(self):
        text = self.lineEdit.text()
        if os.path.isdir(text):
            files = os.listdir(text)
            self.label_2.setText('\n'.join(files))
            self.label_2.adjustSize()
            self.sizeLabel.setText(human_read_format(os.path.getsize(text)))
        elif os.path.isfile(text):
            if text.split('.')[1] in ['jpg', 'png', 'bmp']:
                pixmap = QPixmap(text)
                self.label_2.setPixmap(pixmap)
                self.label_2.resize(pixmap.width(), pixmap.height())
            elif text.split('.')[1] == 'txt':
                f = open(text, 'r')
                self.label_2.setText(f.read())
                self.label_2.adjustSize()
                f.close()
            self.sizeLabel.setText(human_read_format(os.path.getsize(text)))
        else:
            self.label_2.setText('Такого файла не существует. Попробуйте другой.')

    def delete(self):
        reply = QMessageBox.question(self, 'Удаление файла', "Вы уверены, что хотите удалить файл?",
                                           QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            text = self.lineEdit.text()
            if os.path.isdir(text):
                shutil.rmtree(text)
            elif os.path.isfile(text):
                os.remove(text)

    def copy(self):
        text = self.lineEdit.text()

        try:
            i, okBtnPressed = QInputDialog.getText(
                self, "Введите место", "Куда хотите скопировать?"
            )
            if okBtnPressed:
                shutil.copy2(text, i)
        except Exception:
            reply = QMessageBox.question(self, 'Ошибка', "Неправильно указан путь",
                                         QMessageBox.Ok, QMessageBox.Ok)

    def cut(self):
        text = self.lineEdit.text()

        try:
            i, okBtnPressed = QInputDialog.getText(
                self, "Введите место", "Куда хотите скопировать?"
            )
            if okBtnPressed:
                shutil.copy2(text, i)
                if os.path.isdir(text):
                    shutil.rmtree(text)
                elif os.path.isfile(text):
                    os.remove(text)
        except Exception:
            reply = QMessageBox.question(self, 'Ошибка', "Неправильно указан путь",
                                         QMessageBox.Ok, QMessageBox.Ok)

    def rename(self):
        text = self.lineEdit.text()

        try:
            i, okBtnPressed = QInputDialog.getText(
                self, "Введите имя", "Как переименовать файл?"
            )
            if okBtnPressed:
                os.rename(text, i)
        except Exception:
            reply = QMessageBox.question(self, 'Ошибка', "Невозможное имя файла",
                                         QMessageBox.Ok, QMessageBox.Ok)

    def clean(self):
        self.label_2.setText('')
        self.lineEdit.setText('')
        self.sizeLabel.setText('')

    def exit(self):
        reply = QMessageBox.question(self, 'Выход', "Вы точно хотите выйти?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QCoreApplication.exit()


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())