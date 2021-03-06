import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Кдасс для управляения снарядами игрока"""

    def __init__(self, ai_game):
        """Создает объект снаряда в позиции игрока"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Создания снаряда в позиции (0,0) и назначение точной позиции
        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Позиция снаряда
        self.y = float(self.rect.y)

    def update(self):
        """Перемещает снаряд вверх по экрану"""
        # ОБновление позиции снаряда
        self.y -= self.settings.bullet_speed_factor
        # Обновление позиции прямоугольника
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
