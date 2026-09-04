"""
overworld_state.py
Estado de exploracao livre. Por enquanto e so uma demo: um quadrado
(o "player") que anda com as setas do teclado por uma sala vazia.

Quando o sistema de salas (world/room.py) estiver pronto, este estado
vai delegar o desenho do mapa/colisao pro RoomManager. Por ora, serve
pra provar que o StateManager e a transicao de fade funcionam.
"""

import pygame
from states.base_state import BaseState
from settings import WIDTH, HEIGHT, DARK_GRAY, GREEN, WHITE, STATE_COMBAT

PLAYER_SPEED = 220  # pixels por segundo


class OverworldState(BaseState):
    def enter(self, **kwargs):
        # posicao inicial do player. Se vier de uma transicao de sala,
        # dava pra usar kwargs.get("spawn_pos", (...)) aqui.
        self.player_pos = list(kwargs.get("spawn_pos", (WIDTH // 2, HEIGHT // 2)))
        self.player_size = 28
        self.font = pygame.font.SysFont(None, 26)

    def exit(self):
        pass

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # demo: aperta espaco pra "encontrar um inimigo" e entrar em combate
            self.game.state_manager.change_state(STATE_COMBAT, enemy_name="Slime")

    def update(self, dt):
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1

        # normaliza diagonal pra nao andar mais rapido na diagonal
        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        self.player_pos[0] += dx * PLAYER_SPEED * dt
        self.player_pos[1] += dy * PLAYER_SPEED * dt

        half = self.player_size / 2
        self.player_pos[0] = max(half, min(WIDTH - half, self.player_pos[0]))
        self.player_pos[1] = max(half, min(HEIGHT - half, self.player_pos[1]))

    def draw(self, screen):
        screen.fill(DARK_GRAY)

        rect = pygame.Rect(0, 0, self.player_size, self.player_size)
        rect.center = (int(self.player_pos[0]), int(self.player_pos[1]))
        pygame.draw.rect(screen, GREEN, rect)

        text = self.font.render(
            "OVERWORLD (demo) - setas/WASD move | ESPACO simula encontro",
            True, WHITE,
        )
        screen.blit(text, (16, 16))
