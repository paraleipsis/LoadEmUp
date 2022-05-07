import pafy
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

import sys
import os
import urllib.request
import pafy
import humanize

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

    def buttons_handler(self) -> None:
        # register buttons in app
        # download files
        self.pushButton.clicked.connect(self.download) # connect download button in ui w/ download method
        self.pushButton_2.clicked.connect(self.browser_handler)

        # download single yt video
        self.pushButton_5.clicked.connect(self.get_video_data)
        self.pushButton_3.clicked.connect(self.save_browse)
        self.pushButton_4.clicked.connect(self.download_video)

    def progress_handler(self, block_num: int, block_size: int, total_size: int) -> None:
        # progress bar
        readed_data = block_num * block_size

        if total_size > 0:
            download_percentage = readed_data * 100 / total_size
            self.progressBar.setValue(int(download_percentage))
            QApplication.processEvents()

    # --------------------------------------------
    # methods for downloading files by direct link
    # --------------------------------------------
    def browser_handler(self) -> None:
        # os file system browse to choose save location (by pic)
        save_location = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="All Files(*.*)")
        self.lineEdit_2.setText(str(save_location[0]))

    def save(self):
        # enter specific save location (by writing)
        pass

    def download(self) -> None:
        # download file by direct link
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
                return None

        QMessageBox.information(self, 'Download Completed', 'Download Completed Successfully')

        # clear fields and progress bar after downloading
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.progressBar.setValue(0)

    # ---------------------------------------------
    # methods for downloading youtube single video
    # ---------------------------------------------
    def save_browse(self):
        # os file system browse to choose save location
        save_location = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="All Files(*.*)")
        self.lineEdit_4.setText(str(save_location[0]))

    def get_video_data(self):
        # information about video (quality, size, ...) in order to select a specific quality
        video_url = self.lineEdit_3.text()

        if video_url == '':
            QMessageBox.warning(self, 'Error', 'Enter fields should not be empty')
        else:
            video = pafy.new(video_url)
            video_stream = video.videostreams
            for stream in video_stream:
                size = humanize.naturalsize(stream.get_filesize()) # size in readable view
                data = f'{stream.mediatype} {stream.extension} {stream.quality} {size}'
                self.comboBox.addItem(data)

    def download_video(self):
        video_url = self.lineEdit_3.text()
        save_location = self.lineEdit_4.text()

        if video_url == '' or save_location == '':
            QMessageBox.warning(self, 'Error', 'Enter fields should not be empty')

        else:
            video = pafy.new(video_url)
            video_stream = video.videostreams
            video_quality = self.comboBox.currentIndex()
            video_stream[video_quality].download(filepath=save_location, callback=self.download_progress)

    def download_progress(self, total: int, received: int, ratio: int, rate: int, time: int) -> None:
        read_data = received
        if total > 0:
            download_percentage = int(read_data * 100 / total)
            self.progressBar_2.setValue(int(download_percentage))
            remaining_time = int(round(time / 60, 2))

            self.label_5.setText(str(f'{remaining_time} minutes remaining'))
            QApplication.processEvents()


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
