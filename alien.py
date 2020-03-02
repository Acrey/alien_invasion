import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
	"""Класс представляющий пришелца"""
	def __init__(self, ai_game):
		super().__init__()
		self.screen = ai_game.screen

		# Загрузка изображения пришельца и назначение rect
		self.image = pygame.image.load('images/alien.bmp')
		self.rect = self.image.get_rect()

		# Начальная позиция пришельца
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		# Точная позиция пришельца
		self.x = float(self.rect.x)