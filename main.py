from ui import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, Qt
import random, sys, time, datetime, locale
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

x_pozisyon = []
y_pozisyon = []
z_pozisyon = []

x_hiz = []
y_hiz = []
z_hiz = []

x_ivme = []
y_ivme = []
z_ivme = []

pitch = []
roll = []
yaw = []

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, max_deger=100, min_deger=0):
        figure = Figure()
        self.axes = figure.add_subplot(111)
        figure.set_facecolor('none') 
        figure.subplots_adjust(left=0.08, right=0.98, top=0.75, bottom=0.35)
        super(MplCanvas, self).__init__(figure)
        self.setStyleSheet("background: transparent;")
        self.setAttribute(Qt.WA_TranslucentBackground)

class Main(QMainWindow):
    def __init__(self):
        super().__init__() 
        
        self.main = Ui_MainWindow()
        self.main.setupUi(self)
        self.setWindowTitle("HYPERUSH") 
        
        self.main.label_saat.setText(datetime.datetime.now().strftime("%H:%M"))

        locale.setlocale(locale.LC_TIME, 'tr_TR.UTF-8')

        tarih = datetime.datetime.now().strftime("%-d %B %A %Y") 
        self.main.label_tarih.setText(tarih)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.random_veri)
        
        self.start_time = time.time()
        self.timer.start(1000)
        
        self.main.forwardButton.clicked.connect(self.ileri)
        self.main.backwardButton.clicked.connect(self.geri)
        self.main.stopButton.clicked.connect(self.stop)
        
        self.time = []
        self.sicaklik1 = 0
        self.sicaklik2 = 0
        self.guc = 0
        
    def random_veri(self):
        x_pozisyon.append(random.randint(1, 100))
        y_pozisyon.append(random.randint(1,100))
        z_pozisyon.append(random.randint(1, 100))
    
        x_hiz.append(random.randint(1, 10))
        y_hiz.append(random.randint(1, 10))
        z_hiz.append(random.randint(1, 10))
    
        x_ivme.append(random.randint(1, 5))
        y_ivme.append(random.randint(1, 5))
        z_ivme.append(random.randint(1, 5))
    
        pitch.append(random.randint(1, 360))
        roll.append(random.randint(1, 360))
        yaw.append(random.randint(1, 360))
    
        self.sicaklik1 = random.randint(20, 40)
        self.sicaklik2 = random.randint(20, 40)
        self.guc = random.randint(1, 50)
    
        self.time.append(time.time() - self.start_time)
    
        self.grafik_ciz(self.main.frame_pozisyon, self.time, x_pozisyon, y_pozisyon, z_pozisyon, "Pozisyon (m)")
        self.grafik_ciz(self.main.frame_hiz, self.time, x_hiz, y_hiz, z_hiz, "Hız (m/s)")
        self.grafik_ciz(self.main.frame_ivme, self.time, x_ivme, y_ivme, z_ivme, "İvme (m/s²)")
        self.grafik_ciz(self.main.frame_yonelim, self.time, pitch, roll, yaw, "Yönelim (°)")
    
        self.main.label_poz_x.setText(f"X: {x_pozisyon[-1]:.2f}")
        self.main.label_poz_y.setText(f"Y: {y_pozisyon[-1]:.2f}")
        self.main.label_poz_z.setText(f"Z: {z_pozisyon[-1]:.2f}")
        self.main.label_hiz_x.setText(f"X: {x_hiz[-1]:.2f}")
        self.main.label_hiz_y.setText(f"Y: {y_hiz[-1]:.2f}")
        self.main.label_hiz_z.setText(f"Z: {z_hiz[-1]:.2f}")
        self.main.label_ivme_x.setText(f"X: {x_ivme[-1]:.2f}")
        self.main.label_ivme_y.setText(f"Y: {y_ivme[-1]:.2f}")
        self.main.label_ivme_z.setText(f"Z: {z_ivme[-1]:.2f}")
        self.main.label_pitch.setText(f"PITCH: {pitch[-1]:.2f}")
        self.main.label_roll.setText(f"ROLL: {roll[-1]:.2f}")
        self.main.label_yaw.setText(f"YAW: {yaw[-1]:.2f}")
        
        self.sicaklik_grafigi()
        self.guc_ciz()
    
    def ileri(self):
        pass
    def geri(self):
        pass
    def stop(self):
        self.timer.stop()
        
    def grafik_ciz(self, frame, t, y1, y2, y3, title):
        graph = MplCanvas(frame, max_deger=100, min_deger=0)
        
        graph.axes.plot(t, y1, color='red',label='X')
        graph.axes.plot(t, y2, color='green',label='Y')
        graph.axes.plot(t, y3, color='blue',label='Z')
        
        if len(t) > 5:
            graph.axes.set_xlim(t[-5], t[-1])  
            
        elif len(t) == 1:
            graph.axes.set_xlim(0, 1) 
        else:
            graph.axes.set_xlim(t[0], t[-1])
        
        graph.axes.set_facecolor('#ACDDFF') 
        graph.axes.set_title(title, color='white')
        legend = graph.axes.legend(loc='upper right')
            
        for label in graph.axes.get_xticklabels() + graph.axes.get_yticklabels():
            label.set_color('white')
        
        layout = frame.layout()
        if layout is None:
            layout = QVBoxLayout()
            frame.setLayout(layout)
        
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
                
        
        layout.addWidget(graph)
        
    def sicaklik_grafigi(self):
        base_style = ("""#frame{
            background-color: qlineargradient(spread:reflect, x1:1, y1:0.739, x2:1, y2:0, 
            stop:{STOP_1} rgba(121, 207, 214, 255), 
            stop:{STOP_2} rgba(255, 255, 255, 0));
        }""")
        
        temp_progress_p1 = self.sicaklik1 / 40
        temp_progress_p2 = self.sicaklik2 / 40
        
        # Stop değerlerini hesapla
        stop_1_p1 = str(temp_progress_p1 - 0.001)
        stop_2_p1 = str(temp_progress_p1)
        stop_1_p2 = str(temp_progress_p2 - 0.001)
        stop_2_p2 = str(temp_progress_p2)
        
        new_style_p1 = base_style.replace("{STOP_1}", stop_1_p1).replace("{STOP_2}", stop_2_p1)
        new_style_p2 = base_style.replace("{STOP_1}", stop_1_p2).replace("{STOP_2}", stop_2_p2).replace("frame", "frame_2")
        
        self.main.frame.setStyleSheet(new_style_p1)
        self.main.frame_2.setStyleSheet(new_style_p2)
        

        frame_height = self.main.frame.height()
        frame_width = self.main.frame.width()
        frame_2_height = self.main.frame_2.height()
        frame_2_width = self.main.frame_2.width()
        
        label1_height = self.main.label_sicaklik1.height()
        label1_width = self.main.label_sicaklik1.width()
        label2_height = self.main.label_sicaklik2.height()
        label2_width = self.main.label_sicaklik2.width()
        

        y_pos_1 = int(frame_height * (1 - temp_progress_p1)) - (label1_height // 2 - 20)
        y_pos_2 = int(frame_2_height * (1 - temp_progress_p2)) - (label2_height // 2 - 20)
        
        x_pos_1 = (frame_width - label1_width) // 2
        x_pos_2 = (frame_2_width - label2_width) // 2
        
        self.main.label_sicaklik1.move(x_pos_1, y_pos_1)
        self.main.label_sicaklik2.move(x_pos_2, y_pos_2)
        
        self.main.label_sicaklik1.setText(f"{self.sicaklik1}°C")
        self.main.label_sicaklik2.setText(f"{self.sicaklik2}°C")

    
    def guc_ciz(self):
        base_style =("""#widget_guc{
background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(121, 207, 214, 255), stop:{STOP_2} rgba(121, 207, 214, 0), stop:0.981 rgba(185, 51, 34, 0));
border-radius:90px
}""")

        watt_pressure = float((self.guc) / (50))

        stop_1 = str(watt_pressure - 0.001)
        stop_2 = str(watt_pressure)

        new_style = base_style.replace("{STOP_1}", stop_1).replace("{STOP_2}", stop_2)
        self.main.widget_guc.setStyleSheet(new_style)
        self.main.label_guc.setText(f"{self.guc}\nWATT")
    
        
        
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main() 
    main.show() 
    sys.exit(app.exec_()) 