from rugo2024 import Ui_MainWindow
from PyQt5 import QtWidgets, QtGui, QtCore
#from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import serial.tools.list_ports
import serial
import os
from time import sleep

import numpy as np

import hashlib
import sys
import csv
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import pyqtSignal, QObject

from serial import Serial
from time import sleep


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('usb.png'))
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)#FramelessWindowHint
        
        self.ui.BLeer.clicked.connect(self.LeerM)
        self.ui.BBorrar.clicked.connect(self.BorraM)#BorraM)
        self.ui.BSalir.clicked.connect(self.SalirM)
        
        self.ui.MenuL.triggered.connect(self.LeerM)
        self.ui.MenuB.triggered.connect(self.BorraM)
        self.ui.MenuR.triggered.connect(self.Recupera)
        self.ui.MenuS.triggered.connect(self.SalirM)
        
        self.ui.ListB.itemDoubleClicked.connect(self.Ejecutar)
        self.serie = self.Escanear()
        
        self.carpeta = []
 
        
        self.ruta=""
        if (self.serie):
            self.ui.PuertoS.addItem(None)
            for x in self.serie:
                self.ui.PuertoS.addItem(x)

        
    '''def closeEvent(self, event):
        confirmation = QMessageBox.question(self, "Confirmation", "Are you sure you want to close the application?", QMessageBox.Yes | QMessageBox.No)

        if confirmation == QMessageBox.Yes:
            event.accept()  # Close the app
        else:
            event.ignore()  # Don't close the app'''
    def cabezera(a, b):
        print('funcion cabezera')
        print(b)

        archivos = open(b, 'w')
        archivos.write('VIA  : \t')
        archivos.write(a[5:10].decode('utf-8'))
        archivos.write('\n')
        archivos.write('KM   : \t')
        archivos.write(str((a[0]*256)+a[1]))
        archivos.write('\n')
        archivos.write('LONG : \t'+str(a[3]*100))
        archivos.write('\n')
        archivos.write('HORA : \t'+str(a[10])+':'+str(a[11])+':'+str(a[12]))
        archivos.write('\n')
        dia = str((a[13] & ~(0xCF))>>4) + str(a[13] & ~(0xF0))
        mes = str((a[14]&~(0xEF))>>4) + str(a[14]&~(0xF0))
        anio = str((a[15] & ~(0x0F))>>4) + str(a[15] & ~(0xF0))
        archivos.write('FECHA: \t'+dia+'/'+ mes+'/'+anio)
        archivos.write('\n')
        archivos.write('LATITUD : \t')
        archivos.write(str(a[16])+str(a[17])+"."+str(a[18])+str(a[19])+' '+chr(a[20]))
        archivos.write('\n')
        archivos.write('LONGITUD : \t')
        archivos.write(str(a[21])+str(a[22])+"."+str(a[23])+str(a[24])+' '+chr(a[25]))
        archivos.write('\n')
        archivos.write('----------------------------------------------------\n')
        archivos.write('BUMP1\tBUMP2\tHORA\t\tLATITUD\tLONGITUD\n')
        archivos.close()
     
    def DataB(a, b):
        print(b)
        for data in a:
            print(data, end=' ')
        print()
        archivos = open(b, 'a')
        archivos.write(str((a[0]*256)+a[1])+'\t')
        archivos.write(str((a[2]*256)+a[3])+'\t')
        archivos.write(str(a[4])+':'+str(a[5])+':'+str(a[6])+'\t')
        archivos.write(str(a[7])+str(a[8])+"."+str(a[9])+str(a[10])+' S'+'\t')
        archivos.write(str(a[12])+str(a[13])+"."+str(a[14])+str(a[15])+' W'+'\n')
        archivos.close()
    
    def LeerM(self):
        puerto = self.ui.PuertoS.currentText()
        
        if puerto != "":
            print(puerto)
            try:
                with Serial(puerto, baudrate=57600, timeout=1) as ser:
                    ser.write(b'U0')
                    sleep(0.1)
                    RData = ser.read(8)
                    TData = (RData[2]*256)+RData[1]
                    PData = (TData//128) + 1
                    print('Numero de Datos: ', TData)
                    print('Numero de paginas: ', PData)
                    print()
                    
                    sleep(3)#0.5)
                    f = open('BumpData.bin', 'wb')
                    for paginas in range(PData):
                        ser.write(b'U1')
                        sleep(0.1)
                        RData = bytes(ser.read(128))
                        f.write(RData)
        
                        '''for datas in RData:
                            print(datas, end=' ')'''
                        print()
                    f.close()
            except:
                QMessageBox.about(self, "Error Hardware", "Equipo no conectado")
               
            #print(RData, end=' ')
            
        else:
            QMessageBox.about(self, "Error Hardware", "Equipo no conectado")
        
        self.ui.statusbar.showMessage("Boton Leer Memoria")
    
    def BorraM(self):
        #self.ui.statusbar.showMessage("Borrar Memoria")
        puerto = self.ui.PuertoS.currentText()
        
        if puerto != "":
            print(puerto, "estable")
            try:
                with Serial(puerto, baudrate=57600, timeout=1) as ser:
                    ser.write(b'U2')
                    sleep(0.1)
                    print()
            except:
                QMessageBox.about(self, "no enviado u2", "no enviado u2")
            
        else:
            QMessageBox.about(self, "Error Hardware", "Equipo no conectado")
        
    def SalirM(self):
        print('Terminar')
        self.ui.statusbar.showMessage("Salir Ventana")
        self.close()

    def Recupera(self):
        ruta, data = QFileDialog.getOpenFileName(self, 'Buscar Archivo Rugosimetro', '', 'Roughness File (*.bin *.rbd *.txt)')
        if ruta != "":
            self.carpeta.append(os.path.dirname(ruta))
            print(self.carpeta)
            ruta = os.path.basename(ruta)
            total =os.path.getsize(ruta)

            patron = ruta[:-4]
            fuente = open(ruta, 'rb')
            counter = 0
            ListaFile = []
            while (total >= 0):
                a = fuente.read(4)#iniciamos lectura datos
                total-=4

                if (a[0] == 85) & (a[1] == 170) & (a[2] == 85) & (a[3] == 170):
                    archivo = patron+str(counter)+'.txt'
                    ListaFile.append(archivo)
                    
                    counter+=1
                    a = fuente.read(28)
                    total-=28

                    archivos = open(archivo, 'w')
                    archivos.write('VIA  : \t')
                    archivos.write(a[5:10].decode('utf-8'))
                    archivos.write('\n')
                    archivos.write('KM   : \t')
                    archivos.write(str((a[0]*256)+a[1]))
                    archivos.write('\n')
                    archivos.write('LONG : \t'+str(a[3]*100))
                    archivos.write('\n')
                    archivos.write('HORA : \t'+str(a[10])+':'+str(a[11])+':'+str(a[12]))
                    archivos.write('\n')
                    dia = str((a[13] & ~(0xCF))>>4) + str(a[13] & ~(0xF0))
                    mes = str((a[14]&~(0xEF))>>4) + str(a[14]&~(0xF0))
                    anio = str((a[15] & ~(0x0F))>>4) + str(a[15] & ~(0xF0))
                    archivos.write('FECHA: \t'+dia+'/'+ mes+'/'+anio)
                    archivos.write('\n')
                    archivos.write('LATITUD : \t')
                    archivos.write(str(a[16])+str(a[17])+"."+str(a[18])+str(a[19])+' '+chr(a[20]))
                    archivos.write('\n')
                    archivos.write('LONGITUD : \t')
                    archivos.write(str(a[21])+str(a[22])+"."+str(a[23])+str(a[24])+' '+chr(a[25]))
                    archivos.write('\n')
                    archivos.write('----------------------------------------------------\n')
                    archivos.write('BUMP1\tBUMP2\tHORA\t\tLATITUD\tLONGITUD\n')
                    archivos.close()
                elif (a[0] != 255) & (a[1] != 255) & (a[2] != 255) & (a[3] != 255):
                    a += fuente.read(12)
                    total-=12
                    archivos = open(archivo, 'a')
                    archivos.write(str((a[0]*256)+a[1])+'\t')
                    archivos.write(str((a[2]*256)+a[3])+'\t')
                    archivos.write(str(a[4])+':'+str(a[5])+':'+str(a[6])+'\t')
                    archivos.write(str(a[7])+str(a[8])+"."+str(a[9])+str(a[10])+' S'+'\t')
                    archivos.write(str(a[12])+str(a[13])+"."+str(a[14])+str(a[15])+' W'+'\n')
                    archivos.close()
                else:
                    self.ui.statusbar.showMessage("Data Recuperada")
                    self.ui.ListB.addItems(ListaFile)
                    self.ui.Estado.setText('Archivos Recuperados ' + str(self.ui.ListB.count()))
                    break

    def Escanear(self):
        try:
            ports = serial.tools.list_ports.comports()
            puertos = []
            for port, desc, hwid in sorted(ports):
                puerto = port
                puertos.append(puerto)
                #self.ui.statusbar.shooswMessage("Puerto serie detectados")
        except:
            self.ui.statusbar.showMessage("Error scan puerto serie")
        
        return puertos
    def Ejecutar(self):
        ejecuta = self.carpeta[0]+'/'+ self.ui.ListB.currentItem().text()
        os.startfile(ejecuta)




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()


    window.show()
    sys.exit(app.exec_())