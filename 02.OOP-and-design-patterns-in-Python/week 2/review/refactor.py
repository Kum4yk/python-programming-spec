import pygame
import random
import math
"""
Вам предоставляется следующий код на языке Python Вам необходимо провести рефакторинг кода: 
Реализовать класс 2 - мерных векторов Vec2d — определить основные математические операции: сумма Vec2d.__add__, разность Vec2d.__sub__, умножение на скаляр и
cкалярное  умножение(Vec2d.__mul__); добавить возможность вычислять длину вектора a через len(a); добавить метод int_pair для получение пары(tuple) целых чисел. 
Реализовать класс замкнутых ломаных  Polyline, с  возможностями: добавление в ломаную  точки(Vec2d) c  её скоростью;  пересчёт  координат  точек(set_points); отрисовка ломаной(draw_points),
Реализовать класс  Knot — потомок класса Polyline — в котором добавление и пересчёт координат инициируют вызов функции get_knot для расчёта точек кривой по добавляемым опорным.
Все классы должны быть самостоятельными и не использовать  внешние функции. 
Дополнительные задачи(для получения "положительной" оценки не обязательны): 

Реализовать возможность удаления точки из кривой. 
Реализовать возможность удаления / добавления точек сразу для нескольких кривых.
Реализовать возможность ускорения / замедления движения кривых. 
"""


class Vec2d(object):

    def __init__(self, vector):
        self.vector = vector

    def __add__(self, other):  # сумма двух векторов
        return Vec2d((self.vector[0] + other.vector[0], self.vector[1] + other.vector[1]))

    def __sub__(self, other):  # разность двух векторов
        return Vec2d((self.vector[0] - other.vector[0], self.vector[1] - other.vector[1]))

    def __len__(self):  # длинна вектора
        return math.sqrt(self.vector[0] * self.vector[0] + self.vector[1] * self.vector[1])

    def __mul__(self, k):
        if (isinstance(k,float)):
            return (Vec2d((self.vector[0] * k, self.vector[1] * k)))
        elif (len(k) == 2):
            return (Vec2d((self.vector[0] * k.vector[0] + self.vector[1] * k.vector[1])))

    def vec(self, other):
        return (sub(self, other))

    def int_pair(self):
        return ((int(self.vector[0]), int(self.vector[1])))


class Polyline(object):
    points = []
    speeds = []

    def __init__(self,points=None, speeds=None):
        if (points != None):
            self.points = self.points + points
        if (speeds != None):
            self.speeds = self.speeds + speeds

    def del_points(self):
        self.points = []
        self.speeds = []

    def __len__(self):
        return len(self.points)

    def add_point(self, point, speed):
        self.points.append(point)
        self.speeds.append(speed)

    def del_point(self):
        self.points.pop(-1)
        self.speeds.pop(-1)

    def set_points(self, SCREEN_DIM):
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].vector[0] > SCREEN_DIM[0] or self.points[p].vector[0] < 0:
                self.speeds[p] =Vec2d(((-1) * self.speeds[p].vector[0], self.speeds[p].vector[1]))
            if self.points[p].vector[1] > SCREEN_DIM[1] or self.points[p].vector[1] < 0:
                self.speeds[p] = Vec2d((self.speeds[p].vector[0], (-1) * self.speeds[p].vector[1]))

    def draw_points(self, gameDisplay, style="points", width=3, color=(255, 255, 255)):
        import pygame
        if style == "line":
            for p_n in range(-1, len(self.points) - 1):
                pygame.draw.line(gameDisplay, color, (points[p_n].int_pair()),
                                 (points[p_n + 1].int_pair()), width)

        elif style == "points":
            for p in self.points:
                pygame.draw.circle(gameDisplay, color, p.int_pair(), width)

    def make_faster(self):
        for p in range(len(self.speeds)):
            self.speeds[p] = Vec2d((self.speeds[p].vector[0] * 2, self.speeds[p].vector[1] * 2))

    def make_slower(self):
        for p in range(len(self.speeds)):
            self.speeds[p] = Vec2d((self.speeds[p].vector[0] / 2, self.speeds[p].vector[1] / 2))


class Knot(Polyline):
    points = []

    def __init__(self, points, count):
        super().__init__()
        self.points = super().points
        self.count = count

    def add_point(self, point, speed):
        Polyline.add_point(self, point, speed)
        self.get_knot()

    def set_points(self, SCREEN_DIM):
        Polyline.set_points(self, SCREEN_DIM)
        self.get_knot()

    def draw_points(self, gameDisplay, style="points", width=3, color=(255, 255, 255)):
        import pygame
        points = self.get_knot()
        if style == "line":
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(gameDisplay, color, (points[p_n].int_pair()),
                                 (points[p_n + 1].int_pair()), width)

        elif style == "points":
            for p in points:
                pygame.draw.circle(gameDisplay, color, p.int_pair(), width)

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return self.get_point(points, alpha, deg - 1) * (1-alpha) + points[deg] * alpha

    def get_points(self, base_points):
        alpha = 1 / self.count
        res = []
        for i in range(self.count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i+1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i+1] + self.points[i+2]) * 0.5)

            res.extend(self.get_points(ptn))
        return res


SCREEN_DIM = (800, 600)


def draw_help():
    """Function used to view help in game"""
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["W", "More speed"])
    data.append(["s", "Less speed"])
    data.append(["d", "del point"])
    data.append(["", ""])
    data.append([str(steps), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
                      (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    points = []
    speeds = []
    show_help = False
    pause = True

    polyline = Polyline()
    knot = Knot(polyline, steps)
    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    polyline.del_points()
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_d:
                    polyline.del_point()
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                    speed = Vec2d((random.random() * 2, random.random() * 2))
                    point = Vec2d((random.random() * 2, random.random() * 2))
                    polyline.add_point(point, speed)
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0
                    polyline.del_point()
                if event.key == pygame.K_w:
                    polyline.make_faster()
                if event.key == pygame.K_s:
                    polyline.make_slower()
            if event.type == pygame.MOUSEBUTTONDOWN:
                point = Vec2d(event.pos)
                speed = Vec2d((random.random() * 2, random.random() * 2))
                polyline.add_point(point, speed)

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        polyline.draw_points(gameDisplay)
        knot.draw_points(gameDisplay,"line",3,color)
        if not pause:
            knot.set_points(SCREEN_DIM)
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
