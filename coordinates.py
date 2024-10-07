class Rect:
    def __init__(self, x0, y0, x1, y1, side_offset=0):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.side_offset = side_offset  # для определения где находится курсор

    @property
    def width(self):
        return abs(self.x1 - self.x0)

    @property
    def height(self):
        return abs(self.y1 - self.y0)

    @property
    def coordinates(self):
        x0, y0 = min(self.x0, self.x1), min(self.y0, self.y1)
        x1, y1 = max(self.x0, self.x1), max(self.y0, self.y1)
        return [x0, y0, x1, y1]

    def point_inside(self, x, y):  # возвращает bool в зависимости в заданном прямоугольнике
        x0, y0, x1, y1 = self.coordinates
        return x0 < x < x1 and y0 < y < y1

    def __repr__(self):
        return f"Rect [{self.x0, self.y0, self.x1, self.y1}]"
