from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter.ttk import Notebook
from PIL import Image, ImageFilter, ImageEnhance
import os
from image_info import ImageInfo
from enhance_slider_window import EnhanceSliderWindow


class PyPhotoEditor:
    def __init__(self):
        self.root = Tk()  # корен нашего виджета
        self.image_tabs = Notebook(self.root)  # панель для работы с вкладками
        self.button = ttk.Button(self.root, text='Далее', command=self.further)
        self.opened_images = []  # список для открытых вкладок с изображениями
        self.last_viewed_images = []
        self.menu_bar = None

        self.init()  # инициализация окна
        self.open_recent_menu = None

    def init(self):
        self.root.title("Py Photo Editor")
        self.root.geometry(f'630x500+500+50')
        self.root.iconphoto(True, PhotoImage(file="Image/icon.png"))  # закрепили картинку на панели программы
        self.image_tabs.enable_traversal()  # позволяет использовать некоторые сочетания клавиш для переключения между вкладками

        self.root.bind("<Escape>", self._close)  # привязали клавишу ESC на закрытие программы
        self.root.protocol("WM_DELETE_WINDOW", self._close)

    def further(self):
        self.destroy_main_widgets()
        Install(self.root)

    def destroy_main_widgets(self):
        self.image_tabs.destroy()
        self.menu_bar.destroy()
        self.button.destroy()

    def run(self):  # метод запуска окна
        self.draw_menu()  # метод прорисовки меню окна
        self.draw_widgets()  # метод прорисовки виджетов окна
        self.draw_button()

        self.root.mainloop()

    def draw_menu(self):
        self.menu_bar = Menu(self.root)

        #self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_new_images)

        self.open_recent_menu = Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="Open Recent", menu=self.open_recent_menu)
        for path in self.last_viewed_images:
            self.open_recent_menu.add_command(label=path, command=lambda x=path: self.add_new_image(x))

        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self.save_current_image)
        file_menu.add_command(label="Save as", command=self.save_image_as)
        file_menu.add_command(label="Save all", command=self.save_all_changes)
        file_menu.add_separator()
        file_menu.add_command(label="Close image", command=self.close_current_image)
        file_menu.add_separator()
        file_menu.add_command(label="Delete image", command=self.delete_current_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._close)

        self.menu_bar.add_cascade(label="File", menu=file_menu)

        edit_menu = Menu(self.menu_bar, tearoff=0)

        rotate_menu = Menu(edit_menu, tearoff=0)
        rotate_menu.add_command(label="Rotate left by 90", command=lambda: self.rotate_current_image(90))
        rotate_menu.add_command(label="Rotate right by 90", command=lambda: self.rotate_current_image(-90))
        rotate_menu.add_command(label="Rotate left by 180", command=lambda: self.rotate_current_image(180))
        rotate_menu.add_command(label="Rotate right by 180", command=lambda: self.rotate_current_image(-180))

        flip_menu = Menu(edit_menu, tearoff=0)
        flip_menu.add_command(label="Flip horizontally", command=lambda: self.flip_current_image(Image.FLIP_LEFT_RIGHT))
        flip_menu.add_command(label="Flip vertically", command=lambda: self.flip_current_image(Image.FLIP_TOP_BOTTOM))

        resize_menu = Menu(edit_menu, tearoff=0)
        resize_menu.add_command(label="25% of original size", command=lambda: self.resize_current_image(25))
        resize_menu.add_command(label="50% of original size", command=lambda: self.resize_current_image(50))
        resize_menu.add_command(label="75% of original size", command=lambda: self.resize_current_image(75))
        resize_menu.add_command(label="125% of original size", command=lambda: self.resize_current_image(125))
        resize_menu.add_command(label="150% of original size", command=lambda: self.resize_current_image(150))
        resize_menu.add_command(label="175% of original size", command=lambda: self.resize_current_image(175))

        filter_menu = Menu(edit_menu, tearoff=0)
        filter_menu.add_command(label="Blur", command=lambda: self.apply_filter_to_current_image(ImageFilter.BLUR))
        filter_menu.add_command(label="Sharpen",
                                command=lambda: self.apply_filter_to_current_image(ImageFilter.SHARPEN))
        filter_menu.add_command(label="Contur", command=lambda: self.apply_filter_to_current_image(ImageFilter.CONTOUR))
        filter_menu.add_command(label="Detail", command=lambda: self.apply_filter_to_current_image(ImageFilter.DETAIL))
        filter_menu.add_command(label="Smooth", command=lambda: self.apply_filter_to_current_image(ImageFilter.SMOOTH))

        crop_menu = Menu(edit_menu, tearoff=0)
        crop_menu.add_command(label="Start selection", command=self.start_crop_selection_of_current_image)
        crop_menu.add_command(label="Crop selected", command=self.crop_selection_of_current_image)

        enhance_menu = Menu(edit_menu, tearoff=0)
        enhance_menu.add_command(label="Color", command=lambda: self.enhance_current_image("Color", ImageEnhance.Color))
        enhance_menu.add_command(label="Contrast",
                                 command=lambda: self.enhance_current_image("Contrast", ImageEnhance.Contrast))
        enhance_menu.add_command(label="Brightness",
                                 command=lambda: self.enhance_current_image("Brightness", ImageEnhance.Brightness))
        enhance_menu.add_command(label="Sharpness",
                                 command=lambda: self.enhance_current_image("Sharpness", ImageEnhance.Sharpness))

        edit_menu.add_cascade(label="Flip", menu=flip_menu)
        edit_menu.add_cascade(label="Rotate", menu=rotate_menu)
        edit_menu.add_cascade(label="Resize", menu=resize_menu)
        edit_menu.add_separator()
        edit_menu.add_cascade(label="Filter", menu=filter_menu)
        edit_menu.add_cascade(label="Enhance", menu=enhance_menu)
        edit_menu.add_separator()
        edit_menu.add_cascade(label="Crop", menu=crop_menu)

        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

        self.root.configure(menu=self.menu_bar)

    def update_open_recent_menu(self):
        if self.open_recent_menu is None:
            return

        self.open_recent_menu.delete(0, "end")
        for path in self.last_viewed_images:
            self.open_recent_menu.add_command(label=path, command=lambda x=path: self.add_new_image(x))

    def draw_widgets(self):
        self.image_tabs.pack(fill="both", expand=1)  # отрисовали панель

    def draw_button(self):
        self.button.pack(anchor='se')

    def open_new_images(self):
        image_paths = fd.askopenfilenames(filetypes=(("Images", "*.jpeg;*.jpg;*.png"),))
        for image_path in image_paths:
            self.add_new_image(image_path)

########################################################################################################################

    def auto_resize_current_image(self, image):
        w, h = image.size
        max_w = 500
        max_h = 450
        res_w = int()
        res_h = int()

        if w >= h:
            res_w = max_w
            ratio = h / w
            res_h = ratio * max_w
        else:
            res_h = max_h
            ratio = w / h
            res_w = max_h * ratio
        # w = (w * 14) // 100
        # h = (h * 14) // 100

        img = image.resize((round(res_w), round(res_h)), Image.Resampling.LANCZOS)
        return img

########################################################################################################################

    def add_new_image(self, image_path):
        if not os.path.isfile(image_path):
            if image_path in self.last_viewed_images:
                self.last_viewed_images.remove(image_path)
                self.update_open_recent_menu()
            return
        opened_images = [info.path for info in self.opened_images]
        if image_path in opened_images:  # отвечает за то чтобы картинка не открывалась дважды
            index = opened_images.index(image_path)
            self.image_tabs.select(index)
            return

        image = Image.open(image_path)
        image_tab = Frame(self.image_tabs)  # создаем новую вкладку

        image_info = ImageInfo(image, image_path, image_tab)
        self.opened_images.append(image_info)

        #  делаем холст расширяемым
        image_tab.rowconfigure(0, weight=1)
        image_tab.columnconfigure(0, weight=1)

        canvas = Canvas(image_tab, highlightthickness=0)
        canvas.grid(row=0, column=0, sticky="nsew")
        canvas.update()  #  дождаться момента пока холст прогрузится

        image_info.set_canvas(canvas)

        self.image_tabs.add(image_tab, text=image_info.filename())  # добавили новую вкладку и название вкладки
        self.image_tabs.select(image_tab)  # выделяем выбранную вкладку

    def current_image(self):  # возвращает tab, image, path
        current_tab = self.image_tabs.select()  # выбрали вкладку
        if not current_tab:
            return None
        tab_number = self.image_tabs.index(current_tab)  # получили порядковый № вкладки
        return self.opened_images[tab_number]

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
        for image_info in self.opened_images:
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
        self.opened_images.remove(image)

    def delete_current_image(self):
        image = self.current_image()
        if not image:
            return

        if not mb.askokcancel("Удалить картинку?", "Картинка будет удалена с компьютера."):
            return

        image.delete()
        self.image_tabs.forget(image.tab)
        self.opened_images.remove(image)

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

    def enhance_current_image(self, name, enhance):
        image = self.current_image()
        if not image:
            return
        EnhanceSliderWindow(self.root, name, enhance, image, self.update_image_inside_app)

    def unsaved_image(self):
        for info in self.opened_images:
            if info.unsaved:
                return True
        return False

    def _close(self, event=None):
        if self.unsaved_image():
            if not mb.askyesno("Внимание!", "Есть несохраненные изображения."):
                return
        self.root.quit()  # закрываем программу


class Install:
    def __init__(self, root):
        self.root = root
        self.button_back = ttk.Button(self.root, text='Назад', command=lambda: print('Назад'))
        self.button_publish = ttk.Button(self.root, text='Опубликовать', command=self.publish)
        self.label = Label(self.root, font=("Arial", 14), text="Придумай текст")
        self.text = Text(self.root, font=("Arial", 14), padx=10, pady=10, wrap=WORD)

        self.init()

    def init(self):
        self.label.pack()
        self.text.pack(padx=30, pady=110)
        self.button_back.place(relx=1, rely=1, anchor='se', x=-105, y=-10)
        self.button_publish.place(relx=1, rely=1, anchor='se', x=-10, y=-10)

    def publish(self):
        print(self.text.get("1.0", END))


PyPhotoEditor().run()

