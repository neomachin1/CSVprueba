from rugo2024 import Ui_MainWindow
#from PyQt5.QtWidgets import QSizePolicy, QMainWindow
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import serial.tools.list_ports
import serial
import os
from time import sleep
from nmeasim.simulator import Simulator

import numpy as np
import struct
from zipfile import ZipFile as zp
import hashlib
import sys
import csv
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import pyqtSignal, QObject

from serial import Serial
from time import sleep
from nmeasim.simulator import Simulator

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
        self.serie = self.Escanear()
        
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
                    
                    sleep(0.5)
                    f = open('BumpData.bin', 'wb')
                    for paginas in range(PData):
                        ser.write(b'U1')
                        sleep(0.1)
                        RData = bytes(ser.read(128))
                        print(type(RData), type(RData[0]))

                        #data = bytearray(RData)
                        #f.write(b'Inicio')
                        f.write(RData)
        
                        for datas in RData:
                            print(datas, end=' ')
                        print()
                    f.close()
            except:
                QMessageBox.about(self, "Equipo comunicacion", "Equipo no conectado")
               
            #print(RData, end=' ')

            
            
        else:
            QMessageBox.about(self, "Equipo comunicacion", "Equipo no conectado")
        

        '''sim = Simulator()
        sim.serve(output=ser, blocking=False)
        sleep(1)
        sim.kill()'''

        '''ruta, data = QFileDialog.getSaveFileName(self, "Data Roughness", "DataBump.txt", "Data Files (*.txt)")
        self.ui.Estado.setText("...Descargando Data Rugosimetro...")
        self.ruta = os.path.basename(ruta)
        print()
        print(os.path.basename(ruta), os.path.dirname(ruta), sep="\t")
        
        #self.ui.statusbar.showMessage(self.ui.PuertoS.currentText())'''
        self.ui.statusbar.showMessage("Boton Leer Memoria")
    
    def BorraM(self):
        QMessageBox.about(self, "Equipo comunicacion", "Equipo no conectado")
        self.ui.statusbar.showMessage("Borrar Memoria")
        
    
    def SalirM(self):
        print('Terminar')
        self.ui.statusbar.showMessage("Salir Ventana")
        self.close()

        
    def Recupera(self):
        ruta, data = QFileDialog.getOpenFileName(self, 'Buscar Archivo Rugosimetro', '', 'Roughness File (*.abp *.rbd *.txt)')
        #ruta, data = QFileDialog.getSaveFileName(self, "Data Roughness", "DataBump.txt", "Data Files (*.txt)")
        nombre = os.path.basename(ruta)
        carpeta = os.path.dirname(ruta)
        '''print('nombre: ', nombre)
        print('carpeta: ', carpeta)
        print('ruta: ', ruta)'''
        
    
        '''abrir = open(ruta, 'rb')#, encoding='utf-16-le')#, errors='ignore')
        linea = abrir.read(2)
        dos = abrir.read(2)
        print("linea: ", int.from_bytes(linea, byteorder='big'))
        print("dos: ", int.from_bytes(dos, byteorder='big'))
        abrir.close()
        
        with open(ruta, 'rb') as f:
            print(hashlib.sha256(f.read()).hexdigest())
        print('------------------------')'''
        print(os.path.getsize(ruta))
        sizefile = int((os.path.getsize(ruta)/2)-1)
        print(sizefile)
        
        with open(ruta, 'rb') as f:
            cntByte = 0
            cntFile = 0
            High = 0
            Low = 0
            Latitud = 0
            Lati = 0

            Longitud = 0
            Long = 0

            hora = []
            fecha = []
            
            data = np.fromfile(f, dtype='>u2', count=5)
            cntByte+=4
            print('Longitud2: ', sizefile, cntByte)
            data = data[1:]   #Primer Byte descartado
            
            High = data[0]+data[1]
            Low = data[2]+data[3]
            
            while (High == Low) and (High != 0):
                Low = 55
                if ((sizefile < cntByte) or (cntFile >400)):
                    print('termina')
                    break
                nuevo = nombre[:-4]+'9'+str(cntFile)+".csv"
                print(nuevo)
               
                with open(nuevo, 'w', newline='') as csvfile:
                    csvwrite = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    data = np.fromfile(f, dtype='>u2', count=28)
                    cntByte+=28
                    if ((sizefile < cntByte) or (cntFile >400)):
                        print('termina')
                        break
                    
                    High = (data[0]*256)+data[1]
                    High = str(High)+'.'+str(data[2]*100)
                    csvwrite.writerow(['KM', High])
                    
                    High = data[3]*100
                    csvwrite.writerow(['FRECUENCIA', High])
                    
                    csvwrite.writerow(['SENTIDO', chr(data[4])])
                    

                    codvia = ''.join(list(map(lambda x : chr(x), data[5:10])))
                    #print(codvia)
                    csvwrite.writerow(['CODVIA', codvia])
                                     
                    hora = ''.join(list(map(lambda x: '0'+str(x)+':' if x<10 else str(x)+':', data[10:13])))
                    print('hora: ', hora[:-1])
                    csvwrite.writerow(['HORA', hora[:-1]])
                        
                    fecha = ''.join(list(map(lambda x: '0'+str(x)+'/' if x<10 else str(x)+'/', data[13:16]) ))
                    print('fecha: ' , fecha[:-1])
                    csvwrite.writerow(['FECHA', fecha[:-1]])
                    
                    High = (data[16]*256)+data[17]
                    Latitud = High/100
                    Lati = High%100

                    High = (data[18]*1000)
                    Low = (data[19]*256)+data[20]
                    High += Low
                    
                    Lati = round(float(str(Lati) + '.' + str(High))/60, 5)
                    Latitud += Lati
                    if data[21] == 83:#'S'
                        Latitud*=-1
                    Latitud = round(Latitud, 4)
                    print('LATITUD: ', Latitud, data[21], chr(data[21]))
                    csvwrite.writerow(['LATITUD', Latitud])
                    
                    High = (data[22]*256)+data[23]
                    Longitud = High/100
                    Long = High%100

                    High = (data[24]*1000)
                    Low = (data[25]*256)+data[26]
                    High += Low
                    
                    Long = round(float(str(Long) + '.' + str(High))/60, 5)
                    Longitud += Long
                    if data[27] == 87:#'W'
                        Longitud*=-1
                    Longitud = round(Longitud,4)
                    print('LONGITUD: ', Longitud, data[27], chr(data[27]))
                    csvwrite.writerow(['LONGITUD', Longitud])
                    
                    csvwrite.writerow(['CANAL 1', 'CANAL 2', 'HORA', 'FECHA', 'LATITUD', 'LONGITUD'])
                    
                    data = np.fromfile(f, dtype='>u2', count=4)
                    cntByte+=4
                    print(list(map(lambda x: chr(x), data)), 'bytes: ', cntByte)
                    High = data[0]+data[1]
                    Low = data[2]+data[3]
                    
                    while (High != 255) or (Low != 255):  #Data != UaUa
                        if sizefile < cntByte:
                            break
                        filas = []
                        High = (data[0]*256)+data[1]
                        Low = (data[2]*256)+data[3]
                        filas.append(High)
                        filas.append(Low)
                        High = 255
                        Low = 255
                        data = np.fromfile(f, dtype='>u2', count=20)        #Matriz datos 24 bytes
                        cntByte+=20
                        if sizefile < cntByte:
                            break
                        print(data, len(data), 'bytes: ', cntByte)
                        
                        hora = ''.join(list(map(lambda x: '0'+str(x)+':' if x<10 else str(x)+':', data[0:3])))
                        filas.append(hora[:-1])
                            
                        fecha = ''.join(list(map(lambda x: '0'+str(x)+'/' if x<10 else str(x)+'/', data[3:6]) ))
                        filas.append(fecha[:-1])
                        
                        High = (data[6]*256)+data[7]
                        Latitud = High/100
                        Lati = High%100

                        High = (data[8]*1000)
                        Low = (data[9]*256)+data[10]
                        High += Low
                        
                        Lati = round(float(str(Lati) + '.' + str(High))/60, 5)
                        Latitud += Lati
                        if data[11] == 83:#'S'
                            Latitud*=-1
                        Latitud = round(Latitud, 4)
                        filas.append(Latitud)
                        
                        High = (data[12]*256)+data[13]
                        Longitud = High/100
                        Long = High%100

                        High = (data[14]*1000)
                        Low = (data[15]*256)+data[16]
                        High += Low
                        
                        Long = round(float(str(Long) + '.' + str(High))/60, 5)
                        Longitud += Long
                        if data[17] == 87:#'W'
                            Longitud*=-1
                        Longitud = round(Longitud, 4)
                        filas.append(Longitud)            
                        
                        print(filas)
                        csvwrite.writerow(filas)
                        del filas
                        data = np.fromfile(f, dtype='>u2', count=4)        #Matriz datos 24 bytes
                        cntByte+=4
                        print('bytes', cntByte)
                        High = data[0]+data[1]
                        Low = data[2]+data[3]
                        if (sizefile < cntByte):
                            break
                        print('Rutina datos')
                    cntFile+=1
                    
                print('Fin Archivo')#High = 125

            cntFile+=1
            print('with', High)
        
        print(High)
            

        print("Orden nativo", sys.byteorder)
        self.ui.statusbar.showMessage("Recuperar Archivo")
    
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
    def Crear(self):
        print("Creacion opciones")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.Crear()

    window.show()
    sys.exit(app.exec_())