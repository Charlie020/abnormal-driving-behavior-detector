import sys

from PyQt5.QtWidgets import QApplication
from qt_material import apply_stylesheet

from menu_ui import MenuWindow
from detector_ui import DetectorWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # apply_stylesheet(app, theme="dark_teal.xml")
    # window = MenuWindow()
    window = DetectorWindow()
    window.show()
    sys.exit(app.exec_())


