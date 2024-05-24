import cv2
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QStackedWidget, QPushButton, QLabel, QVBoxLayout, QFrame


class Guide_Demonstrator(QWidget):
    def __init__(self):
        super().__init__()

        # 标题
        self.text_label = QLabel('操作指南', self)
        self.text_label.setFont(QFont('SimHei', 16))
        self.text_label.setGeometry(0, 0, 150, 60)

        # 展示页面
        self.img_num = 2
        self.stackedWidget = QStackedWidget(self)
        self.stackedWidget.setGeometry(0, 50, 830, 600)
        self.stackedWidget.setFrameShape(QFrame.Box)

        # 图片、视频检测页面指南
        self.page_0 = QWidget()
        self.__upload_guide_label = QLabel(self)
        self.__upload_guide_label.setPixmap(self.get_pixmap('resource/guide_img/upload_guide.png'))
        self.__upload_guide_label.setScaledContents(True)
        page_0_layout = QVBoxLayout(self.page_0)
        page_0_layout.addWidget(self.__upload_guide_label)
        self.stackedWidget.addWidget(self.page_0)

        # 实时检测页面指南
        self.page_1 = QWidget()
        self.__realtime_guide_label = QLabel(self)
        self.__realtime_guide_label.setPixmap(self.get_pixmap('resource/guide_img/realtime_guide.png'))
        self.__realtime_guide_label.setScaledContents(True)
        page_1_layout = QVBoxLayout(self.page_1)
        page_1_layout.addWidget(self.__realtime_guide_label)
        self.stackedWidget.addWidget(self.page_1)

        # 跳转按钮
        self.jump_left_button = QPushButton(self)
        self.jump_left_button.setGeometry(150, 15, 25, 25)
        self.jump_left_button.setText('◀')
        self.jump_left_button.clicked.connect(self.jump_left)

        self.jump_right_button = QPushButton(self)
        self.jump_right_button.setGeometry(180, 15, 25, 25)
        self.jump_right_button.setText('▶')
        self.jump_right_button.clicked.connect(self.jump_right)

        self.stackedWidget.setCurrentIndex(0)

    def get_pixmap(self, path):
        img = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)
        h, w, ch = img.shape
        bytes_per_line = ch * w
        return QPixmap.fromImage(QImage(img.data, w, h, bytes_per_line, QImage.Format_RGB888))

    def jump_left(self):
        self.stackedWidget.setCurrentIndex((self.stackedWidget.currentIndex() + self.img_num - 1) % self.img_num)

    def jump_right(self):
        self.stackedWidget.setCurrentIndex((self.stackedWidget.currentIndex() + 1) % self.img_num)