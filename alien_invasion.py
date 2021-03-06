import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button


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

        self.stats = GameStats(self)
        self.stats.high_score = self._read_high_score()
        self.scoreboard = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, 'Play')

    def run_game(self):
        """Запуск основного цикла игры."""

        while True:
            # Отслеживание событий клавиатуры и мыши.
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        """Обрабатывает нажатия клавишь и события в игре"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._exit_game()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _exit_game(self):
        """Сохраняет лучший счет перед закрытием игры."""

        prev_high_score = self._read_high_score()
        if self.stats.high_score > prev_high_score:
            self._write_high_score()

        sys.exit()

    def _read_high_score(self):
        """Считывает лучший счет из файла."""

        try:
            with open('highscore.txt') as f:
                prev_high_score = f.read().strip()
        except FileNotFoundError:
            return 0
        else:
            if not prev_high_score:
                prev_high_score = 0
            return int(prev_high_score)

    def _write_high_score(self):
        """Записывает лучший счет в файл."""

        with open('highscore.txt', 'w') as f:
            f.write(str(self.stats.high_score))

    def _check_keydown_events(self, event):
        """Обрабатывает нажатия клавишь на клавиатуре."""

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self._exit_game()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            self._start_game()

    def _fire_bullet(self):
        """Создание нового снаряла и включение его в группу bullets."""

        if len(self.bullets) < self.settings.bullet_allowed:
            self.bullets.add(Bullet(self))

    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии Play."""

        is_button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if is_button_clicked:
            self._start_game()

    def _start_game(self):
        """Запускает игровой процесс."""

        if not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.scoreboard.prep_images()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            pygame.mouse.set_visible(False)

    def _check_keyup_events(self, event):
        """Обрабатывает отпускание клавишь клавиатуры."""

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_bullets(self):
        """Обновялет позиции снарядов и уничтожает старые."""

        self.bullets.update()
        # Удаления снарядов
        for bullet in self.bullets.copy():
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """
        Проверяет столькновения между снарядами и пришельцами.
        Также создает новый флот при уничтожении старого.
        """

        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()

        if not self.aliens:
            self._start_new_level()

    def _start_new_level(self):
        """Подготавливает сцену для нового уровня."""

        self.bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()
        self.stats.level += 1
        self.scoreboard.prep_level()

    def _update_aliens(self):
        """Обновляет позиции пришельцев."""

        self._check_fleet_edges()
        self.aliens.update()
        # Проверяет коллизии корабль-пришелец
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # Провряет добрались ли пришельцы до нижней части экрана
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Проверяет достижение пришельцем границ экрана."""

        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Опускает флот и меняет его направлени."""

        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.alien_drop_speed
        self.settings.alien_direction *= -1

    def _ship_hit(self):
        """Обрабатывает столкновение корабля с пришельцем."""

        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()

            self.bullets.empty()
            self.aliens.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Проверяет столкновние пришельца с низом экрана."""

        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _create_fleet(self):
        """Создает флот пришельцев."""

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
        """Создание пришельца и размещение его в ряду."""

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien_height * row_number
        self.aliens.add(alien)

    def _update_screen(self):
        """Обновляет экран."""

        # При каждой итерации перерисовывается экран.
        self.screen.fill(self.settings.screen_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        if not self.stats.game_active:
            self.play_button.draw_button()

        self.scoreboard.show()

        # Отобраэение последнего прорисованного экрана.
        pygame.display.flip()


if __name__ == '__main__':
    # Создание экземляра и запуск игры
    ai = AlienInvasion()
    ai.run_game()
