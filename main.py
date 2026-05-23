import sys
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QListWidget
)

import kagglehub
from kagglehub import KaggleDatasetAdapter

from descriptions import descriptions # Импорт descriptions.py
import check_data # Импорт check_data.py

# Список всех категорий для удобства
CATEGORIES = [
    'Без категории',
    'Семейная',
    'Внедорожная',
    'Спортивная',
]

# Список цен для каждой категории для удобства
PRICES = [
    [(20000, 25000),
    (25000, 40000),
    (40000, 55000),],
    [(38000, 45000),
    (45000, 52000),
    (52000, 100000),],
    [(140000, 220000),
    (220000, 350000),
    (350000, 1000000),],
]

# Список путей к фотографиям интерфейса для удобства
PHOTOS = [
    ['cars_photos/family_Low.png',
     'cars_photos/family_Mid.png',
     'cars_photos/family_High.png',],
    ['cars_photos/SUV_Low.png',
     'cars_photos/SUV_Mid.png',
     'cars_photos/SUV_High.png',],
    ['cars_photos/sport_Low.png',
     'cars_photos/sport_Mid.png',
     'cars_photos/sport_High.png',],
]

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

        self.fig = Figure(figsize=(6, 5))                   # 
        self.canvas = FigureCanvas(self.fig)                #
        self.axes = self.fig.add_subplot(111)               #  Добавление холста для графика
        self.toolbar = NavigationToolbar(self.canvas, self) # 
        self.Plot.addWidget(self.toolbar)                   # 
        self.Plot.addWidget(self.canvas)                    #

        # Подключение кнопок
        self.btn_show.clicked.connect(self.show_all)
        self.btn_category_1.clicked.connect(lambda: self.choose_category(1))
        self.btn_category_2.clicked.connect(lambda: self.choose_category(2))
        self.btn_category_3.clicked.connect(lambda: self.choose_category(3))
        self.btn_goto_LowPrice.clicked.connect(lambda: self.choose_price(0))
        self.btn_goto_MidPrice.clicked.connect(lambda: self.choose_price(1))
        self.btn_goto_HighPrice.clicked.connect(lambda: self.choose_price(2))
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
            self.rebuild_scene()
            current = self.stackedWidget.currentIndex()
            self.stackedWidget.setCurrentIndex(current-1)
        if menu: # Меню
            self.rebuild_scene()
            self.stackedWidget.setCurrentIndex(0)
    
    def show_all(self):
        # Вывод всего датасета целиком
        self.rebuild_scene(do_rebuild=True) # 
        self.category_index = 0 # Без категории - нулевой индекс
        self.category = 'Без категории' # Назначение категории
        self.price = (20000, 1000000) # Назначение цены от минимальной до максимальной
        self.draw_results() # Отрисовка 3 страницы
        self.switch_pages(forward=True) # Переход на 2 страницы вперёд
        self.switch_pages(forward=True) # чтобы пропустить экран выбора цены

    def choose_category(self, choice):
         # Функционал кнопок на первой странице
        self.category_index = choice # Назначение индекса категории
        self.category = CATEGORIES[self.category_index] # Назначение категории
        self.draw_price(self.category_index) # Отрисовка цен на второй странице

        photos = PHOTOS[choice - 1] # Блок отрисовки фотографий интерфейса
        for i in range(len(photos)):
            pixmap = QPixmap(photos[i])
            if pixmap.isNull(): # Проверка на Null
                pixmap = QPixmap("cars_photos/default_image.png") # Если Null, то загружается заглушка default_image из той же папки
            scaled_pixmap = pixmap.scaled( # 
                self.photo.width(),        # 
                self.photo.height(),       # Автоматическое масштабирование изображения
                Qt.KeepAspectRatio         # 
            )                              #
            label = getattr(self, f"photo_price_{i+1}") 
            label.setPixmap(scaled_pixmap) # Отрисовка загруженной фотографии

        self.switch_pages(forward=True) # Переход на следующую страницу

    def draw_price(self, index):
        # Отрисовывает значение цен на второй странице
        category = PRICES[index - 1]  # Получение списка цен для конкретной категории
        self.lb_LowPrice.setText(f'${category[0][0]} — ${category[0][1]}')  # 
        self.lb_MidPrice.setText(f'${category[1][0]} — ${category[1][1]}')  # Отрисовка цен
        self.lb_HighPrice.setText(f'${category[2][0]} — ${category[2][1]}') # 

    def choose_price(self, choice):
        # Функционал кнопок на второй странице 
        self.price_index = choice # Назначение индекса цен
        self.price = PRICES[self.category_index - 1][self.price_index] # Получение конкретного кортежа цен tuple(from, to)
        self.draw_results() # Отрисовка 3 страницы
        self.switch_pages(forward=True) # Переход на следующую страницу

    def draw_results(self):
        # Отрисовывает информацию на 3 странице 
        self.lb_category.setText(self.category) # Меняет название категории справа сверху
        self.lb_price.setText(f'${self.price[0]}    —    ${self.price[1]}') # Меняет цену справа сверху
        self.lb_info.setText(descriptions[self.category]) # Меняет описание категории
        self.update_bar(self.filters()) # Обновление графика
        self.update_list(self.filters()) # Обновление списка
        for i in range(self.table.rowCount()): # 
            table_item = self.table.item(i, 1) # Очистка таблицы от прошлых значений
            table_item.setText(' ')            #
        self.photo.clear() # Очистка прошлой фотографии
        self.photo.setToolTip("") # Очистка подсказки при наведении на фотографию

    def filters(self):
        # Возвращает отфильтрованный датасет 
        FILTERS = [
            lambda: check_data.filter_family(self.df, self.price_index), # 
            lambda: check_data.filter_SUV(self.df, self.price_index),    # Список лямбда функций для упрощения синтаксиса
            lambda: check_data.filter_sport(self.df, self.price_index),  # 
        ]
        
        if self.category_index != 0:
            filtered = FILTERS[self.category_index - 1]() # Получение отфильтрованного датасета
        else:
            filtered = self.df # Если category_index == 0 т.е. "Без категории", то берётся датасет целиком
        filtered["Label"] = filtered["Company Names"] + " " + filtered["Cars Names"] # Формируем названия машин в формате "Компания" + "Марка"
        return filtered

    def update_bar(self, df):
        # Обновляет график
        COLUMNS = [
            'Seats',               # 
            'CC/Battery Capacity', # Список задействованных столбцов для упрощения синтаксиса
            'HorsePower',          # 
        ]
        
        self.fig.clear()                      # Очистка холста от предыдущего графика
        self.axes = self.fig.add_subplot(111) # 
        if self.category_index != 0:
            self.axes.barh(df["Label"], df[f"{COLUMNS[self.category_index - 1]}"]) # 
            self.axes.set_yticks(range(len(df["Label"])))                          # 
            self.axes.set_yticklabels(df["Label"], rotation=0)                     # 
            self.axes.set_xlabel('Марка, модель машины')                           # 
            match self.category:                                                   # 
                case 'Семейная':                                                   # Если category_index != 0 т.е. категория есть,
                    self.axes.set_ylabel('Кол-во сидений')                         # формируем собственный столбчатый график для каждой категории
                case 'Внедорожная':                                                # 
                    self.axes.set_ylabel('Объем двигателя')                        # 
                case 'Спортивная':                                                 # 
                    self.axes.set_ylabel('Кол-во лошадинных сил')                  # 
        else:
            counts = df["Company Names"].value_counts() # 
            threshold = 0.02 * counts.sum()             # 
            other = counts[counts < threshold].sum()    # 
            counts = counts[counts >= threshold]        # 
            counts["Другие"] = other                    # 
            self.axes.pie(                              # Если category_index == 0 т.е. категории нет,
                counts.values,                          # Формируем круговую диаграмму
                labels=counts.index,                    # 
                autopct='%1.1f%%',                      # 
                startangle=90,                          # 
                pctdistance=0.75,                       # 
                labeldistance=1.1,                      # 
            )
        self.fig.tight_layout() # Масштабирование графика по содержимому
        self.canvas.draw() # Отрисовка графика

    def update_list(self, new_list):
        # Обновляет список
        self.list.clear() # Очистка от прошлых значений
        self.list.addItems(new_list['Label']) # Добавление новых значений

    def inspect(self):
        # Обновляет таблицу для выбранного из списка автомобиля
        current_item = self.list.currentItem() # Получение выбранного предмета списка
        if current_item: # Проверка на None 
            car_name = current_item.text() # Получение текстового значения выбранного предмета списка (Название автомобиля)
            df = self.filters()
            row = df[df['Label'] == car_name].to_numpy().tolist()[0] # Получение массива с данными выбранного автомобиля
            for i in range(1, self.table.rowCount()+1): # 
                table_item = self.table.item(i-1, 1)    # Заполнение таблицы полученными данными
                table_item.setText(str(row[i+1]))       #
        
            pixmap = QPixmap(f"cars_photos/{car_name.split()[1]}.png") # Загрузка фотографии машины из папки cars_photos
            if pixmap.isNull(): # Проверка на Null
                pixmap = QPixmap("cars_photos/default_image.png") # Если Null, то загружается заглушка default_image из той же папки
            scaled_pixmap = pixmap.scaled( # 
                self.photo.width(),        # 
                self.photo.height(),       # Автоматическое масштабирование изображения
                Qt.KeepAspectRatio         # 
            )                              # 
            self.photo.setPixmap(scaled_pixmap) # Отрисовка загруженной фотографии
            self.photo.setToolTip(car_name) # Установка подсказки при наведении

    def rebuild_scene(self, do_rebuild=False):
        if do_rebuild:
            self.btn_back_2.hide()                   # 
            self.btn_menu.move(50, 30)               # 
            self.lb_info.hide()                      # Перестройка сцены
            self.lb_list.move(50 ,110)               # 
            self.list.setGeometry(50, 170, 300, 540) # 
        else:
            self.lb_info.show()
            self.btn_back_2.show()                    # 
            self.btn_menu.move(210, 30)               # Перестройка сцены
            self.lb_list.move(50 ,420)                # 
            self.list.setGeometry(50, 480, 300, 230)  # 

if __name__ == "__main__":
    df = pd.read_csv('CarsDataset.csv', encoding='latin1')                         # Загрузка Датасета
    df = df.sort_values(by=["Company Names", "Cars Names"]).reset_index(drop=True) # Сортировка в алфавитном порядке
    check_data.clean_df(df) # Очистка датасета

    app = QApplication(sys.argv) # 
    window = MainWindow(df)      # Запуск окна
    window.show()                # 
    sys.exit(app.exec_())        # 
