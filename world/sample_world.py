"""
sample_world.py
Monta um mundo de exemplo com 2 salas conectadas por portas, so pra
validar o RoomManager + a colisao + a transicao entre salas de ponta
a ponta. Substitua isso pelos mapas de verdade (Tiled/.tmx via pytmx)
quando os assets do Gemini estiverem prontos - o RoomManager e a Room
nao precisam mudar, so a forma como o grid e construido aqui.
"""

import pygame
from world.room_manager import RoomManager
from world.room import Door
from settings import TILE_SIZE, WIDTH, HEIGHT

COLS = WIDTH // TILE_SIZE
ROWS = HEIGHT // TILE_SIZE


def build_sample_world():
    rm = RoomManager()
    mid = ROWS // 2

    # ---------- sala 1 ----------
    grid1 = []
    for y in range(ROWS):
        row = ""
        for x in range(COLS):
            is_border = x == 0 or x == COLS - 1 or y == 0 or y == ROWS - 1
            is_door_gap = x == COLS - 1 and mid - 1 <= y <= mid + 1
            if is_border and not is_door_gap:
                row += "#"
            else:
                row += "."
        grid1.append(row)

    door_1_to_2 = Door(
        rect=pygame.Rect((COLS - 1) * TILE_SIZE, (mid - 1) * TILE_SIZE, TILE_SIZE, TILE_SIZE * 3),
        target_room="room_2",
        spawn=(2, mid),
    )
    rm.add_room("room_1", grid1, doors=[door_1_to_2])

    # ---------- sala 2 ----------
    grid2 = []
    for y in range(ROWS):
        row = ""
        for x in range(COLS):
            is_border = x == 0 or x == COLS - 1 or y == 0 or y == ROWS - 1
            is_door_gap = x == 0 and mid - 1 <= y <= mid + 1
            if is_border and not is_door_gap:
                row += "#"
            elif (x, y) in {(9, 6), (10, 6), (9, 7), (10, 7)}:
                row += "~"  # um laguinho de enfeite, so pra mostrar outro tile
            else:
                row += "."
        grid2.append(row)

    door_2_to_1 = Door(
        rect=pygame.Rect(0, (mid - 1) * TILE_SIZE, TILE_SIZE, TILE_SIZE * 3),
        target_room="room_1",
        spawn=(COLS - 3, mid),
    )
    rm.add_room("room_2", grid2, doors=[door_2_to_1])

    rm.current_room_id = "room_1"
    return rm
