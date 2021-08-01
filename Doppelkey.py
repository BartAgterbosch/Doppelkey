import mouse
import keyboard
import sys
from webbrowser import open as launch
from threading import Thread
from time import sleep
from os import path
from PyQt5 import QtCore, QtGui, QtWidgets

global mouse_recording

mouse_recording = []
record_process = False
thread_count = 0

doppelkey_icon = path.join(getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__))),"./doppelkey.ico")
doppelkey_img = path.join(getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__))),"./doppelkey_img.png")

title = path.join(getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__))),"./title.png")
title_rec = path.join(getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__))),"./title_rec.png")
title_done = path.join(getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__))),"./title_done.png")
title_play = path.join(getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__))),"./title_play.png")
title_stop = path.join(getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__))),"./title_stop.png")

play_unpressed = path.join(getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__))),"./play_unpressed.png")
play_pressed = path.join(getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__))),"./play_pressed.png")
play_disabled = path.join(getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__))),"./play_disabled.png")

rec_unpressed = path.join(getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__))),"./rec_unpressed.png")
rec_pressed = path.join(getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__))),"./rec_pressed.png")
rec_disabled = path.join(getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__))),"./rec_disabled.png")


def instructions():
        launch("https://github.com/BartAgterbosch/Doppelkey/blob/main/README.md")


def playthread():
        global terminate

        num = 1
        terminate = False
        speed = speedbox.value()
        rep = repbox.value()
        
        infobutton.setDisabled(True)
        speedbox.setDisabled(True)
        repbox.setDisabled(True)
        playbutton.setChecked(True)
        sleep(0.2)
        playbutton.setChecked(False)
        sleep(0.2)
        playbutton.setDisabled(True)
        recbutton.setDisabled(True)
        titleframe.setPixmap(QtGui.QPixmap(title_play))       

        while ((num <= rep) and (not terminate)):
                mouse.move(pos[0], pos[1], absolute=True, duration=0)
                keyboard.play(keyboard_recordings, speed_factor=speed)
                mouse.play(mouse_recording, speed_factor=speed, include_wheel=True, include_clicks=True)
                num += 1
        playbutton.setDisabled(False)
        recbutton.setDisabled(False)
        speedbox.setDisabled(False)
        repbox.setDisabled(False)
        infobutton.setDisabled(False)
        terminate = True
        titleframe.setPixmap(QtGui.QPixmap(title))


def play():
        playthreadbg = Thread(target=playthread)
        playthreadbg.daemon = True
        playthreadbg.start()


def recordstart():
        global record_process
        global rec_present
        global mouse_recording
        global pos

        rec_present = False
        record_process = True
        mouse_recording = []

        if (playbutton.isEnabled()): rec_present = True
        recbutton.setChecked(True)
        sleep(0.2)
        recbutton.setChecked(False)
        sleep(0.2)
        infobutton.setDisabled(True)
        playbutton.setDisabled(True)
        repbox.setDisabled(True)
        speedbox.setDisabled(True)
        titleframe.setPixmap(QtGui.QPixmap(title_rec))
        pos = mouse.get_position()
        keyboard.start_recording()
        mouse.hook(mouse_recording.append)


def recordstop():
        global keyboard_recordings
        global mouse_recording
        global rec_present
        global record_process

        sleep(0.2)
        recbutton.setChecked(False)
        keyboard_recordings = keyboard.stop_recording()
        mouse.unhook(mouse_recording.append)
        infobutton.setDisabled(False)
        playbutton.setDisabled(False)
        repbox.setDisabled(False)
        speedbox.setDisabled(False)
        titleframe.setPixmap(QtGui.QPixmap(title_done))

        if (rec_present): playbutton.setDisabled(False) 
        record_process = False


def record():
        global thread_count
        global recordstartthread

        if (record_process):
                if (thread_count >= 1):
                        recordstopthread = Thread(target=recordstop)
                        recordstopthread.daemon = True
                recordstopthread.start()
        else:
                if (thread_count >= 1):
                        recordstartthread = Thread(target=recordstart)
                        recordstartthread.daemon = True
                recordstartthread.start()
        thread_count += 1

        if (thread_count == 1):
                f7thread = Thread(target=hotkey_f7)
                f7thread.daemon = True
                f7thread.start()


def hotkey_f8():
        while (True):
                keyboard.wait("f8")
                record()


def hotkey_f7():
        global terminate
        while (True):
                keyboard.wait("f7")

                if (terminate):
                        play()
                else:
                        terminate = True
                        titleframe.setPixmap(QtGui.QPixmap(title_stop))


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
# Main window
        font = QtGui.QFont()
        font.setFamily("Roboto")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(doppelkey_icon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(654, 181)
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(654, 181))
        MainWindow.setMaximumSize(QtCore.QSize(654, 181))
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: rgb(66, 66, 66);")
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        MainWindow.setFont(font)


# Start repgroup
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.repGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.repGroup.setGeometry(QtCore.QRect(50, 90, 121, 21))
        self.repGroup.setTitle("")
        self.repGroup.setObjectName("repGroup")

        global repbox
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setBold(True)
        font.setWeight(75)
        self.repBox = QtWidgets.QSpinBox(self.repGroup)
        self.repBox.setGeometry(QtCore.QRect(80, 0, 42, 22))
        self.repBox.setMinimum(1)
        self.repBox.setFont(font)
        self.repBox.setAutoFillBackground(False)
        self.repBox.setStyleSheet("color: rgb(255, 255, 255);")
        self.repBox.setWrapping(False)
        self.repBox.setFrame(False)
        self.repBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.repBox.setProperty("value", 1)
        self.repBox.setObjectName("repBox")
        repbox = self.repBox

        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label = QtWidgets.QLabel(self.repGroup)
        self.label.setGeometry(QtCore.QRect(0, 0, 81, 21))
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: rgb(66, 66, 66);\n""color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
# End repgroup

# Start speedgroup
        self.speedGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.speedGroup.setGeometry(QtCore.QRect(50, 120, 121, 21))
        self.speedGroup.setTitle("")
        self.speedGroup.setObjectName("speedGroup")

        global speedbox
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setBold(True)
        font.setWeight(75)
        self.speedBox = QtWidgets.QSpinBox(self.speedGroup)
        self.speedBox.setGeometry(QtCore.QRect(80, 0, 42, 22))
        self.speedBox.setMinimum(1)
        self.speedBox.setFont(font)
        self.speedBox.setStyleSheet("color: rgb(255, 255, 255);")
        self.speedBox.setFrame(False)
        self.speedBox.setProperty("value", 1)
        self.speedBox.setObjectName("speedBox")
        speedbox = self.speedBox
        
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2 = QtWidgets.QLabel(self.speedGroup)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 81, 21))
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background-color: rgb(66, 66, 66);\n""color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")
# End speedgroup

# Play button
        global playbutton
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(play_unpressed), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(play_pressed), QtGui.QIcon.Normal, QtGui.QIcon.On)
        icon1.addPixmap(QtGui.QPixmap(play_disabled), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(play_disabled), QtGui.QIcon.Disabled, QtGui.QIcon.On)
        icon1.addPixmap(QtGui.QPixmap(play_unpressed), QtGui.QIcon.Active, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(play_pressed), QtGui.QIcon.Active, QtGui.QIcon.On)
        icon1.addPixmap(QtGui.QPixmap(play_unpressed), QtGui.QIcon.Selected, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(play_pressed), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.playButton = QtWidgets.QPushButton(self.centralwidget)
        self.playButton.setGeometry(QtCore.QRect(350, 85, 71, 61))
        self.playButton.setWhatsThis("")
        self.playButton.setStyleSheet("border: none;\n""margin: 0px;\n""padding: 0px;")
        self.playButton.setText("")
        self.playButton.setIcon(icon1)
        self.playButton.setIconSize(QtCore.QSize(70, 70))
        self.playButton.setCheckable(True)
        self.playButton.setFlat(True)
        self.playButton.setDisabled(True)
        self.playButton.setObjectName("playButton")
        playbutton = self.playButton

# Record button
        global recbutton
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(rec_unpressed), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(rec_pressed), QtGui.QIcon.Normal, QtGui.QIcon.On)
        icon2.addPixmap(QtGui.QPixmap(rec_disabled), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(rec_disabled), QtGui.QIcon.Disabled, QtGui.QIcon.On)
        icon2.addPixmap(QtGui.QPixmap(rec_unpressed), QtGui.QIcon.Active, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(rec_pressed), QtGui.QIcon.Active, QtGui.QIcon.On)
        icon2.addPixmap(QtGui.QPixmap(rec_unpressed), QtGui.QIcon.Selected, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(rec_pressed), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.recButton = QtWidgets.QPushButton(self.centralwidget)
        self.recButton.setGeometry(QtCore.QRect(245, 85, 71, 61))
        self.recButton.setAutoFillBackground(False)
        self.recButton.setStyleSheet("border: none;\n""margin: 0px;\n""padding: 0px;")
        self.recButton.setText("")
        self.recButton.setIcon(icon2)
        self.recButton.setIconSize(QtCore.QSize(70, 70))
        self.recButton.setCheckable(True)
        self.recButton.setFlat(True)
        self.recButton.setObjectName("recButton")
        recbutton = self.recButton

# Information button
        global infobutton
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(doppelkey_img), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.info = QtWidgets.QPushButton(self.centralwidget)
        self.info.setEnabled(True)
        self.info.setGeometry(QtCore.QRect(600, 120, 41, 41))
        self.info.setText("")
        self.info.setIcon(icon3)
        self.info.setObjectName("info")
        self.info.setToolTip("<html><head/><body><p>Instructions</p></body></html>")
        self.info.setFlat(True)
        infobutton = self.info

# Title frame
        global titleframe
        self.frame = QtWidgets.QLabel(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 651, 181))
        self.frame.setText("")
        self.frame.setTextFormat(QtCore.Qt.RichText)
        self.frame.setPixmap(QtGui.QPixmap(title))
        self.frame.setObjectName("frame")
        self.frame.raise_()
        titleframe = self.frame

# Initialize widgets
        self.repGroup.raise_()
        self.speedGroup.raise_()
        self.playButton.raise_()
        self.recButton.raise_()
        self.info.raise_()

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Doppelkey"))
        self.label.setText(_translate("MainWindow", "Repeats:"))
        self.label_2.setText(_translate("MainWindow", "Speed:"))
        
        
        global recordstartthread
        global terminate

        recordstopthread = Thread(target=recordstop)
        recordstartthread = Thread(target=recordstart)
        f8thread = Thread(target=hotkey_f8)

        recordstopthread.daemon = True
        recordstartthread.daemon = True
        f8thread.daemon = True
        terminate = True

        playbutton.clicked.connect(play)
        recbutton.clicked.connect(record)
        infobutton.clicked.connect(instructions)
        f8thread.start()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
