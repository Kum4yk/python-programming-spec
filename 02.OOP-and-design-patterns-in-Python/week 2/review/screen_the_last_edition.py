import pygame
import random
import math

SCREEN_DIM = (800, 600)

class Vec2d():
    """  2d vector class  """

    def __init__(self,x=0,y=0):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):        
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

    def __add__(self, other):
        #self.x = self.x + other.x
        #self.y = self.y + other.y
        return Vec2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        #self.x = self.x - other.x
        #self.y = self.y - other.y
        return Vec2d(self.x - other.x, self.y - other.y)

    def __mul__(self, num):
        #self.x = self.x * num
        #self.y = self.y * num
        return Vec2d(self.x * num, self.y * num)

    def len(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def int_pair(self):
        return tuple(self.x,self.y)


class Polyline():
    """  Polyline class  """

    def __init__(self):
        self.reset()

    def reset(self):
        self.points=[]
        self.speeds=[]

    def addPoint(self, point,speed):
        self.points.append(point)
        self.speeds.append(speed)

    def set_points(self):
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p].x = - self.speeds[p].x
            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p].y = - self.speeds[p].y

    def draw_points(self, points_to_drow=None, style="points", width=3, color=(255, 255, 255)):
        if points_to_drow==None:
            points_to_drow=self.points
        if style == "line":
            for p_n in range(-1, len(points_to_drow) - 1):
                pygame.draw.line(gameDisplay, color,
                                 (int(points_to_drow[p_n].x), int(points_to_drow[p_n].y)),
                                 (int(points_to_drow[p_n + 1].x), int(points_to_drow[p_n + 1].y)), width)

        elif style == "points":
            for p in self.points:
                pygame.draw.circle(gameDisplay, color,
                                   (int(p.x), int(p.y)), width)
        

class Knot(Polyline):
    """  Knot class  extends Polyline  """

    def __init__(self, steps=35):
        self.steps=steps
        super().__init__()

    def get_point(self, point_list, alpha, deg=None):
        if deg is None:
            deg = len(point_list) - 1
        if deg == 0:
            return point_list[0]
        return point_list[deg] * alpha + self.get_point(point_list,alpha, deg - 1) * (1 - alpha)

    def get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)

            res.extend(self.get_points(ptn, self.steps))
        return res

    def draw_points(self, points_to_drow=None, style="points", width=3, color=(255, 255, 255)):
        if points_to_drow==None:
            super().draw_points(self.get_knot(), style, width, color)
        else:
            super().draw_points(None, style, width, color)


if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    working = True
    show_help = False
    pause = True

    #  List for knots
    knots=[]
    
    my_line=Knot()   
    knots.append(my_line)    # Add first knot to the list

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
                    my_line.reset()
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_a:   # Press A button to set one more knot
                    my_line=Knot()
                    knots.append(my_line)
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                my_line.addPoint(Vec2d(event.pos[0],event.pos[1]),Vec2d(random.random() * 2, random.random() * 2))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)

        #  To draw all knots
        for ln in knots:
            ln.draw_points()
            ln.draw_points(None,"line", 3, color)
            if not pause:
                ln.set_points()

        if show_help:
            pass

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
