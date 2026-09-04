"""
room.py
Representa uma sala/tela do jogo.

Por enquanto o mapa e definido por uma grade simples de caracteres
(lista de strings) - isso deixa testar o sistema todo sem depender de
assets prontos. Quando os sprites/tiles do Gemini + o Tiled entrarem,
a ideia e trocar SO a forma como 'grid' e gerado (carregar um .tmx com
pytmx em vez do grid hardcoded); o resto - colisao, portas, desenho -
continua igual, porque tudo trabalha em cima de 'self.grid'.

Cada sala ocupa exatamente 1 tela, sem scroll - igual ao Zelda classico
(A Link to the Past / Link's Awakening). Trocar de sala = fade, nao scroll.
"""

import pygame
from settings import TILE_SIZE

# codigo do tile -> se pode andar em cima + cor placeholder (sem asset ainda)
TILE_TYPES = {
    ".": {"walkable": True, "color": (40, 90, 40)},    # grama
    "#": {"walkable": False, "color": (70, 70, 80)},   # parede/obstaculo
    "~": {"walkable": False, "color": (40, 70, 130)},  # agua (bloqueia por enquanto)
}


class Door:
    """Uma porta/saida de sala.
    rect         -> area (em pixels) que ativa a troca ao encostar
    target_room  -> id da sala de destino
    spawn        -> posicao (em TILES, nao pixels) onde o player aparece la
    """
    def __init__(self, rect, target_room, spawn):
        self.rect = rect
        self.target_room = target_room
        self.spawn = spawn


class Room:
    def __init__(self, room_id, grid, doors=None, enemies=None):
        self.room_id = room_id
        self.grid = grid
        self.doors = doors or []
        self.enemies = enemies or []  # reservado pro sistema de combate/spawns

        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows else 0

        # pre-calcula os retangulos de colisao das paredes uma unica vez,
        # em vez de recalcular todo frame dentro do loop do jogo
        self.wall_rects = []
        for y, row in enumerate(grid):
            for x, char in enumerate(row):
                tile = TILE_TYPES.get(char, TILE_TYPES["."])
                if not tile["walkable"]:
                    self.wall_rects.append(
                        pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    )

    def draw(self, screen):
        for y, row in enumerate(self.grid):
            for x, char in enumerate(row):
                tile = TILE_TYPES.get(char, TILE_TYPES["."])
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, tile["color"], rect)

        # desenha as portas em amarelo por cima, so pra visualizar em dev
        for door in self.doors:
            pygame.draw.rect(screen, (230, 200, 60), door.rect, 3)

    def get_door_at(self, entity_rect):
        for door in self.doors:
            if entity_rect.colliderect(door.rect):
                return door
        return None

    def collides(self, rect):
        return any(rect.colliderect(w) for w in self.wall_rects)
