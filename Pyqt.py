import sys
import mysql.connector
from PyQt5 import QtCore, QtWidgets, QtGui
import PyQt5
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,*args,**kwargs):
        super(MainWindow,self).__init__(*args,**kwargs)
        self.InitUI()

    def InitUI(self):
        self.setWindowTitle('Variables de maquinaria')
        self.SetGeometry(300,100,800,600)
        self.setWindowIcon(QtGui.QIcon("esp32.jpg"))
       
        #Create Core Widget that holds all of the others
        self.CoreWidget=QtWidgets.QWidget()
        self.setCentralWidget(self.CoreWidget)
       
        #Create toolbar
        self.toolbar=NavigationToolbar(self.Canvas,parent=self.CoreWidget)
        
        #Define Main Canvas
        self.Canvas=MplCanvas(parent=self.CoreWidget,width=5,height=4,dpi=100)
        
        #Layouts
        layout=QtWidgets.QVBoxLayout(self.CoreWidget)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.Canvas)
        
        #Actions for Menu Bar
        #Temperature
        temperature_action=QAction('Temperatura',self)
        temperature_action.setStatusTip('Temperatura')
        temperature_action.triggered.connect(lambda:self.Search("temperatura"))
        #Humidity
        humidity_action=QAction('Humedad',self)
        humidity_action.setStatusTip('Humedad')
        humidity_action.triggered.connect(lambda:self.Search("humedad"))
        #Presión Atmosférica
        presion_action=QAction('Presión Atmosférica',self)
        presion_action.setStatusTip('Presión Atmosférica')
        presion_action.triggered.connect(lambda:self.Search("presion"))
        #Consumo Eléctrico
        consumo_action=QAction('Consumo Eléctrico',self)
        consumo_action.setStatusTip('Consumo Eléctrico')
        consumo_action.triggered.connect(lambda:self.Search("consumo"))
       
        #Status Bar
        self.statusBar()

        #Menu Bar
        self.mainMenu = self.menuBar()
        self.SearchMenu = self.mainMenu.addMenu('Search')
        self.SearchMenu.addAction(temperature_action)
        self.SearchMenu.addAction(humidity_action)
        self.SearchMenu.addAction(presion_action)
        self.SearchMenu.addAction(consumo_action)
        
        #Buttons
        #Button1
        self.button1=QPushButton('Amplify',parent=self.CoreWidget) 
        self.button1.setToolTip('Press to display this graph only')
        self.button1.resize(60,25)
        self.button1.move(296,49)
        self.button1.clicked.connect(lambda: self.amplify_function(1))
        #Button2
        self.button2=QPushButton('Amplify',parent=self.CoreWidget)
        self.button2.setToolTip('Press to display this graph only')
        self.button2.resize(60,25)
        self.button2.move(694,49)
        self.button2.clicked.connect(lambda: self.amplify_function(2))
        #Button3
        self.button3=QPushButton('Amplify',parent=self.CoreWidget)
        self.button3.setToolTip('Press to display this graph only')
        self.button3.resize(60,25)
        self.button3.move(296,304)
        self.button3.clicked.connect(lambda: self.amplify_function(3))
        #Button4
        self.button4=QPushButton('Amplify',parent=self.CoreWidget)
        self.button4.setToolTip('Press to display this graph only')
        self.button4.resize(60,25)
        self.button4.move(694,304)
        self.button4.clicked.connect(lambda: self.amplify_function(4))

        #Connect to update_plot function and shows window
        self.update_plot()
        self.show()

        #Define timer to update
        self.timer=QtCore.QTimer()
        self.timer.setInterval(30000)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    #functions
    def update_plot(self):
        #Connect to DB
        cnx = mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1',
                                  database='esp32')
        #Lists for appending values
        Id=[]
        Temperature=[]
        Humidity=[]
        Date=[]
        #Define cursor
        cursor= cnx.cursor()
        #Query to get last row
        id_query=("SELECT MAX(id) FROM temperature")
        cursor.execute(id_query)
        id_end=int(cursor.fetchone()[0]) #Tenemos ultimo valor agregado
        print(id_end)
        #We get the last added row in id_end and 10 previous rows with id_start
        id_start=id_end-10
        #Query to get the data from the last 10 added rows
        query = ("SELECT id, temperature, humidity, date FROM temperature WHERE id BETWEEN %s AND %s")
        cursor.execute(query, (id_start, id_end))
        for (id, temperature, humidity, date) in cursor: 
            print("ID:{}, temperature:{}, humidity: {}, date: {}".format(id, temperature, humidity, date))
            Id.append(id)
            Temperature.append(temperature)
            Humidity.append(humidity)
            Date.append(date)
        cursor.close()
        #Plot data 
        self.Canvas.ax1.clear()
        self.Canvas.ax1.set_title("Temperatura")
        self.Canvas.ax1.plot(Date,Temperature,marker='o',color='r')
        self.Canvas.ax2.clear()
        self.Canvas.ax2.set_title("Humedad")
        self.Canvas.ax2.plot(Date,Humidity,marker='o',color='b')
        self.Canvas.draw()

    #@pyqtSlot()
    def amplify_function(self, button_number):
        if button_number==1:
            Temperature_Window(1)
            
        elif button_number==2:
            return
        elif button_number==3:
            return
        else:
            return

    def Amplify_Window(button_pressed):
        T=QDialog()
        layoutV=QtWidgets.QVBoxLayout(T)
            
        if button_pressed == 1:
            Temp_Canvas=Temperature_Canvas(parent=T,title='Temperature')
            T.setWindowTitle('Temperatura Window')
            toolbar=NavigationToolbar(Temp_Canvas,parent=T)
            layoutV.addWidget(toolbar)
            layoutV.addWidget(Temp_Canvas)
        elif button_pressed == 2:
            Hum_Canvas=Amplify_Canvas(parent=T,title='Humidity')
            T.setWindowTitle('Humedad Window')
            toolbar=NavigationToolbar(Hum_Canvas,parent=T)
            layoutV.addWidget(toolbar)
            layoutV.addWidget(Hum_Canvas)
        elif button_pressed == 3:
            Presion_Canvas=Amplify_Canvas(parent=T,title='Presión Atmosférica')
            T.setWindowTitle('Presión  Window')
            toolbar=NavigationToolbar(Presion_Canvas,parent=T)
            layoutV.addWidget(toolbar)
            layoutV.addWidget(Presion_Canvas) 
        else:
            Consumo_Canvas=Amplify_Canvas(parent=T,title='Consumo Eléctrico')
            T.setWindowTitle('Consumo Eléctrico Window')  
            toolbar=NavigationToolbar(Consumo_Canvas,parent=T)
            layoutV.addWidget(toolbar)
            layoutV.addWidget(Consumo_Canvas)
        toolbar=NavigationToolbar(self.Canvas,parent=self.CoreWidget) 
        T.setWindowModality(Qt.ApplicationModal)
        T.exec_()

'''####################################
###         CANVAS CLASSES          ###
####################################'''
#Main Canvas
class MplCanvas(FigureCanvas):
    def __init__(self,parent=None,width=5,height=4,dpi=100):
        fig=Figure(figsize=(width,height),dpi=dpi)
        self.ax1=fig.add_subplot(1,2,1)
        self.ax1.title.set_text("Temperatura")
        self.ax2=fig.add_subplot(1,2,2)
        self.ax2.title.set_text("Humedad")
        self.ax3=fig.add_subplot(2,2,3)
        self.ax3.title.set_text("Presión Atmosférica")
        self.ax4=fig.add_subplot(2,2,4)
        self.ax4.title.set_text("Consumo Eléctrico")
        #Padding between plots
        fig.subplots_adjust(left=0.05,bottom=0.05,right=0.95,top=0.95,wspace=0.3,hspace=0.3)
        #data
        super(MplCanvas,self).__init__(fig)
        self.setParent(parent)
#Canvas for when the amplify button is pressed
class Amplify_Canvas(FigureCanvas):
    def __init__(self,parent=None,title=''):
        fig=Figure(figsize=(70,70),dpi=100)
        self.ax_temp=fig.add_subplot(1,1,1)
        self.ax_temp.title.set_text(str(title))
        super(Amplify_Canvas,self).__init__(fig)
        self.setParent(parent)
#Search Canvas



app=QtWidgets.QApplication(sys.argv)
w=MainWindow()
w.show()
sys.exit(app.exec_())