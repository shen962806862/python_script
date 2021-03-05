# -*- coding:utf-8 -*-
import datetime
import sxtwl
import linecache
import sys
from PyQt5.QtWidgets import QWidget,QApplication,QPushButton,QVBoxLayout,QLabel
from PyQt5.QtCore import QCoreApplication,Qt

class CountDown():
    def getDateInYear(self, current, next):
        c = list(map(int, current.split('-')))
        n = list(map(int, next.split('-')))
        if c[1] == n[0]:
            if c[2] != n[1]:
                return n[1] - c[2]
            else:
                return 0
        else:
            return self.dayInYear(c[0], n[0], n[1]) - self.dayInYear(c[0], c[1], c[2])


    def getDateDiffer(self, first, current):
        f = list(map(int, first.split('-')))
        c = list(map(int, current.split('-')))
        if f[0] == c[0]:
            if f[1] == c[1]:
                if f[2] != c[2]:
                    return c[2] - f[2]
                else:
                    return 0
            else:
                return self.dayInYear(c[0],c[1],c[2]) - self.dayInYear(f[0],f[1],f[2])
        else:
            if self.isLeap(f[0]):
                day1 = 366 - self.dayInYear(f[0],f[1],f[2])
            else:
                day1 = 365 - self.dayInYear(f[0], f[1], f[2])
            day2 = self.dayInYear(c[0],c[1],c[2])
            day3 = 0
            for i in range(c[0] - f[0] - 1):
                if self.isLeap(f[0] + i + 1):
                    day3 += 366
                else:
                    day3 += 365
            return day1 + day2 + day3

    def isLeap(self, year):
        return (year % 4 == 0 or year % 400 == 0) and (year % 100 != 0)

    def dayInYear(self, y, m, d):
        mDay = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if self.isLeap(y):
            mDay[1] = 29
        for i in range(m-1):
            d += mDay[i]
        return d

class Msg(QWidget):

    def __init__(self):
        super().__init__()

        self.__init_ui()

    def __init_ui(self):
        self.resize(500, 300)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowOpacity(0.88)
        self.setStyleSheet('background-color:#DCDCDC;')
        self.show()

        self.txt = QLabel()
        self.txt.setAlignment(Qt.AlignCenter)
        self.txt.setStyleSheet('font:bold 30px;')
        self.btn = QPushButton('OK', self)
        self.btn.clicked.connect(QCoreApplication.instance().quit)
        self.btn.setStyleSheet('background-color:#00BFFF;')

        qv = QVBoxLayout()
        qv.addWidget(self.txt)
        qv.addWidget(self.btn)
        self.setLayout(qv)

    def settext(self,data):
        tt = ''
        for i in range(len(data)):
            tt += data[i]
        self.txt.setText(tt)

if __name__ == '__main__':
    #如何开机自动运行脚本请自百度
    today = datetime.date.today()
    lunar = sxtwl.Lunar()
    cd = CountDown()
    # 注：脚本运行需外挂一个txt文件，文件格式如下：帅哥-8.10-Lunar (Lunar为农历，Solar阳历) 每个一行
    data = linecache.getlines('../data/reminder.txt')
    msg = []

    for i in data:
        i = i.replace('\n', '').split('-')
        if i[2] == 'Lunar':
            day = lunar.getDayByLunar(today.year, int(i[1].split('.')[0]), int(i[1].split('.')[1]), False)
            resttime = cd.getDateInYear(today.strftime("%Y-%m-%d"), str(day.m) + '-' + str(day.d))
        else:
            resttime = cd.getDateInYear(today.strftime("%Y-%m-%d"), i[1].replace('.', '-'))
        if resttime == 7:
            msg.append('距离'+i[0]+'生日还有 7 天\n\n')
        elif resttime == 1:
            msg.append('距离'+i[0]+'生日还有 1 天\n\n')
        elif resttime == 0:
            msg.append(i[0]+'生日就是 今天 !\n\n')
    if len(msg):
        app = QApplication(sys.argv)
        ex2 = Msg()
        ex2.settext(msg)
        sys.exit(app.exec_())
