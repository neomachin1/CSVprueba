'''import pickle
print("WORKING WITH BINARY FILES")
bfile=open("empfile.dat","ab")
recno=1
print ("Enter Records of Employees")
print()
#taking data from user and dumping in the file as list object
while True:
 print("RECORD No.", recno)
 eno=int(input("\tEmployee number : "))
 ename=input("\tEmployee Name : ")
 ebasic=int(input("\tBasic Salary : "))
 allow=int(input("\tAllowances : "))
 totsal=ebasic+allow
 print("\tTOTAL SALARY : ", totsal)
 edata=[eno,ename,ebasic,allow,totsal]
 pickle.dump(edata,bfile)
 ans=input("Do you wish to enter more records (y/n)? ")
 recno=recno+1
 if ans.lower()=='n':
    print("Record entry OVER ")
    print()
    break
# retrieving the size of file
print("Size of binary file (in bytes):",bfile.tell())
bfile.close()

# Reading the employee records from the file using load() module
print("Now reading the employee records from the file")
print()
readrec=1
try:
  with open("empfile.dat","rb") as bfile:
    while True:
      edata=pickle.load(bfile)
      print("Record Number : ",readrec)
      print(edata)
      readrec=readrec+1
except EOFError:
    print('Final File')
bfile.close()'''

from PyQt5 import QtCore, QtGui, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure

import seaborn as sns

from gui import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        sns.set_theme(style="darkgrid")
        tips = sns.load_dataset("tips")

        self.plot(self.ui.Level1, tips, "plot1")
        self.plot(self.ui.Level2, tips, "plot2")
        self.plot(self.ui.Level3, tips, "plot3")

    def plot(self, widget, df, title):
        canvas = FigureCanvas(Figure())
        ax = canvas.figure.subplots()
        sns.boxplot(ax=ax, x="day", y="total_bill", data=df, width=0.2, whis=10)
        ax.set_title(title)
        lay = QtWidgets.QVBoxLayout(widget)
        lay.addWidget(canvas)
        canvas.draw()
        return canvas


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    w = MainWindow()
    w.show()
    app.exec_()