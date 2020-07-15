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

#---------------Create DataBase----------------#
#----------------------------------------------#
import sqlite3
global curs
global conn

conn = sqlite3.connect("sDynaDB.db")
curs = conn.cursor()

curs.execute("DELETE FROM sDyna")
conn.commit()

curs.execute("CREATE TABLE IF NOT EXISTS sDyna(                     \
                Floor INTEGER NOT NULL PRIMARY KEY,                 \
                Mass INTEGER NOT NULL,                              \
                Rigidity INTEGER NOT NULL)")
conn.commit()


#---------------SAVE---------------#
#----------------------------------#
def addData():
    _lne_Mass = ui.lne_Mass.text()
    _lne_Rigidity = ui.lne_Rigidity.text()
    _cm_Floor = ui.cm_Floor.currentText()

    curs.execute("INSERT INTO sDyna (Floor, Mass, Rigidity) VALUES (?,?,?)", (_cm_Floor,_lne_Mass,_lne_Rigidity))
    conn.commit()
    makeList()


#---------------LIST---------------#
#----------------------------------#
def makeList():
    ui.tb_data.clearContents() #tablo içeriğini siler.
    curs.execute("SELECT * FROM sDyna")
    for rowIndex, rowData in enumerate(curs):
        for columnIndex, columnData in enumerate(rowData):
            ui.tb_data.setItem(rowIndex,columnIndex,QTableWidgetItem(str(columnData)))


#------------RESET ALL---------------#
#------------------------------------#
def deleteAll():
    curs.execute("DELETE FROM sDyna")
    conn.commit()
    ui.tb_data.clearContents() #tablo içeriğini siler.
    ui.lne_Mass.clear()
    ui.lne_Rigidity.clear()
    ui.cm_Floor.setCurrentIndex(-1) # "-1" comboBox içine hiçbirşey yazmamayı ifade eder.
    ui.lne_EQData.clear()
    ui.lne_Seperator.clear()
    ui.label_savedFloor.clear()


#------------------EXIT-------------------#
#-----------------------------------------#
def exit_():
    answer = QMessageBox.question(WinMain,"EXIT","Are you sure to exit from program?",\
                                    QMessageBox.Yes | QMessageBox.No)
    if answer == QMessageBox.Yes:
        conn.close()
        sys.exit(Application.exec_())
    else:
        WinMain.show()

#------------------DELETE-ROW-------------------#
#-----------------------------------------------#
def deleteRow():
    answer = QMessageBox.question(WinMain,"Delete the floor","Are you sure to delete this floor?",\
                                    QMessageBox.Yes | QMessageBox.No)

    if answer == QMessageBox.Yes:
        slcted = ui.tb_data.selectedItems()
        dlt = slcted[0].text()

        try:
            curs.execute("DELETE FROM sDyna WHERE Floor='%s'"%(dlt))
            conn.commit()
            makeList()
            ui.statusbar.showMessage(str(dlt)+". floor's data has been deleted successfully.",10000) #10000 milisaniye=10 saniye mesaj görünecek.
        
        except Exception as Error:
            ui.statusbar.showMessage("Error:"+str(Error),10000)

    else:
        ui.statusbar.showMessage("Deleting process has been cancelled.",10000)
        WinMain.show()


#---------------SIGNAL-SLOT---------------#
#-----------------------------------------#
ui.pb_Save.clicked.connect(addData)
ui.pb_reset.clicked.connect(deleteAll)
ui.pb_Exit.clicked.connect(exit_)
ui.pb_Print.clicked.connect(deleteRow)




sys.exit(Application.exec_()) #Çıkış yaparken uygulama ile ilgili tüm işlemleri sonlandırır.