import pygame
from pygame.sprite import  Sprite

class Ship(Sprite):
    """Класс для управления кораблем"""

    def __init__(self, ai_game):
        """инициализирует корабль и задает его начальную позицию"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #Загружает изображение корабля и получает прямоугольник
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        # каждый новый корабль появляется у нижнего края экрана
        self.rect.midbottom = self.screen_rect.midbottom

        # созранение вещественной координаты центра корабля
        self.x = float(self.rect.x)

        # флаг перемещения
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """обнавляет позицию корабля с учетом флага"""
        # обнавляется атрубут x, а не rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed_factor
        elif self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed_factor
        # обновление атрибута rect на основании self.x
        self.rect.x = self.x
    def blitme(self):
        """рисует кораль в текущей позиции"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """ размещает корабль в центре нижней стороны"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
