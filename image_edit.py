from PIL import Image, ImageTk, ImageOps, ImageFilter, ImageEnhance
from coordinates import Rect


class ImageEdit:
    def __init__(self, image):
        self.original_image = image
        self.image = image.copy()  # изображение, которое будет редактироваться

        self.canvas = None
        self.zoom_container = None
        self.image_container = None

        self.imscale = 1.0  # на сколько увеличивается картинка в рамках программы (1.0 = ориг картинка)
        self.zoom_delta = 1.3  # на сколько увеличивается картинка при скроле

        self.crop_selection = None
        self.sel_rect = None
        self.sel_change_side = ""  # узнаем какая сторона выбрана, для изменения
        self.sel_move_x = 0
        self.sel_move_y = 0

    @property
    def image_tk(self):
        return ImageTk.PhotoImage(self.image)

    def set_canvas(self, canvas):
        self.canvas = canvas
        self._bind_zoom()
        self.zoom_container = self.canvas.create_rectangle(0, 0, self.image.width, self.image.height, width=0)
        self._show_zoomed_image()

    def update_image_on_canvas(self):
        if self.canvas is None:
            raise RuntimeError("Холст изображения не указан")

        self._show_zoomed_image()

    def rotate(self, degrees):
        self.image = self.image.rotate(degrees, expand=True)
        self.canvas.delete("all")
        self._reset_scale()

    def flip(self, mode):
        self.image = self.image.transpose(mode)

    def resize(self, percents):
        w, h = self.image.size
        w = (w * percents) // 100
        h = (h * percents) // 100

        self.image = self.image.resize((w, h), Image.Resampling.LANCZOS)
        self._reset_scale()

    def filter(self, filter_type):
        self.image = self.image.filter(filter_type)

    def start_crop_selection(self):
        self._unbind_zoom()  # запретили двигать картинкой во время обрезания
        bbox = self.canvas.bbox(self.image_container)  # создаем новый прямоугольник
        # bbox = (0, 0, 500, 500)
        # print(bbox)
        self.crop_selection = Rect(*bbox, side_offset=5)

        self.sel_rect = self.canvas.create_rectangle(
            *self.crop_selection.coordinates,
            dash=(10, 10), fill="cyan", width=1,
            stipple="gray25", outline="black"
        )  # отрисовали прямогульник

        self._bind_crop()

    def _bind_crop(self):
        self.canvas.bind("<Motion>", self._change_crop_cursor)
        self.canvas.bind("<B1-Motion>", self._move_crop_side)
        self.canvas.bind("<ButtonPress-1>", self._start_crop_area_movement)
        self.canvas.bind("<Double-Button-1>", self._set_crop_area_full_image)

    def _unbind_crop(self):
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<Double-Button-1>")

        self.canvas["cursor"] = ""

    def _change_crop_cursor(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        if self.crop_selection.top_left.point_inside(x, y):  # если курсор находится в заданной облости выделения
            self.canvas["cursor"] = "top_left_corner"
            self.sel_change_side = "top_left"
        elif self.crop_selection.top_right.point_inside(x, y):
            self.canvas["cursor"] = "top_right_corner"
            self.sel_change_side = "top_right"
        elif self.crop_selection.bottom_left.point_inside(x, y):
            self.canvas["cursor"] = "bottom_left_corner"
            self.sel_change_side = "bottom_left"
        elif self.crop_selection.bottom_right.point_inside(x, y):
            self.canvas["cursor"] = "bottom_right_corner"
            self.sel_change_side = "bottom_right"
        elif self.crop_selection.top.point_inside(x, y):
            self.canvas["cursor"] = "top_side"
            self.sel_change_side = "top"
        elif self.crop_selection.left.point_inside(x, y):
            self.canvas["cursor"] = "left_side"
            self.sel_change_side = "left"
        elif self.crop_selection.bottom.point_inside(x, y):
            self.canvas["cursor"] = "bottom_side"
            self.sel_change_side = "bottom"
        elif self.crop_selection.right.point_inside(x, y):
            self.canvas["cursor"] = "right_side"
            self.sel_change_side = "right"
        elif self.crop_selection.center(offset=20).point_inside(x, y):
            self.canvas["cursor"] = "sizing"
            self.sel_change_side = "center"
        else:
            self.canvas["cursor"] = ""
            self.sel_change_side = ""

    def _move_crop_side(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        bbox = self.canvas.bbox(self.image_container)  # получили коордианаты изображения
        #bbox = (0, 0, 500, 500)
        image = Rect(*bbox)

        if self.sel_change_side == "top_left":
            x = max(x, image.x0)
            y = max(y, image.y0)
            if self.crop_selection.width < 20:
                x = min(self.crop_selection.x0, x)
            if self.crop_selection.height < 20:
                y = min(self.crop_selection.y0, y)
            self.crop_selection.change(x0=x, y0=y)

        elif self.sel_change_side == "top_right":
            x = min(x, image.x1)
            y = max(y, image.y0)
            if self.crop_selection.width < 20:
                x = max(self.crop_selection.x1, x)
            if self.crop_selection.height < 20:
                y = min(self.crop_selection.y0, y)
            self.crop_selection.change(x1=x, y0=y)

        elif self.sel_change_side == "bottom_left":
            x = max(x, image.x0)
            y = min(y, image.y1)
            if self.crop_selection.width < 20:
                x = min(self.crop_selection.x0, x)
            if self.crop_selection.height < 20:
                y = max(self.crop_selection.y1, y)
            self.crop_selection.change(x0=x, y1=y)

        elif self.sel_change_side == "bottom_right":
            x = min(x, image.x1)
            y = min(y, image.y1)
            if self.crop_selection.width < 20:
                x = max(self.crop_selection.x1, x)
            if self.crop_selection.height < 20:
                y = max(self.crop_selection.y1, y)
            self.crop_selection.change(x1=x, y1=y)

        elif self.sel_change_side == "top":
            y = max(y, image.y0)
            if self.crop_selection.height < 20:
                y = min(self.crop_selection.y0, y)
            self.crop_selection.change(y0=y)

        elif self.sel_change_side == "left":
            x = max(x, image.x0)
            if self.crop_selection.width < 20:
                x = min(self.crop_selection.x0, x)
            self.crop_selection.change(x0=x)

        elif self.sel_change_side == "bottom":
            y = min(y, image.y1)
            if self.crop_selection.height < 20:
                y = max(self.crop_selection.y1, y)
            self.crop_selection.change(y1=y)

        elif self.sel_change_side == "right":
            x = min(x, image.x1)
            if self.crop_selection.width < 20:
                x = max(self.crop_selection.x1, x)
            self.crop_selection.change(x1=x)

        elif self.sel_change_side == "center":
            dx = x - self.sel_move_x
            dy = y - self.sel_move_y

            self.sel_move_x = x
            self.sel_move_y = y

            if self.crop_selection == image:  # если равняется исходной картинке
                return

            w = self.crop_selection.width
            h = self.crop_selection.height

            x0 = self.crop_selection.x0 + dx
            x1 = self.crop_selection.x1 + dx
            if x0 < image.x0:  # учитываем, что мы не выходим за рамки картинки
                x0 = image.x0
                x1 = x0 + w
            if x1 > image.x1:
                x1 = image.x1
                x0 = x1 - w

            y0 = self.crop_selection.y0 + dy
            y1 = self.crop_selection.y1 + dy
            if y0 < image.y0:  # учитываем, что мы не выходим за рамки картинки
                y0 = image.y0
                y1 = y0 + h
            if y1 > image.y1:
                y1 = image.y1
                y0 = y1 - h
            self.crop_selection.change(x0=x0, y0=y0, x1=x1, y1=y1)

        self.canvas.coords(self.sel_rect, *self.crop_selection.coordinates)

    def _set_crop_area_full_image(self, event):
        bbox = self.canvas.bbox(self.image_container)
        self.crop_selection = Rect(*bbox, side_offset=5)
        self.canvas.coords(self.sel_rect, *bbox)

    def _start_crop_area_movement(self, event):
        if self.sel_change_side == "center":
            self.sel_move_x = self.canvas.canvasx(event.x)
            self.sel_move_y = self.canvas.canvasy(event.y)

    def crop_selected_area(self):
        if self.sel_rect is None:
            raise ValueError("Нет операции обрезки области выделения")

        self._unbind_crop()

        bbox = self.canvas.bbox(self.image_container)
        image = Rect(*bbox)

        dx0 = (self.crop_selection.x0 - image.x0) / image.width
        dx1 = (image.width - (image.x1 - self.crop_selection.x1)) / image.width
        dy0 = (self.crop_selection.y0 - image.y0) / image.height
        dy1 = (image.height - (image.y1 - self.crop_selection.y1)) / image.height

        self.canvas.delete(self.sel_rect)
        self.sel_rect = None

        x0 = int(dx0 * self.image.width)
        y0 = int(dy0 * self.image.height)
        x1 = int(dx1 * self.image.width)
        y1 = int(dy1 * self.image.height)

        if x0 == 0 and y0 == 0 and x1 == self.image.width and y1 == self.image.height:
            self.crop_selection = None
            self._bind_zoom()
            return

        self.image = self.image.crop([x0, y0, x1, y1])
        self._reset_scale()

        self.crop_selection = None
        self._bind_zoom()

    def cancel_crop_selection(self):
        if self.sel_rect is None:
            raise ValueError("Нет операции обрезки области выделения")

        self._unbind_crop()
        self._bind_zoom()
        self.canvas.delete(self.sel_rect)

        self.sel_rect = None
        self.crop_selection = None

    def get_enhancer(self, enhancer):
        return enhancer(self.image)

    def set_image(self, image):
        self.image = image

    def _bind_zoom(self):
        self.canvas.bind("<ButtonPress-1>", self._move_from)
        self.canvas.bind("<B1-Motion>", self._move_to)
        self.canvas.bind("<MouseWheel>", self._zoom_with_wheel)  # Windows and MacOS
        self.canvas.bind("<Button-4>", self._zoom_with_wheel)  # Linux
        self.canvas.bind("<Button-5>", self._zoom_with_wheel)  # Linux

    def _unbind_zoom(self):
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<MouseWheel>")
        self.canvas.unbind("<Button-4>")
        self.canvas.unbind("<Button-5>")

    def _reset_scale(self):
        self.imscale = 1.0

        cx, cy = self.canvas.canvasx(0), self.canvas.canvasy(0)
        self.canvas.delete(self.zoom_container)
        self.zoom_container = self.canvas.create_rectangle(cx, cy, self.image.width + cx, self.image.height + cy, width=0)

    def _move_from(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def _move_to(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        self._show_zoomed_image()

    def _zoom_with_wheel(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        bbox = self.canvas.bbox(self.zoom_container)
        image_area = Rect(*bbox)

        if not (image_area.x0 < x < image_area.x1 and image_area.y0 < y < image_area.y1):
            return

        scale = 1.0
        # event.num - Linux, event.delta - Windows and MacOS
        if event.num == 5 or event.delta == -120:  # скролит вниз
            i = min(self.image.width, self.image.height)
            if int(i * self.imscale) < 30:  # если картинка меньше 30 пикселей
                return
            self.imscale /= self.zoom_delta
            scale /= self.zoom_delta

        if event.num == 4 or event.delta == 120:  # скролит вверх
            i = min(self.canvas.winfo_width(), self.canvas.winfo_height())
            if i < self.imscale:  # можно ли еще увелисить картинку
                return
            self.imscale *= self.zoom_delta
            scale *= self.zoom_delta

        self.canvas.scale('all', x, y, scale, scale)  # изменение масштаба всех объектов canvas
        self._show_zoomed_image()

    def _show_zoomed_image(self, event=None):
        bbox = self.canvas.bbox(self.zoom_container)
        rect = Rect(*bbox)
        #  удаляем с каждой стороны прямоугольника по 1 пикселю, чтобы он был чуть меньше, чем холст
        rect.x0 += 1
        rect.y0 += 1
        rect.x1 -= 1
        rect.y1 -= 1
        #  делаем видимым
        visible = Rect(
            self.canvas.canvasx(0), self.canvas.canvasy(0),
            self.canvas.canvasx(self.canvas.winfo_width()),
            self.canvas.canvasy(self.canvas.winfo_height())
        )
        #  получить поле области прокрутки
        scroll = Rect(
            min(rect.x0, visible.x0), min(rect.y0, visible.y0),
            max(rect.x1, visible.x1), max(rect.y1, visible.y1)
        )
        #  когда изображение находится в видимой области
        if scroll.x0 == visible.x0 and scroll.x1 == visible.x1:
            scroll.x0 = rect.x0
            scroll.x1 = rect.x1
        if scroll.y0 == visible.y0 and scroll.y1 == visible.y1:
            scroll.y0 = rect.y0
            scroll.y1 = rect.y1

        self.canvas.configure(scrollregion=scroll.coordinates)
        #  получаем кусочки координат
        tile = Rect(
            max(scroll.x0 - rect.x0, 0), max(scroll.y0 - rect.y0, 0),
            min(scroll.x1, rect.x1) - rect.x0,
            min(scroll.y1, rect.y1) - rect.y0
        )

        if tile.width > 0 and tile.height > 0:  #  показывать изображение, если оно находится в видимой области
            x = min(int(tile.x1 / self.imscale), self.image.width)
            y = min(int(tile.y1 / self.imscale), self.image.height)

            image = self.image.crop([int(tile.x0 / self.imscale), int(tile.y0 / self.imscale), x, y])
            imagetk = ImageTk.PhotoImage(image.resize([int(tile.width), int(tile.height)]))

            if self.image_container is not None:
                self.canvas.delete(self.image_container)

            self.image_container = self.canvas.create_image(
                max(scroll.x0, rect.x0), max(scroll.y0, rect.y0),
                anchor='nw', image=imagetk
            )

            self.canvas.lower(self.image_container)  #  установаем изображение на задний план
            self.canvas.imagetk = imagetk  #  сохраняем дополнительные ссылки, чтобы сборщик мусора не удалил их
