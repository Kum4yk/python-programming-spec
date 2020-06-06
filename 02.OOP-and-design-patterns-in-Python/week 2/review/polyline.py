# pip3 install pygame=2.0.0.dev6 to work with MacOS Mojave

import pygame
import random
from math import sqrt


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
LIGHT_BLUE = (64, 128, 255)
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)
ORANGE = (255, 69, 0)

K_ARROW_UP = 1073741906
K_ARROW_DOWN = 1073741905


class Vec2d:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2d(x=self.x + other.x,
                     y=self.y + other.y)

    def __sub__(self, other):
        return Vec2d(x=self.x - other.x,
                     y=self.y - other.y)

    def __mul__(self, k):
        return Vec2d(x=self.x * k, y=self.y * k)

    def __str__(self):
        return "x={0}, y={1}\n".format(self.x, self.y)

    def __len__(self):
        return int(sqrt(self.x**2 + self.y**2))

    def __hash__(self):
        return hash(self.int_pair())

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __repr__(self):
        return "x={0}, y={1}\n".format(self.x, self.y)

    def int_pair(self) -> tuple:
        return int(self.x), int(self.y)


class Polyline:

    def __init__(self):
        self.points = []
        self.speed = []
        self._hue = 0

    def add_point(self,
                  point: Vec2d,
                  ):
        self.points.append(point)
        self.speed.append(Vec2d(x=random.random() * 2, y=random.random() * 2))

    def drop_point(self, drop_point: Vec2d):
        drop_index = -1
        min_difference = float("inf")
        for i in range(len(self.points)):
            distance = len(drop_point - self.points[i])
            if distance < min_difference:
                drop_index = i
                min_difference = distance
        if drop_index == -1:
            return
        self.points.pop(drop_index)
        self.speed.pop(drop_index)

    def change_speed(self, change_coefficient: float):
        for i in range(len(self.speed)):
            self.speed[i] *= change_coefficient

    def set_points(self):
        for i in range(len(self.points)):
            self.points[i] = self.points[i] + self.speed[i]
            if self.points[i].x > SCREEN_DIM[0] or self.points[i].x < 0:
                self.speed[i].x *= -1
            if self.points[i].y > SCREEN_DIM[1] or self.points[i].y < 0:
                self.speed[i].y *= -1

    def draw_points(self, game_display, width=5):
        color = GREEN

        for point in self.points:
            pygame.draw.circle(game_display, color,
                               point.int_pair(),
                               width)

    def draw_line(self, game_display, width=3, points=None):
        points = points or self.points

        color = pygame.Color(0)
        self._hue = (self._hue + 1) % 360
        color.hsla = (self._hue, 100, 50, 100)

        if len(points) <= 2:
            return

        for i in range(-1, len(points)-1):
            pygame.draw.line(game_display, color,
                             points[i].int_pair(),
                             points[i+1].int_pair(),
                             width)


class Knot(Polyline):
    def __init__(self, steps=2):
        self.steps = steps
        super().__init__()

    @property
    def steps(self):
        return self._steps

    @steps.setter
    def steps(self, value):
        if value < 1:
            self._steps = 1
        else:
            self._steps = value

    def get_point(self, points, alpha, deg=None) -> Vec2d:
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self.get_point(points, alpha, deg - 1) * (1 - alpha)

    def get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_knot(self, count):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = [
                (self.points[i] + self.points[i + 1]) * 0.5,
                self.points[i + 1],
                (self.points[i + 1] + self.points[i + 2]) * 0.5
            ]
            res.extend(self.get_points(ptn, count))
        return res

    def draw_line(self, game_display, width=3, points=None):
        super().draw_line(game_display, width, points=self.get_knot(count=self._steps))

    def draw_help(self, game_display):

        game_display.fill(GRAY)
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        data = []
        data.append(["F1", "Show Help"])
        data.append(["R", "Restart"])
        data.append(["P", "Pause/Play"])
        data.append(["+", "More points"])
        data.append(["-", "Less points"])
        data.append(["Arrow Up", "Speed Up"])
        data.append(["Arrow Down", "Speed Down"])
        data.append(["D", "Delete Point Mode ON/OFF. To delete point click on board"])
        data.append(["", ""])
        data.append([str(len(self.points)), "Current points"])

        pygame.draw.lines(game_display, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            game_display.blit(font1.render(
                text[0], True, ORANGE), (100, 100 + 30 * i))
            game_display.blit(font2.render(
                text[1], True, ORANGE), (200, 100 + 30 * i))


if __name__ == "__main__":
    SCREEN_DIM = (1050, 900)

    working = True
    pause = True
    show_help = False
    delete_point_mode = False

    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")
    gameDisplay.fill(WHITE)

    polyline1 = Knot()

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                point = Vec2d(*event.pos)
                if not delete_point_mode:
                    polyline1.add_point(point)
                else:
                    polyline1.drop_point(drop_point=point)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_d:
                    delete_point_mode = not delete_point_mode
                if event.key == pygame.K_r:
                    polyline1.points = []
                    polyline1.speed = []
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key in (pygame.K_EQUALS, pygame.K_KP_PLUS):
                    polyline1.steps += 1
                if event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    polyline1.steps -= 1
                if event.key in (K_ARROW_UP, pygame.K_UP):
                    polyline1.change_speed(1.1)
                if event.key in (K_ARROW_DOWN, pygame.K_DOWN):
                    polyline1.change_speed(0.9)

        gameDisplay.fill(WHITE)
        polyline1.draw_points(gameDisplay)
        polyline1.draw_line(gameDisplay)
        if not pause:
            polyline1.set_points()
        if show_help:
            polyline1.draw_help(gameDisplay)

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
