# from concurrent.futures import thread
from http import client
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPixmap
from playsound import playsound
from GUI_mooier_ui import Ui_MainWindow
from PIL import Image
import cv2
import string
import random
import sys
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
import single_player
import steen_schaar
import client
import threading
import time


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

        self.disply_width = 360
        self.display_height = 390

        self.ui.create.clicked.connect(self.create)
        self.ui.join.clicked.connect(self.join)
        self.ui.single.clicked.connect(self.single)
        self.ui.how.clicked.connect(self.how)

        self.ui.pushButton.clicked.connect(self.ret)
        self.ui.pushButton_2.clicked.connect(self.ret)
        self.ui.pushButton_3.clicked.connect(self.ret)
        self.ui.pushButton_4.clicked.connect(self.ret)
        self.ui.pushButton_5.clicked.connect(self.start_single_player)

        self.ui.rooms.setSpacing(5)
        self.ui.rooms.clicked.connect(self.item_clicked)
        self.ui.rooms.setFocusPolicy(Qt.NoFocus)
        self.ui.pushButton_7.clicked.connect(self.join_code)
        self.ui.label_10.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.ui.label_11.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.ui.label_14.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.ui.label_16.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.ui.label_14.setText('0')
        self.ui.label_16.setText('0')

        self.ui.create_2.clicked.connect(self.create_and_join)
        self.ui.label_12.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.ui.label_13.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.ui.label_15.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.ui.label_17.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.ui.label_15.setText('0')
        self.ui.label_17.setText('0')

        self.ui.label_18.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.ui.label_19.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.ui.label_20.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.ui.label_21.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)


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
        room = item.split(' ')
        print(room[1])
        self.multi()
        speler = client.Client(steen_schaar.main, self.get_img, 'join', 'x' + room[1])
        speler.run_startup()
        # t1 = threading.Thread(target= client.random_pick)
        # t1.start()
        # t1.join()

    def join_code(self):
        code = self.ui.lineEdit.text()
        print(code)
        self.multi()
        speler = client.Client(steen_schaar.main, self.get_img, 'join', code)
        speler.run_startup()
        # t1 = threading.Thread(target= client.test_receive('join'))
        # t1.start()
        # t1.join()

    def create(self):
        self.ui.label_7.setText(rand())
        self.ui.stackedWidget.setCurrentWidget(self.ui.create_game)


    def join(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.join_game)

    def how(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.how_to)

    # def child(self):
    #     print('\nA new child ',  os.getpid())
    #     os._exit(0)

    def player_img(self, move):
        if move == 'scissor':
            afbeelding = 'schaar'
        elif move == 'rock':
            afbeelding = 'steen'
        elif move == 'paper':
            afbeelding = 'papier'
        pixmap = QPixmap(afbeelding)
        self.ui.label_10.setPixmap(pixmap)
        # self.ui.label_10.setAlignment(Qt.AlignCenter)

    def com_img(self, com_move):
        if com_move == 'scissor':
            afbeelding = 'schaar'
        elif com_move == 'rock':
            afbeelding = 'steen'
        elif com_move == 'paper':
            afbeelding = 'papier'
        pixmap = QPixmap(afbeelding)
        self.ui.label_11.setPixmap(pixmap)
        # self.ui.label_11.setAlignment(Qt.AlignCenter)

    def add_score_player(self,count):
        self.ui.label_14.setText(str(count))

    def add_score_com(self, count):
        self.ui.label_16.setText(str(count))

    def get_wins(self, results):
        play_w = results.count(0)
        com_w = results.count(1)
        return (play_w, com_w)

    def start_single_player(self):
        results = []
        for i in range (5):
            print(i)
            move = steen_schaar.main()
            com_move, result = single_player.random_com_move(move)

            self.player_img(move)
            self.com_img(com_move)

            final = single_player.get_winner(move, com_move)
            results.append(final)
            play_w, com_w = self.get_wins(results)
            self.add_score_com(com_w)
            self.add_score_player(play_w)
            # time.sleep(3)
        single_player.show_winner(results)

    # Roep deze method aan om over te gaan naar singleplayer widget
    def single(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.single_game)
        # self.thread = VideoThread()
        # connect its signal to the update_image slot
        # self.thread.change_pixmap_signal.connect(self.update_image_single)
        # start the thread
        # self.thread.start()

    def player1_img(self, move):
        print('move', move)
        if move == 'scissor':
            afbeelding = 'schaar'
        elif move == 'rock':
            afbeelding = 'steen'
        else :
            afbeelding = 'papier'
        pixmap = QPixmap(afbeelding)
        self.ui.label_12.setPixmap(pixmap)

    def player2_img(self, com_move):
        if com_move == 'scissor':
            afbeelding = 'schaar'
        elif com_move == 'rock':
            afbeelding = 'steen'
        elif com_move == 'paper':
            afbeelding = 'papier'
        pixmap = QPixmap(afbeelding)
        self.ui.label_13.setPixmap(pixmap)


    def get_wins(self, results):
        play1_w = results.count(0)
        play2_w = results.count(1)
        return (play1_w, play2_w)

    def create_and_join(self):
        room_code = self.ui.label_7.text()
        self.multi()
        speler = client.Client(steen_schaar.main, self.get_img, 'create', room_code)
        speler.run_startup()

    def play2_move_lost(self, play_move):
        if play_move == 'rock':
            return 'schaar'
        elif play_move == 'scissor':
            return 'papier'
        elif play_move == 'paper':
            return 'steen'

    def play2_move_won(self, play_move):
        if play_move == 'rock':
            return 'papier'
        elif play_move == 'scissor':
            return 'steen'
        elif play_move == 'paper':
            return 'schaar'

    def add_score_play1(self):
       score = self.ui.label_15.text()
       new_score = int(score) + 1
       self.ui.label_15.setText(str(new_score))

    def add_score_play2(self):
       score = self.ui.label_17.text()
       new_score = int(score) + 1
       self.ui.label_17.setText(str(new_score))


    def get_img(self, command, last_move):
        if (' ' in command):
            afbeelding = ''
            print('hopelijk goed', command)
            move = command.split(' ')
            if move[1] == 'scissor':
                afbeelding = 'schaar'
            elif move[1] == 'rock':
                afbeelding = 'steen'
            elif move[1] == 'paper':
                afbeelding = 'papier'
            pixmap = QPixmap(afbeelding)
            self.ui.label_12.setPixmap(pixmap)
        else:
            if command == 'draw':
                print('DRAW', last_move)
                if last_move == 'scissor':
                    afbeelding = 'schaar'
                elif last_move == 'rock':
                    afbeelding = 'steen'
                elif last_move == 'paper':
                    afbeelding = 'papier'
                pixmap = QPixmap(afbeelding)
                self.ui.label_13.setPixmap(pixmap)
            elif command == 'won':
                print('WON', last_move)
                move = self.play2_move_lost(last_move)
                pixmap = QPixmap(move)
                self.ui.label_13.setPixmap(pixmap)
                self.add_score_play1()
            elif command == 'lost':
                print("LOST", last_move)
                move = self.play2_move_won(last_move)
                pixmap = QPixmap(move)
                self.ui.label_13.setPixmap(pixmap)
                self.add_score_play2()
        time.sleep(3)


    # Roep deze method aan om over te gaan naar multiplayer widget
    def multi(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.multi_game)


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
