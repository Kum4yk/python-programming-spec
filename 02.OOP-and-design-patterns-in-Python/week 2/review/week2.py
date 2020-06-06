import pygame
import random
import math

SCREEN_DIM = (800, 600)


class Vec2d:
    def __init__(self, vector, speed=None):
        self.vector = vector
        self.speed = speed
        
    def __add__(self, other):
        return Vec2d((self.vector[0] + other.vector[0], 
                      self.vector[1] + other.vector[1]))
    
    def __sub__(self, other):
        return Vec2d((self.vector[0] - other.vector[0], 
                      self.vector[1] - other.vector[1]))
    
    def __mul__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.vector[0] * other.vector,
                         self.vector[1] * other.vector)
        else:
            return Vec2d((self.vector[0] * other, 
                          self.vector[1] * other))
        
    def __len__(self):
        return (self.vector[0] ** 2 + self.vector[1] ** 2) ** (1 / 2)
    
    def int_pair(self):
        return int(self.vector[0]), int(self.vector[1])


class Polyline:
    def __init__(self, points=None):
        self.points = points or []
        
    def __add__(self, other):
        self.points.append(other)
        return self
        
    def __len__(self):
        return len(self.points)
    
    def set_points(self):
        for point in self.points:
            point += Vec2d(point.speed)
            if point.vector[0] > SCREEN_DIM[0] or point.vector[0] < 0:
                point.speed = (- point.speed[0], point.speed[1])
            if point.vector[1] > SCREEN_DIM[1] or  point.vector[1] < 0:
                point.speed = (point.speed[0], - point.speed[1])
        
    def draw_points(self, style="points", width=3, color=(255, 255, 255)):
        if style == 'line':
            for point_ind in range(-1, len(self.points) - 1):
                pygame.draw.line(gameDisplay, color, self.points[point_ind].int_pair(),
                                 self.points[point_ind + 1].int_pair(), width)
        elif style == "points":
            for point in self.points:
                pygame.draw.circle(gameDisplay, color, point.int_pair(), width)


class Knot(Polyline):
    def __init__(self, points=None):
        super().__init__(points)
        
    def get_knot(self):
        if len(self) < 3:
            return []
        
        result= []
        for point_index in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[point_index] + self.points[point_index + 1]) * 0.5)
            ptn.append(self.points[point_index + 1])
            ptn.append((self.points[point_index + 1] + self.points[point_index + 2]) * 0.5)
            result.extend(Knot.get_points(ptn, len(self)))
        return result
    
    @staticmethod
    def get_points(base_points, count):
        alpha = 1 / count
        result = []
        for i in range(count):
            result.append(Knot.get_point(base_points, i * alpha))
        return result
    
    @staticmethod
    def get_point(points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        elif deg == 0:
            return points[0]
        return (points[deg] * alpha) + (Knot.get_point(points, alpha, deg - 1) * (1 - alpha))


# Отрисовка справки
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



# Основная программа
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    working = True
    show_help = False
    pause = True
    polyline = Polyline()
    
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
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_F1:
                    show_help = not show_help

            if event.type == pygame.MOUSEBUTTONDOWN:
                v = Vec2d(event.pos, (random.random() * 2, random.random() * 2))
                polyline += v

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        polyline.draw_points()
        knots = Knot(polyline.points)
        Knot(knots.get_knot()).draw_points("line", 3, color)
        if not pause:
            polyline.set_points()
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
