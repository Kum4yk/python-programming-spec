import random

import pygame

SCREEN_DIM = (800, 600)

class Vec2d():
    vec_start = (0,0)
    def __init__(self, pos):
        '''
        :param pos: tuple(int | float(x), int | float(x)), x >=0
        '''
        self.pos = pos

    #Vec2d.__add__ (сумма),
    def __add__(self, other):
        '''
        :param other: Vec2d
        :returns : tuple(int | float, int | float)
        '''
        return Vec2d((self.pos[0] + other.pos[0], self.pos[1] + other.pos[1]))

    # Vec2d.__sub__ (разность),
    def __sub__(self, other):
        '''
        :param other: Vec2d
        :return: tuple(int | float, int | float)
        '''
        return Vec2d((self.pos[0] - other.pos[0], self.pos[1] - other.pos[1]))

    #Vec2d.__mul__
    def __mul__(self, number):
        '''
        :param number: int | float
        :return: tuple(int | float, int | float)
        '''
        return Vec2d((self.pos[0] * number, self.pos[1] * number))

    def __len__(self):

        return (((self.vec_start[0]-self.pos[0])**2 + (self.vec_start[1] - self.pos[1])**2)**0.5)

    def int_pair(self):
        '''
        :return: (int, int)
        '''
        return (int(self.pos[0]), int(self.pos[1]))

class Polyline():
    width = 3
    color = (255, 255, 255)

    def __init__(self):
        self.points = []
        self.speeds = []

    '''с методами отвечающими за добавление в ломаную точки (Vec2d) c её скоростью'''
    def add_point(self, vec2, speed):
        '''
        :param vec2: Vec2d
        :param vec2: (float, float)
        '''
        self.points.append(vec2)
        self.speeds.append(speed)

    def add_speed(self, p):
        '''
        :param p: int
        :return: tuple (int|float, int|float)
        '''

        self.points[p] = self.points[p] + Vec2d(self.speeds[p])

    def get_speed(self, p):
        '''
        :param p: int
        :return: tuple (float, float)
        '''
        return self.speeds[p]

    def set_speed(self, speed, p):
        self.speeds[p] = speed

    def set_points(self):
        """функция перерасчета координат опорных точек"""
        for p in range(len(self.points)):
            self.add_speed(p)
            pos = self.points[p].int_pair()
            curr_speed = self.get_speed(p)
            if pos[0] > SCREEN_DIM[0] or pos[0] < 0:
                self.set_speed((- curr_speed[0], curr_speed[1]), p)
            elif pos[1] > SCREEN_DIM[1] or pos[1] < 0:
                self.set_speed((curr_speed[0], - curr_speed[1]), p)

    def draw_points(self):
        """функция отрисовки точек на экране"""
        for p in self.points:
            pygame.draw.circle(gameDisplay, self.color,
                               (p.int_pair()), self.width)

    def has_this_pos(self, pos, width=3):
        remove = None
        which = None
        for point in self.points:
            if (((point.pos[0] - pos[0]) ** 2 + (point.pos[1] - pos[1]) ** 2) ** 0.5) <= width:
                remove = True
                which = point
                break
        if remove:
            self.points.remove(which)

        return remove

    def increase_speed(self):
        new_speed = []
        for speed in self.speeds:
            new_speed.append((speed[0] + 0.1 * speed[0], speed[1] + 0.1 * speed[1]))
        self.speeds = new_speed


    def decrease_speed(self):
        new_speed = []
        for speed in self.speeds:
            new_speed.append((speed[0] - 0.1 * speed[0], speed[1] - 0.1 * speed[1]))
        self.speeds = new_speed


class Knot(Polyline):
    steps = 0
    ptn = []
    width = 3
    color = (255, 255, 255)
    def __init__(self):
        super(Knot, self).__init__()
        self.knot_points = []
        self.ptn = []
        self.steps = 3

    def get_point(self, alpha, deg=None):
        if deg is None:
            deg = len(self.ptn) - 1
        if deg == 0:
            return self.ptn[0]
        return ((self.ptn[deg] * alpha) + ((self.get_point(alpha, deg - 1) )* (1 - alpha)))

    def get_points(self):
        alpha = 1 / self.steps
        res = []
        for i in range(self.steps):
            res.append(self.get_point(i * alpha))
        return res

    def get_knot(self):
        self.knot_points = []
        length = len(self.points)
        if  length >= 3:
            for i in range(-2, length - 2):
                self.ptn = []
                new_point = (self.points[i] + self.points[i + 1]) * 0.5

                self.ptn.append(new_point)
                self.ptn.append(self.points[i + 1])

                third_point = (self.points[i + 1] + self.points[i + 2]) * 0.5
                self.ptn.append(third_point)
                self.knot_points.extend(self.get_points())


    def draw_points(self):
        super(Knot, self).draw_points()
        for p_n in range(-1, len(self.knot_points) - 1):
            pygame.draw.line(gameDisplay, color,
                         self.knot_points[p_n].int_pair(),
                         self.knot_points[p_n + 1].int_pair(), self.width)

    def draw_help(self):
        """функция отрисовки экрана справки программы"""
        gameDisplay.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        data = []
        data.append(["F1", "Show Help"])
        data.append(["R", "Restart"])
        data.append(["P", "Pause/Play"])
        data.append(["Num+", "More points for current polyline"])
        data.append(["Num-", "Less points for current polyline"])
        data.append(["Space", "Add new polyline"])
        data.append(["Tab", "Switch between polylines"])
        data.append(["-> ", "Increase current line speed"])
        data.append(["<- ", "Decrease current line speed"])
        data.append(["", ""])
        data.append([str(self.steps), "Current points"])

        pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            gameDisplay.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            gameDisplay.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * i))

# =======================================================================================
# Основная программа
# =======================================================================================
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 3
    working = True
    polylines = []
    current_line = 0
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
                    polylines = []
                    current_line = 0
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    polylines[current_line].steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    polylines[current_line].steps -= 1 if polylines[current_line].steps > 1 else 0
                if event.key == pygame.K_TAB:
                    length = len(polylines)
                    if length-1 > current_line:
                        current_line += 1
                    else:
                        current_line = 0
                if event.key == pygame.K_SPACE:
                    current_line += 1
                    polylines.append(Knot())


                if event.key == pygame.K_RIGHT:
                    polylines[current_line].increase_speed()
                if event.key == pygame.K_LEFT:
                    polylines[current_line].decrease_speed()



            if event.type == pygame.MOUSEBUTTONDOWN:
                if len(polylines) == 0:
                    polylines.append(Knot())
                removed_point = None
                remove_line = None
                for polyline in polylines:
                    removed = polyline.has_this_pos(event.pos)
                    if removed:
                        if len(polyline.points) == 0:
                            remove_line = polyline
                        break
                if not removed:
                    polylines[current_line].add_point(Vec2d(event.pos), (random.random() * 2, random.random() * 2))
                if remove_line:
                    print (polylines)
                    polylines.remove(remove_line)
                    if current_line >= len(polylines):
                        current_line -= 1
                    print (polylines)


        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        for polyline in polylines:
            polyline.get_knot()
            polyline.draw_points()
            if not pause:
                polyline.set_points()
            if show_help:
                polyline.draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
