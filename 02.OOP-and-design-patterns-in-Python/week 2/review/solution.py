import pygame
import random
import math

SCREEN_DIM = (800, 600)

class Vec2d():
    def __init__(self, coord_x, coord_y):
        self.coord_x = coord_x
        self.coord_y = coord_y
    
    def __sub__(self, obj):
        return Vec2d(self.coord_x - obj.coord_x, self.coord_y - obj.coord_y)

    def __add__(self, obj):
        return Vec2d(self.coord_x + obj.coord_x, self.coord_y + obj.coord_y)

    def __len__(self):
        return int(math.sqrt(self.coord_x * self.coord_x + self.coord_y * self.coord_y))

    def __mul__(self, k):
        return Vec2d(self.coord_x * k, self.coord_y * k)
    
    def int_pair(self):
        return (self.coord_x, self.coord_y)
    

class Polyline():
    def __init__(self):
        self.points=[]
        self.speeds=[]

    def set_points(self):
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p][0] > SCREEN_DIM[0] or self.points[p][0] < 0:
                self.speeds[p] = (- self.speeds[p][0], self.speeds[p][1])
            if self.points[p][1] > SCREEN_DIM[1] or self.points[p][1] < 0:
                self.speeds[p] = (self.speeds[p][0], -self.speeds[p][1])

    def draw_points(self, display, style="points", width=3, color=(255, 255, 255)):
        if style == "line":
            for p_n in range(-1, len(self.points) - 1):
                pygame.draw.line(display, color,
                                self.points[p_n].int_pair(),
                                self.points[p_n + 1].int_pair(), width)
        elif style == "points":
            for p in self.points:
                pygame.draw.circle(display, color,
                                p.int_pair(), width)


class Knot(Polyline):
    knots = []

    def __init__(self, count):
        super().__init__()
        self.count = count
        Knot.knots.append(self)
    
    def add_point(self, point):
        self.points.append(point)
        self.get_knot()

    def get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append(self.points[i] + self.points[i + 1] * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append(self.points[i + 1] + self.points[i + 2] * 0.5)

            res.extend(self.get_points(ptn))
        return res

    def get_points(self, base_points):
        alpha = 1 / self.count
        res = []
        for i in range(self.count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return (points[deg] * alpha) + self.get_point(points, alpha, deg - 1) * (1 - alpha)


def draw_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
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

    knot = Knot(steps)

    working = True
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
                if event.key == pygame.K_r:
                    polyline = Polyline()
                    knot = Knot(steps)
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                event_pos = Vec2d(*event.pos)
                speed = Vec2d(random.random() * 2, random.random() * 2)
                knot.add_point((event_pos, speed))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)

        knot.draw_points(gameDisplay)
        knot.draw_points(gameDisplay, "line", 3, color)
        if not pause:
            knot.set_points()
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)