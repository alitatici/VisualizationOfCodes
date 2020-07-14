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

sys.exit(Application.exec_()) #Çıkış yaparken uygulama ile ilgili tüm işlemleri sonlandırır.

#---------------Create DataBase----------------#
#----------------------------------------------#

