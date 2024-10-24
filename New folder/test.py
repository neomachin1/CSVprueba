print ( 1 | 1)
print ( 2 | 1)
print ( 3 | 1)
print ( 4 | 1)
print ( 5 | 1)
print ( 6 | 1)
data = bytearray(10)
print(data)

from os import strerror
data = bytearray(10)

for i in range(len(data)):
    data[i] = 10 + i

'''try:
    bf = open('Data.txt', 'wb')
    bf.write(data)
    bf.close()
except IOError as e:
    print("Se produjo un error de E/S:", strerror(e.errno))'''

try:
    binary_file = open('Data.txt', 'rb')
    binary_file.readinto(data)
    binary_file.close()

    for b in data:
        print(hex(b), end=' ')
except IOError as e:
    print("Se produjo un error de E/S:", strerror(e.errno))
    
print()
print()
try:
    binary_file = open('Data.txt', 'rb')
    data = bytearray(binary_file.read(20))
    binary_file.close()

    for b in data:
        print(hex(b), b, end=' ')

except IOError as e:
    print("Se produjo un error de E/S:", strerror(e.errno))

'''
print()
print()
import os
import platform
print(platform.uname())
from datetime import date

import time
today = date.today()

print("Hoy:", today)
print("Año:", today.year)
print("Mes:", today.month)
print("Día:", today.day)

timestamp = time.time()
print("Marca de tiempo:", timestamp)

d = date.fromtimestamp(timestamp)
print("Fecha:", d)

d = date(1991, 2, 5)
print(d)

d = d.replace(year=1992, month=1, day=16)
print(d)

d = date(2019, 11, 4)
print(d.weekday())


d = date(2020, 1, 4)
print(d.strftime('%Y/%m/%d'))

from datetime import time
from datetime import datetime
t = time(14, 53)
print(t.strftime("%H:%M:%S"))

dt = datetime(2020, 11, 4, 14, 53)
print(dt.strftime("%y/%B/%d %H:%M:%S"))

from datetime import timedelta

delta = timedelta(weeks=2, days=2, hours=3)
print(delta)
print("Días:", delta.days)
print("Segundos:", delta.seconds)
print("Microsegundos:", delta.microseconds)

import calendar
#calendar.prcal(2020)
print(calendar.calendar(2020))
print(calendar.month(2020, 11))

calendar.setfirstweekday(calendar.SUNDAY)
calendar.prmonth(2020, 12)

print(calendar.weekday(2020, 12, 24))

print(calendar.weekheader(2))

print("Es biciesto 2020? ", calendar.isleap(2020))
print("Cuantos biciestos 2010-2021? ", calendar.leapdays(2010, 2021))

#c = calendar.Calendar(calendar.SUNDAY)

for weekday in c.iterweekdays():
    print(weekday, end=" ")
print()
c = calendar.Calendar()

for date in c.itermonthdates(2019, 11):
    print(date, end=" ")
print()
c = calendar.Calendar()

for iter in c.itermonthdays(2019, 11):
    print(iter, end=" ")
print()

c = calendar.Calendar()

for data in c.monthdays2calendar(2020, 12):
    print(data)


tupla = (0, 1, 2, 3, 4, 5, 6)
foo = list(filter(lambda x: x-0 and x-1, tupla))
print(foo)

def I():
    s = 'abcdef'
    for c in s[::2]:
        yield c


for x in I():
    print(x, end='')

def fun(n):
    s = '+'
    for i in range(n):
        s += s
        yield s


for x in fun(2):
    print(x, end='');

def o(p):
    def q():
        return '*' * p
    return q


r = o(1)
s = o(2)
print(r() + s())

b = bytearray(3)
print(b)

b = bytearray(3)
print(b)

import os

os.mkdir('pictures')
os.chdir('pictures')
os.mkdir('thumbnails')
os.chdir('thumbnails')
os.mkdir('tmp')
os.chdir('../')

print(os.getcwd())

import os

os.mkdir('thumbnails')
os.chdir('thumbnails')

sizes = ['small', 'medium', 'large']

for size in sizes:
    os.mkdir(size)

print(os.listdir())

from datetime import date

date_1 = date(1992, 1, 16)
date_2 = date(1991, 2, 5)

print(date_1 - date_2)

datetime = datetime(2019, 11, 27, 11, 27, 22)
print(datetime.strftime('%y/%B/%d %H:%M:%S'))

print(calendar.weekheader(2))'''
print()
import calendar
c = calendar.Calendar()

for weekday in c.iterweekdays():
    print(weekday, end=" ")

import math
print(dir(math))

print(__name__)

try:
    raise Exception
except BaseException:
    print("a")
except Exception:
    print("b")
except:
    print("c")

for line in open('Data.txt', 'rb'):
    print (line)

'''try:
    raise Exception
except:
    print("c")
except BaseException:
    print("a")
except Exception:
    print("b")'''

import calendar

calendar.setfirstweekday(calendar.SUNDAY)
print(calendar.weekheader(3))



