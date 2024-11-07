import sys
import cv2
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QProgressBar, QPushButton

class TreeClassificationApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Clasificación de Árboles en Tiempo Real")
        self.setGeometry(100, 100, 1000, 850)
        self.setStyleSheet("background-color: #0C2029")

        # Configuración de la cámara con OpenCV
        self.cap = cv2.VideoCapture(0)

        # Configuración de la interfaz
        self.init_ui()

        # Iniciar el temporizador para actualizar la imagen de la cámara
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(10)

    def init_ui(self):
        # Layout principal
        layout = QVBoxLayout(self)

        # Layout horizontal para dividir en 2 secciones principales
        top_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()

        # Parte superior izquierda: video
        video_panel = QWidget(self)
        video_layout = QVBoxLayout(video_panel)
        self.video_label = QLabel(self)
        self.video_label.setFixedSize(600, 500)
        self.video_label.setStyleSheet("background-color: #000000;")
        video_layout.addWidget(self.video_label)
        top_layout.addWidget(video_panel)

        # Parte superior derecha: información del árbol
        info_panel = QWidget(self)
        info_layout = QVBoxLayout(info_panel)

        # Título de la sección
        self.label_tree_info = QLabel("Información del árbol", self)
        self.label_tree_info.setStyleSheet("""
            color: white;
            background-color: #183749;
            padding: 15px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 5px;
            text-align: center;
            margin-bottom: 20px;""")
        info_layout.addWidget(self.label_tree_info)

        # Información aleatoria del árbol
        tree_data = [
            "Familia: Fagaceae",
            "Especie: Quercus robur",
            "Altura: 15 metros",
            "Ancho de copa: 10 metros",
            "Edad estimada: 40 años",
            "Distribución geográfica: Europa, Asia Menor",
            "Estado de conservación: Común",
            "Tipo de Hoja: Caduca",
            "Floración: Primavera"
        ]
       
        # Añadir cada dato al layout
        for data in tree_data:
            label = QLabel(data, self)
            label.setStyleSheet("""
                color: white;
                padding: 2px;
                font-size: 14px;
                text-align: center;
                font-family: "Arial", "Helvetica", sans-serif;  
                border-bottom: 2px solid white;
            """)   
            info_layout.addWidget(label)

        # Agregar el panel de información al layout superior
        top_layout.addWidget(info_panel)

        # Parte inferior izquierda: barra de progreso y nombre del árbol
        bottom_left_panel = QWidget(self)
        bottom_left_layout = QVBoxLayout(bottom_left_panel)
        self.label_status = QLabel("Arbol 1", self)
        self.label_status.setStyleSheet("""
            border-bottom: 2px solid white;
            color: white;   
            text-align: center;
            font-size: 20px;
        """)
        bottom_left_layout.addWidget(self.label_status)
        self.label_status.setFixedWidth(500)  
        self.label_status.setFixedHeight(100)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedWidth(self.width() // 2) 
        self.progress_bar.setFixedHeight(35) 
        self.progress_bar.setStyleSheet("""
            QProgressBar {
            text-align: center;
            font-size: 14px;
            color: white;
            background-color: #405B66;  
            border-radius: 5px;
            }
            QProgressBar::chunk {
            background-color: #D9320D;
            border-radius: 5px;
            }
        """)
        bottom_left_layout.addWidget(self.progress_bar)
        bottom_layout.addWidget(bottom_left_panel)

        # Parte inferior derecha: botones (Clasificar y Salir)
        button_panel = QWidget(self)
        button_layout = QHBoxLayout(button_panel)  # Cambié de QVBoxLayout a QHBoxLayout
        self.btn_clasificar = QPushButton("Clasificar", self)
        self.btn_clasificar.setStyleSheet("""
            QPushButton {
                font-family: Arial, sans-serif;
                background-color: #183749;
                color: white;
                padding: 10px 20px;
                font-size: 20px;
                font-weight: bold;
                margin-right:40px;
                transition: background-color 0.5s ease;
            }
            QPushButton:hover {
                color: black;
                background-color: #D1E3E8;
            }
        """)
        self.btn_clasificar.clicked.connect(self.classify_image)
        button_layout.addWidget(self.btn_clasificar)

        self.btn_salir = QPushButton("Salir", self)
        self.btn_salir.setStyleSheet("""
            QPushButton {
                font-family: Arial, sans-serif;
                background-color: #183749;
                color: white;
                padding: 10px 20px;
                font-size: 20px;
                font-weight: bold;
                margin-right:20px;
                transition: background-color 0.5s ease;
            }
            QPushButton:hover {
                color: black;
                background-color: #D1E3E8;
            }
        """)
        self.btn_salir.clicked.connect(self.close)
        button_layout.addWidget(self.btn_salir)
        
        bottom_layout.addWidget(button_panel)

        # Añadir los layouts de la parte superior y la parte inferior al layout principal
        layout.addLayout(top_layout)
        layout.addLayout(bottom_layout)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(q_img))

    def classify_image(self):
        self.label_status.setText("Estado: Clasificando...")
        for i in range(101):
            self.progress_bar.setValue(i)
            QApplication.processEvents()
        self.label_status.setText("Estado: Clasificación completada")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TreeClassificationApp()
    window.show()
    sys.exit(app.exec_())
