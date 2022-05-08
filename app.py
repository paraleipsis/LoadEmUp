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
        self.tabWidget.tabBar().setVisible(False)
        if self.tabWidget.currentIndex() == 0:
            for i in range(8, 12):
                exec(f'self.pushButton_{i}.hide()')
        else:
            for i in range(8, 12):
                exec(f'self.pushButton_{i}.show()')

    def buttons_handler(self) -> None:
        # register buttons in app
        # download files
        self.pushButton.clicked.connect(self.download_file) # connect download button in ui w/ download method
        self.pushButton_2.clicked.connect(self.browser_handler_for_file)

        # download single yt video
        self.pushButton_5.clicked.connect(self.get_video_data)
        self.pushButton_3.clicked.connect(self.browser_handler_for_yt_video)
        self.pushButton_4.clicked.connect(self.download_yt_video)

        # download yt playlist
        self.pushButton_7.clicked.connect(self.download_yt_playlist)
        self.pushButton_6.clicked.connect(self.browser_handler_for_yt_playlist)

        # tab buttons
        self.pushButton_8.clicked.connect(lambda checked: self.open_tab(0))
        self.pushButton_9.clicked.connect(lambda checked: self.open_tab(1))
        self.pushButton_10.clicked.connect(lambda checked: self.open_tab(2))
        self.pushButton_11.clicked.connect(lambda checked: self.open_tab(3))

    # --------------------------------------------
    # methods for downloading files by direct link
    # --------------------------------------------
    def progress_handler_file(self, block_num: int, block_size: int, total_size: int) -> None:
        # progress bar
        readed_data = int(block_num * block_size)

        if total_size > 0:
            download_percentage = int(readed_data * 100 / total_size)
            self.progressBar.setValue(int(download_percentage))
            QApplication.processEvents()

    def browser_handler_for_file(self) -> None:
        # os file system browse to choose save location (by pic)
        save_location = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="All Files(*.*)")
        self.lineEdit_2.setText(str(save_location[0]))

    def save(self) -> None:
        # enter specific save location (by writing)
        pass

    def download_file(self) -> None:
        # download file by direct link
        download_url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()

        # input data validation
        if download_url == '' or save_location == '':
            QMessageBox.warning(self, 'Error', 'Enter fields should not be empty')
        else:
            try:
                urllib.request.urlretrieve(download_url, save_location, self.progress_handler_file)
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
    def browser_handler_for_yt_video(self) -> None:
        # os file system browse to choose save location
        save_location = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="All Files(*.*)")
        self.lineEdit_4.setText(str(save_location[0]))

    def get_video_data(self) -> None:
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

    def download_yt_video(self) -> None:
        video_url = self.lineEdit_3.text()
        save_location = self.lineEdit_4.text()

        if video_url == '' or save_location == '':
            QMessageBox.warning(self, 'Error', 'Enter fields should not be empty')

        else:
            video = pafy.new(video_url)
            video_stream = video.videostreams
            video_quality = self.comboBox.currentIndex()
            video_stream[video_quality].download(filepath=save_location, callback=self.progress_handler_yt_video)

    def progress_handler_yt_video(self, total: int, received: int, ratio: int, rate: int, time: int) -> None:
        read_data = received
        if total > 0:
            download_percentage = int(read_data * 100 / total)
            self.progressBar_2.setValue(int(download_percentage))
            remaining_time = int(round(time / 60, 2))

            self.label_5.setText(str(f'{remaining_time} minutes remaining'))
            QApplication.processEvents()

    # ---------------------------------------------
    # methods for downloading youtube playlist
    # ---------------------------------------------
    def download_yt_playlist(self) -> None:
        playlist_url = self.lineEdit_5.text()
        save_location = self.lineEdit_6.text()

        if playlist_url == '' or save_location == '':
            QMessageBox.warning(self, 'Error', 'Enter fields should not be empty')

        else:
            playlist = pafy.get_playlist2(playlist_url)
            playlist_videos = playlist['items']

            self.lcdNumber_2.display(len(playlist_videos))

            os.chdir(save_location)
            if os.path.exists(str(playlist['title'])):
                os.chdir(str(playlist['title']))
            else:
                os.mkdir(str(playlist['title']))
                os.chdir(str(playlist['title']))

            current_video_in_download = 1
            quality = self.comboBox_2.currentIndex()

            QApplication.processEvents()

            for video in playlist_videos:
                current_video = video['pafy']
                current_video_stream = current_video.videostreams
                self.lcdNumber.display(current_video_in_download)
                current_video_stream[quality].download(callback=self.progress_handler_yt_playlist)
                QApplication.processEvents()

                current_video_in_download += 1

    def progress_handler_yt_playlist(self, total, received, ratio, rate, time) -> None:
        read_data = received
        if total > 0:
            download_percentage = int(read_data * 100 / total)
            self.progressBar_3.setValue(int(download_percentage))
            remaining_time = int(round(time / 60, 2))

            self.label_6.setText(str(f'{remaining_time} minutes remaining'))
            QApplication.processEvents()

    def browser_handler_for_yt_playlist(self):
        save_location = QFileDialog.getExistingDirectory(self, 'Select Download Directory')
        self.lineEdit_6.setText(save_location)

    # ---------------------------------------------
    # methods for UI changes
    # ---------------------------------------------
    def open_tab(self, i: int):
        # open tabs by clicking on sidebar menu buttons
        self.tabWidget.setCurrentIndex(i)
        # if home tab checked then other tabs in sidebar menu should hide
        if self.tabWidget.currentIndex() == 0:
            for i in range(8, 12):
                exec(f'self.pushButton_{i}.hide()')
        else:
            for i in range(8, 12):
                exec(f'self.pushButton_{i}.show()')


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
