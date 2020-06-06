import pygame
import random
import math


class Vec2D:
    """
    класс 2-мерных векторов

    """
    def __init__(self, x, y=0):
        if ((type(x) == tuple or type(x) == list) and
                (type(x[0]) == int or type(x[0]) == float) and
                (type(x[1]) == int or type(x[1]) == float)):
            self._x = int(x[0])
            self._y = int(x[1])
        elif ((type(x) == int or type(x) == float) and
              (type(y) == int or type(y) == float)):
            self._x = int(x)
            self._y = int(y)
        else:
            raise ValueError('class Vec2D.__init__:         \
                              параметры не является числом')

    def int_pair(self):
        """
        возвращает  кортеж из двух целых чисел (текущие координаты вектора).
        """
        return self._x, self._y

    def __str__(self):
        return f'Vec2D({self._x}, {self._y})'

    def __add__(self, b: 'Vec2D'):
        """возвращает сумму двух векторов"""
        return Vec2D(self._x + b._x, self._y + b._y)

    def __sub__(self, b: 'Vec2D'):
        """возвращает разность двух векторов"""
        return Vec2D(self._x - b._x, self.y - b._y)

    def __mul__(self, k: 'int or float'):
        """возвращает произведение вектора на число справа """
        if type(k) == int or type(k) == float:
            return Vec2D(self._x * k, self._y * k)
        else:
            raise ValueError('class Vec2D.__mul__:          \
                              множитель не является числом')
            return

    def __len__(self):
        """ duck typing: возвращает длину вектора, округленную до целого """
        return int(math.sqrt(self._x ** 2 + self._y ** 2))


class Polyline:
    """
    класс замкнутых ломаных Polyline с методами отвечающими за
    добавление в ломаную точки (Vec2d) c её скоростью,
    пересчёт координат точек (set_points) и
    отрисовку ломаной (draw_points)

    """
    def __init__(self, drow_screen):
        self.drow_screen = drow_screen
        self.base_points = []
        self.base_speeds = []
        self.line_points = []
        self._new_base_point = False
        self._velocity = 0.05

    def add_point(self, point, screen_dim):
        """ добавление новой точки (координата мыши) """
        self.base_points.append(Vec2D(point))
        self.base_speeds.append(Vec2D(random.randint(1, int(screen_dim[0]/5)),
                                      random.randint(1, int(screen_dim[1]/5))))
        self._new_base_point = True

    def delete_points(self):
        """ удаление всех точек """
        self.base_points = []
        self.base_speeds = []
        self._new_base_point = True

    def velocity_increase(self):
        """ увеличиваем скорость """
        self._velocity *= 1.25

    def velocity_decrease(self):
        """ уменьшаем скорость """
        self._velocity *= 0.8

    def set_points(self, screen_dim):
        """ пересчёт координат опорных точек """
        for p in range(len(self.base_points)):
            self.base_points[p] = (self.base_points[p] +
                                   self.base_speeds[p]*self._velocity)
            """ стенки """
            z = self.base_points[p].int_pair()
            if z[0] > screen_dim[0] or z[0] < 0:
                v = self.base_speeds[p].int_pair()
                self.base_speeds[p] = Vec2D(- v[0], v[1])
            if z[1] > screen_dim[1] or z[1] < 0:
                v = self.base_speeds[p].int_pair()
                self.base_speeds[p] = Vec2D(v[0], -v[1])

    def draw_points(self, style="points", width=3, color=(255, 255, 255)):
        """функция отрисовки ломаной и точек на экране"""
        if style == "line":
            for p_n in range(-1, len(self.line_points) - 1):
                pygame.draw.line(self.drow_screen, color,
                                 self.line_points[p_n].int_pair(),
                                 self.line_points[p_n+1].int_pair(), width)

        elif style == "points":
            for point in self.base_points:
                pygame.draw.circle(self.drow_screen, color,
                                   point.int_pair(), width)


class Knot(Polyline):
    """
    наследник класса Polyline,
    в котором добавление и пересчёт координат инициируют вызов функции get_knot
    для расчёта точек кривой по добавляемым «опорным» точкам

    """
    def __init__(self, drow_screen):
        super().__init__(drow_screen)
        self.hue = 0
        self.color = pygame.Color(0)
        self._count = 35

    def get_count(self):
        """ количество разбиений отрезка для сглаживания линии"""
        return self._count

    def count_vary(self, vary: int):
        """ именяем количество разбиений отрезка для сглаживания линии"""
        z = self._count + vary
        self._count = z if z > 1 else 1

    def drow(self, screen_dim: tuple, pause: bool, hide_points: bool):
        if not pause:
            self.set_points(screen_dim)
        if not pause or self._new_base_point:
            ''' нет паузы или есть новая базовая точка '''
            self.get_knot()
        if not hide_points:
            ''' drow base_points '''
            self.draw_points(style="points")
        self.hue = (self.hue + 1) % 360
        self.color.hsla = (self.hue, 100, 50, 100)
        ''' drow polyline '''
        self.draw_points(style="line", width=3, color=self.color)

    def get_knot(self):
        self._new_base_point = False
        if len(self.base_points) < 3:
            return []
        self.line_points = []
        for i in range(-2, len(self.base_points) - 2):
            ptn = []
            ptn.append((self.base_points[i] + self.base_points[i + 1]) * 0.5)
            ptn.append(self.base_points[i + 1])
            ptn.append((self.base_points[i + 1] +
                        self.base_points[i + 2]) * 0.5)
            self.line_points.extend(self._get_points(ptn, self._count))

    def _get_points(self, points_3, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self._get_point(points_3, i * alpha))
        return res

    def _get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return (points[deg]*alpha +
                self._get_point(points, alpha, deg - 1)*(1-alpha))


def draw_help():
    """функция отрисовки экрана справки программы"""
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["Escape", "Exit"])
    data.append(["MOUSEBUTTONDOWN", "Set base point"])
    data.append(["P", "Pause/Play"])
    data.append(["R", "Restart"])
    data.append(["Insert", "Add new line"])
    data.append(["Tab", "Select line"])
    data.append(["Delete", "Remove selected line"])
    data.append(["Home", "Hide/show base points"])
    data.append(["Uparrow", "Increase velocity"])
    data.append(["Downarrow", "Decrease velocity"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["", ""])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (400, 100 + 30 * i))


if __name__ == '__main__':
    """
    """
    pygame.init()
    screen_dimention = (800, 600)
    gameDisplay = pygame.display.set_mode(screen_dimention)
    caption_base = "MyScreenSaver"
    pygame.display.set_caption(caption_base)

    polylines = []
    polylines.append(Knot(gameDisplay))

    working = True
    show_help = False
    pause = True
    hide_points = False

    selected = 0
    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            """keyboard"""
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                """ управление линиями """
                if event.key == pygame.K_TAB:         # выбор активной линии
                    selected += 1
                    selected %= len(polylines)
                if event.key == pygame.K_INSERT:      # добавление линии
                    polylines.append(Knot(gameDisplay))
                    selected = len(polylines)-1
                if event.key == pygame.K_DELETE:     # удаление активной линии
                    if len(polylines) > 1:
                        polylines.pop(selected)
                        selected %= len(polylines)
                if event.key == pygame.K_HOME:        # скрыть базовые точки
                    hide_points = not hide_points
                """ пауза """
                if event.key == pygame.K_p:
                    pause = not pause
                """ управление базовыми точками """
                if event.key == pygame.K_r:
                    polylines[selected].delete_points()
                """ скорость """
                if event.key == pygame.K_UP:
                    polylines[selected].velocity_increase()
                if event.key == pygame.K_DOWN:
                    polylines[selected].velocity_decrease()
                """ сглаживание """
                if event.key == pygame.K_KP_PLUS:
                    polylines[selected].count_vary(1)
                if event.key == pygame.K_KP_MINUS:
                    polylines[selected].count_vary(-1)
                """help"""
                if event.key == pygame.K_F1:
                    show_help = not show_help
            """ mouse """
            if event.type == pygame.MOUSEBUTTONDOWN:
                polylines[selected].add_point(event.pos, screen_dimention)

        caption = f"{caption_base}:    Всего линий {len(polylines)}, активная №{selected+1} \
                скорость = {round(polylines[selected]._velocity,5)}  \
                точек сглаживания = {polylines[selected]._count}"
        pygame.display.set_caption(caption)

        gameDisplay.fill((0, 0, 0))
        for polyline in polylines:
            polyline.drow(screen_dimention, pause, hide_points)

        if show_help:
            draw_help()                 # функция экрана справки программы

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
