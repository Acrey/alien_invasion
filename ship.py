import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """Класс для управления кораблем."""

    def __init__(self, ai_game):
        """Инициализирует корабль и задает начальную позицию."""

        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Загружает изображение корабля и получает прямоугольник
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        # Кадлый новый корабль появляется у нижнего края экрана
        self.rect.midbottom = self.screen_rect.midbottom

        # Флаги перемещения корабля
        self.moving_right = False
        self.moving_left = False

        # Позиция
        self.x = float(self.rect.x)

    def blitme(self):
        """Рисует корабль в текущей позиции"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Обновляет позицию корабля"""
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.ship_speed_factor
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed_factor

        self.rect.x = self.x

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
