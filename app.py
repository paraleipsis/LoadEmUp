from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

import sys
import os
import urllib.request

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
        # register buttons in app
        self.pushButton.clicked.connect(self.download) # connect download button in ui w/ download method
        self.pushButton_2.clicked.connect(self.browser_handler)

    def progress_handler(self, block_num, block_size, total_size):
        # progress bar
        readed_data = block_num * block_size

        if total_size > 0:
            download_percentage = readed_data * 100 / total_size
            self.progressBar.setValue(int(download_percentage))
            QApplication.processEvents()

    def browser_handler(self):
        # os file system browse to choose save location (by pic)
        save_location = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="All Files(*.*)")
        self.lineEdit_2.setText(str(save_location[0]))

    def save(self):
        # enter specific save location (by writing)
        pass

    def download(self):
        # download file
        download_url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()

        # input data validation
        if download_url == '' or save_location == '':
            QMessageBox.warning(self, 'Error', 'Enter fields should not be empty')
        else:
            try:
                urllib.request.urlretrieve(download_url, save_location, self.progress_handler)
            except Exception:
                QMessageBox.warning(self, 'Download Error', 'Enter a valid URL or save location')
                return

        QMessageBox.information(self, 'Download Completed', 'Download Completed Successfully')

        # clear fields and progress bar after downloading
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.progressBar.setValue(0)


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
