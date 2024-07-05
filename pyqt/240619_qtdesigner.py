import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

#나만의 윈도우 정의
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #ui 파일 연결
        uic.loadUi("main.ui", self)

        self.lwList : QListWidget
        self.pbButton : QPushButton

        #리스트
        self.lwList.addItem('잘가')
        self.lwList.addItems(['또만나', '하하'])
        self.lwList.itemDoubleClicked.connect(self.lwList_callback)

        #이벤트 처리
        self.pbButton.clicked.connect(self.pbButton_callback)


    def lwList_callback(self, data):
        print(data.text())

    def pbButton_callback(self):
        '''
        idx = self.lwList.currentRow()
        item = self.lwList.currentItem()

        print(idx, item.text())
        '''
        for i in range(self.lwList.count()):
            print(i, self.lwList.item(i).text())

app = QApplication(sys.argv)

#나만의 윈도우 만들기
win = MyWindow()
win.show()

app.exec_()