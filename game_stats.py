class GameStats():
    """отслеживание статистики для игры Alien Invasion"""

    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        # игра зупускается в не активном состоянии
        self.game_active = False
        # рекорд не дожен сбрасываться
        self.high_score = 0
        self.level = 1

    def reset_stats(self):
        """инициализирует статистику, изменения в ходе игры"""
        self.ship_left = self.settings.ship_limit
        self.score = 0