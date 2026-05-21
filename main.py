import kagglehub
from kagglehub import KaggleDatasetAdapter
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import uic
import sys
import os

from descriptions import descriptions # импорт descriptions.py


def resource_path(relative_path):
    # Функция которая в будущем понадобится для сборки приложения
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class MainWindow(QMainWindow):
    def __init__(self, dataframe):
        super().__init__()
        uic.loadUi(resource_path("main.ui"), self) # Загрузка .ui файла (Интерфейс)

        self.df = dataframe # Подключение датасета в класс

        self.fig = Figure()                   # 
        self.canvas = FigureCanvas(self.fig)  # Добавление холста для графика
        self.axes = self.fig.add_subplot(111) # 
        self.Plot.addWidget(self.canvas)      # 

        # Подключение кнопок
        self.btn_show.clicked.connect(lambda: self.pick_category('Без категории'))
        self.btn_category_1.clicked.connect(lambda: self.pick_category('Спорт'))
        self.btn_category_2.clicked.connect(lambda: self.pick_category('2'))
        self.btn_category_3.clicked.connect(lambda: self.pick_category('3'))
        self.btn_category_4.clicked.connect(lambda: self.pick_category('4'))
        self.btn_goto_LowPrice.clicked.connect(lambda: self.pick_price((10, 20)))
        self.btn_goto_MidPrice.clicked.connect(lambda: self.pick_price((20,30)))
        self.btn_goto_HighPrice.clicked.connect(lambda: self.pick_price((30,40)))
        self.btn_back.clicked.connect(lambda: self.switch_pages(back=True))
        self.btn_back_2.clicked.connect(lambda: self.switch_pages(back=True))
        self.btn_menu.clicked.connect(lambda: self.switch_pages(menu=True))
        self.btn_inspect.clicked.connect(self.inspect)

    def switch_pages(self, forward=False, back=False, menu=False):
        # Меняет страницу в зависимости от переданных переменных
        if forward: # Вперёд
            current = self.stackedWidget.currentIndex()
            self.stackedWidget.setCurrentIndex(current+1)
        if back: # Назад
            current = self.stackedWidget.currentIndex()
            self.stackedWidget.setCurrentIndex(current-1)
        if menu: # Меню
            self.stackedWidget.setCurrentIndex(0)
    
    def pick_category(self, category):
        # Записывает выбранную категорию в формате str (Для отсутствия категории - отдельный функционал)
        self.category = category
        if category == 'Без категории':
            self.price = (0, 40) # Здесь нужно установить цену от минимальной до максиальной (Вручную)
            self.btn_back_2.hide()                   # 
            self.btn_menu.move(50, 30)               # 
            self.lb_info.hide()                      # Перестройка сцены
            self.lb_list.move(50 ,110)               # 
            self.list.setGeometry(50, 170, 300, 540) # 
            self.show_category() # Т.к выводится весь список, страница с ценами пропускается
            self.switch_pages(forward=True) # 2 раза переходим на следующую страницу
            self.switch_pages(forward=True) # (чтобы не создавать отдельный случай)
        else:
            self.lb_info.show()
            self.btn_back_2.show()                    # 
            self.btn_menu.move(210, 30)               # Перестройка сцены
            self.lb_list.move(50 ,430)                # 
            self.list.setGeometry(50, 490, 300, 220)  # 
            self.switch_pages(forward=True) # Переход на следующую страницу
    
    def pick_price(self, price):
        # Записывает выбранную ценовую категорию в формате tuple(low, high)
        self.price = price
        self.show_category() # Вызов функции которая выводит 3 страницу со всеми данными
        self.switch_pages(forward=True) # Переход на следующую страницу

    def show_category(self):
        # Переопределяет всю информацию

        self.lb_category.setText(self.category) # Изменение верхнего текста на третьей странице на название выбранной категории
        self.lb_price.setText(f'${self.price[0]}    —    ${self.price[1]}')
        self.lb_info.setText(descriptions[self.category]) # Изменение описания категории
        self.update_bar([1, 2, 3, 4, 5], np.random.randint(low=0, high=100, size=5)) # Вызов функции, которая обновляет график (Параметры пока что случайные)
        self.update_list(self.categories(self.category)) # Вызов функции, которая обновляет список
        for i in range(self.table.rowCount()):     # 
                table_item = self.table.item(i, 1) # Очистка таблицы от прошлых значений
                table_item.setText(' ')            # 
        self.photo.clear() # Очистка прошлой фотографии
        self.photo.setToolTip("")

    def categories(self, category):
        # Возвращает отсортированный список по заранее заданным критериям по категориям.
        match(category):
            case 'Без категории': filtered = self.df # Исходный датасет без фильтров
            case 'Спорт': filtered = self.df.loc[(self.df['acceleration'] > 12) & (self.df['horsepower'] > 200)] # Фильтры пока что случайные
            # Сюда в будущем добавлять остальные категории
        return filtered
    
    def inspect(self):
        # Обновляет таблицу для выбранного из списка автомобиля
        current_item = self.list.currentItem() # Получение выбранного предмета списка
        if current_item: # Проверка на None 
            car_name = current_item.text() # Получение текстового значения выбранного предмета списка (Название автомобиля)
            row = df[df['name'] == car_name].to_numpy().tolist()[0] # Получение массива с данными выбранного автомобиля
            for i in range(1, self.table.rowCount()+1): # 
                table_item = self.table.item(i-1, 1)    # Заполнение таблицы полученными данными
                table_item.setText(str(row[i]))         #
        
            pixmap = QPixmap(f"cars_photos/{car_name}.png") # Загрузка фотографии машины из папки cars_photos (на фотографии ford f250 другая машина)
            if pixmap.isNull(): # Проверка на Null
                pixmap = QPixmap("cars_photos/default_image.png") # Если Null, то загружается заглушка default_image из той же папки
            scaled_pixmap = pixmap.scaled( # 
                self.photo.width(),        # 
                self.photo.height(),       # Автоматическое масштабирование изображения
                Qt.KeepAspectRatio         # 
            )                              # 
            self.photo.setPixmap(scaled_pixmap) # Отрисовка загруженной фотографии
            self.photo.setToolTip(car_name) # Установка подсказки при наведении


    def update_bar(self, x, height):
        # Обновляет график
        self.axes.clear() # Очистка от прошлый значений
        self.axes.barh(x, height) # Задание новых значений
        self.canvas.draw() # Отрисовка графика

    def update_list(self, new_list):
        # Обновляет список
        self.list.clear() # Очистка от прошлых значений
        self.list.addItems(new_list['name']) # Добавление новых значений

if __name__ == "__main__":
    df = kagglehub.dataset_load(                     # 
        KaggleDatasetAdapter.PANDAS,                 # 
        "whenamancodes/automobiles-project-dataset", #  Загрузка датасета
        "Automobile.csv",                            # 
        pandas_kwargs={"encoding": "cp1252"},        # 
    )                                                # 

    app = QApplication(sys.argv) # 
    window = MainWindow(df)      # Запуск окна
    window.show()                # 
    sys.exit(app.exec_())        # 
