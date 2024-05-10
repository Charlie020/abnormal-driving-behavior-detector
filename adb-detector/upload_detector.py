import os
import cv2
import numpy as np

from PyQt5.QtCore import Qt, QUrl, pyqtSignal
from PyQt5.QtGui import QFont, QImage, QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QLabel, QFrame, QWidget, QTableWidget, QPushButton, QFileDialog, QTableWidgetItem, \
    QHeaderView, QAbstractItemView, QStackedWidget, QVBoxLayout
from ultralytics import YOLO

from video_surface import myVideoSurface


class Upload_Detector(QWidget):

    # 导出功能的状态信号, 用于更新主窗口状态栏
    exporting_signal = pyqtSignal()
    exported_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.path = ''
        self.folder_path = ''
        self.src_type = None

        # 初始化默认文件夹
        self.resource_folder = ''
        self.result_folder = ''
        self.init_sys()

        # 选择图片
        self.file_open_button = QPushButton('选择图片', self)
        self.file_open_button.setGeometry(705, 5, 100, 30)
        self.file_open_button.clicked.connect(self.open_file)

        # 文件浏览器
        self.folder_open_button = QPushButton('选择文件夹', self)
        self.folder_open_button.setGeometry(705, 70, 100, 30)
        self.folder_open_button.clicked.connect(self.open_folder)

        self.file_table = QTableWidget(self)
        self.file_table.setGeometry(680, 105, 150, 300)
        self.file_table.setColumnCount(1)
        self.file_table.verticalHeader().setMaximumWidth(50)
        self.file_table.setHorizontalHeaderLabels(['文件名'])
        self.file_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.file_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.file_table.cellClicked.connect(self.table_cell_clicked)
        self.file_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # 选择视频
        self.video_open_button = QPushButton('选择视频', self)
        self.video_open_button.setGeometry(705, 440, 100, 30)
        self.video_open_button.clicked.connect(self.open_video)

        # 展示页
        self.res_stack = QStackedWidget(self)
        self.res_stack.setGeometry(5, 5, 660, 645)
        self.res_stack.setFrameShape(QFrame.Box)

        # page_0 默认页
        self.page_0 = QWidget()
        self.example_label = QLabel('显示区域')
        self.example_label.setFont(QFont('SimHei', 50))
        self.example_label.setStyleSheet('color: #B0B0B0;')
        self.example_label.setAlignment(Qt.AlignCenter)
        page_0_layout = QVBoxLayout(self.page_0)
        page_0_layout.addWidget(self.example_label)
        self.res_stack.addWidget(self.page_0)

        # page_1 图片检测页
        self.page_1 = QWidget()
        self.origin_src_label = QLabel('原图', self.page_1)
        self.origin_src_label.setGeometry(10, 5, 600, 20)
        self.set_obj_font(self.origin_src_label)
        self.file_path_label = QLabel('', self.page_1)
        self.file_path_label.setGeometry(110, 5, 600, 20)
        self.file_path_label.setTextInteractionFlags(self.file_path_label.textInteractionFlags() | Qt.TextSelectableByMouse)
        self.file_path_label.setFont(QFont('Times New Roman', 10))
        self.image_label = QLabel(self.page_1)
        self.image_label.setGeometry(10, 40, 640, 595)
        self.res_stack.addWidget(self.page_1)

        # page_2 视频检测页
        self.page_2 = QWidget()
        self.origin_src_label_2 = QLabel('原视频', self.page_2)
        self.origin_src_label_2.setGeometry(10, 5, 200, 20)
        self.set_obj_font(self.origin_src_label_2)
        self.video_path_label = QLabel('', self.page_2)
        self.video_path_label.setGeometry(110, 5, 600, 20)
        self.video_path_label.setTextInteractionFlags(self.video_path_label.textInteractionFlags() | Qt.TextSelectableByMouse)
        self.video_path_label.setFont(QFont('Times New Roman', 10))

        self.video_frame_label = QLabel('显示区域', self.page_2)
        self.video_frame_label.setFont(QFont('SimHei', 50))
        self.video_frame_label.setStyleSheet('color: #B0B0B0;')
        self.video_frame_label.setGeometry(10, 40, 640, 595)
        self.video_frame_label.setAlignment(Qt.AlignCenter)

        self.video_surface = myVideoSurface()
        self.video_surface.frameAvailable.connect(self.update_frame)
        self.video_player = QMediaPlayer()
        self.video_player.setVolume(15)
        self.video_player.setVideoOutput(self.video_surface)
        self.video_player.positionChanged.connect(self.get_video_position)

        self.res_stack.addWidget(self.page_2)

        # 视频功能按钮
        self.restart_button = QPushButton(self)
        self.restart_button.setGeometry(720, 475, 30, 30)
        self.restart_button.setStyleSheet(f'border-image:url({self.resource_folder}/button/restart.jpg);')
        self.restart_button.clicked.connect(self.restart_video)
        self.restart_button.setEnabled(False)

        self.pause_button = QPushButton(self)
        self.pause_button.setGeometry(760, 475, 30, 30)
        self.pause_button.setStyleSheet(f'border-image:url({self.resource_folder}/button/pause.jpg);')
        self.pause_button.clicked.connect(self.pause_video)
        self.pause_button.setEnabled(False)

        # 检测按钮
        self.start_detect_button = QPushButton('开始检测', self)
        self.start_detect_button.setGeometry(705, 540, 100, 50)
        self.start_detect_button.clicked.connect(self.detect)

        # 模型
        from main import get_yolo_weight
        self.model = YOLO(get_yolo_weight())

        self.res_stack.setCurrentIndex(0)
        self.show_bbox = False
        self.position = 0
        self.pause = False

        # 导出按钮
        self.export_file_button = QPushButton(self)
        self.export_file_button.setGeometry(807, 10, 20, 20)
        self.export_file_button.setStyleSheet(f'border-image:url({self.resource_folder}/button/export.jpg);')
        self.export_file_button.clicked.connect(self.export_file)

        self.export_folder_button = QPushButton(self)
        self.export_folder_button.setGeometry(807, 75, 20, 20)
        self.export_folder_button.setStyleSheet(f'border-image:url({self.resource_folder}/button/export.jpg);')
        self.export_folder_button.clicked.connect(self.export_folder)

        self.export_video_button = QPushButton(self)
        self.export_video_button.setGeometry(807, 445, 20, 20)
        self.export_video_button.setStyleSheet(f'border-image:url({self.resource_folder}/button/export.jpg);')
        self.export_video_button.clicked.connect(self.export_video)

    def open_file(self):
        self.path, _ = QFileDialog.getOpenFileName(self, '选择图片', '', 'Images (*.png *.jpg)')
        if self.path:
            self.show_bbox = False    # 第一次打开，默认不检测
            self.render_img(self.path)

    def open_folder(self):
        self.folder_path = QFileDialog.getExistingDirectory(self, '选择文件夹')
        if self.folder_path:
            self.show_bbox = False
            self.load_files(self.folder_path)

    def load_files(self, folder_path):
        file_names = [i for i in os.listdir(folder_path) if i.lower().endswith('jpg') or i.lower().endswith('png')]
        self.file_table.setRowCount(len(file_names))
        for i, file_name in enumerate(file_names):
            item = QTableWidgetItem(file_name)
            self.file_table.setItem(i, 0, item)  # (行, 列, 内容)
        if file_names:
            self.table_cell_clicked(0, 0)  # 选中文件夹后默认展示第一张图片

    def table_cell_clicked(self, row, column):
        self.path = os.path.join(self.folder_path, self.file_table.item(row, column).text())
        self.render_img(self.path)

    def render_img(self, path):
        self.file_path_label.setText(f'{path}')
        self.video_setting(False)
        if self.show_bbox is False:
            self.start_detect_button.setText('开始检测')
            self.origin_src_label.setText('原图')
            self.show_img(cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB))
        else:
            self.start_detect_button.setText('停止检测')
            self.origin_src_label.setText('检测结果')
            detect_res = self.model.predict(source=cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB))
            annotated_frame = detect_res[0].plot()
            self.show_img(annotated_frame)
        self.src_type = 'pic'
        self.res_stack.setCurrentIndex(1)

    def show_img(self, img):
        h, w, ch = img.shape
        scale_ratio = min(self.image_label.width() / w, self.image_label.height() / h)  # 计算图像缩放比例
        resized_img = cv2.resize(img, (int(w * scale_ratio), int(h * scale_ratio)))
        pixmap = QPixmap.fromImage(QImage(resized_img.data, resized_img.shape[1], resized_img.shape[0], resized_img.strides[0],
                          QImage.Format_RGB888))
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)

    def open_video(self):
        self.path, _ = QFileDialog.getOpenFileName(self, '选择图片', '', 'Videos (*.avi *.mp4)')
        if self.path:
            self.show_bbox = False
            self.render_video(self.path)

    def render_video(self, path, position=None):
        self.video_path_label.setText(f'{path}')
        self.video_setting(True)
        if self.show_bbox is False:
            self.start_detect_button.setText('开始检测')
            self.origin_src_label_2.setText('原视频')
        else:
            self.start_detect_button.setText('停止检测')
            self.origin_src_label_2.setText('检测结果')
        self.video_player.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
        if position:
            self.video_player.setPosition(position)
        self.video_player.play()  # 开始将视频帧传入video_surface, 每传入一帧便调用一次update_frame
        self.src_type = 'video'
        self.res_stack.setCurrentIndex(2)

    def update_frame(self, img):
        pixmap = QPixmap.fromImage(img)
        if self.show_bbox:
            # QPixmap to opencv
            qimage = pixmap.toImage()
            shape = (qimage.height(), qimage.bytesPerLine() * 8 // qimage.depth())
            shape += (4,)
            ptr = qimage.bits()
            ptr.setsize(qimage.byteCount())
            cvimg = np.array(ptr, dtype=np.uint8).reshape(shape)
            cvimg = cvimg[..., :3]

            # predict
            result = self.model.predict(source=cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB))
            annotated_frame = result[0].plot()

            # opencv to QPixmap
            h, w, ch = annotated_frame.shape
            bytes_per_line = ch * w
            pixmap = QPixmap.fromImage(QImage(annotated_frame.data, w, h, bytes_per_line, QImage.Format_RGB888))

        scaled_pixmap = pixmap.scaled(self.video_frame_label.size(), Qt.KeepAspectRatio)
        self.video_frame_label.setPixmap(scaled_pixmap)

    def get_video_position(self, position):
        self.position = position

    def detect(self):
        self.show_bbox = not self.show_bbox
        if self.src_type == 'pic':
            self.render_img(self.path)
        elif self.src_type == 'video':
            self.render_video(self.path, position=self.position)

    def video_setting(self, flag):
        if flag is False:
            self.video_player.stop()
            self.video_player.setMedia(QMediaContent())
        self.pause_button.setEnabled(flag)
        self.pause_button.setStyleSheet(f'border-image:url({self.resource_folder}/button/pause.jpg);')
        self.restart_button.setEnabled(flag)

    def restart_video(self):
        self.render_video(self.path, position=0)

    def pause_video(self):
        if self.pause is False:
            self.pause = True
            self.video_player.pause()
            self.pause_button.setStyleSheet(f'border-image:url({self.resource_folder}/button/start.jpg);')
        else:
            self.pause = False
            self.video_player.play()
            self.pause_button.setStyleSheet(f'border-image:url({self.resource_folder}/button/pause.jpg);')

    def export_file(self):
        if self.src_type == 'pic':
            self.exporting_signal.emit()
            res_folder = os.path.join(self.result_folder, 'file')
            if not os.path.exists(res_folder):
                os.makedirs(res_folder)

            result = self.model.predict(source=cv2.cvtColor(cv2.imread(self.path), cv2.COLOR_BGR2RGB))
            annotated_frame = result[0].plot()

            # e.g., ./result/file/00001_annotated.jpg
            cv2.imwrite(f'{os.path.join(res_folder, os.path.basename(self.path).replace(".jpg", "_annotated.jpg"))}', cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR))
            self.exported_signal.emit()

    def export_folder(self):
        if self.src_type == 'pic' and self.folder_path:
            self.exporting_signal.emit()
            """
                创建与选定文件夹的basename同名并加上 '_annotated' 后缀的文件夹
                e.g.,选中文件夹的路径(即self.folder_path): E:/.../abnormal-driving-behavior/mydataset/images
                --> ./result/folder/images_annotated
            """
            res_folder = os.path.join(self.result_folder, f'folder/{os.path.basename(self.folder_path)}_annotated')
            if not os.path.exists(res_folder):
                os.makedirs(res_folder)

            file_list = os.listdir(self.folder_path)
            for file in file_list:
                file_path = os.path.join(self.folder_path, file)
                result = self.model.predict(source=cv2.cvtColor(cv2.imread(file_path), cv2.COLOR_BGR2RGB))
                annotated_frame = result[0].plot()

                # e.g., ./result/folder/images_annotated/00001_annotated.jpg
                cv2.imwrite(f'{os.path.join(res_folder, file.replace(".jpg", "_annotated.jpg"))}',
                            cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR))

            self.exported_signal.emit()

    def export_video(self):
        if self.src_type == 'video':
            self.exporting_signal.emit()
            res_folder = os.path.join(self.result_folder, 'video')
            if not os.path.exists(res_folder):
                os.makedirs(res_folder)

            cap = cv2.VideoCapture(self.path)   # 由于是cv2读取, 所以导出时间会较长

            # 创建视频编解码器对象和视频编写器对象
            frame_width = int(cap.get(3))
            frame_height = int(cap.get(4))
            if self.path.lower().endswith('.mp4'):
                print(1)
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(os.path.join(res_folder, os.path.basename(self.path).replace('.mp4', '_annotate.mp4')), fourcc, 20.0, (frame_width, frame_height))
                print(2)
            elif self.path.lower().endswith('.avi'):
                print(3)
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter(os.path.join(res_folder, os.path.basename(self.path).replace('.avi', '_annotate.avi')), fourcc, 20.0, (frame_width, frame_height))
                print(4)

            while cap.isOpened():
                success, frame = cap.read()
                if success:
                    result = self.model.predict(source=frame)
                    annotated_frame = result[0].plot()
                    out.write(annotated_frame)
                else:
                    break
            cap.release()

            self.exported_signal.emit()

    def set_obj_font(self, obj):
        obj.setFont(QFont('SimHei', 16))

    def init_sys(self):
        self.resource_folder = 'resource'
        if not os.path.exists(self.resource_folder):
            os.makedirs(self.resource_folder)

        self.result_folder = 'result'
        if not os.path.exists(self.result_folder):
            os.makedirs(self.result_folder)

