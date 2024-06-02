import cv2
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QStackedWidget, QPushButton, QLabel, QVBoxLayout, QFrame
from qfluentwidgets import TitleLabel, ToolButton, FluentIcon


class Guide_Demonstrator(QWidget):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text.replace(' ', '-'))

        # 标题
        self.title_label = TitleLabel('操作指南', self)
        self.title_label.setFont(QFont('SimHei', 20))
        self.title_label.setGeometry(15, 5, 200, 50)

        # 展示页面
        self.img_num = 2
        self.stackedWidget = QStackedWidget(self)
        self.stackedWidget.setGeometry(15, 50, 830, 600)
        self.stackedWidget.setFrameShape(QFrame.Box)

        # 图片、视频检测页面指南
        self.page_0 = QWidget()
        self.__upload_guide_label = QLabel(self)
        self.__upload_guide_label.setPixmap(self.get_pixmap('resource/img/upload_guide.png'))
        self.__upload_guide_label.setScaledContents(True)
        page_0_layout = QVBoxLayout(self.page_0)
        page_0_layout.addWidget(self.__upload_guide_label)
        self.stackedWidget.addWidget(self.page_0)

        # 实时检测页面指南
        self.page_1 = QWidget()
        self.__realtime_guide_label = QLabel(self)
        self.__realtime_guide_label.setPixmap(self.get_pixmap('resource/img/realtime_guide.png'))
        self.__realtime_guide_label.setScaledContents(True)
        page_1_layout = QVBoxLayout(self.page_1)
        page_1_layout.addWidget(self.__realtime_guide_label)
        self.stackedWidget.addWidget(self.page_1)

        # 跳转按钮
        self.jump_left_button = ToolButton(FluentIcon.RETURN, self)
        self.jump_left_button.setGeometry(400, 660, 40, 40)
        self.jump_left_button.clicked.connect(self.jump_left)

        self.jump_right_button = ToolButton(FluentIcon.RIGHT_ARROW, self)
        self.jump_right_button.setGeometry(450, 660, 40, 40)
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