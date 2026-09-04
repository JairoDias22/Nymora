"""
base_state.py
Classe base para todos os estados do jogo (Overworld, Combat, Menu, etc).

Cada estado novo deve herdar de BaseState e sobrescrever os metodos
que fizerem sentido. Isso mantem o StateManager generico: ele nao
precisa saber o que cada estado faz, so precisa chamar esses metodos.
"""


class BaseState:
    def __init__(self, game):
        # 'game' e a referencia pro objeto principal do jogo,
        # assim qualquer estado consegue acessar o StateManager,
        # a tela (screen), o clock, etc.
        self.game = game

    def enter(self, **kwargs):
        """Chamado toda vez que o StateManager troca PARA este estado.
        kwargs serve pra passar dados entre estados (ex: qual sala carregar,
        contra qual inimigo lutar)."""
        pass

    def exit(self):
        """Chamado toda vez que o StateManager sai deste estado."""
        pass

    def handle_event(self, event):
        """Trata um evento do pygame (teclado, mouse, etc)."""
        pass

    def update(self, dt):
        """Atualiza a logica do estado. dt = delta time em segundos."""
        pass

    def draw(self, screen):
        """Desenha o estado na tela."""
        pass
