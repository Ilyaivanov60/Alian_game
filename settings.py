class Settings():
    """Класс для хранения всех настроик игры Alien Invasion"""

    def __init__(self):
        """инициализирует статистические настройки игры"""
        # Параметры экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        # настройки корабля
        self.ship_limit = 3
        # параметры снаряда
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (100, 0, 30)
        self.bullets_allowed = 30
        # настройка пришельцев
        self.fleet_drop_speed = 10
        # темп ускорения игры
        self.speedup_scale = 1.5
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """инициалищирует насройки, изменяющиеся в ходе игры"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3.0
        self.alien_speed_factor = 1.0
        self.alien_points = 50

        # fleet_direction = 1 обозначает движение вправо; а -1 - влево
        self.fleet_direction = 1

    def increase_speed(self):
        """увиличение настройки скорости и стоимость пришельцев"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
