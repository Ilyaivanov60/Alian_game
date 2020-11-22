import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """Класс для управления ресурсами и поведением игры"""

    def __init__(self):
        """инициализирует игру и создает игровые ресурсы"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((
            self.settings.screen_width, self.settings.screen_height
        ))
        pygame.display.set_caption("Alien Invasion")

        # создание экземпляра для зранения игровой статистики
        # и панели результатов
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # создание кнопки Play
        self.play_button = Button(self, "Play")

    def run_game(self):
        """запуск основного цикла игры"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """обработка нажатия клавиш и события мыши"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """запускает новую игру при нажатии кнопки Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # сброс игровых настроек
            self.settings.initialize_dynamic_settings()
            # сброс игровой статистики
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()

            # очистака списков пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()

            #создание нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()

            # указатель мыши скрывается
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """реагирует на нажатие клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """реагиркет на отпускание клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """создание нового снаряда и включение его в  группу bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """обновляет позиции снарядов и уничтожает старые снаряды"""
        # обновление позиции снаряда
        self.bullets.update()

        # удаление снарядов, вышедших за пределы экрана
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_allien_collisions()

    def _check_bullet_allien_collisions(self):
        """
        проверка попадания в пришельца
        при обнаружении попадания удалить снаряд и пришельца
        """
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        elif not self.aliens:
            # уничтожение существующих снарядов и создание нового фтлота
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # увиличение уровня
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """проверяет, достиг ли фтот края экрана,
        с последующим обновление позиции всез пришельце во фтоте"""
        self._check_fleet_edges()
        self.aliens.update()
        # проверка колизий пришелец корабль
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # проверить, добрались ли пришельцы до нижнего края экрана
        self._check_aliens_bottom()

    def _ship_hit(self):
        """обрабатывает сталкновение коробля с пришельцами"""
        if self.stats.ship_left > 0:
            # уменьшает ship_left
            self.stats.ship_left -= 1

            # очистка спосок пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()

            # создагие нового флота и размищение корабля в центре
            self._create_fleet()
            self.ship.center_ship()

            # пауза
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """ проверяет, добрались ли пришельцы до нижнего края экрана"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # происзодит то де, что при столкнавении с коробкой
                self._ship_hit()
                break

    def _create_fleet(self):
        """создание флота вторжения """
        # создание пришельца и вычисление количества пришельцев в ряду
        # интервали между соседними пришельцами равн ширине пришельца
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        """опредиление коллчиства рядов, помещающихся на экране"""
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height)
                             - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        # создание превого ряда пришельцев
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """создание пришльца и размищение его в ряду"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """реагирует на достижение пришельцем края экрана"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """опускает весь флот и меняет направление"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """обновляет изображение на экране и отбражает новый экран"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        #выводит информацию о счете
        self.sb.show_score()
        # кнопка play отабражается в том случае, если игра не активна
        if not self.stats.game_active:
            self.play_button.draw_button()

        """отабражение последнего запуска игры"""
        pygame.display.flip()


if __name__ == '__main__':
    # создание экземпляра и запуск игры
    ai = AlienInvasion()
    ai.run_game()
