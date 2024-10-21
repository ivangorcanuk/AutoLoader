from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter.ttk import Notebook
from PIL import Image, ImageFilter, ImageEnhance, ImageTk
import os
from image_info import ImageInfo
from enhance_slider_window import EnhanceSliderWindow


class MainView:
    root = Tk()  # корень нашего виджета
    list_opened_images = list()  # список для открытых вкладок с изображениями
    description_view = None
    image_tabs = Notebook(root)

    def __init__(self):
        self.button = None
        self.list_last_viewed_images = list()
        self.menu_bar = None

        self.init()  # инициализация окна
        self.open_recent_menu = None

    def init(self):
        self.root.title("Py Photo Editor")
        self.root.geometry(f'630x552+500+50')
        #self.root.iconphoto(True, PhotoImage(file="Image/icon.png"))  # закрепили картинку на панели программы
        self.image_tabs.enable_traversal()  # позволяет использовать некоторые сочетания клавиш для переключения между вкладками

        self.root.bind("<Escape>", self._close)  # привязали клавишу ESC на закрытие программы
        self.root.protocol("WM_DELETE_WINDOW", self._close)

    def go_next(self):
        if self.list_opened_images:
            self.root.configure(menu=Menu())
            self.image_tabs.pack_forget()
            self.button.pack_forget()
            if not self.description_view:
                self.description_view = DescriptionView()
            self.description_view.pack()

    def save_img(self):
        folder_path = "C:/Users/user/PycharmProjects/AutoUploader/Image"  # Замените на ваш путь
        for image in self.list_opened_images:
            new_image_path = folder_path + "/" + image.path.split('/')[-1]
            image.set_path(new_image_path)
            image.save(True)
            print(f"Изображение сохранено: {image.path}")

    def run(self, meaning_bool=False):  # метод запуска окна
        self.draw_menu()  # метод прорисовки меню окна
        self.draw_widgets()  # метод прорисовки виджетов окна
        self.draw_button()
        if meaning_bool:
            self.open_new_images(True)
        else:
            self.root.mainloop()

    def draw_menu(self):
        self.menu_bar = Menu(self.root)

        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Открыть", command=self.open_new_images)

        self.open_recent_menu = Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="Открыть недавний", menu=self.open_recent_menu)
        # for path in self.last_viewed_images:
        #     self.open_recent_menu.add_command(label=path, command=lambda x=path: self.add_new_image(x))

        file_menu.add_separator()
        file_menu.add_command(label="Сохранить", command=self.save_current_image)
        file_menu.add_command(label="Сохранить как", command=self.save_image_as)
        file_menu.add_command(label="Сохранить всё", command=self.save_all_changes)
        file_menu.add_separator()
        file_menu.add_command(label="Закрыть", command=self.close_current_image)
        file_menu.add_separator()
        file_menu.add_command(label="Удалить", command=self.delete_current_image)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self._close)

        self.menu_bar.add_cascade(label="Файл", menu=file_menu)

        edit_menu = Menu(self.menu_bar, tearoff=0)

        rotate_menu = Menu(edit_menu, tearoff=0)
        rotate_menu.add_command(label="Влево на 90˚", command=lambda: self.rotate_current_image(90))
        rotate_menu.add_command(label="Вправо на 90˚", command=lambda: self.rotate_current_image(-90))
        rotate_menu.add_command(label="Влево на 180˚", command=lambda: self.rotate_current_image(180))
        rotate_menu.add_command(label="Вправо на 180˚", command=lambda: self.rotate_current_image(-180))

        flip_menu = Menu(edit_menu, tearoff=0)
        flip_menu.add_command(label="По горизонтали", command=lambda: self.flip_current_image(Image.FLIP_LEFT_RIGHT))
        flip_menu.add_command(label="По вертикали", command=lambda: self.flip_current_image(Image.FLIP_TOP_BOTTOM))

        resize_menu = Menu(edit_menu, tearoff=0)
        resize_menu.add_command(label="25% от первоначального размера", command=lambda: self.resize_current_image(25))
        resize_menu.add_command(label="50% от первоначального размера", command=lambda: self.resize_current_image(50))
        resize_menu.add_command(label="75% от первоначального размера", command=lambda: self.resize_current_image(75))
        resize_menu.add_command(label="125% от первоначального размера", command=lambda: self.resize_current_image(125))
        resize_menu.add_command(label="150% от первоначального размера", command=lambda: self.resize_current_image(150))
        resize_menu.add_command(label="175% от первоначального размера", command=lambda: self.resize_current_image(175))

        filter_menu = Menu(edit_menu, tearoff=0)
        filter_menu.add_command(label="Размытие", command=lambda: self.apply_filter_to_current_image(ImageFilter.BLUR))
        filter_menu.add_command(label="Резкость",
                                command=lambda: self.apply_filter_to_current_image(ImageFilter.SHARPEN))
        filter_menu.add_command(label="Контур", command=lambda: self.apply_filter_to_current_image(ImageFilter.CONTOUR))
        filter_menu.add_command(label="Детализация", command=lambda: self.apply_filter_to_current_image(ImageFilter.DETAIL))
        filter_menu.add_command(label="Сглаживание", command=lambda: self.apply_filter_to_current_image(ImageFilter.SMOOTH))

        crop_menu = Menu(edit_menu, tearoff=0)
        crop_menu.add_command(label="Начать выделение", command=self.start_crop_selection_of_current_image)
        crop_menu.add_command(label="Обрезать", command=self.crop_selection_of_current_image)
        crop_menu.add_command(label="Отменить", command=self.cancel_selection_of_current_image)

        enhance_menu = Menu(edit_menu, tearoff=0)
        enhance_menu.add_command(label="Цвет", command=lambda: self.enhance_current_image("Color", ImageEnhance.Color))
        enhance_menu.add_command(label="Контраст",
                                 command=lambda: self.enhance_current_image("Contrast", ImageEnhance.Contrast))
        enhance_menu.add_command(label="Яркость",
                                 command=lambda: self.enhance_current_image("Brightness", ImageEnhance.Brightness))
        enhance_menu.add_command(label="Чёткость",
                                 command=lambda: self.enhance_current_image("Sharpness", ImageEnhance.Sharpness))

        edit_menu.add_cascade(label="Отзеркалить", menu=flip_menu)
        edit_menu.add_cascade(label="Повернуть", menu=rotate_menu)
        edit_menu.add_cascade(label="Изменить размер", menu=resize_menu)
        edit_menu.add_separator()
        edit_menu.add_cascade(label="Фильтр", menu=filter_menu)
        edit_menu.add_cascade(label="Повысить", menu=enhance_menu)
        edit_menu.add_separator()
        edit_menu.add_cascade(label="Обрезание", menu=crop_menu)

        self.menu_bar.add_cascade(label="Редактировать", menu=edit_menu)

        self.root.configure(menu=self.menu_bar)

    def update_open_recent_menu(self):
        if self.open_recent_menu is None:
            return

        self.open_recent_menu.delete(0, "end")
        for path in self.list_last_viewed_images:
            self.open_recent_menu.add_command(label=path, command=lambda x=path: self.add_new_image(x))

    def draw_widgets(self):
        self.image_tabs.pack(fill="both", expand=1)  # отрисовали панель

    def draw_button(self):
        self.button = ttk.Button(self.root, text='Далее', command=self.go_next)
        self.button.pack(anchor='se')

    def open_new_images(self, images_loaded=False):
        if images_loaded:
            for image in self.list_opened_images:
                self.draw_new_image(image, True)
        else:
            image_paths = fd.askopenfilenames(filetypes=(("Images", "*.jpeg;*.jpg;*.png"),))
            for image_path in image_paths:
                self.add_new_image(image_path)

    def auto_resize_current_image(self, image):
        res_w = int()
        res_h = int()
        w, h = image.size
        max_w = 500
        max_h = 500

        if w >= h:
            res_w = max_w
            ratio = h / w
            res_h = ratio * max_w
        else:
            res_h = max_h
            ratio = w / h
            res_w = max_h * ratio

        return image.resize((round(res_w), round(res_h)), Image.Resampling.LANCZOS)

    def add_new_image(self, image_path):
        if not os.path.isfile(image_path):
            if image_path in self.list_last_viewed_images:
                self.list_last_viewed_images.remove(image_path)
                self.update_open_recent_menu()
            return
        opened_images = [info.path for info in self.list_opened_images]
        if image_path in opened_images:  # отвечает за то чтобы картинка не открывалась дважды
            index = opened_images.index(image_path)
            self.image_tabs.select(index)
            return

        image = Image.open(image_path)
        image = self.auto_resize_current_image(image)
        image_tab = Frame(self.image_tabs)  # создаем новую вкладку

        image_info = ImageInfo(image, image_path, image_tab)
        self.list_opened_images.append(image_info)
        self.draw_new_image(image_info, False)

    def draw_new_image(self, image, isRedraw):
        # делаем холст расширяемым
        image.tab.rowconfigure(0, weight=1)
        image.tab.columnconfigure(0, weight=1)

        canvas = Canvas(image.tab, highlightthickness=0)
        canvas.grid(row=0, column=0, sticky="nsew")
        canvas.update()  # дождаться момента пока холст прогрузится

        image.set_canvas(canvas)
        if not isRedraw:
            self.image_tabs.add(image.tab, text=image.filename())  # добавили новую вкладку и название вкладки
        self.image_tabs.select(image.tab)  # выделяем выбранную вкладку

    def current_image(self):  # возвращает tab, image, path
        current_tab = self.image_tabs.select()  # выбрали вкладку
        if not current_tab:
            return None
        tab_number = self.image_tabs.index(current_tab)  # получили порядковый № вкладки
        return self.list_opened_images[tab_number]

    def save_current_image(self):
        image = self.current_image()
        if not image:
            return
        if not image.unsaved:
            return

        image.save()
        self.image_tabs.add(image.tab, text=image.filename())

    def save_image_as(self):
        image = self.current_image()
        if not image:
            return

        try:
            image.save_as()
            self.update_image_inside_app(image)
        except ValueError as e:
            mb.showerror("Cохранить как ошибку", str(e))

    def save_all_changes(self):
        for image_info in self.list_opened_images:
            if image_info.unsaved:  # если нет изменений
                continue
            image_info.save()
            self.image_tabs.tab(image_info.tab, text=image_info.filename())

    def close_current_image(self):
        image = self.current_image()
        if not image:
            return

        if image.unsaved:
            if not mb.askyesno("Несохраненные изменения", "Закрыть без сохранения изменений?"):
                return

        image.close()
        self.image_tabs.forget(image.tab)
        self.list_opened_images.remove(image)

    def delete_current_image(self):
        image = self.current_image()
        if not image:
            return

        if not mb.askokcancel("Удалить картинку?", "Картинка будет удалена с компьютера."):
            return

        image.delete()
        self.image_tabs.forget(image.tab)
        self.list_opened_images.remove(image)

    def update_image_inside_app(self, image_info):
        image_info.update_image_on_canvas()
        self.image_tabs.tab(image_info.tab, text=image_info.filename())

    def rotate_current_image(self, degrees):
        image = self.current_image()
        if not image:
            return

        image.rotate(degrees)
        image.unsaved = True
        self.update_image_inside_app(image)

    def flip_current_image(self, mode):
        image = self.current_image()
        if not image:
            return

        image.flip(mode)
        image.unsaved = True
        self.update_image_inside_app(image)

    def resize_current_image(self, percents):
        image = self.current_image()
        if not image:
            return

        image.resize(percents)
        image.unsaved = True
        self.update_image_inside_app(image)

    def apply_filter_to_current_image(self, filter_type):
        image = self.current_image()
        if not image:
            return

        image.filter(filter_type)
        image.unsaved = True
        self.update_image_inside_app(image)

    def start_crop_selection_of_current_image(self):
        image = self.current_image()
        if not image:
            return

        image.start_crop_selection()

    def crop_selection_of_current_image(self):
        image = self.current_image()
        if not image:
            return

        try:
            image.crop_selected_area()
            image.unsaved = True
            self.update_image_inside_app(image)
        except ValueError as e:
            mb.showerror("Ошибка обрезки", str(e))

    def cancel_selection_of_current_image(self):
        image = self.current_image()
        if not image:
            return

        try:
            image.cancel_crop_selection()
        except ValueError as e:
            mb.showerror("Ошибка обрезки", str(e))

    def enhance_current_image(self, name, enhance):
        image = self.current_image()
        if not image:
            return
        EnhanceSliderWindow(self.root, name, enhance, image, self.update_image_inside_app)

    def unsaved_image(self):
        for info in self.list_opened_images:
            if info.unsaved:
                return True
        return False

    def _close(self, event=None):
        if self.unsaved_image():
            if not mb.askyesno("Внимание!", "Есть несохраненные изображения."):
                return
        self.root.quit()  # закрываем программу


class DescriptionView(MainView):
    title_of_post = ""
    final_window = None

    def __init__(self):
        super().__init__()
        #self.final_window = FinalWindow()

        self.label_select_images = Label(self.root, font=("Arial", 14), text="Выбранные изображения:")

        self.photo = ImageTk.PhotoImage(self.merge_images())
        self.label_merge_image = Label(self.root, image=self.photo)

        self.label = Label(self.root, font=("Arial", 14), text="Придумай текст:")
        self.text = Text(self.root, font=("Arial", 14), padx=10, pady=10, wrap=WORD)
        self.text.insert(END, self.title_of_post)
        self.button_back = ttk.Button(self.root, text='Назад', command=self.back)
        self.button_publish = ttk.Button(self.root, text='Опубликовать', command=self.publish)

    def merge_images(self):
        list_images = list()
        width_merge_images = 588  # общая ширина виджета склеиных изображений
        width_image = 98  # ширина одного изображения в виджете width_merge_images
        images = [Image.open(image.path) for image in self.list_opened_images]

        if len(images) > 6:
            width_image = 588 // len(images)

        for image in images:
            img = image.resize((width_image, 100), Image.Resampling.LANCZOS)
            list_images.append(img)

        # Получаем ширину и высоту для нового изображения
        total_width = sum(image.width for image in list_images)
        max_height = max(image.height for image in list_images)

        # Создаём новое изображение для склеивания
        new_image = Image.new('RGB', (total_width, max_height))

        # Склеиваем изображения
        x_offset = 0
        for image in list_images:
            new_image.paste(image, (x_offset, 0))
            x_offset += image.width

        return new_image

    def pack(self):
        self.label_select_images.place(x=20, y=10)
        self.label_merge_image.place(x=20, y=40)
        self.label.place(x=20, y=150)
        self.text.place(width=590, height=320, x=20, y=182)
        self.button_back.place(relx=1, rely=1, anchor='se', x=-105, y=-10)
        self.button_publish.place(relx=1, rely=1, anchor='se', x=-10, y=-10)

    def publish(self):
        if self.text.get("1.0", END) != "\n":
            if mb.askyesno("Вопрос", "Вы уверены?"):
                #self.save_img()
                print(self.title_of_post)
                self.forget_widgets()

                self.final_window = FinalWindow()
                print(self.final_window)
                self.final_window.pack_final_window()

    def back(self, window_description_view=True):
        if window_description_view:
            if self.text.get("1.0", END) != "\n":
                DescriptionView.title_of_post = self.text.get("1.0", END)
            self.forget_widgets()
        else:
            print(type(self.final_window))
            self.final_window.forget_widgets()
        self.run(True)

    def forget_widgets(self):
        self.label_select_images.place_forget()
        self.label_merge_image.place_forget()
        self.label.place_forget()
        self.text.place_forget()
        self.button_back.place_forget()
        self.button_publish.place_forget()


class FinalWindow(DescriptionView):
    def __init__(self):
        super().__init__()
        self.label_window_3 = Label(self.root, font=("Arial", 14), text="Ваши изображения опубликованы")
        self.button_return = ttk.Button(self.root, text='Вернуться', command=lambda: self.back(False))
        self.button_exit = ttk.Button(self.root, text='Выход', command=self._close)

    def pack_final_window(self):
        self.label_window_3.pack()
        self.button_return.pack()
        self.button_exit.pack()

    def forget_widgets(self):
        self.label_window_3.pack_forget()
        self.button_return.place_forget()
        self.button_exit.place_forget()



MainView().run()

