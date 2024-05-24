import sys
import pickle

from PyQt5.QtWidgets import QApplication, QVBoxLayout, QMainWindow, QWidget
import pyqtgraph as pg  # pyqtgraph必须在PyQt5后面import


class PlotWindow(QMainWindow):
    def __init__(self, pkl_path, parent=None):
        super().__init__(parent)
        self.setGeometry(300, 300, 500, 350)
        self.setWindowTitle('Curve')

        pg.setConfigOption('background', '#FFFFFF')
        pg.setConfigOption('foreground', 'k')
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLabel('left', 'Score')
        self.plot_widget.setLabel('bottom', 'Time (s)')

        self.pkl_path = pkl_path

        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)

        self.centralWidget = QWidget()
        self.centralWidget.setLayout(layout)
        self.setCentralWidget(self.centralWidget)

        self.load_curve_data(self.pkl_path)

    def load_curve_data(self, pkl_path):
        with open(pkl_path, 'rb') as f:
            x, y = pickle.load(f)
        self.plot_widget.plot(x, y, pen='b', symbol='o', symbolPen='b', symbolBrush='r')


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = PlotWindow(r'logs/real-time_detection_curve.pkl')

    window.show()
    sys.exit(app.exec_())
