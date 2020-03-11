import pygame.font


class Scoreboard():
    """Класс для вывода игровой информации."""

    def __init__(self, game):
        self.settings = game.settings
        self.stats = game.stats
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.text_color = (35, 35, 35)
        self.font = pygame.font.SysFont(None, 48)

        self.prep_score()
        self.prep_high_score()
        self.prep_level()

    def prep_score(self):
        """Форматиурует счет и создает его изображение."""

        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.screen_color)
        self.score_image_rect = self.score_image.get_rect()
        self.score_image_rect.right = self.screen_rect.right - 20
        self.score_image_rect.top = 20

    def prep_high_score(self):
        """Форматиурует лучший счет и создает его изображение."""

        rounded_high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(rounded_high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.screen_color)
        self.high_score_image_rect = self.high_score_image.get_rect()
        self.high_score_image_rect.centerx = self.screen_rect.centerx
        self.high_score_image_rect.top = self.screen_rect.top

    def prep_level(self):
        """Форматиурует уровень и создает его изображение."""

        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.screen_color)
        self.level_image_rect = self.level_image.get_rect()
        self.level_image_rect.right = self.score_image_rect.right
        self.level_image_rect.top = self.score_image_rect.bottom + 10

    def show(self):
        """Выводит статистику на экран."""

        self.screen.blit(self.score_image, self.score_image_rect)
        self.screen.blit(self.high_score_image, self.high_score_image_rect)
        self.screen.blit(self.level_image, self.level_image_rect)

    def check_high_score(self):
        """Проверяет достигнут ли новый лучший счет"""

        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
