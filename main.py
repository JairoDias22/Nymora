"""
main.py
Ponto de entrada do jogo. Inicializa o pygame, cria a janela, registra
os estados no StateManager e roda o loop principal.

Rode com: python main.py
"""

import pygame
import sys

from settings import WIDTH, HEIGHT, TITLE, FPS, STATE_OVERWORLD, STATE_COMBAT
from states.state_manager import StateManager
from states.overworld_state import OverworldState
from states.combat_state import CombatState


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # o StateManager precisa de uma referencia pro 'game' pra que
        # os estados consigam chamar self.game.state_manager.change_state(...)
        self.state_manager = StateManager(self)
        self.state_manager.add_state(STATE_OVERWORLD, OverworldState(self))
        self.state_manager.add_state(STATE_COMBAT, CombatState(self))

        # estado inicial, sem transicao
        self.state_manager.set_state(STATE_OVERWORLD)

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # delta time em segundos

            self._handle_events()
            self.state_manager.update(dt)
            self.state_manager.draw(self.screen)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                self.state_manager.handle_event(event)


if __name__ == "__main__":
    Game().run()
