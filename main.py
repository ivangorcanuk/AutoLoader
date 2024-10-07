# import easygui
# from selenium import webdriver
# import time
# import random
# from fake_useragent import UserAgent
# from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
#
# url = "https://www.instagram.com"
#
# # options
# options = webdriver.FirefoxOptions()  # создали объект опций
#
# #useragent
# useragent = UserAgent()  # не получается!!
# options.set_preference("general.useragent.override", 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0')
#
# options.add_argument("--headless")  # сделали фоновый режим
#
# driver = webdriver.Firefox(options=options)
#
# #executable_path='C:\\Users\\user\\PycharmProjects\\AutoUploader\\DriverFireFox\\geckodriver'
# #"https://www.whatismybrowser.com/detect/what-is-my-user-agent"  ссылка на просмотр моего user-agent
#
# try:
#
#     driver.get(url="https://stepik.org/")
#
#     time.sleep(10)
#
#     driver.find_element(By.ID, "ember452").click()
#
#     time.sleep(5)
#
#     city_input = driver.find_element(By.ID, "id_login_email")
#     city_input.send_keys('ivangorcanuk464@gmail.com')
#
#     time.sleep(5)
#
#     city_input = driver.find_element(By.ID, "id_login_password")
#     city_input.send_keys('iwaniwan1998')
#
#     time.sleep(5)
#
#     city_input.send_keys(Keys.ENTER)
#
#     time.sleep(5)
#
#     driver.find_element(By.XPATH, "//button[@class='rubricator-onboarding__popup-btn']").click()
#
#     time.sleep(5)
#
#     driver.find_element(By.XPATH,
#                         "//button[@class='navbar__profile-toggler st-button_style_none']").click()  # клинул на профиль
#
#     time.sleep(5)
#
#     driver.find_element(By.LINK_TEXT, "Настройки").click()  # клинул настройки
#
#     time.sleep(5)
#
#     driver.find_element(By.XPATH,
#                         "//button[@class='user-edit__image-upload btn-link ']").click()  # клинул загрузить фото
#
#     time.sleep(500)
#
#     # city_input = WebDriverWait(driver, 10).until(
#     #     EC.visibility_of_element_located((By.XPATH, "//input[@class='input js-input']"))
#     # )
#     #
#     # city = input('Введите город: ')
#     #
#     # city_input.send_keys(city)
#     # time.sleep(1)
#     # city_input.send_keys(Keys.ENTER)
#     #
#     # # Ждем загрузки информации о погоде
#     # weather = WebDriverWait(driver, 10).until(
#     #     EC.visibility_of_element_located((By.XPATH, "//div[@class='weather-value']"))
#     # )
#     # print(weather.text)
#
#     # #driver.get(url="https://www.whatismybrowser.com/detect/what-is-my-user-agent")
#     # driver.get(url="https://gismeteo.by/")
#     # time.sleep(1)
#     #
#     # driver.find_element(By.CLASS_NAME, "search-form").click()
#     #
#     # time.sleep(5)
#     #
#     # city_input = driver.find_element(By.XPATH, "//input[@class='input js-input']")
#     # city_input.send_keys('Москва')
#     # time.sleep(5)
#     #
#     # city_input.send_keys(Keys.ENTER)
#     # time.sleep(5)
#     #
#     # weather = driver.find_element(By.XPATH, "//div[@class='weather-value']")
#     # print(weather.text)
#
# except Exception as ex:
#     print(ex)
# finally:
#     driver.close()
#     driver.quit()
#
#
# class Conductor:
#     def __init__(self):
#         self.input_file = easygui.diropenbox()
#
# #input_file = easygui.diropenbox()
# #print(input_file)
#
#
#
#
#
#
#
#
# from tkinter import *
# from tkinter import filedialog as fd
# from tkinter import messagebox as mb
# from tkinter.ttk import Notebook
# from PIL import Image, ImageTk, ImageOps, ImageFilter
# import os
#
#
# class PyPhotoEditor:
#     def __init__(self):
#         self.root = Tk()  # корен нашего виджета
#         self.image_tabs = Notebook(self.root)  # панель для работы с вкладками
#         self.opened_images = []  # список для открытых вкладок с изображениями
#         self.init()  # инициализация окна
#
#     def init(self):
#         self.root.title("Py Photo Editor")
#         self.root.iconphoto(True, PhotoImage(file="Image/icon.png"))  # закрепили картинку на панели программы
#         self.image_tabs.enable_traversal()  # позволяет использовать некоторые сочетания клавиш для переключения между вкладками
#
#         self.root.bind("<Escape>", self._close)  # привязали клавишу ESC на закрытие программы
#         self.root.protocol("WM_DELETE_WINDOW", self._close)
#
#     def run(self):  # метод запуска окна
#         self.draw_menu()  # метод прорисовки меню окна
#         self.draw_widgets()  # метод прорисовки виджетов окна
#
#         self.root.mainloop()
#
#     def draw_menu(self):
#         menu_bar = Menu(self.root)
#
#         file_menu = Menu(menu_bar, tearoff=0)
#         menu_bar.add_cascade(label="File", menu=file_menu)
#         file_menu.add_command(label="Open", command=self.open_new_images)
#         file_menu.add_command(label="Save", command=self.save_current_image)
#         file_menu.add_command(label="Save as", command=self.save_image_as)
#         file_menu.add_command(label="Save all", command=self.save_all_changes)
#         file_menu.add_separator()
#         file_menu.add_command(label="Exit", command=self._close)
#
#         edit_menu = Menu(menu_bar, tearoff=0)
#         transform_menu = Menu(edit_menu, tearoff=0)
#
#         rotate_menu = Menu(transform_menu, tearoff=0)
#         rotate_menu.add_command(label="Rotate left by 90", command=lambda: self.rotate_current_image(90))
#         rotate_menu.add_command(label="Rotate right by 90", command=lambda: self.rotate_current_image(-90))
#         rotate_menu.add_command(label="Rotate left by 180", command=lambda: self.rotate_current_image(180))
#         rotate_menu.add_command(label="Rotate right by 180", command=lambda: self.rotate_current_image(-180))
#         transform_menu.add_cascade(label="Rotate", menu=rotate_menu)
#
#         flip_menu = Menu(edit_menu, tearoff=0)
#         flip_menu.add_command(label="Flip horizontally", command=lambda: self.flip_current_type('horizontally'))
#         flip_menu.add_command(label="Flip vertically", command=lambda: self.flip_current_type('vertically'))
#
#         resize_menu = Menu(edit_menu, tearoff=0)
#         resize_menu.add_command(label="25% of original size", command=lambda: self.resize_current_image(25))
#         resize_menu.add_command(label="50% of original size", command=lambda: self.resize_current_image(50))
#         resize_menu.add_command(label="75% of original size", command=lambda: self.resize_current_image(75))
#         resize_menu.add_command(label="125% of original size", command=lambda: self.resize_current_image(125))
#         resize_menu.add_command(label="150% of original size", command=lambda: self.resize_current_image(150))
#         resize_menu.add_command(label="175% of original size", command=lambda: self.resize_current_image(175))
#
#         filter_menu = Menu(edit_menu, tearoff=0)
#         filter_menu.add_command(label="Blur", command=lambda: self.apply_filter_to_current_image(ImageFilter.BLUR))
#         filter_menu.add_command(label="Sharpen", command=lambda: self.apply_filter_to_current_image(ImageFilter.SHARPEN))
#         filter_menu.add_command(label="Contur", command=lambda: self.apply_filter_to_current_image(ImageFilter.CONTOUR))
#         filter_menu.add_command(label="Detail", command=lambda: self.apply_filter_to_current_image(ImageFilter.DETAIL))
#         filter_menu.add_command(label="Smooth", command=lambda: self.apply_filter_to_current_image(ImageFilter.SMOOTH))
#
#         edit_menu.add_cascade(label="Flip", menu=flip_menu)
#         edit_menu.add_cascade(label="Transform", menu=transform_menu)
#         edit_menu.add_cascade(label="Resize", menu=resize_menu)
#         edit_menu.add_cascade(label="Filter", menu=filter_menu)
#         menu_bar.add_cascade(label="Edit", menu=edit_menu)
#
#         self.root.configure(menu=menu_bar)
#
#     def draw_widgets(self):
#         self.image_tabs.pack(fill="both", expand=1)  # отрисовали панель
#
#     def open_new_images(self):
#         image_paths = fd.askopenfilenames(filetypes=(("Images", "*.jpeg;*.jpg;*.png"),))
#         for image_path in image_paths:
#             self.add_new_image(image_path)
#
#     def add_new_image(self, image_path):
#         image = Image.open(image_path)
#         image_tk = ImageTk.PhotoImage(image)  # преобразовали картинку в ImageTk чтобы отрисовать на экране
#         self.opened_images.append([image_path, image])
#
#         image_tab = Frame(self.image_tabs)  # создаем новую вкладку
#         image_label = Label(image_tab, image=image_tk)
#         image_label.image = image_tk  # сохраняем картику, чтобы не пропала
#         image_label.pack(side="bottom", fill="both", expand=1)
#
#         self.image_tabs.add(image_tab, text=image_path.split('/')[-1])  # добавили новую вкладку и название вкладки
#         self.image_tabs.select(image_tab)  # выделяем выбранную вкладку
#
#     def get_current_working_data(self):  # возвращает tab, image, path
#         current_tab = self.image_tabs.select()  # выбрали вкладку
#         if not current_tab:
#             return None, None, None
#         tab_number = self.image_tabs.index(current_tab)  # получили порядковый № вкладки
#         path, image = self.opened_images[tab_number]
#
#         return current_tab, path, image
#
#     def save_current_image(self):
#         current_tab, path, image = self.get_current_working_data()
#         if not current_tab:
#             return
#         tab_number = self.image_tabs.index(current_tab)  # получили порядковый № вкладки
#         if path[-1] == '*':
#             path = path[:-1]
#             self.opened_images[tab_number][0] = path
#             image.save(path)
#             self.image_tabs.add(current_tab, text=path.split('/')[-1])
#
#     def save_image_as(self):
#         current_tab, path, image = self.get_current_working_data()
#         if not current_tab:
#             return
#         tab_number = self.image_tabs.index(current_tab)  # получили порядковый № вкладки
#         old_path, old_ext = os.path.splitext(path)
#         if old_ext[-1] == '*':
#             old_ext = old_ext[:-1]
#         new_path = fd.asksaveasfilename(initialdir=old_path, filetypes=(("Images", "*.jpeg;*.jpg;*.png"),))  # запросили новый путь для сохранения картики
#         if not new_path:
#             return
#         new_path, new_ext = os.path.splitext(new_path)
#         if not new_ext:
#             new_ext = old_ext
#         elif old_ext != new_ext:
#             print('qwe')
#             mb.showerror("Неправильное разрешене файла", f"Получили неправильное расширение: {new_ext}. Предыдущее: {old_ext}")
#             return
#         image.save(new_path + new_ext)
#         image.close()
#
#         del self.opened_images[tab_number]
#         self.image_tabs.forget(current_tab)
#
#         self.add_new_image(new_path + new_ext)
#
#     def save_all_changes(self):
#         # enumerate([1, 4, 1, 2]) => (0, 1), (1, 4), (2, 1), (3, 2)
#         for index, (path, image) in enumerate(self.opened_images):
#             if path[-1] != "*":
#                 continue
#             path = path[:-1]
#             self.opened_images[index][0] = path
#             image.save(path)
#             self.image_tabs.tab(index, text=path.split('/')[-1])
#
#     def update_image_inside_app(self, current_tab, image):
#         tab_number = self.image_tabs.index(current_tab)  # получили порядковый № вкладки
#         # children = {'!frame': <tkinter.Frame object .!notebook.!frame>}
#         tab_frame = self.image_tabs.children[current_tab[current_tab.rfind('!'):]]
#         label = tab_frame.children["!label"]
#
#         self.opened_images[tab_number][1] = image  # выбрали изображение
#
#         image_tk = ImageTk.PhotoImage(image)
#         label.configure(image=image_tk)
#         label.image = image_tk
#
#         image_path = self.opened_images[tab_number][0]
#         if image_path[-1] != "*":
#             image_path += "*"
#             self.opened_images[tab_number][0] = image_path
#             image_name = image_path.split('/')[-1]
#             self.image_tabs.tab(current_tab, text=image_name)
#
#     def rotate_current_image(self, degrees):
#         current_tab, path, image = self.get_current_working_data()
#         if not current_tab:
#             return
#
#         image = image.rotate(degrees)  # развернули картинку на degrees градусов
#         self.update_image_inside_app(current_tab, image)
#
#     def flip_current_type(self, flip_type):
#         current_tab, path, image = self.get_current_working_data()
#         if not current_tab:
#             return
#
#         if flip_type == 'horizontally':
#             image = ImageOps.mirror(image)
#         elif flip_type == 'vertically':
#             image = ImageOps.mirror(image)
#         self.update_image_inside_app(current_tab, image)
#
#     def resize_current_image(self, percents):
#         current_tab, path, image = self.get_current_working_data()
#         if not current_tab:
#             return
#
#         w, h = image.size
#         w = (w * percents) // 100
#         h = (h * percents) // 100
#
#         image = image.resize((w, h), Image.Resampling.LANCZOS)
#         self.update_image_inside_app(current_tab, image)
#
#     def apply_filter_to_current_image(self, filter_type):
#         current_tab, path, image = self.get_current_working_data()
#         if not current_tab:
#             return
#         image = image.filter(filter_type)
#         self.update_image_inside_app(current_tab, image)
#
#     def unsaved_image(self):
#         for path, _ in self.opened_images:
#             if path[-1] == "*":
#                 return True
#         return False
#
#     def _close(self, event=None):
#         if self.unsaved_image():
#             if not mb.askyesno("Внимание!", "Есть несохраненные изображения."):
#                 return
#         self.root.quit()  # закрываем программу
#
#
# PyPhotoEditor().run()





import tkinter as tk
from tkinter import ttk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Приложение с вкладками")

        # Создаём панель вкладок
        self.tab_control = ttk.Notebook(self.root)

        # Создаем вкладки
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab1, text='Вкладка 1')
        self.create_tab1()

        self.tab2 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab2, text='Вкладка 2')
        self.create_tab2()

        self.tab3 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab3, text='Вкладка 3')
        self.create_tab3()

        # Размещаем панель вкладок
        self.tab_control.pack(expand=1, fill='both')

        # Создаем кнопку для размещения под панелью вкладок
        self.button = ttk.Button(self.root, text="Нажми меня", command=self.button_clicked)
        self.button.pack(anchor="se", pady=10)  # Размещаем кнопку под панелью вкладок

    def create_tab1(self):
        label = ttk.Label(self.tab1, text="Содержимое вкладки 1")
        label.pack(pady=20)

    def create_tab2(self):
        label = ttk.Label(self.tab2, text="Содержимое вкладки 2")
        label.pack(pady=20)

        entry = ttk.Entry(self.tab2)
        entry.pack(pady=10)

    def create_tab3(self):
        label = ttk.Label(self.tab3, text="Содержимое вкладки 3")
        label.pack(pady=20)

        # Например, добавить текстовое поле
        text_area = tk.Text(self.tab3, height=10, width=40)
        text_area.pack(pady=10)

    def button_clicked(self):
        print("Кнопка была нажата!")

# Основной код
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()