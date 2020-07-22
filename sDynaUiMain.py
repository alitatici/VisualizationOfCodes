#--------------------Library-------------------#
#----------------------------------------------#
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from sDynaUi import *
from about import *
from results import *
import xlsxwriter
import xlrd
from MDOF import *
import matplotlib.pyplot as plt
import numpy as np

#--------------Create Application--------------#
#----------------------------------------------#
Application = QApplication(sys.argv)
WinMain = QMainWindow()
ui = Ui_sDyna() #sDynaUi.py class isminden kopyalandı.
ui.setupUi(WinMain) #tasarımdaki form ile pencereyi birleştir
WinMain.show() #pencereyi göster.

WinAbout=QDialog()
uiAbout = Ui_Dialog()
uiAbout.setupUi(WinAbout)

WinResults = QDialog()
uiResults = Ui_Results()
uiResults.setupUi(WinResults)


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
                Floor NUMERIC NOT NULL PRIMARY KEY,                             \
                Mass NUMERIC NOT NULL,                              \
                Rigidity NUMERIC NOT NULL)")
conn.commit()

#---------------lineEdit Enable----------------#
#----------------------------------------------#

ui.lne_Mass.setEnabled(False)
ui.lne_Rigidity.setEnabled(False)
ui.progressBar.hide()

def comboact():
    ui.lne_Mass.setEnabled(True)
    ui.lne_Rigidity.setEnabled(True)


#---------------SAVE---------------#
#----------------------------------#
def addData():
    checkUnique = 1
    _lne_Mass = ui.lne_Mass.text()
    _lne_Rigidity = ui.lne_Rigidity.text()
    _cm_Floor = ui.cm_Floor.currentText()
    try:
        _lne_Mass= float(_lne_Mass)
        _lne_Rigidity=float(_lne_Rigidity)
        if bool(_lne_Mass) and bool(_lne_Rigidity) and bool(_cm_Floor)==True:
        
            curs.execute("SELECT Floor FROM sDyna")
            liste = curs.fetchall()
            if len(liste) != 0:
                for j in range(len(liste)):
                    for i in liste[j]:
                        if i == int(_cm_Floor):
                            checkUnique = 0

            if checkUnique == 1:
                curs.execute("INSERT INTO sDyna (Floor, Mass, Rigidity) VALUES (?,?,?)", (_cm_Floor,_lne_Mass,_lne_Rigidity))
                conn.commit()
                makeList()
                ui.lne_Mass.setEnabled(False)
                ui.lne_Rigidity.setEnabled(False)

            elif checkUnique == 0:
                QMessageBox.about(WinMain,"Error","This floor has added already. Use Change button to change")
                WinMain.show()

            checkUnique = 0

        else:
            ui.statusbar.showMessage("Error: Data must be entered.",10000)


    except Exception:
        QMessageBox.about(WinMain,'Error','Input can only be a number')
        pass

    
#---------------LIST---------------#
#----------------------------------#
def makeList():
    ui.tb_data.clearContents() #tablo içeriğini siler.
    curs.execute("SELECT * FROM sDyna")
    for rowIndex, rowData in enumerate(curs):
        for columnIndex, columnData in enumerate(rowData):
            ui.tb_data.setItem(rowIndex,columnIndex,QTableWidgetItem(str(columnData)))
    ui.lne_Mass.clear()
    ui.lne_Rigidity.clear()
    ui.cm_Floor.setCurrentIndex(-1) # "-1" comboBox içine hiçbirşey yazmamayı ifade eder.

    #-----Current Floor Number-----#
    curs.execute("SELECT COUNT (*) FROM sDyna")
    floorNumber = curs.fetchone()
    ui.label_savedFloor.setText(str(floorNumber[0]))

    # floorNumber[0] bizim kat sayımızı veriyor!!
    # floorNumbers = curs.fetchall()
    # ui.label_savedFloor.setText(str(len(floorNumbers)))



#------------RESET ALL---------------#
#------------------------------------#
def deleteAll():
    answer1 = QMessageBox.question(WinMain,"Delete all","Are you sure to reset data?",\
                                    QMessageBox.Yes | QMessageBox.No)
    if answer1 == QMessageBox.Yes:    
        curs.execute("DELETE FROM sDyna")
        conn.commit()
        ui.tb_data.clearContents() #tablo içeriğini siler.
        ui.lne_Mass.clear()
        ui.lne_Rigidity.clear()
        ui.cm_Floor.setCurrentIndex(-1) # "-1" comboBox içine hiçbirşey yazmamayı ifade eder.
        ui.lne_EQData.clear()
        ui.lne_Seperator.clear()
        ui.label_savedFloor.clear()
    else:
        WinMain.show()


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

        if bool(slcted)==True:
            dlt = slcted[0].text()

            try:
                curs.execute("DELETE FROM sDyna WHERE Floor='%s'"%(dlt))
                conn.commit()
                makeList()
                ui.statusbar.showMessage(str(dlt)+". floor's data has been deleted successfully.",10000) #10000 milisaniye=10 saniye mesaj görünecek.
            
            except Exception as Error:
                ui.statusbar.showMessage("Error:"+str(Error),10000)
        
        else:
            ui.statusbar.showMessage("There is no selected items.",10000)


    else:
        ui.statusbar.showMessage("Deleting process has been cancelled.",10000)
        WinMain.show()

#------------------CHANGE-ROW-------------------#
#-----------------------------------------------#
def changeRow():
    answer2 = QMessageBox.question(WinMain,"Change the floor's features","Are you sure to change this floor?",\
                                    QMessageBox.Yes | QMessageBox.No)
    uniquenumber=1            
    _lne_Mass = ui.lne_Mass.text()
    _lne_Rigidity = ui.lne_Rigidity.text()
    _cm_Floor = ui.cm_Floor.currentText()

    try:
        _lne_Mass=float(_lne_Mass)
        _lne_Rigidity=float(_lne_Rigidity)

        if answer2 == QMessageBox.Yes:

            if bool(_lne_Mass) and bool(_lne_Rigidity) and bool(_cm_Floor)==True:
                
                curs.execute("SELECT Floor FROM sDyna")
                liste = curs.fetchall()
                for j in range(len(liste)):
                    for i in liste[j]:
                        if i == int(_cm_Floor):
                            uniquenumber=0
                
                if uniquenumber==0:
                    curs.execute("UPDATE sDyna SET Mass = ?, Rigidity = ? WHERE Floor = ?" , (_lne_Mass,_lne_Rigidity,_cm_Floor))
                    conn.commit()
                    makeList()
                    ui.lne_Mass.setEnabled(False)
                    ui.lne_Rigidity.setEnabled(False)

                else:
                    QMessageBox.about(WinMain,"Error","Choosen floor cannot be find in table.Please save the floor first.")
                    # WinMain.show()

                
                checkUnique = 0

            else:
                ui.statusbar.showMessage("Error: All data must be entered.",10000)
        
        else:
            ui.statusbar.showMessage("Changing process has been cancelled.",10000)
            WinMain.show()
    
    except Exception:
        QMessageBox.about(WinMain,'Error','Input can only be a number')
        pass


#--------------------SEARCH---------------------#
#-----------------------------------------------#
def search_():
    search1=ui.cm_Floor.currentText()
    search2=ui.lne_Mass.text()
    search3=ui.lne_Rigidity.text()
    curs.execute("SELECT * FROM sDyna WHERE Floor=? OR Mass=? OR Rigidity=? OR\
                    (Mass=? AND Rigidity=?) OR (Floor=? AND Rigidity=?) OR (Mass=? AND Floor=?)",\
                    (search1,search2,search3,search2,search3,search1,search3,search2,search1))
    conn.commit
    ui.tb_data.clearContents()
    for rowIndex, rowData in enumerate(curs):
        for columnIndex, columnData in enumerate(rowData):
            ui.tb_data.setItem(rowIndex,columnIndex,QTableWidgetItem(str(columnData)))


#-----------------ABOUT-------------------#
#-----------------------------------------#
def about_():
    WinAbout.show()

#---------------EQ FILE-------------------#
#-----------------------------------------#
def eqfile():
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getOpenFileName(WinMain,"Select Earthquake File", "","All Files(*);; Text Files (*.txt);; Excel Files (*.xlsx);; CSV Files (*.csv)", options=options)
    ui.lne_EQData.setText(fileName)

#---------------SAVE EXCEL FILE-----------#
#-----------------------------------------#
def saveExcelFile():
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    savedfileName, _ = QFileDialog.getSaveFileName(WinMain,"Save File","","Xlsx Files (*.xlsx)", options=options)
    if savedfileName.endswith(".xlsx")==True:
        workbook=xlsxwriter.Workbook(savedfileName)
    else:

        workbook=xlsxwriter.Workbook(savedfileName+ ".xlsx")
    worksheet=workbook.add_worksheet("sDyna")
    curs.execute("SELECT * FROM sDyna")
    colnames = [desc[0] for desc in curs.description]
    data = curs.fetchall()


    # Start from the first cell. Rows and columns are zero indexed.
    row = 1
    col = 0
    row1=0

    # Iterate over the data and write it out row by row.
    
    for header in range(0,len(colnames)):
        worksheet.write(row1,col+header,colnames[header])
    

    for Floor, Mass, Rigidity in (data):
        worksheet.write(row, col,     Floor)
        worksheet.write(row, col + 1, Mass)
        worksheet.write(row, col + 2, Rigidity)
        row += 1

    workbook.close()


#-------------OPEN EXCEL FILE-------------#
#-----------------------------------------#
def openExcelFile():

    # Choosing Excel File
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getOpenFileName(WinMain,"Select Database", "","Excel Files (*.xlsx)", options=options)
    
    try: 
        
        wb = xlrd.open_workbook(fileName) 
        sheet = wb.sheet_by_index(0) 
        sheet.cell_value(0, 0)
        
        
        for i in range(1,sheet.nrows): 
            floorExcel=sheet.cell_value(i, 0)
            massExcel=sheet.cell_value(i,1)
            rigidityExcel=sheet.cell_value(i,2)
            curs.execute("INSERT INTO sDyna (Floor,Mass,Rigidity) VALUES (?,?,?)", (floorExcel,massExcel,rigidityExcel))
            conn.commit()
        
        makeList()
    
    except Exception:
        pass


#-------------------RUN-------------------#
#-----------------------------------------#
def run():
    
    curs.execute("Select Mass From sDyna")
    massList = curs.fetchall()
    for i in range(len(massList)):
        massList[i] = massList[i][0]

    curs.execute("Select Rigidity From sDyna")
    rigidityList = curs.fetchall()
    for i in range(len(rigidityList)):
        rigidityList[i] = rigidityList[i][0]
    
    #-----Total Floor Number-----#
    curs.execute("SELECT COUNT (*) FROM sDyna")
    floorNumber = curs.fetchone()

    _lne_EQData = ui.lne_EQData.text()
    _lne_Seperator = ui.lne_Seperator.text()

    #-----------Run MDOF-----------#
    yapi=Yapi(massList, rigidityList, floorNumber[0])

    yapi.rigidityMatrix()
    yapi.massMatrix()
    yapi.naturalFrequency()
    yapi.dampingRatio(0.05)
    yapi.dampingMatrix()
    yapi.amplitudeCalc()
    yapi.generalMassMat()
    yapi.generalStiffnessMat()
    yapi.generalDampingMat()
    yapi.modeParticipatingFactor()
    yapi.effectiveParticipatingMass()
    ui.progressBar.setProperty("value", 90)
    yapi.earthquakeData(_lne_EQData,_lne_Seperator)
    yapi.spectra1()
    yapi.psuedoAcceleration()
    yapi.baseShear()
    yapi.baseShearSRSS()
    ui.progressBar.setProperty("value", 100)
    
    WinResults.show()
    ui.progressBar.hide()
    ui.progressBar.setProperty("value", 0)



#--------------ProgressBar----------------#
#-----------------------------------------#
def run_():
    ui.progressBar.show()

    answer4 = QMessageBox.question(WinMain,"Run","Are you sure to run?",\
                                    QMessageBox.Yes | QMessageBox.No)
    if answer4 == QMessageBox.Yes:
        completed = 0
        while completed < 90:
            completed += 0.0001
            ui.progressBar.setValue(completed)
        run()
    else:
        ui.progressBar.hide()
        ui.statusbar.showMessage("Progress has been cancelled.",10000)
        WinMain.show()
    


#---------------SIGNAL-SLOT---------------#
#-----------------------------------------#
ui.pb_Add.clicked.connect(addData)
ui.pb_reset.clicked.connect(deleteAll)
ui.pb_Exit.clicked.connect(exit_)
ui.pb_dltRow.clicked.connect(deleteRow)
ui.pb_find.clicked.connect(search_)
ui.pb_list.clicked.connect(makeList)
ui.menuHelp.triggered.connect(about_)
ui.pb_change.clicked.connect(changeRow)
ui.cm_Floor.activated.connect(comboact) ########
ui.pb_fromfile.clicked.connect(eqfile)
ui.pb_Save.clicked.connect(saveExcelFile)
ui.pb_Open.clicked.connect(openExcelFile)
ui.pb_run.clicked.connect(run_)





sys.exit(Application.exec_()) #Çıkış yaparken uygulama ile ilgili tüm işlemleri sonlandırır.