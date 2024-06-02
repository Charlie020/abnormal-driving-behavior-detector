import sys

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QFrame
from qfluentwidgets import NavigationItemPosition, FluentWindow, SubtitleLabel, setFont, SplashScreen
from qfluentwidgets import FluentIcon

from guide_demonstrator import Guide_Demonstrator
from upload_detector import Upload_Detector
from real_time_detector import RealTime_Detector


# YOLOv8权重路径
def get_yolo_weight():
    return r'resource/model_weight/best.pt'


class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)

        # 必须给子界面设置全局唯一的对象名
        self.setObjectName(text.replace(' ', '-'))


class MainWindow(FluentWindow):
    """ 主界面 """

    def __init__(self):
        super().__init__()
        self.init_window()

        # 创建启动页面
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(102, 102))

        # 在创建其他子页面前先显示主界面
        self.show()

        # 创建子界面
        self.home_interface = Widget('Home Interface', self)
        self.guide_interface = Guide_Demonstrator('Guide Interface', self)
        self.img_video_interface = Upload_Detector('Image/Video Interface', self)
        self.realtime_interface = RealTime_Detector('Real-time Interface', self)
        self.setting_interface = Widget('Setting Interface', self)
        self.init_navigation()

        # 隐藏启动页面
        self.splashScreen.finish()

    def init_navigation(self):
        self.addSubInterface(self.home_interface, FluentIcon.HOME, 'Home')

        self.navigationInterface.addSeparator()
        self.addSubInterface(self.guide_interface, FluentIcon.BOOK_SHELF, 'Guide')
        self.addSubInterface(self.img_video_interface, FluentIcon.PHOTO, 'Image/Video Detector')
        self.addSubInterface(self.realtime_interface, FluentIcon.CAMERA, 'Real-time Detector')

        self.addSubInterface(self.setting_interface, FluentIcon.SETTING, 'Settings', NavigationItemPosition.BOTTOM)

    def init_window(self):
        self.resize(950, 760)
        self.setMinimumSize(950, 760)
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('驾驶员异常驾驶行为识别系统')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

