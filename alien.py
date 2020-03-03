import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
	"""Класс представляющий пришелца"""
	def __init__(self, ai_game):
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings

		# Загрузка изображения пришельца и назначение rect
		self.image = pygame.image.load('images/alien.bmp')
		self.rect = self.image.get_rect()

		# Начальная позиция пришельца
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		# Точная позиция пришельца
		self.x = float(self.rect.x)

	def update(self):
		self.x += self.settings.alien_speed * self.settings.alien_direction
		self.rect.x = self.x

	def check_edges(self):
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right or self.rect.x <= 0:
			return True