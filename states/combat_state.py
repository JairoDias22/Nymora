"""
combat_state.py
Estado de combate em turno. Ainda e uma demo simples so pra validar
a transicao vindo do Overworld - o sistema de verdade (fila de turno,
menu de acoes, calculo de dano) vai morar em combat/battle_system.py
e ser encaixado aqui.
"""

import pygame
from states.base_state import BaseState
from settings import WIDTH, HEIGHT, BLACK, RED, WHITE, YELLOW, STATE_OVERWORLD


class CombatState(BaseState):
    def enter(self, **kwargs):
        self.enemy_name = kwargs.get("enemy_name", "Inimigo")
        self.font_big = pygame.font.SysFont(None, 40)
        self.font_small = pygame.font.SysFont(None, 24)

    def exit(self):
        pass

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            # demo: ESC "vence" o combate e volta pro overworld
            self.game.state_manager.change_state(STATE_OVERWORLD)

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill(BLACK)

        title = self.font_big.render(f"COMBATE: {self.enemy_name}", True, RED)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))

        hint = self.font_small.render(
            "(demo) pressione ESC para encerrar o combate e voltar",
            True, YELLOW,
        )
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))
