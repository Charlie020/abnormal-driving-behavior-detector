import sys

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import NavigationItemPosition, FluentWindow, SplashScreen, FluentIcon

from home import Home
from guide_demonstrator import Guide_Demonstrator
from upload_detector import Upload_Detector
from real_time_detector import RealTime_Detector
from settings import Settings


class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        self.init_window()

        # 启动页显示
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(102, 102))
        self.show()

        # 创建子控件
        self.home_interface = Home('主页', self)
        self.guide_interface = Guide_Demonstrator('操作指南', self)
        self.upload_interface = Upload_Detector('图片/视频检测', self)
        self.realtime_interface = RealTime_Detector('实时检测', self)
        self.setting_interface = Settings('设置', self)

        # 创建导航页
        self.init_navigation()

        # 启动页隐藏
        self.splashScreen.finish()

    def init_navigation(self):
        self.addSubInterface(self.home_interface, FluentIcon.HOME, '主页')
        self.home_interface.switch_to_guide_signal.connect(self.switch_to_guide_interface)
        self.home_interface.switch_to_upload_signal.connect(self.switch_to_upload_interface)
        self.home_interface.switch_to_realtime_signal.connect(self.switch_to_realtime_interface)
        self.home_interface.switch_to_setting_signal.connect(self.switch_to_setting_interface)

        self.navigationInterface.addSeparator()
        self.addSubInterface(self.guide_interface, FluentIcon.BOOK_SHELF, '操作指南')
        self.addSubInterface(self.upload_interface, FluentIcon.PHOTO, '图片/视频检测')
        self.addSubInterface(self.realtime_interface, FluentIcon.CAMERA, '实时检测')
        self.addSubInterface(self.setting_interface, FluentIcon.SETTING, '设置', NavigationItemPosition.BOTTOM)

    def init_window(self):
        self.resize(950, 780)
        self.setMinimumSize(950, 780)
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('驾驶员异常驾驶行为识别系统')

    def switch_to_guide_interface(self):
        self.switchTo(self.guide_interface)

    def switch_to_upload_interface(self):
        self.switchTo(self.upload_interface)

    def switch_to_realtime_interface(self):
        self.switchTo(self.realtime_interface)

    def switch_to_setting_interface(self):
        self.switchTo(self.setting_interface)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

