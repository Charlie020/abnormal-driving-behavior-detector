from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget
from detector_ui import DetectorWindow


class MenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('菜单')
        self.setGeometry(800, 250, 400, 300)

        self.start_button = QPushButton('开始', self)
        self.start_button.setFixedSize(100, 60)
        font = QFont()
        font.setPointSize(18)
        self.start_button.setFont(font)
        self.start_button.clicked.connect(self.start_detect)

        self.end_button = QPushButton('结束', self)
        self.end_button.setFixedSize(100, 60)
        self.end_button.setFont(font)
        self.end_button.clicked.connect(self.end_menu)

        layout = QVBoxLayout()
        layout.addWidget(self.start_button)
        layout.addSpacing(50)
        layout.addWidget(self.end_button)
        layout.setAlignment(Qt.AlignCenter)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def start_detect(self):
        self.detect_window = DetectorWindow()
        self.close()
        self.detect_window.show()

    def end_menu(self):
        self.close()