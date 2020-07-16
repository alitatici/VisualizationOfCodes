import sys
from PyQt5 import QtWidgets, QtGui

def Pencere() :

    app = QtWidgets.QApplication(sys.argv)

    #Pencere Açma
    pencere = QtWidgets.QWidget()
    pencere.setWindowTitle("PyQt5 Deneme 1")

    #Yazı Ekleme
    etiket1=QtWidgets.QLabel(pencere)
    etiket1.setText("Lord of the Codes")
    etiket1.move(200,30)

    #Fotograf Ekleme
    etiket2=QtWidgets.QLabel(pencere)
    etiket2.setPixmap(QtGui.QPixmap("OnurSS.png"))
    etiket2.move(190,80)

    #Pencereye buton ekleme.
    buton = QtWidgets.QPushButton(pencere)
    buton.setText("CODE")
    buton.move(210,300)

    #Pencere Lokasyonu ve Boyutu
    pencere.setGeometry(0,0,500,500)
    pencere.show()

    sys.exit(app.exec_())  

Pencere()

