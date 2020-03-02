import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion():
    """Класс для управления ресурсами и поведением игры."""

    def __init__(self):
        """Инициируем игру и создаем игровые ресурсы."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            # Отслеживание событий клавиатуры и мыши.
            self._check_events()
            self.ship.update()
            self._update_bullets()            
            self._update_screen()

    def _check_events(self):
        """Обрабатывает нажатия клавишь и события в игре"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Создание нового снаряла и включение его в группу bullets."""
        if len(self.bullets) < self.settings.bullet_allowed:
            self.bullets.add(Bullet(self))

    def _update_bullets(self):
        """Обновялет позиции снарядов и уничтожает старые."""
        self.bullets.update()
        # Удаления снарядов
        for bullet in self.bullets.copy():
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)

    def _create_fleet(self):
        """Создает флот пришельцев"""
        alien = Alien(self)

        alien_width, alien_height = alien.rect.size
        # Определяет колличество пришельцев в ряду
        availabel_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = availabel_space_x // (2 * alien_width)

        # Определяет колличество рядов пришельцев
        ship_height = self.ship.rect.height
        availabel_space_y = (self.settings.screen_height - 
            (3 * alien_height) - ship_height)
        number_rows = availabel_space_y // (2 * alien_height)

        # Создание флота
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Создание пришельца и размещение его в ряду"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien_height * row_number
        self.aliens.add(alien)

    def _update_screen(self):
        # При каждой итерации перерисовывается экран.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Отобраэение последнего прорисованного экрана.
        pygame.display.flip()


if __name__ == '__main__':
    # Создание экземляра и запуск игры
    ai = AlienInvasion()
    ai.run_game()
