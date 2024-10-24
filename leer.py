import os
import csv
from openpyxl import Workbook

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

h = open('BumpData.bin', 'rb')
total =os.path.getsize('BumpData.bin')
print('total bytes: ', total)
counter=0


while (total >= 7):
    a = h.read(4)#iniciamos lectura datos
    total-=4
    print(total)
    if (a[0] == 85) & (a[1] == 170) & (a[2] == 85) & (a[3] == 170):
        archivo = 'file'+str(counter)+'.txt'
        counter+=1
        a = h.read(28)
        total-=28
        print()
        cabezera(a, archivo)
    elif (a[0] != 255) & (a[1] != 255) & (a[2] != 255) & (a[3] != 255):
        a += h.read(12)
        total-=12
        DataB(a, archivo)
    else:
        print('Acabo el archivo')
        break

        

print()
'''print('km :', (a[0]*256)+a[1], '.', a[2], sep='') #a[4], a[5]
#print('km.d: ', a[6])
print('long: ', a[3]*100)
print('sentido: ', chr(a[4]))
print('Codvia: ', end='')
for data in a[5:10]:
    print(chr(data), end='')
print()
print('hora, minuto, segundo: ', a[10], a[11], a[12], sep=' ')

dia = (a[13] & ~(0xCF))>>4
dia1= a[13] & ~(0xF0)

mes = (a[14]&~(0xEF))>>4
mes1= a[14]&~(0xF0)

anio = (a[15] & ~(0x0F))>>4
onio = a[15] & ~(0xF0)

print('dia, mes, año: ', dia, dia1,' ',  mes, mes1, ' ', anio, onio, sep='')
print('LATITUD: ', a[16], a[17], a[18], a[19], chr(a[20]))
print('LONGITUD: ', a[21], a[22], a[23], a[24], chr(a[25]))
print('Cierre: ', a[26], a[27])
a = h.read(4)

if (a[0] == 85) & (a[1] == 170):
    if (a[2] == 85) & (a[3] == 170):
        print('Segundo grupo de datos')
        print('cabezera correcta: ', end='')
        for data in a[:4]:
            print(data, chr(data), end=' ')
        a = h.read(28)
counter=0
print()
print('km :', (a[0]*256)+a[1], '.', a[2], sep='') #a[4], a[5]
#print('km.d: ', a[6])
print('long: ', a[3]*100)
print('sentido: ', chr(a[4]))
print('Codvia: ', end='')
for data in a[5:10]:
    print(chr(data), end='')
print()
print('hora, minuto, segundo: ', a[10], a[11], a[12], sep=' ')

dia = (a[13] & ~(0xCF))>>4
dia1= a[13] & ~(0xF0)

mes = (a[14]&~(0xEF))>>4
mes1= a[14]&~(0xF0)

anio = (a[15] & ~(0x0F))>>4
onio = a[15] & ~(0xF0)

print('dia, mes, año: ', dia, dia1,' ',  mes, mes1, ' ', anio, onio, sep='')
print('LATITUD: ', a[16], a[17], a[18], a[19], chr(a[20]))
print('LONGITUD: ', a[21], a[22], a[23], a[24], chr(a[25]))
print('Cierre: ', a[26], a[27])

if (a[0] == 85) & (a[1] == 170):
    if (a[2] == 85) & (a[3] == 170):
        print('Tercer grupo de datos')
        print('cabezera correcta: ', end='')
        for data in a[:4]:
            print(data, chr(data), end=' ')
        a = h.read(28)'''

h.close()



