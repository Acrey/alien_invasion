import sys

import pygame

from settings import Settings
from ship import Ship

class AlienInvasion():
	"""Класс для управления ресурсами и поведением игры."""

	def __init__(self):
		"""Инициируем игру и создаем игровые ресурсы."""
		pygame.init()
		self.settings = Settings()

		self.screen = pygame.display.set_mode(
			(self.settings.screen_width, self.settings.screen_height))
		pygame.display.set_caption("Alien Invasion")

		self.ship = Ship(self)

	def run_game(self):
		"""Запуск основного цикла игры."""
		while True:
			#Отслеживание событий клавиатуры и мыши.
			self._check_events()
			self._update_screen()
			

	def _check_events(self):
		"""Обрабатывает нажатия клавишь и события в игре"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

	def _update_screen(self):
		#Прикаждой итерации перерисовывается экран.
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()

		#Отобраэение последнего прорисованного экрана.
		pygame.display.flip()


if __name__ == '__main__':
	#Создание экземляра и запуск игры
	ai = AlienInvasion()
	ai.run_game()