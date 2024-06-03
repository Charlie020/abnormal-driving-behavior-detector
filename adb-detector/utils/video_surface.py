from PyQt5.QtMultimedia import QAbstractVideoSurface, QVideoFrame
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QImage


class myVideoSurface(QAbstractVideoSurface):

    frameAvailable = pyqtSignal(QImage)

    def __init__(self, parent=None):
        super().__init__(parent)

    def supportedPixelFormats(self, type=None):
        support_format = [
            QVideoFrame.Format_ARGB32,
            QVideoFrame.Format_ARGB32_Premultiplied,
            QVideoFrame.Format_ARGB8565_Premultiplied,
            QVideoFrame.Format_AYUV444,
            QVideoFrame.Format_AYUV444_Premultiplied,
            QVideoFrame.Format_BGR24,
            QVideoFrame.Format_BGR32,
            QVideoFrame.Format_BGR555,
            QVideoFrame.Format_BGR565,
            QVideoFrame.Format_BGRA32,
            QVideoFrame.Format_BGRA32_Premultiplied,
            QVideoFrame.Format_BGRA5658_Premultiplied,
            QVideoFrame.Format_CameraRaw,
            QVideoFrame.Format_IMC1,
            QVideoFrame.Format_IMC2,
            QVideoFrame.Format_IMC3,
            QVideoFrame.Format_IMC4,
            QVideoFrame.Format_Jpeg,
            QVideoFrame.Format_NV12,
            QVideoFrame.Format_NV21,
            QVideoFrame.Format_RGB24,
            QVideoFrame.Format_RGB32,
            QVideoFrame.Format_RGB555,
            QVideoFrame.Format_RGB565,
            QVideoFrame.Format_User,
            QVideoFrame.Format_UYVY,
            QVideoFrame.Format_Y16,
            QVideoFrame.Format_Y8 ,
            QVideoFrame.Format_YUV420P,
            QVideoFrame.Format_YUV444,
            QVideoFrame.Format_YUYV,
            QVideoFrame.Format_YV12,
        ]
        return support_format

    def present(self, frame: 'QVideoFrame'):
        if frame.isValid():
            self.frameAvailable.emit(frame.image())  # emit QImage
        return True