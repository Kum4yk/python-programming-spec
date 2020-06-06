#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math

SCREEN_DIM = (800, 600)


# =======================================================================================
# Функции для работы с векторами
# =======================================================================================


class Vec2d:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __add__(self, other):
        if not isinstance(other, Vec2d):
            raise ValueError('Vec2d can only be added to Vec2d')
        return Vec2d(self._x + other._x, self._y + other._y)

    def __sub__(self, other):
        if not isinstance(other, Vec2d):
            raise ValueError('Vec2d can only be subtracted to Vec2d')
        return Vec2d(self._x - other._x, self._y - other._y)

    def __mul__(self, num):
        return Vec2d(self._x * num, self._y * num)

    def __len__(self):
        return math.sqrt(self.x**2 + self.y**2)

    def int_pair(self):
        return int(self.x), int(self.y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


class Polyline:
    def __init__(self):
        self._points = []
        self._speeds = []

    def append(self, other: Vec2d):
        if not isinstance(other, Vec2d):
            ValueError('Only Vec2d objects can be added to polyline')
        self._points.append(other)
        self._speeds.append(Vec2d(random.random() * 2, random.random() * 2))

    def set_points(self):
        for p in range(len(self._points)):
            self._points[p] = self._points[p] + self._speeds[p]
            if self._points[p].x > SCREEN_DIM[0] or self._points[p].x < 0:
                self._speeds[p] = Vec2d(- self._speeds[p].x, self._speeds[p].y)
            if self._points[p].y > SCREEN_DIM[1] or self._points[p].y < 0:
                self._speeds[p] = Vec2d(self._speeds[p].x, -self._speeds[p].y)

    def draw_points(self, display, width=3, color=(255, 255, 255)):
        for p in self._points:
            pygame.draw.circle(display, color,
                               (int(p.x), int(p.y)), width)

    def reset(self):
        self.__init__()


class Knot(Polyline):
    def __init__(self):
        super().__init__()
        self._knots = []

    def get_knot(self, count):
        if len(self._points) < 3:
            self._knots = []
            return
        res = []
        for i in range(-2, len(self._points) - 2):
            ptn = []
            ptn.append((self._points[i] + self._points[i + 1]) * 0.5)
            ptn.append(self._points[i + 1])
            ptn.append((self._points[i + 1] + self._points[i + 2]) * 0.5)

            res.extend(self._get_points(ptn, count))
        self._knots = res

    def draw_points(self, display, width=3, color=(255, 255, 255)):
        super().draw_points(display, width)
        for p_n in range(-1, len(self._knots) - 1):
            pygame.draw.line(display, color, self._knots[p_n].int_pair(),
                             self._knots[p_n+1].int_pair(), width)

    @classmethod
    def _get_points(cls, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(cls._get_point(base_points, i * alpha))
        return res

    @classmethod
    def _get_point(cls, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + cls._get_point(points, alpha, deg - 1) * (1 - alpha)
# =======================================================================================
# Функции отрисовки
# =======================================================================================
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
    data.append(["", ""])
    data.append([str(steps), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))
# =======================================================================================
# Функции, отвечающие за расчет сглаживания ломаной
# =======================================================================================
# =======================================================================================
# Основная программа
# =======================================================================================
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    points = Knot()
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
                    points.reset()
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                points.append(Vec2d(*event.pos))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        points.get_knot(steps)
        points.draw_points(gameDisplay, 3, color)
        if not pause:
            points.set_points()
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
