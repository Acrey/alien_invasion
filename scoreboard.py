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

    def prep_score(self):
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.screen_color)
        self.score_image_rect = self.score_image.get_rect()
        self.score_image_rect.right = self.screen_rect.right - 20
        self.score_image_rect.top = 20

    def show(self):
        self.screen.blit(self.score_image, self.score_image_rect)
