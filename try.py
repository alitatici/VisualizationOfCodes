# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'try.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(10, 20, 61, 22))
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(4)
        self.spinBox.setSingleStep(1)
        self.spinBox.setProperty("value", 1)
        self.spinBox.setObjectName("spinBox")
        value = self.spinBox.value()

        if value == 1 :
            self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            self.horizontalLayoutWidget.setGeometry(QtCore.QRect(80, 20, 701, 22))
            self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
            self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
            self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.horizontalLayout.setObjectName("horizontalLayout")
            self.lineEdit_2 = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
            self.lineEdit_2.setObjectName("lineEdit_2")
            self.horizontalLayout.addWidget(self.lineEdit_2)
            self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
            self.lineEdit.setObjectName("lineEdit")
            self.horizontalLayout.addWidget(self.lineEdit)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        print(str(self.spinBox.value()))

        value = self.spinBox.value()

        if value == 2 :
            self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
            self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(80, 50, 701, 22))
            self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
            self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
            self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
            self.horizontalLayout_2.setObjectName("horizontalLayout_2")
            self.lineEdit_3 = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
            self.lineEdit_3.setObjectName("lineEdit_3")
            self.horizontalLayout_2.addWidget(self.lineEdit_3)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

