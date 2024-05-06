from PyQt5 import QtCore, QtGui, QtWidgets
from real_time_detector import RealTime_Detector
from upload_detector import Upload_Detector


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1100, 750)
        MainWindow.setMinimumSize(1100, 750)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setStyleSheet("#MainWindow{border-image:url(resource/background/mikasa.png);}")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.choose_frame = QtWidgets.QFrame(self.centralwidget)
        self.choose_frame.setGeometry(QtCore.QRect(20, 80, 200, 200))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.choose_frame.sizePolicy().hasHeightForWidth())
        self.choose_frame.setSizePolicy(sizePolicy)
        self.choose_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.choose_frame.setObjectName("choose_frame")

        # 功能选择按钮
        self.verticalLayout = QtWidgets.QVBoxLayout(self.choose_frame)
        self.verticalLayout.setObjectName("verticalLayout")

        self.main_frame_button = QtWidgets.QPushButton(self.choose_frame)
        self.main_frame_button.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_frame_button.sizePolicy().hasHeightForWidth())
        self.main_frame_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.main_frame_button.setStyleSheet("background-color: transparent; border: 1px solid black;")
        self.main_frame_button.setFont(font)
        self.main_frame_button.setObjectName("main_frame_button")
        self.main_frame_button.clicked.connect(self.show_main_page)
        self.verticalLayout.addWidget(self.main_frame_button)

        self.detect_button = QtWidgets.QPushButton(self.choose_frame)
        self.detect_button.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.detect_button.sizePolicy().hasHeightForWidth())
        self.detect_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.detect_button.setStyleSheet("background-color: transparent; border: 1px solid black;")
        self.detect_button.setFont(font)
        self.detect_button.setObjectName("detect_button")
        self.detect_button.clicked.connect(self.show_upload_detect_page)
        self.verticalLayout.addWidget(self.detect_button)

        self.real_time_detect_button = QtWidgets.QPushButton(self.choose_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.real_time_detect_button.sizePolicy().hasHeightForWidth())
        self.real_time_detect_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(17)
        self.real_time_detect_button.setStyleSheet("background-color: transparent; border: 1px solid black;")
        self.real_time_detect_button.setFont(font)
        self.real_time_detect_button.setObjectName("real_time_detect_button")
        self.real_time_detect_button.clicked.connect(self.show_real_time_detect_page)
        self.verticalLayout.addWidget(self.real_time_detect_button)

        # 标题
        self.title_label = QtWidgets.QLabel(self.centralwidget)
        self.title_label.setGeometry(QtCore.QRect(175, 10, 800, 60))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title_label.sizePolicy().hasHeightForWidth())
        self.title_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(21)
        self.title_label.setFont(font)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setWordWrap(True)
        self.title_label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.title_label.setObjectName("title_label")

        # 页面切换栈
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(240, 60, 850, 675))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setFrameShape(QtWidgets.QFrame.Box)
        self.stackedWidget.setObjectName("stackedWidget")

        # 初始页
        self.page_0 = QtWidgets.QWidget()
        self.page_0.setObjectName("page_0")
        self.example_label = QtWidgets.QLabel(self.page_0)
        self.example_label.setGeometry(QtCore.QRect(10, 10, 830, 655))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.example_label.sizePolicy().hasHeightForWidth())
        self.example_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(29)
        self.example_label.setFont(font)
        self.example_label.setAlignment(QtCore.Qt.AlignCenter)
        self.example_label.setObjectName("example_label")
        self.stackedWidget.addWidget(self.page_0)

        # 图片/视频检测页面
        self.page_1 = QtWidgets.QWidget()
        self.page_1.setObjectName("page_1")
        self.upload_detector = Upload_Detector()
        self.upload_detector.setFixedSize(835, 775)
        page_1_layout = QtWidgets.QVBoxLayout(self.page_1)
        page_1_layout.addWidget(self.upload_detector)
        self.stackedWidget.addWidget(self.page_1)

        # 实时检测页面
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.real_time_detector = RealTime_Detector()
        self.real_time_detector.setFixedSize(835, 775)
        page_2_layout = QtWidgets.QVBoxLayout(self.page_2)
        page_2_layout.addWidget(self.real_time_detector)
        self.stackedWidget.addWidget(self.page_2)

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

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "驾驶员异常驾驶行为识别系统"))
        self.main_frame_button.setText(_translate("MainWindow", "主页面"))
        self.detect_button.setText(_translate("MainWindow", "图片/视频检测"))
        self.real_time_detect_button.setText(_translate("MainWindow", "实时检测"))
        self.title_label.setText(_translate("MainWindow", "驾驶员异常驾驶行为识别系统"))
        self.example_label.setText(_translate("MainWindow", "功能区"))
