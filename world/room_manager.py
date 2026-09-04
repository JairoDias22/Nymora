"""
room_manager.py
Guarda todas as salas do mundo e controla qual esta ativa no momento.

Fica separado do StateManager de proposito: o StateManager troca entre
"telas grandes" do jogo (Overworld / Combate / Menu). O RoomManager
troca entre salas DENTRO do Overworld. Sao dois niveis de navegacao
diferentes, cada um com sua responsabilidade.
"""

from world.room import Room
from settings import TILE_SIZE


class RoomManager:
    def __init__(self):
        self.rooms = {}
        self.current_room_id = None

    def add_room(self, room_id, grid, doors=None, enemies=None):
        self.rooms[room_id] = Room(room_id, grid, doors, enemies)

    @property
    def current_room(self):
        return self.rooms.get(self.current_room_id)

    def change_room(self, room_id, spawn_tile=None):
        """Troca a sala ativa. 'spawn_tile' e em coordenadas de TILE
        (nao pixel). Retorna a posicao em pixels pro OverworldState
        reposicionar o player."""
        self.current_room_id = room_id
        if spawn_tile is None:
            spawn_tile = (2, 2)
        return (spawn_tile[0] * TILE_SIZE + TILE_SIZE // 2,
                spawn_tile[1] * TILE_SIZE + TILE_SIZE // 2)
