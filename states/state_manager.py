"""
state_manager.py
Controla qual estado do jogo esta ativo (Overworld, Combat, Menu...)
e cuida da transicao (fade) entre eles.

A ideia: em vez de criar um "TransitionState" separado que os outros
estados precisam conhecer, a transicao fica embutida aqui dentro.
Assim, OverworldState e CombatState nao sabem (e nao precisam saber)
que existe uma animacao de fade rolando - eles so pedem
'troca pro estado X' e o StateManager cuida do resto.
"""

import pygame
from settings import WIDTH, HEIGHT, FADE_SPEED, BLACK


class StateManager:
    def __init__(self, game):
        self.game = game
        self.states = {}          # nome -> instancia do estado (BaseState)
        self.current_name = None
        self.current_state = None

        # --- controle da transicao de fade ---
        self._transitioning = False
        self._fade_alpha = 0
        self._fade_direction = 1     # 1 = escurecendo, -1 = clareando
        self._pending_state = None   # nome do estado pra onde vamos
        self._pending_kwargs = {}

        # superficie preta usada na transicao (com canal alpha)
        self._fade_surface = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
        self._fade_surface.fill(BLACK)

    def add_state(self, name, state_instance):
        """Registra um estado (ex: 'overworld' -> OverworldState(...))."""
        self.states[name] = state_instance

    def set_state(self, name, **kwargs):
        """Troca de estado IMEDIATAMENTE, sem transicao.
        Util so pra iniciar o jogo no primeiro estado."""
        if self.current_state:
            self.current_state.exit()
        self.current_name = name
        self.current_state = self.states[name]
        self.current_state.enter(**kwargs)

    def change_state(self, name, **kwargs):
        """Pede uma troca de estado COM transicao de fade.
        E o metodo que o Overworld/Combat devem chamar
        (ex: self.game.state_manager.change_state('combat', enemy='slime'))."""
        if self._transitioning:
            return  # ja tem uma transicao rolando, ignora pedidos extras
        self._transitioning = True
        self._fade_direction = 1
        self._fade_alpha = 0
        self._pending_state = name
        self._pending_kwargs = kwargs

    def handle_event(self, event):
        # durante a transicao, ignoramos input do jogo (evita o jogador
        # agir "as cegas" enquanto a tela esta preta)
        if not self._transitioning and self.current_state:
            self.current_state.handle_event(event)

    def update(self, dt):
        if self._transitioning:
            self._update_fade()
        elif self.current_state:
            self.current_state.update(dt)

    def _update_fade(self):
        self._fade_alpha += self._fade_direction * FADE_SPEED

        # tela ficou totalmente preta -> e o momento de trocar o estado
        # de verdade, por baixo do preto, sem o jogador ver a troca
        if self._fade_alpha >= 255 and self._fade_direction == 1:
            self._fade_alpha = 255
            if self.current_state:
                self.current_state.exit()
            self.current_name = self._pending_state
            self.current_state = self.states[self._pending_state]
            self.current_state.enter(**self._pending_kwargs)
            self._fade_direction = -1  # comeca a clarear

        # terminou de clarear -> transicao acabou
        elif self._fade_alpha <= 0 and self._fade_direction == -1:
            self._fade_alpha = 0
            self._transitioning = False

    def draw(self, screen):
        if self.current_state:
            self.current_state.draw(screen)

        # desenha o overlay preto por cima, com a transparencia atual
        if self._transitioning or self._fade_alpha > 0:
            self._fade_surface.set_alpha(self._fade_alpha)
            screen.blit(self._fade_surface, (0, 0))
