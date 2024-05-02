import queue

import cv2
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QImage, QPixmap
from PyQt5.QtWidgets import QLabel, QPushButton, QAction, QMainWindow, QFrame, QVBoxLayout, QWidget, QMenu
from ultralytics import YOLO


class DetectorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('驾驶员异常驾驶行为识别平台')
        self.setGeometry(800, 250, 835, 575)
        self.setFixedSize(835, 575)

        # 摄像头检测区域
        self.timer = QTimer(self)  # 更新图片的计时器

        self.detect_area_label = QLabel('摄像头检测区域', self)
        self.detect_area_label.setGeometry(10, 30, 150, 20)
        self.set_obj_font(self.detect_area_label)

        self.img_frame = QFrame(self)
        self.img_frame.setFrameShape(QFrame.Box)
        self.img_frame.setGeometry(5, 60, 600, 500)
        # self.img_frame.setStyleSheet('background-color: white')

        self.image_label = QLabel(self.img_frame)
        self.image_label.setGeometry(5, 5, 590, 490)
        self.cap = cv2.VideoCapture(0)
        self.cap.release()

        self.fps_label = QLabel(self.image_label)
        self.fps_label.setGeometry(7, 7, 90, 20)
        self.fps_label.setStyleSheet('color: rgb(0, 255, 255); background-color: transparent')
        self.set_obj_font(self.fps_label)

        # 模型
        self.model = YOLO(r'E:\PythonCode\abnormal-driving-behavior\ultralytics-main\runs\detect\yolov8s_300\weights\best.pt')
        # self.model = YOLO(r'E:\PythonCode\abnormal-driving-behavior\ultralytics-main\runs\detect\train\weights\best.pt')

        # 得分
        self.classes = ['eye_open', 'eye_close', 'mouth', 'yawn', 'face', 'smoke', 'phone', 'drink']
        self.adb = {'eye_close': 0, 'yawn': 0, 'smoke': 0, 'phone': 0, 'drink': 0}  # 是否有异常动作
        self.SCORE = 100
        self.adb_score = {'eye_close': 40, 'yawn': 5, 'smoke': 10, 'phone': 30, 'drink': 15}

        self.adb_frame_cnt = {'eye_close': 0, 'yawn': 0, 'smoke': 0, 'phone': 0, 'drink': 0}  # 单位时间内异常动作帧数统计
        self.frame_threshold = 0.3  # 被判定为异常行为的帧数所占正常帧数的比例阈值
        self.queue = queue.Queue()  # 帧队列，存有单位时间（1s）内每一帧的异常行为

        # 异常驾驶行为统计次数
        self.cnt_label = QLabel('异常驾驶行为统计与分析', self)
        self.cnt_label.setGeometry(625, 190, 200, 20)
        self.set_obj_font(self.cnt_label)

        self.analyse_label = QLabel(self)
        self.set_obj_font(self.analyse_label)
        self.analyse_label.setWordWrap(True)
        self.analyse_label.setTextInteractionFlags(self.analyse_label.textInteractionFlags() | Qt.TextSelectableByMouse)

        self.cnt_frame = QFrame(self)
        self.cnt_frame.setFrameShape(QFrame.Box)
        self.cnt_frame.setGeometry(625, 215, 200, 250)

        cnt_frame_layout = QVBoxLayout()
        cnt_frame_layout.addWidget(self.analyse_label)
        self.cnt_frame.setLayout(cnt_frame_layout)

        # 结果
        self.res_label = QLabel('实时检测结果分析', self)
        self.res_label.setGeometry(625, 30, 150, 20)
        self.set_obj_font(self.res_label)

        self.res_frame = QFrame(self)
        self.res_frame.setFrameShape(QFrame.Box)
        self.res_frame.setGeometry(625, 60, 200, 125)

        self.res_content_label = QLabel(self.res_frame)
        self.res_content_label.setGeometry(10, 10, 180, 105)
        self.res_content_label.setWordWrap(True)
        self.set_obj_font(self.res_content_label)
        self.res_content_label.setTextInteractionFlags(self.res_content_label.textInteractionFlags() | Qt.TextSelectableByMouse)

        # 更新'异常驾驶行为统计与分析'与'实时检测结果分析'模块
        self.init_adb()
        self.set_text()

        # 按钮
        self.start_detect_button = QPushButton('开始检测', self)
        self.start_detect_button.clicked.connect(self.start_detect)
        self.start_detect_button.setFixedSize(100, 30)
        self.set_obj_font(self.start_detect_button)

        self.end_detect_button = QPushButton('结束', self)
        self.end_detect_button.clicked.connect(self.end_detect)
        self.end_detect_button.setFixedSize(100, 30)
        self.set_obj_font(self.end_detect_button)

        self.button_frame = QFrame(self)
        self.button_frame.setGeometry(625, 470, 200, 90)
        self.button_frame.setFrameShape(QFrame.Box)
        button_frame_layout = QVBoxLayout()
        button_frame_layout.addWidget(self.start_detect_button)
        button_frame_layout.addWidget(self.end_detect_button)
        button_frame_layout.setAlignment(Qt.AlignCenter)
        self.button_frame.setLayout(button_frame_layout)

        # 菜单栏
        menu_bar = self.menuBar()

        back_action = QAction('返回', self)
        back_action.triggered.connect(self.back_to_menu)

        set_menu = QMenu('设置', self)
        self.show_bbox = True
        show_bbox_action = QAction('显示边界框', self)
        show_bbox_action.setCheckable(True)
        show_bbox_action.setChecked(True)
        show_bbox_action.triggered.connect(self.switch_show_bbox)
        set_menu.addAction(show_bbox_action)

        menu_bar.addAction(back_action)
        menu_bar.addMenu(set_menu)

    def start_detect(self):
        if self.start_detect_button.text() == '开始检测':
            if not self.cap.isOpened():
                self.cap = cv2.VideoCapture(0)
            # 定时更新图片帧
            self.init_adb()
            self.set_text()

            self.timer.timeout.connect(self.update_frame)
            self.timer.start(5)
            self.start_detect_button.setText('正在检测中')

    def update_frame(self):
        loop_start = cv2.getTickCount()
        success, frame = self.cap.read()  # 读取摄像头帧
        if success:
            frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
            detect_res = self.model.predict(source=frame)  # 镜像图片送入检测
            annotated_frame = detect_res[0].plot()

            loop_cycle = cv2.getTickCount() - loop_start
            total_time = loop_cycle / cv2.getTickFrequency()
            FPS = int(1.0 / total_time)
            self.fps_label.setText(f"FPS: {FPS:.1f}")

            # 使用检测结果更新'异常驾驶行为统计与分析'与'实时检测结果分析'模块
            self.update_adb(classes=detect_res[0].boxes.cls, FPS=max(24, FPS))

            h, w, ch = annotated_frame.shape
            bytes_per_line = ch * w
            if self.show_bbox is True:
                qt_image = QImage(annotated_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            else:
                qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)

    def update_adb(self, classes=None, FPS=24):
        cur_frame_adb = []
        if classes is not None:
            for each_idx in classes:     # 根据classes中下标获取对应adb
                idx = int(each_idx.item())
                if self.classes[idx] in self.adb:
                    cur_frame_adb.append(self.classes[idx])

        self.queue.put(cur_frame_adb)

        for adb in cur_frame_adb:
            self.adb_frame_cnt[adb] += 1
        while self.queue.qsize() > FPS * 2:  # 动态维护一个长度为FPS * 5的队列，存放一段时间内帧的检测结果
            head_frame_cnt = self.queue.get()
            for adb in head_frame_cnt:
                self.adb_frame_cnt[adb] -= 1

        for adb, frame in self.adb_frame_cnt.items():
            if frame / self.queue.qsize() >= self.frame_threshold:  # 如果异常帧所占一段时间内帧的比例超过了threshold
                if self.adb[adb] == 0:
                    self.SCORE -= self.adb_score[adb]
                self.adb[adb] = 1
            else:
                if self.adb[adb] == 1:
                    self.SCORE += self.adb_score[adb]
                self.adb[adb] = 0

        self.set_text()

    def init_adb(self):
        self.image_label.clear()

        self.frame_cnt = 0
        self.calculated_times = 0
        self.fps_label.clear()

        self.queue.queue.clear()
        self.adb = {'eye_close': 0, 'yawn': 0, 'smoke': 0, 'phone': 0, 'drink': 0}
        self.adb_frame_cnt = {'eye_close': 0, 'yawn': 0, 'smoke': 0, 'phone': 0, 'drink': 0}
        self.SCORE = 100

    def set_text(self):
        self.analyse_label.setText(f'闭眼: {self.adb["eye_close"]}\n\n'
                                   f'打哈欠: {self.adb["yawn"]}\n\n'
                                   f'抽烟: {self.adb["smoke"]}\n\n'
                                   f'使用手机: {self.adb["phone"]}\n\n'
                                   f'喝水: {self.adb["drink"]}\n\n'
                                   f'驾驶行为评分: {self.SCORE}\n\n'
                                   f'危险驾驶分级: {self.get_level(self.SCORE)}\n\n')

        if self.cap.isOpened():
            self.res_content_label.setText('检测中...\n'
                                           '- - - - - - - - -\n'
                                           f'当前驾驶状态: {self.get_level(self.SCORE)}\n'
                                           '- - - - - - - - -\n'
                                           f'异常驾驶行为: {self.get_adb_str(self.adb)}')
        else:
            self.res_content_label.setText('点击\"开始检测\"按钮启动')

    def get_adb_str(self, adb):
        adb_classes = []
        adb_mapping = {'eye_close': '闭眼', 'yawn': '打哈欠', 'smoke': '抽烟', 'phone': '使用手机', 'drink': '喝水'}
        for adb_cls, value in adb.items():
            if value:
               adb_classes.append(adb_mapping[adb_cls])
        adb_str = ', '.join(adb_classes) if len(adb_classes) else '无'
        return adb_str

    def get_level(self, SCORE):
        if SCORE == 100:
            level = '安全'
        elif SCORE > 90:
            level = '较为安全'
        elif SCORE > 75:
            level = '轻度危险'
        elif SCORE > 60:
            level = '中度危险'
        else:
            level = '非常危险'
        return level

    def end_detect(self):
        if self.start_detect_button.text() == '正在检测中':
            self.timer.stop()
            if self.cap.isOpened():
                self.cap.release()
            self.init_adb()
            self.set_text()
            self.start_detect_button.setText('开始检测')

    def set_obj_font(self, obj):
        obj.setFont(QFont("SimHei", 11))

    def back_to_menu(self):
        from menu_ui import MenuWindow
        self.menu_window = MenuWindow()
        self.close()
        self.menu_window.show()
        self.cap.release()

    def switch_show_bbox(self):
        self.show_bbox = not self.show_bbox
        action = self.sender()
        if action.isChecked():
            action.setIconVisibleInMenu(True)
        else:
            action.setIconVisibleInMenu(False)


