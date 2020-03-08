class Settings:
    """Класс для хранения всех настроек игры Alien Invasion."""

    def __init__(self):
        """Инициализация настроек игры."""
        # Параметры экрана
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230, 230, 230)

        # Параметры корабля
        self.ship_speed = 1.5
        self.ship_limit = 3

        # Параметры снаряда игрока
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3

        # Параметры пришельца
        self.alien_speed = 1.0
        self.alien_drop_speed = 10
        self.alien_direction = 1
