##############################################
## 기본형
'''
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

#나만의 윈도우 정의
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #윈도우 꾸미기
        #self.resize(500, 500)
        #self.move(300, 300)
        self.setGeometry(1500, 300, 700, 700)
        self.setWindowTitle('My 1st Window')
        self.setWindowIcon(QIcon('icon.png'))

        #위젯만들기


app = QApplication(sys.argv)

#나만의 윈도우 만들기
win = MyWindow()
win.show()

app.exec_()
'''

##############################################
## 마이윈도우 + 버튼
'''
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

#나만의 윈도우 정의
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #윈도우 꾸미기
        #self.resize(500, 500)
        #self.move(300, 300)
        self.setGeometry(1500, 300, 700, 700)
        self.setWindowTitle('My 1st Window')
        self.setWindowIcon(QIcon('icon.png'))

        #위젯만들기
        btn = QPushButton('1', self)
        btn.resize(150, 30)
        btn.move(10, 10)
        btn.clicked.connect(self.test)

        btn2 = QPushButton('2', self)
        btn2.resize(150, 30)
        btn2.move(170, 10)
        btn2.clicked.connect(self.test)

        btn3 = QPushButton('3', self)
        btn3.resize(150, 30)
        btn3.move(10, 40)
        btn3.clicked.connect(self.test)

        btn4 = QPushButton('4', self)
        btn4.resize(150, 30)
        btn4.move(170, 40)
        btn4.clicked.connect(self.test)

    def test(self):
        btn = self.sender()
        print(btn.text())




app = QApplication(sys.argv)

#나만의 윈도우 만들기
win = MyWindow()
win.show()

app.exec_()
'''


#############################################
## 마이윈도우 + 레이블
'''
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

#나만의 윈도우 정의
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #윈도우 꾸미기
        #self.resize(500, 500)
        #self.move(300, 300)
        self.setGeometry(1500, 300, 700, 700)
        self.setWindowTitle('My 1st Window')
        self.setWindowIcon(QIcon('icon.png'))

        #위젯만들기
        self.label1 = QLabel('고객ID', self)
        self.label1.resize(150, 30)
        self.label1.move(10, 10)

        self.label2 = QLabel('ID비밀번호', self)
        self.label2.resize(150, 30)
        self.label2.move(10, 50)

        self.label3 = QLabel('인증비밀번호', self)
        self.label3.resize(150, 30)
        self.label3.move(10, 90)

app = QApplication(sys.argv)

#나만의 윈도우 만들기
win = MyWindow()
win.show()

app.exec_()
'''

#########################################
## 마이윈도우 + 레이블 + 버튼
'''
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

#나만의 윈도우 정의
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #윈도우 꾸미기
        #self.resize(500, 500)
        #self.move(300, 300)
        self.setGeometry(1500, 300, 700, 700)
        self.setWindowTitle('My 1st Window')
        self.setWindowIcon(QIcon('icon.png'))

        #위젯만들기
        self.label = QLabel(self)
        self.label.setGeometry(10, 10, 300, 30)

        self.btn = QPushButton("clicked", self)
        self.btn.setGeometry(10, 50, 100, 50)
        self.btn.clicked.connect(self.btn_callback)

        self.cnt = 0

    def btn_callback(self):
        #self.label.setText(self.btn.text())
        self.cnt += 1
        self.label.setText(str(self.cnt))


app = QApplication(sys.argv)

#나만의 윈도우 만들기
win = MyWindow()
win.show()

app.exec_()
'''

###############################################
## 타이머
'''
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

#나만의 윈도우 정의
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #윈도우 꾸미기
        #self.resize(500, 500)
        #self.move(300, 300)
        self.setGeometry(1500, 300, 700, 700)
        self.setWindowTitle('My 1st Window')
        self.setWindowIcon(QIcon('icon.png'))

        #위젯만들기
        self.label = QLabel(self)
        self.label.setGeometry(20, 20, 200, 200)

        #기타 작업
        #timer = QTimer(self)
        #timer.start(1000)
        #timer.timeout.connect(self.timer_callback)
        QTimer.singleShot(5000, self.timer_callback)

        self.num = 0

    def timer_callback(self):
        print(self.num)
        #self.label.setText(str(self.num))
        self.num += 1
        self.label.setText("프로그램 실행 후 5초 경과")


app = QApplication(sys.argv)

#나만의 윈도우 만들기
win = MyWindow()
win.show()

app.exec_()
'''

######################################################
## QTimer 1초에 한번씩 숫자를 카운트하여 label에 보여주고,
## 버튼을 누르면 clicked 메시지를 터미널에 출력함
'''
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time

#나만의 윈도우 정의
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #윈도우 꾸미기
        #self.resize(500, 500)
        #self.move(300, 300)
        self.setGeometry(1500, 300, 700, 700)
        self.setWindowTitle('My 1st Window')
        self.setWindowIcon(QIcon('icon.png'))

        #위젯만들기
        self.btn = QPushButton('버튼', self)
        self.btn.resize(150, 100)
        self.btn.move(10, 100)
        self.btn.clicked.connect(self.btn_callback)

        self.label = QLabel(self)
        self.label.resize(100, 50)
        self.label.move(10, 10)

        timer = QTimer(self)
        timer.start(1000)
        timer.timeout.connect(self.timeout_callback)

        self.cnt = 0

    def timeout_callback(self):
        self.cnt += 1
        self.label.setText(str(self.cnt))
        print('before sleep')
        #time.sleep(5)
        print('after sleep')
        pass

    def btn_callback(self):
        print('button clicked!!!')



app = QApplication(sys.argv)

#나만의 윈도우 만들기
win = MyWindow()
win.show()

app.exec_()
'''

############################################
## 데이터 전달 : 메인스레드<->워크스레드
'''
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Worker(QThread):
    mysignal = pyqtSignal(int, str)

    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        num = 0
        while True:
            self.mysignal.emit(num, self.name)
            num += 1
            self.sleep(1)

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #윈도우꾸미기

        #위젯올리기

        #기타작업
        self.worker = Worker('정수진')
        self.worker.start()
        self.worker.mysignal.connect(self.worker_callback)

    @pyqtSlot(int, str)
    def worker_callback(self, data, data2):
        print(data, data2)

app = QApplication(sys.argv)

win = MyWindow()
win.show()

app.exec_()
'''
#################################################
## 워커스레드에서 파일오픈해서 label에 출력하기

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time

class Worker(QThread):
    mySignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        f = open('large_text_file.txt', 'r')
        while True:
            line = f.readline().strip()            
            if not line:
                break
            print(line)
            self.mySignal.emit(line)
            time.sleep(0.1)

        f.close()

#나만의 윈도우 정의
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #윈도우 꾸미기
        self.setGeometry(1500, 300, 700, 700)
        self.setWindowTitle('My 1st Window')
        self.setWindowIcon(QIcon('icon.png'))

        #위젯만들기
        self.label = QLabel(self)
        self.label.resize(300, 100)
        self.label.move(20, 20)

        #기타작업
        self.worker = Worker()
        self.worker.start()
        self.worker.mySignal.connect(self.worker_callback)

    @pyqtSlot(str)
    def worker_callback(self, data):
        self.label.setText(data)



app = QApplication(sys.argv)

#나만의 윈도우 만들기
win = MyWindow()
win.show()

app.exec_()