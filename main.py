import kagglehub
from kagglehub import KaggleDatasetAdapter
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QInputDialog, QLineEdit, QApplication, QWidget, QVBoxLayout, QPushButton, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5 import uic
import sys
import os


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(resource_path("main.ui"), self)


        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.axes = self.fig.add_subplot(111)
        self.Plot.addWidget(self.canvas)

        self.btn_show.clicked.connect(self.show_category)
        self.btn_back.clicked.connect(self.back_to_menu)

    def show_category(self):
        self.lb_category.setText(self.cb_categories.currentText())
        self.update_plot()
        self.stackedWidget.setCurrentIndex(1)

    def back_to_menu(self):
        self.stackedWidget.setCurrentIndex(0)

    def update_plot(self):
        self.axes.clear()
        self.axes.bar([1, 2, 3, 4, 6], np.random.randint(low=0, high=100, size=5))
        self.canvas.draw()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


    # df = kagglehub.dataset_load(
    #     KaggleDatasetAdapter.PANDAS,
    #     "krupalpatel07/nvidia-historical-data",
    #     "NVDA.csv",
    # )
