#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math
import time

SCREEN_DIM = (800, 600)


class Vec2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __sub__(self, other):
        """"возвращает разность двух векторов"""
        return Vec2d(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        """возвращает сумму двух векторов"""
        return Vec2d(self.x + other.x, self.y + other.y)

    def __len__(self):
        """возвращает длину вектора"""
        return math.sqrt(self.x * self.x + self.y * self.y)

    def __mul__(self, k):
        """возвращает произведение вектора на число"""
        return Vec2d(self.x * k, self.y * k)

    def int_pair(self, other):
        """возвращает пару координат, определяющих вектор (координаты точки конца вектора),
        координаты начальной точки вектора совпадают с началом системы координат (0, 0)"""
        return other - self


class Polyline:
    def __init__(self):
        self.points = []
        self.speeds = []
        self.steps = 35

        self.hue = 0
        self.color = pygame.Color(0)

    def add_poin(self, p):
        self.points.append(Vec2d(p[0], p[1]))
        self.speeds.append(Vec2d(random.random() * 2, random.random() * 2))

    def delete(self):
        self.points.pop()
        self.speeds.pop()

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return (points[deg]*alpha) + (self.get_point(points, alpha, deg-1) * (1-alpha))

    def get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def set_points(self):
        """функция перерасчета координат опорных точек"""
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p] = Vec2d(- self.speeds[p].x, self.speeds[p].y)
            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p] = Vec2d(self.speeds[p].x, -self.speeds[p].y)

    def draw_points(self, points, style="points", width=3, color=(255, 255, 255)):
        """функция отрисовки точек на экране"""
        if style == "line":
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(gameDisplay, color,
                                 (int(points[p_n].x), int(points[p_n].y)),
                                 (int(points[p_n + 1].x), int(points[p_n + 1].y)), width)

        elif style == "points":
            for p in points:
                pygame.draw.circle(gameDisplay, color, (int(p.x), int(p.y)), width)


class Knot(Polyline):
    def __init__(self):
        self.knots =[]
        super().__init__()

    def add_poin(self, p):
        super().add_poin(p)
        self.knots = self.get_knot()

    def set_points(self):
        super().set_points()
        self.knots = self.get_knot()

    def delete(self):
        super().delete()
        self.knots = self.get_knot()

    def draw(self):
        self.hue = (self.hue + 1) % 360
        self.color.hsla = (self.hue, 100, 50, 100)
        self.draw_points(self.points, "points", 3, (255, 255, 255))
        self.draw_points(self.knots, "line", 3, self.color)

    def get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append(((self.points[i] + self.points[i + 1]) * 0.5))
            ptn.append(self.points[i + 1])
            ptn.append(((self.points[i + 1] + self.points[i + 2]) * 0.5))

            res.extend(self.get_points(ptn, self.steps))
        return res



def draw_help():
    """функция отрисовки экрана справки программы"""
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append([str(knot.steps), "Current points"])
    data.append(["", ""])
    data.append(["D", "Delete last"])
    data.append(["+", "Faster"])
    data.append(["-", "Slower"])
    data.append([str(wait*1000), "Current wait"])

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

    knot = Knot()

    working = True
    show_help = False
    pause = True
    wait = 0.01

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    knot.points = []
                    knot.speeds = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_d:
                    knot.delete()
                if event.key == pygame.K_PLUS:
                    wait += 0.001
                if event.key == pygame.K_MINUS:
                    wait -= 0.001
                    if wait <0:
                        wait =0;
                if event.key == pygame.K_KP_PLUS:
                    knot.steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    knot.steps -= 1 if knot.steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                knot.add_poin(event.pos)

        gameDisplay.fill((0, 0, 0))
        knot.draw()
        if not pause:
            knot.set_points()
        if show_help:
            draw_help()

        pygame.display.flip()
        time.sleep(wait)

    pygame.display.quit()
    pygame.quit()
    exit(0)
