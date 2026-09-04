"""
overworld_state.py
Estado de exploracao. Desenha e colide com a sala ativa do RoomManager,
e troca de sala (com fade) quando o player encosta numa porta.
"""

import pygame
from states.base_state import BaseState
from settings import WHITE, TILE_SIZE, STATE_COMBAT
from world.sample_world import build_sample_world

PLAYER_SPEED = 220


class OverworldState(BaseState):
    def enter(self, **kwargs):
        # o mundo so e criado na PRIMEIRA vez que entra nesse estado -
        # assim, voltar do combate nao reseta as salas nem a posicao
        if not hasattr(self, "room_manager"):
            self.room_manager = build_sample_world()

        self.player_size = 24
        spawn = kwargs.get("spawn_pos")
        if spawn is None:
            spawn = (TILE_SIZE * 2, TILE_SIZE * 2)
        self.player_pos = list(spawn)
        self.font = pygame.font.SysFont(None, 22)

    def exit(self):
        pass

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
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
        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        room = self.room_manager.current_room
        half = self.player_size / 2

        # move X e Y separadamente, pra poder "deslizar" na parede em vez
        # de travar totalmente quando bate na diagonal
        new_x = self.player_pos[0] + dx * PLAYER_SPEED * dt
        rect_x = pygame.Rect(0, 0, self.player_size, self.player_size)
        rect_x.center = (new_x, self.player_pos[1])
        if not room.collides(rect_x):
            self.player_pos[0] = new_x

        new_y = self.player_pos[1] + dy * PLAYER_SPEED * dt
        rect_y = pygame.Rect(0, 0, self.player_size, self.player_size)
        rect_y.center = (self.player_pos[0], new_y)
        if not room.collides(rect_y):
            self.player_pos[1] = new_y

        # checa se encostou numa porta - so dispara se nao tiver fade rolando,
        # senao troca de sala varias vezes seguidas por engano
        player_rect = pygame.Rect(0, 0, self.player_size, self.player_size)
        player_rect.center = self.player_pos
        door = room.get_door_at(player_rect)
        if door and not self.game.state_manager.is_transitioning:
            self._go_through_door(door)

    def _go_through_door(self, door):
        def on_black():
            spawn_px = self.room_manager.change_room(door.target_room, door.spawn)
            self.player_pos = list(spawn_px)
        self.game.state_manager.fade_action(on_black)

    def draw(self, screen):
        room = self.room_manager.current_room
        room.draw(screen)

        rect = pygame.Rect(0, 0, self.player_size, self.player_size)
        rect.center = (int(self.player_pos[0]), int(self.player_pos[1]))
        pygame.draw.rect(screen, (60, 200, 90), rect)

        text = self.font.render(
            "Setas/WASD anda | borda amarela = porta pra outra sala | ESPACO simula combate",
            True, WHITE,
        )
        screen.blit(text, (10, 10))
