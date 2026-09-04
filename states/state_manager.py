"""
state_manager.py
Controla qual estado do jogo esta ativo (Overworld, Combat, Menu...)
e cuida da transicao (fade) tanto entre ESTADOS quanto entre SALAS
dentro do mesmo estado (ex: Overworld trocando de sala).

A logica de fade fica centralizada aqui: escurece a tela, executa uma
acao "as escuras" (troca de estado OU troca de sala, quem chamou decide),
e depois clareia. Quem usa isso (change_state / fade_action) so entrega
um callback; o StateManager nao precisa saber o que tem dentro dele.
"""

import pygame
from settings import WIDTH, HEIGHT, FADE_SPEED, BLACK


class StateManager:
    def __init__(self, game):
        self.game = game
        self.states = {}
        self.current_name = None
        self.current_state = None

        # --- controle da transicao de fade ---
        self._transitioning = False
        self._fade_alpha = 0
        self._fade_direction = 1     # 1 = escurecendo, -1 = clareando
        self._on_black = None        # callback executado no pico do preto

        self._fade_surface = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
        self._fade_surface.fill(BLACK)

    @property
    def is_transitioning(self):
        return self._transitioning

    def add_state(self, name, state_instance):
        self.states[name] = state_instance

    def set_state(self, name, **kwargs):
        """Troca de estado IMEDIATAMENTE, sem fade. So pra iniciar o jogo."""
        if self.current_state:
            self.current_state.exit()
        self.current_name = name
        self.current_state = self.states[name]
        self.current_state.enter(**kwargs)

    def change_state(self, name, **kwargs):
        """Troca de ESTADO (ex: Overworld -> Combat) com fade."""
        def _do_change():
            if self.current_state:
                self.current_state.exit()
            self.current_name = name
            self.current_state = self.states[name]
            self.current_state.enter(**kwargs)

        self._start_fade(_do_change)

    def fade_action(self, callback):
        """Roda uma transicao de fade SEM trocar de estado - usado por ex.
        quando o player muda de sala dentro do proprio Overworld.
        'callback' e chamado no momento em que a tela esta 100% preta."""
        self._start_fade(callback)

    def _start_fade(self, on_black):
        if self._transitioning:
            return  # ja tem uma transicao rolando, ignora pedidos extras
        self._transitioning = True
        self._fade_direction = 1
        self._fade_alpha = 0
        self._on_black = on_black

    def handle_event(self, event):
        # durante a transicao, ignora input do jogo (evita agir "as cegas")
        if not self._transitioning and self.current_state:
            self.current_state.handle_event(event)

    def update(self, dt):
        if self._transitioning:
            self._update_fade()
        elif self.current_state:
            self.current_state.update(dt)

    def _update_fade(self):
        self._fade_alpha += self._fade_direction * FADE_SPEED

        if self._fade_alpha >= 255 and self._fade_direction == 1:
            self._fade_alpha = 255
            if self._on_black:
                self._on_black()
            self._fade_direction = -1  # comeca a clarear

        elif self._fade_alpha <= 0 and self._fade_direction == -1:
            self._fade_alpha = 0
            self._transitioning = False
            self._on_black = None

    def draw(self, screen):
        if self.current_state:
            self.current_state.draw(screen)

        if self._transitioning or self._fade_alpha > 0:
            self._fade_surface.set_alpha(self._fade_alpha)
            screen.blit(self._fade_surface, (0, 0))
