from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPixmap
from resize_ui import Ui_MainWindow
from PIL import Image
import cv2
import string
import random
import sys
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np

# Generates random game code
def rand(chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(8))

# Hierin moet de videocapturing komen
class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()


class MainWindows(QWidget):
    def __init__(self):
        super().__init__()
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)

        self.ui.stackedWidget.setCurrentWidget(self.ui.home)


        
        self.disply_width = self.ui.label_10.width()
        self.display_height = self.ui.label_10.height()

        self.ui.create.clicked.connect(self.create)
        self.ui.join.clicked.connect(self.join)
        self.ui.single.clicked.connect(self.single)
        self.ui.how.clicked.connect(self.how)

        self.ui.pushButton.clicked.connect(self.ret)
        self.ui.pushButton_2.clicked.connect(self.ret)
        self.ui.pushButton_3.clicked.connect(self.ret)
        self.ui.pushButton_4.clicked.connect(self.ret)
        self.ui.rooms.setSpacing(5)
        self.ui.rooms.clicked.connect(self.item_clicked)
        self.ui.rooms.setFocusPolicy(Qt.NoFocus)
        self.ui.label_10.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.ui.centralwidget.setStyleSheet('background-color:lightgrey')

    # Deze method gebruiken om items toe te voegen aan lijst van beschikbare rooms
    def add_item(self, item):
        item = QListWidgetItem(item)
        item.setTextAlignment(Qt.AlignHCenter)
        self.ui.rooms.addItem(item)

    # Deze methode gebruiken om naar een room te gaan, item is het gene dat geklikt
    # is (dus de gewenste room)
    def item_clicked(self):
        item = self.ui.rooms.currentItem().text()
        # print(item)

    def create(self):
        self.ui.label_7.setText(rand())
        self.ui.stackedWidget.setCurrentWidget(self.ui.create_game)

    def join(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.join_game)

    def how(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.how_to)

    # Roep deze method aan om over te gaan naar singleplayer widget
    def single(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.single_game)
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image_single)
        # start the thread
        self.thread.start()

    # Roep deze method aan om over te gaan naar multiplayer widget
    def multi(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.multi_game)
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image_multi)
        # start the thread
        self.thread.start()

    # Roep deze methode aan om de move van de tweede player in te vullen in de label
    # Voor multiplayer is de mode 1, single is de mode 0.
    def player2(self, mode, move):
        if mode == 1:
            self.ui.label_13.setText(move)
        else:
            self.ui.label_11.setText(move)

    def ret(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.home)
        # playsound('okay.mp3')

    # Kan gebruikt worden om de random gegenereerde code te krijgen.
    def get_code(self):
        return self.ui.label_7.text()

    def show(self):
        self.main_win.show()

    @pyqtSlot(np.ndarray)
    def update_image_single(self, cv_img):
        """Updates the image_label with a new opencv image"""
        cv_img = cv2.flip(cv_img, 1)
        qt_img = self.convert_cv_qt(cv_img)
        self.ui.label_10.setPixmap(qt_img)

    def update_image_multi(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.ui.label_12.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(
            rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(
            self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindows()
    main_win.show()
    sys.exit(app.exec_())
