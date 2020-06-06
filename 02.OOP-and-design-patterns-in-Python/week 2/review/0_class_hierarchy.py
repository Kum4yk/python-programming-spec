import math
import random

import pygame


SCREEN_DIM = (800, 600)


class Vec2d(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2d(self.x - other.x, self.y - other.y)

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def __len__(self):
        return int(self.length())

    def __mul__(self, other):
        if isinstance(other, Vec2d):
            return self.x * other.x + self.y * other.y
        else:
            return Vec2d(self.x * other, self.y * other)

    __rmul__ = __mul__

    def __repr__(self):
        return f'v({self.x}, {self.y})'

    def int_pair(self):
        return int(self.x), int(self.y)

    def flip_x(self):
        self.x = -self.x

    def flip_y(self):
        self.y = -self.y


class Polyline(object):

    eps = int(SCREEN_DIM[0] * 0.005)

    def __init__(self, velocity=20):
        self.points = []
        self.speeds = []
        self.velocity = velocity

    def __len__(self):
        return len(self.points)

    def accelerate(self):
        self.velocity = min(100, self.velocity + 1)

    def decelerate(self):
        self.velocity = max(0, self.velocity - 1)

    def add(self, point, speed=None):
        if speed is None:
            speed = Vec2d(random.random(), random.random())
        self.points.append(point)
        self.speeds.append(speed)

    def get_idx_at_point(self, point):
        for j, p in enumerate(self.points):
            if len(p - point) <= self.eps:
                return j
        return None

    def delete(self, point):
        ix = self.get_idx_at_point(point)
        if ix is not None:
            self.points.pop(ix)
            self.speeds.pop(ix)
            return True
        return False

    def add_or_delete(self, point):
        if not self.delete(point):
            self.add(point)

    def set_points(self):
        for p in range(len(self.points)):
            self.points[p] = (self.points[p] +
                              self.speeds[p] * (self.velocity * 0.1))
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p].flip_x()
            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p].flip_y()

    def draw_points(self, display,
                    style="points", width=3, color=(255, 255, 255)):
        if style == "line":
            for j in range(-1, len(self.points) - 1):
                pygame.draw.line(
                    display, color,
                    self.points[j].int_pair(), self.points[j + 1].int_pair(),
                    width
                )
        elif style == "points":
            for p in self.points:
                pygame.draw.circle(
                    display, color,
                    p.int_pair(),
                    width
                )


class Knot(Polyline):

    def __init__(self, steps=5):
        super(Knot, self).__init__()
        self.__steps = steps

    @property
    def steps(self):
        return self.__steps

    @steps.setter
    def steps(self, steps):
        if steps < 1:
            self.__steps = 1
        elif steps > 50:
            self.__steps = 50
        else:
            self.__steps = steps

    @staticmethod
    def __get_point(points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return (points[deg] * alpha +
                Knot.__get_point(points, alpha, deg - 1) * (1 - alpha))

    @staticmethod
    def __get_points(base_points, count):
        alpha = 1 / count
        return [Knot.__get_point(base_points, i * alpha)
                for i in range(count)]

    def get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = [
                (self.points[i] + self.points[i + 1]) * 0.5,
                self.points[i + 1],
                (self.points[i + 1] + self.points[i + 2]) * 0.5
            ]
            res.extend(self.__get_points(ptn, self.steps))
        return res

    def draw_points(self, display,
                    style="points", width=3, color=(255, 255, 255)):
        if style == "points":
            super(Knot, self).draw_points(
                display, style=style, width=width, color=color)
        elif style == "line":
            knot = self.get_knot()
            for j in range(-1, len(knot)-1):
                pygame.draw.line(
                    display, color,
                    knot[j].int_pair(), knot[j+1].int_pair(),
                    width
                )


class KnotSet(object):

    def __init__(self, n_knots=1, steps=5, velocity=20):
        self.n_knots = n_knots
        self.knots = [Knot(steps=steps) for _ in range(self.n_knots)]
        self.steps = steps
        self.velocity = velocity

    @property
    def steps(self):
        return self.__steps

    @steps.setter
    def steps(self, steps):
        if steps < 1:
            self.__steps = 1
        elif steps > 50:
            self.__steps = 50
        else:
            self.__steps = steps
        for k in self.knots:
            k.steps = self.steps

    def accelerate(self):
        self.velocity = min(100, self.velocity + 1)
        for k in self.knots:
            k.accelerate()

    def decelerate(self):
        self.velocity = max(0, self.velocity - 1)
        for k in self.knots:
            k.decelerate()

    def add_or_delete(self, point):
        if not any(k.delete(point) for k in self.knots):
            for k in self.knots:
                k.add(point)

    def draw_points(self, *args, **kwargs):
        for k in self.knots:
            k.draw_points(*args, **kwargs)

    def set_points(self):
        for k in self.knots:
            k.set_points()

    @property
    def points_count(self):
        return sum(len(k) for k in self.knots)


def draw_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = [
        ["Show Help", "F1"],
        ["Restart", "R"],
        ["Pause/Play", "P"],
        ["Accelerate", "A"],
        ["Decelerate", "D"],
        ["More steps", "Num+"],
        ["Fewer steps", "Num-"],
        ["Delete point", "Click on point"],
        ["Add point", "Click elsewhere"],
        ["", ""],
        ["Current steps", f'{knots.steps}'],
        ["Current speed", f'{knots.velocity}'],
        ["Total points", f'{knots.points_count}']
    ]
    pygame.draw.lines(
        gameDisplay, (255, 50, 50, 255), True,
        [(0, 0), (800, 0), (800, 600), (0, 600)],
        5
    )
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (400, 100 + 30 * i))


if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")
    working = True
    n_knots = 2
    n_steps = 10
    knots = KnotSet(n_knots, n_steps)
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_r:
                    knots = KnotSet(knots.n_knots, knots.steps)
                if event.key == pygame.K_KP_PLUS:
                    knots.steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    knots.steps -= 1
                if event.key == pygame.K_a:
                    knots.accelerate()
                if event.key == pygame.K_d:
                    knots.decelerate()
            if not show_help and event.type == pygame.MOUSEBUTTONDOWN:
                knots.add_or_delete(Vec2d(*event.pos))
        gameDisplay.fill((0, 0, 0))
        if show_help:
            draw_help()
        else:
            hue = (hue + 1) % 360
            color.hsla = (hue, 100, 50, 100)
            knots.draw_points(gameDisplay)
            knots.draw_points(gameDisplay, "line", 3, color)
        if not pause and not show_help:
            knots.set_points()
        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
