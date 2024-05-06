import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from mainwindow import Ui_MainWindow
from qt_material import apply_stylesheet


# YOLO权重路径
def get_yolo_weight():
    return r'resource/model_weight/best.pt'


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)

    # apply_stylesheet(app, theme='dark_teal.xml')
    window.show()
    sys.exit(app.exec())

