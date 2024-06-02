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

    def __init__(self):
        super().__init__()
        self.init_window()

        # 启动页显示
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(102, 102))
        self.show()

        # 创建子控件
        self.home_interface = Widget('主页', self)
        self.guide_interface = Guide_Demonstrator('操作指南', self)
        self.img_video_interface = Upload_Detector('图片/视频检测', self)
        self.realtime_interface = RealTime_Detector('实时检测', self)
        self.setting_interface = Widget('设置', self)
        self.init_navigation()

        # 启动页隐藏
        self.splashScreen.finish()

    def init_navigation(self):
        self.addSubInterface(self.home_interface, FluentIcon.HOME, '主页')
        self.navigationInterface.addSeparator()
        self.addSubInterface(self.guide_interface, FluentIcon.BOOK_SHELF, '操作指南')
        self.addSubInterface(self.img_video_interface, FluentIcon.PHOTO, '图片/视频检测')
        self.addSubInterface(self.realtime_interface, FluentIcon.CAMERA, '实时检测')
        self.addSubInterface(self.setting_interface, FluentIcon.SETTING, '设置', NavigationItemPosition.BOTTOM)

    def init_window(self):
        self.resize(950, 780)
        self.setMinimumSize(950, 780)
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('驾驶员异常驾驶行为识别系统')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

