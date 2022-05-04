from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

import sys
import os

ui, _ = loadUiType('main.ui')


class MainApp(QMainWindow, ui):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.init_ui()
        self.buttons_handler()

    def init_ui(self):
        # contain all ui changes
        pass

    def buttons_handler(self):
        # handle buttons in app
        self.pushButton.clicked.connect(self.download) # connect download button in ui w/ download method

    def progress_handler(self):
        # progress bar
        pass

    def browse_handler(self):
        # os file system browse to choose save location (by pic)
        pass

    def save(self):
        # enter specific save location (by writing)
        pass

    def download(self):
        # download file
        print('Starting Download...')


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
