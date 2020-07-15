#--------------------Library-------------------#
#----------------------------------------------#
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from sDynaUi import *

#--------------Create Application--------------#
#----------------------------------------------#

Application = QApplication(sys.argv)
WinMain = QMainWindow()
ui = Ui_MainWindow() #sDynaUi.py class isminden kopyalandı.
ui.setupUi(WinMain) #tasarımdaki form ile pencereyi birleştir
WinMain.show() #pencereyi göster.

#sys.exit(Application.exec_()) #Çıkış yaparken uygulama ile ilgili tüm işlemleri sonlandırır.

#---------------Create DataBase----------------#
#----------------------------------------------#

import sqlite3

con = sqlite3.connect("sDynaDB.db")
cursor = con.cursor()

# queryCreTbl = ("CREATE TABLE IF NOT EXISTS sDyna(                    \
#                 Floor INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,   \
#                 Mass INTEGER NOT NULL,                              \
#                 Rigidity INTEGER NOT NULL)")

cursor.execute("CREATE TABLE IF NOT EXISTS sDyna(                    \
                Floor INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,   \
                Mass INTEGER NOT NULL,                              \
                Rigidity INTEGER NOT NULL)")
con.commit()

#---------------SAVE---------------#
#----------------------------------#

def addData():
    _lne_Mass = ui.lne_Mass.text()
    _lne_Rigidity = ui.lne_Rigidity.text()

    cursor.execute("INSERT INTO sDyna (Mass, Rigidity) VALUES (?,?)", (_lne_Mass,_lne_Rigidity))
    con.commit()

#---------------SIGNAL-SLOT---------------#
#-----------------------------------------#

ui.pb_Save.clicked.connect(addData)

sys.exit(Application.exec_())