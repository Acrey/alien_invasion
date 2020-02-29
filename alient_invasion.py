import sys

import pygame

from settings import Settings

class AlienInvasion():
	"""Класс для управления ресурсами и поведением игры."""

	def __init__(self):
		"""Инициируем игру и создаем игровые ресурсы."""
		pygame.init()
		self.settings = Settings()

		self.screen = pygame.display.set_mode(
			(self.settings.screen_width, self.settings.screen_height))
		pygame.display.set_caption("Alien Invasion")

	def run_game(self):
		"""Запуск основного цикла игры."""
		while True:
			#Отслеживание событий клавиатуры и мыши.
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

			#Прикаждой итерации перерисовывается экран.
			self.screen.fill(self.settings.bg_color)

			#Отобраэение последнего прорисованного экрана.
			pygame.display.flip()


if __name__ == '__main__':
	#Создание экземляра и запуск игры
	ai = AlienInvasion()
	ai.run_game()