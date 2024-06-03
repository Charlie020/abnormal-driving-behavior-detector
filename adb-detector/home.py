from PyQt5.QtCore import pyqtSignal, Qt, QUrl
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from qfluentwidgets import ImageLabel, TitleLabel, ScrollArea, SubtitleLabel, FluentIcon, CardWidget, \
    IconWidget, TextWrap, StrongBodyLabel, BodyLabel, HyperlinkLabel


class SampleCard(CardWidget):

    switch_signal = pyqtSignal()

    def __init__(self, icon, title, content, parent=None):
        super().__init__(parent=parent)

        self.iconWidget = IconWidget(icon, self)
        self.titleLabel = StrongBodyLabel(title, self)
        self.titleLabel.setFont(QFont('SimHei', 12))
        self.contentLabel = QLabel(TextWrap.wrap(content, 45, False)[0], self)
        self.contentLabel.setFont(QFont('SimHei', 10))
        self.contentLabel.setStyleSheet("color: grey;")

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedSize(360, 90)
        self.iconWidget.setFixedSize(48, 48)

        self.hBoxLayout.setSpacing(28)
        self.hBoxLayout.setContentsMargins(20, 0, 0, 0)
        self.vBoxLayout.setSpacing(2)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)

        self.hBoxLayout.setAlignment(Qt.AlignVCenter)
        self.hBoxLayout.addWidget(self.iconWidget)
        self.hBoxLayout.addLayout(self.vBoxLayout)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addWidget(self.contentLabel)
        self.vBoxLayout.addStretch(1)

        self.titleLabel.setObjectName('titleLabel')
        self.contentLabel.setObjectName('contentLabel')

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.switch_signal.emit()


class Home(QWidget):
    switch_to_guide_signal = pyqtSignal()
    switch_to_upload_signal = pyqtSignal()
    switch_to_realtime_signal = pyqtSignal()
    switch_to_setting_signal = pyqtSignal()

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text.replace(' ', '-'))

        central_widget = QWidget()
        central_layout = QVBoxLayout(central_widget)

        # 横幅
        self.img_label = ImageLabel('resource/img/banner.png', self)
        self.img_label.setFixedSize(880, 385)
        self.img_label.setBorderRadius(8, 8, 8, 8)
        central_layout.addWidget(self.img_label)

        # 主标题
        central_layout.addSpacing(25)
        self.title_label = TitleLabel('驾驶员异常驾驶行为识别系统', self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont('SimHei', 20))
        self.title_label.setFixedSize(880, 30)
        central_layout.addWidget(self.title_label)

        url_card = QWidget()
        url_layout = QHBoxLayout(url_card)
        url_layout.setAlignment(Qt.AlignCenter)
        self.model_url = HyperlinkLabel(QUrl('https://github.com/ultralytics/ultralytics'), 'YOLOv8')
        self.model_url.setFont(QFont('SimHei', 12))
        url_layout.addWidget(self.model_url)
        url_layout.addSpacing(50)
        self.ui_url = HyperlinkLabel(QUrl('https://github.com/zhiyiYo/PyQt-Fluent-Widgets'), 'PyQt-Fluent-Widgets')
        self.ui_url.setFont(QFont('SimHei', 12))
        url_layout.addWidget(self.ui_url)
        url_layout.addSpacing(50)
        self.my_github_url = HyperlinkLabel(QUrl('https://github.com/Charlie020/abnormal-driving-behavior-detector'), 'GitHub')
        self.my_github_url.setFont(QFont('SimHei', 12))
        url_layout.addWidget(self.my_github_url)
        central_layout.addWidget(url_card)

        # “系统介绍”模块
        central_layout.addSpacing(20)
        self.intro_title = SubtitleLabel('  系统介绍', self)
        self.intro_title.setFont(QFont('SimHei', 16))
        self.intro_title.setFixedSize(400, 30)
        central_layout.addWidget(self.intro_title)

        self.intro_text = BodyLabel(self)
        self.intro_text.setFont(QFont('SimHei', 12))
        self.intro_text.setWordWrap(True)
        self.intro_text.setContentsMargins(20, 0, 20, 0)
        self.intro_text.setText('    本系统界面基于PyQt5和PyQt-Fluent-Widgets框架搭建，'
                                '系统检测模型采用了YOLOv8在自建数据集上训练的模型，'
                                '本系统代码已开源至GitHub。')
        central_layout.addWidget(self.intro_text)

        # “快速开始”模块
        central_layout.addSpacing(20)
        self.get_start_title = SubtitleLabel('  快速开始', self)
        self.get_start_title.setFont(QFont('SimHei', 16))
        self.get_start_title.setFixedSize(400, 30)
        central_layout.addWidget(self.get_start_title)

        card_1 = QWidget()
        card_1_layout = QHBoxLayout(card_1)
        self.guide_interface_card = SampleCard(FluentIcon.BOOK_SHELF, '操作指南', '快速了解系统功能及使用方式', self)
        self.guide_interface_card.switch_signal.connect(self.switch_to_guide_interface)
        card_1_layout.addWidget(self.guide_interface_card)
        self.upload_interface_card = SampleCard(FluentIcon.PHOTO, '图片/视频检测', '上传图片或视频进行检测', self)
        self.upload_interface_card.setFixedSize(365, 95)
        self.upload_interface_card.switch_signal.connect(self.switch_to_upload_interface)
        card_1_layout.addWidget(self.upload_interface_card)
        central_layout.addWidget(card_1)

        card_2 = QWidget()
        card_2_layout = QHBoxLayout(card_2)
        self.realtime_interface_card = SampleCard(FluentIcon.CAMERA, '实时检测', '调用摄像头进行实时检测', self)
        self.realtime_interface_card.setFixedSize(365, 95)
        self.realtime_interface_card.switch_signal.connect(self.switch_to_realtime_interface)
        card_2_layout.addWidget(self.realtime_interface_card)
        self.setting_interface_card = SampleCard(FluentIcon.SETTING, '设置', '配置系统文件夹路径', self)
        self.setting_interface_card.setFixedSize(365, 95)
        self.setting_interface_card.switch_signal.connect(self.switch_to_setting_interface)
        card_2_layout.addWidget(self.setting_interface_card)
        central_layout.addWidget(card_2)

        # 整体页面设计
        self.scroll_area = ScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none;")
        self.scroll_area.setWidget(central_widget)
        vBoxLayout = QVBoxLayout(self)
        vBoxLayout.setContentsMargins(0, 0, 0, 0)
        vBoxLayout.addWidget(self.scroll_area)

    def switch_to_guide_interface(self):
        self.switch_to_guide_signal.emit()

    def switch_to_upload_interface(self):
        self.switch_to_upload_signal.emit()

    def switch_to_realtime_interface(self):
        self.switch_to_realtime_signal.emit()

    def switch_to_setting_interface(self):
        self.switch_to_setting_signal.emit()