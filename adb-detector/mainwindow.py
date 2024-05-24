import random

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QStatusBar, QLabel, QPushButton

from real_time_detector import RealTime_Detector
from upload_detector import Upload_Detector
from guide_demonstrator import Guide_Demonstrator


class Ui_MainWindow():
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1120, 800)
        MainWindow.setMinimumSize(1120, 800)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # 标题
        self.title_label = QtWidgets.QLabel(self.centralwidget)
        self.title_label.setGeometry(QtCore.QRect(175, 10, 800, 60))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title_label.sizePolicy().hasHeightForWidth())
        self.title_label.setSizePolicy(sizePolicy)
        self.title_label.setFont(QtGui.QFont('', 21))
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setWordWrap(True)
        self.title_label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextSelectableByMouse)
        self.title_label.setObjectName("title_label")

        # 按钮框
        self.choose_frame = QtWidgets.QFrame(self.centralwidget)
        self.choose_frame.setGeometry(QtCore.QRect(20, 85, 200, 200))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.choose_frame.sizePolicy().hasHeightForWidth())
        self.choose_frame.setSizePolicy(sizePolicy)
        self.choose_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.choose_frame.setObjectName("choose_frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.choose_frame)
        self.verticalLayout.setObjectName("verticalLayout")

        # 显示操作指南页面按钮
        self.guide_page_button = QtWidgets.QPushButton(self.choose_frame)
        self.guide_page_button.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.guide_page_button.sizePolicy().hasHeightForWidth())
        self.guide_page_button.setSizePolicy(sizePolicy)
        self.guide_page_button.setFont(QtGui.QFont('', 14))
        self.guide_page_button.setObjectName("guide_page_button")
        self.guide_page_button.clicked.connect(self.show_main_page)
        self.verticalLayout.addWidget(self.guide_page_button)

        # 显示图片、视频检测页面按钮
        self.upload_page_button = QtWidgets.QPushButton(self.choose_frame)
        self.upload_page_button.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.upload_page_button.sizePolicy().hasHeightForWidth())
        self.upload_page_button.setSizePolicy(sizePolicy)
        self.upload_page_button.setFont(QtGui.QFont('', 14))
        self.upload_page_button.setObjectName("upload_page_button")
        self.upload_page_button.clicked.connect(self.show_upload_detect_page)
        self.verticalLayout.addWidget(self.upload_page_button)

        # 显示实时检测页面按钮
        self.realtime_page_button = QtWidgets.QPushButton(self.choose_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.realtime_page_button.sizePolicy().hasHeightForWidth())
        self.realtime_page_button.setSizePolicy(sizePolicy)
        self.realtime_page_button.setFont(QtGui.QFont('', 14))
        self.realtime_page_button.setObjectName("realtime_page_button")
        self.realtime_page_button.clicked.connect(self.show_real_time_detect_page)
        self.verticalLayout.addWidget(self.realtime_page_button)

        # tips页面
        self.tips_label = QLabel(self.centralwidget)
        self.tips_label.setGeometry(QtCore.QRect(20, 315, 130, 30))
        self.tips_label.setFont(QtGui.QFont('SimHei', 16))

        self.fresh_button = QPushButton(self.centralwidget)
        self.fresh_button.clicked.connect(self.fresh_tips)
        self.fresh_button.setGeometry(190, 315, 30, 30)
        self.fresh_button.setFont(QtGui.QFont('Webdings'))
        self.fresh_button.setText('q')
        self.tips = [
                "避免使用手机，专心驾驶安全。",
                "不要疲劳驾驶，保持精神清醒。",
                "禁止酒后驾车，确保自身安全。",
                "集中注意力，勿分心驾驶操作。",
                "保持适当车距，防止追尾事故。",
                "不要吃喝驾驶，双手握住方向。",
                "调整好座椅和后视镜视野。",
                "系好安全带，防止意外伤害。",
                "遵守交通信号，勿闯红灯危险。",
                "避免激烈驾驶，安全第一要务。",
                "不超速行驶，遵守道路限速。",
                "不频繁变道，保持车道稳定。",
                "避免长时间闭眼，防止意外发生。",
                "保持冷静驾驶，避免路怒行为。",
                "不在车内抽烟，注意行车安全。",
                "使用免提设备，避免分心驾驶。",
                "避免分心娱乐，专注驾驶任务。",
                "定期检查车况，确保行车安全。",
                "保持清醒状态，避免困倦驾驶。",
                "及时休息调整，防止疲劳驾驶。"
            ]
        self.tips_text_label = QLabel(self.centralwidget)
        self.tips_text_label.setGeometry(QtCore.QRect(20, 350, 200, 410))
        self.tips_text_label.setFrameShape(QtWidgets.QFrame.Box)
        self.tips_text_label.setWordWrap(True)
        self.tips_text_label.setFont(QtGui.QFont('SimHei', 11))

        # 页面切换栈
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(240, 85, 850, 675))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setFrameShape(QtWidgets.QFrame.Box)
        self.stackedWidget.setObjectName("stackedWidget")

        # 操作指南页面
        self.page_0 = QtWidgets.QWidget()
        self.page_0.setObjectName("page_0")
        self.__guide_demonstrator = Guide_Demonstrator()
        self.__guide_demonstrator.setFixedSize(835, 775)
        page_0_layout = QtWidgets.QVBoxLayout(self.page_0)
        page_0_layout.addWidget(self.__guide_demonstrator)
        self.stackedWidget.addWidget(self.page_0)

        # 图片/视频检测页面
        self.page_1 = QtWidgets.QWidget()
        self.page_1.setObjectName("page_1")
        self.__upload_detector = Upload_Detector()
        self.__upload_detector.setFixedSize(835, 775)
        self.__upload_detector.exporting_signal.connect(self.exporting_status_bar)
        self.__upload_detector.exported_signal.connect(self.exported_status_bar)
        page_1_layout = QtWidgets.QVBoxLayout(self.page_1)
        page_1_layout.addWidget(self.__upload_detector)
        self.stackedWidget.addWidget(self.page_1)

        # 实时检测页面
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.__real_time_detector = RealTime_Detector()
        self.__real_time_detector.setFixedSize(835, 775)
        page_2_layout = QtWidgets.QVBoxLayout(self.page_2)
        page_2_layout.addWidget(self.__real_time_detector)
        self.stackedWidget.addWidget(self.page_2)

        # 状态栏
        self.status_bar = QStatusBar(MainWindow)
        self.status_bar.setStyleSheet('QStatusBar{color:cyan; alignment:center;}')
        MainWindow.setStatusBar(self.status_bar)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def show_main_page(self):
        self.stackedWidget.setCurrentIndex(0)

    def show_upload_detect_page(self):
        self.stackedWidget.setCurrentIndex(1)

    def show_real_time_detect_page(self):
        self.stackedWidget.setCurrentIndex(2)

    def exporting_status_bar(self):
        self.status_bar.showMessage('正在导出...')

    def exported_status_bar(self):
        self.status_bar.showMessage('导出完成', 3000)

    def fresh_tips(self):
        selected_tips = random.sample(self.tips, 5)
        tips_with_numbers = [f"{i + 1}、{tip}" for i, tip in enumerate(selected_tips)]
        tips_text = '\n\n\n'.join(tips_with_numbers)
        self.tips_text_label.setText(tips_text)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "驾驶员异常驾驶行为识别系统"))
        self.guide_page_button.setText(_translate("MainWindow", "操作指南"))
        self.upload_page_button.setText(_translate("MainWindow", "图片/视频检测"))
        self.realtime_page_button.setText(_translate("MainWindow", "实时检测"))
        self.title_label.setText(_translate("MainWindow", "驾驶员异常驾驶行为识别系统"))
        self.tips_label.setText(_translate("MainWindow", "温馨提示"))
        self.fresh_tips()
