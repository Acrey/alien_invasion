import pygame.font


class Scoreboard():
    """Класс отвечает за хранение очков."""

    def __init__(self, game):
        self.settings = game.settings
        self.stats = game.stats
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.text_color = (35, 35, 35)
        self.score = self.stats.score
        self.font = pygame.font.SysFont(None, 48)

        self.prep_score()

    def prep_score(self):
        self.score_image = self.font.render(self.score, True, self.text_color, self.settings.screen_color)
        self.score_image_rect = self.score_image.get_rect()
        self.score_image_rect.centerx = self.screen_rect.centerx
        self.score_image_rect.top = self.screen_rect.top

    def show(self):
        self.screen.blit(self.score_image, self.score_image_rect)
