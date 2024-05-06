import os
import threading
import cv2
import queue
import pickle

from PyQt5.QtCore import QTimer, Qt, QDateTime
from PyQt5.QtGui import QFont, QImage, QPixmap
from PyQt5.QtWidgets import QLabel, QPushButton, QFrame, QVBoxLayout, QWidget, QScrollArea, QTextEdit
import pyqtgraph as pg  # pyqtgraph必须在PyQt5后面import
from playsound import playsound

from ultralytics import YOLO


class RealTime_Detector(QWidget):
    def __init__(self):
        super().__init__()
        # 初始化默认文件夹
        self.logs_folder = ''
        self.resource_folder = ''
        self.result_folder = ''
        self.init_sys()

        # 摄像头检测区域
        self.update_frame_timer = QTimer(self)  # 更新图片的计时器
        self.update_log_timer = QTimer(self)   # 更新日志的计时器
        self.update_plot_timer = QTimer(self)  # 更新曲线的计时器

        self.detect_area_label = QLabel('摄像头检测结果显示区域', self)
        self.detect_area_label.setGeometry(5, 0, 200, 20)
        self.set_obj_font(self.detect_area_label)

        self.img_frame = QFrame(self)
        self.img_frame.setFrameShape(QFrame.Box)
        self.img_frame.setGeometry(5, 30, 600, 500)

        self.image_label = QLabel(self.img_frame)
        self.image_label.setGeometry(5, 5, 590, 490)
        self.cap = cv2.VideoCapture(0)
        self.cap.release()

        self.fps_label = QLabel(self.image_label)
        self.fps_label.setGeometry(5, 5, 80, 20)
        self.fps_label.setStyleSheet('color: rgb(0, 255, 255); background-color: transparent')
        self.set_obj_font(self.fps_label)

        # 模型
        from main import get_yolo_weight
        self.model = YOLO(get_yolo_weight())

        # 得分
        self.classes = ['eye_open', 'eye_close', 'mouth', 'yawn', 'face', 'smoke', 'phone', 'drink']
        self.adb = {'eye_close': 0, 'yawn': 0, 'smoke': 0, 'phone': 0, 'drink': 0}  # 是否有异常动作
        self.score = 100
        self.adb_score = {'eye_close': 40, 'yawn': 5, 'smoke': 10, 'phone': 30, 'drink': 15}

        self.adb_frame_cnt = {'eye_close': 0, 'yawn': 0, 'smoke': 0, 'phone': 0, 'drink': 0}  # 单位时间内异常动作帧数统计
        self.frame_threshold = 0.3  # 被判定为异常行为的帧数所占正常帧数的比例阈值
        self.queue = queue.Queue()  # 帧队列，存有单位时间（1s）内每一帧的异常行为

        # 实时检测结果分析
        self.res_label = QLabel('实时检测结果分析', self)
        self.res_label.setGeometry(625, 0, 150, 20)
        self.set_obj_font(self.res_label)

        self.res_frame = QFrame(self)
        self.res_frame.setFrameShape(QFrame.Box)
        self.res_frame.setGeometry(625, 30, 200, 125)

        self.res_content_label = QLabel(self.res_frame)
        self.res_content_label.setGeometry(10, 10, 180, 105)
        self.res_content_label.setWordWrap(True)
        self.set_obj_font(self.res_content_label)
        self.res_content_label.setTextInteractionFlags(self.res_content_label.textInteractionFlags() | Qt.TextSelectableByMouse)

        # 异常驾驶行为统计次数
        self.cnt_label = QLabel('异常驾驶行为统计与分析', self)
        self.cnt_label.setGeometry(625, 160, 200, 20)
        self.set_obj_font(self.cnt_label)

        self.analyse_label = QLabel(self)
        self.set_obj_font(self.analyse_label)
        self.analyse_label.setWordWrap(True)
        self.analyse_label.setTextInteractionFlags(self.analyse_label.textInteractionFlags() | Qt.TextSelectableByMouse)

        self.cnt_frame = QFrame(self)
        self.cnt_frame.setFrameShape(QFrame.Box)
        self.cnt_frame.setGeometry(625, 185, 200, 250)

        cnt_frame_layout = QVBoxLayout()
        cnt_frame_layout.addWidget(self.analyse_label)
        self.cnt_frame.setLayout(cnt_frame_layout)

        # 按钮
        self.start_detect_button = QPushButton('开始检测', self)
        self.start_detect_button.clicked.connect(self.start_detect)
        self.start_detect_button.setFixedSize(100, 30)
        self.start_detect_button.setStyleSheet("background-color: transparent; border: 1px solid black;")
        self.set_obj_font(self.start_detect_button)

        self.end_detect_button = QPushButton('结束', self)
        self.end_detect_button.clicked.connect(self.end_detect)
        self.end_detect_button.setFixedSize(100, 30)
        self.end_detect_button.setStyleSheet("background-color: transparent; border: 1px solid black;")
        self.set_obj_font(self.end_detect_button)

        self.button_frame = QFrame(self)
        self.button_frame.setGeometry(625, 440, 200, 90)
        self.button_frame.setFrameShape(QFrame.Box)
        button_frame_layout = QVBoxLayout()
        button_frame_layout.addWidget(self.start_detect_button)
        button_frame_layout.addWidget(self.end_detect_button)
        button_frame_layout.setAlignment(Qt.AlignCenter)
        self.button_frame.setLayout(button_frame_layout)

        # 功能按钮
        self.show_bbox = True
        self.show_bbox_button = QPushButton(self)
        self.show_bbox_button.setFont(QFont('Webdings'))
        self.show_bbox_button.setText('r')
        self.show_bbox_button.clicked.connect(self.switch_show_bbox)
        self.show_bbox_button.setGeometry(550, 0, 25, 25)
        self.show_bbox_button.setToolTip('隐藏边界框')

        self.export_log_button = QPushButton(self)
        self.export_log_button.setFont(QFont('Webdings'))
        self.export_log_button.setText('6')
        self.export_log_button.clicked.connect(self.export_log)
        self.export_log_button.setGeometry(580, 0, 25, 25)
        self.export_log_button.setToolTip('导出日志')

        # 将日志信息放置在滚动区域中
        self.log_text = QTextEdit()
        self.log_text.setPlainText('日志：')
        self.log_text.setFont(QFont('KaiTi', 8))
        self.log_text.setReadOnly(True)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setGeometry(5, 540, 300, 110)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.log_text)
        self.scroll_area.setStyleSheet("background-color: transparent;")

        # 实时曲线
        pg.setConfigOption('background', '#FFFFFF')
        pg.setConfigOption('foreground', 'k')
        self.plot_widget = pg.PlotWidget(self)
        self.plot_widget.setGeometry(315, 540, 510, 110)
        self.plot_widget.setLabel('left', 'Score')
        self.plot_widget.setLabel('bottom', 'Time (s)')
        self.TIME = [0]
        self.SCORE = [self.score]

        # 更新'异常驾驶行为统计与分析'与'实时检测结果分析'模块
        self.isAlarm = False
        self.init_adb()
        self.set_text()

    def start_detect(self):
        if self.start_detect_button.text() == '开始检测':
            if not self.cap.isOpened():
                self.cap = cv2.VideoCapture(0)
            # 定时更新图片帧
            self.init_adb()
            self.set_text()

            self.update_frame_timer.timeout.connect(self.update_frame)
            self.update_frame_timer.start(5)

            self.log_text.setPlainText('日志：')
            self.update_log_timer.timeout.connect(self.update_log)
            self.update_log_timer.start(1000)

            self.update_plot_timer.timeout.connect(self.update_plot)
            self.update_plot_timer.start(1000)
            self.plot_widget.clear()
            self.TIME = [0]
            self.SCORE = [self.score]
            self.plot_widget.plot(self.TIME, self.SCORE, pen='b', symbol='o', symbolPen='b', symbolBrush='r')

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
            self.fps_label.setText(f"FPS: {int(FPS)}")

            # 使用检测结果更新'异常驾驶行为统计与分析'与'实时检测结果分析'模块
            self.update_adb(classes=detect_res[0].boxes.cls, FPS=max(24, FPS))

            h, w, ch = annotated_frame.shape
            bytes_per_line = ch * w
            if self.show_bbox is True:
                pixmap = QPixmap.fromImage(QImage(annotated_frame.data, w, h, bytes_per_line, QImage.Format_RGB888))
            else:
                pixmap = QPixmap.fromImage(QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888))
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
                    self.score -= self.adb_score[adb]
                self.adb[adb] = 1
            else:
                if self.adb[adb] == 1:
                    self.score += self.adb_score[adb]
                self.adb[adb] = 0

        if self.score <= 80 and self.isAlarm == False:
            self.isAlarm = True
            alarm_thread = threading.Thread(target=self.alarm)
            alarm_thread.daemon = True
            alarm_thread.start()

        self.set_text()

    def alarm(self):
        for _ in range(5):
            playsound(f'{self.resource_folder}/audio/alarm_80.mp3')
        self.isAlarm = False

    def set_text(self):
        self.analyse_label.setText(f'闭眼: {self.adb["eye_close"]}\n\n'
                                   f'打哈欠: {self.adb["yawn"]}\n\n'
                                   f'抽烟: {self.adb["smoke"]}\n\n'
                                   f'使用手机: {self.adb["phone"]}\n\n'
                                   f'喝水: {self.adb["drink"]}\n\n'
                                   f'驾驶行为评分: {self.score}\n\n'
                                   f'危险驾驶分级: {self.get_level()}\n\n')

        if self.cap.isOpened():
            self.res_content_label.setText('检测中...\n'
                                           '- - - - - - - - -\n'
                                           f'当前驾驶状态: {self.get_level()}\n'
                                           '- - - - - - - - -\n'
                                           f'异常驾驶行为: {self.get_adb_str(self.adb)}')
        else:
            self.res_content_label.setText('点击\"开始检测\"按钮启动')

    def update_log(self):
        self.log_text.append(f'{QDateTime.currentDateTime().toString("yyyy年MM月dd日 hh:mm:ss")}: {self.get_adb_str(self.adb)}')

    def export_log(self):
        with open(os.path.join(self.logs_folder, 'real-time_detection_curve.pkl'), 'wb') as f:  # 保存绘图数据
            pickle.dump((self.TIME, self.SCORE), f)
        with open(os.path.join(self.logs_folder, 'real-time_detection_logs.txt'), 'w', encoding='utf-8') as f:
            f.write(self.log_text.toPlainText())

    def update_plot(self):
        self.TIME.append(self.TIME[-1] + 1)
        self.SCORE.append(self.score)
        self.plot_widget.plot(self.TIME, self.SCORE, pen='b', symbol='o', symbolPen='b', symbolBrush='r')

    def init_adb(self):
        self.image_label.setFont(QFont('SimHei', 50))
        self.image_label.setStyleSheet("color: #B0B0B0;")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setText('显示区域')
        self.fps_label.clear()

        self.queue.queue.clear()
        self.adb = {'eye_close': 0, 'yawn': 0, 'smoke': 0, 'phone': 0, 'drink': 0}
        self.adb_frame_cnt = {'eye_close': 0, 'yawn': 0, 'smoke': 0, 'phone': 0, 'drink': 0}
        self.score = 100
        self.isAlarm = False

    def get_adb_str(self, adb):
        adb_classes = []
        adb_mapping = {'eye_close': '闭眼', 'yawn': '打哈欠', 'smoke': '抽烟', 'phone': '使用手机', 'drink': '喝水'}
        for adb_cls, value in adb.items():
            if value:
               adb_classes.append(adb_mapping[adb_cls])
        adb_str = ', '.join(adb_classes) if len(adb_classes) else '无'
        return adb_str

    def get_level(self):
        if self.score == 100:
            level = '安全'
        elif self.score > 90:
            level = '较为安全'
        elif self.score > 75:
            level = '轻度危险'
        elif self.score > 60:
            level = '中度危险'
        else:
            level = '非常危险'
        return level

    def end_detect(self):
        if self.start_detect_button.text() == '正在检测中':
            self.update_frame_timer.stop()
            self.update_frame_timer.timeout.disconnect(self.update_frame)
            self.update_log_timer.stop()
            self.update_log_timer.timeout.disconnect(self.update_log)
            self.update_plot_timer.stop()
            self.update_plot_timer.timeout.disconnect(self.update_plot)
            if self.cap.isOpened():
                self.cap.release()
            self.init_adb()
            self.set_text()
            self.start_detect_button.setText('开始检测')

    def set_obj_font(self, obj):
        obj.setFont(QFont("SimHei", 11))

    def switch_show_bbox(self):
        self.show_bbox = not self.show_bbox
        if self.show_bbox_button.text() == 'r':
            self.show_bbox_button.setToolTip('显示边界框')
            self.show_bbox_button.setText('a')
        else:
            self.show_bbox_button.setToolTip('隐藏边界框')
            self.show_bbox_button.setText('r')

    def init_sys(self):
        self.logs_folder = 'logs'
        if not os.path.exists(self.logs_folder):
            os.makedirs(self.logs_folder)

        self.resource_folder = 'resource'
        if not os.path.exists(self.resource_folder):
            os.makedirs(self.resource_folder)

        self.result_folder = 'result'
        if not os.path.exists(self.result_folder):
            os.makedirs(self.result_folder)

