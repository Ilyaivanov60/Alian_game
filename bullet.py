import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """класс для управления снарядами, выпущенными кораблем"""

    def __init__(self, ai_game):
        """создает обект снаряда в текущей позиции корабля"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # создаание снаряда в позиции (0,0) и назначение правильной позиции
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        # позиция снаряда хранится в вещественном формате
        self.y = float(self.rect.y)

    def update(self):
        """перемещение снаряда вверх по экрану"""
        # обновленние позиции снаряда в вещественном формате
        self.y -= self.settings.bullet_speed_factor
        # обновлениепозиции треугольника
        self.rect.y = self.y

    def draw_bullet(self):
        """вывод снаряда на экран"""
        pygame.draw.rect(self.screen, self.color, self.rect)
