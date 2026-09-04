"""
settings.py
Constantes globais do jogo. Centralizar aqui evita "numeros magicos"
espalhados pelo codigo e facilita ajustar o jogo depois.
"""

# --- Janela ---
WIDTH = 800
HEIGHT = 600
FPS = 60
TITLE = "Projeto Zelda-like (Turn-Based)"

# --- Tiles ---
TILE_SIZE = 32

# --- Cores (RGB) ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (30, 30, 30)
RED = (200, 60, 60)
GREEN = (60, 180, 90)
BLUE = (60, 100, 200)
YELLOW = (230, 200, 60)

# --- Nomes dos estados (usados pelo StateManager) ---
STATE_OVERWORLD = "overworld"
STATE_COMBAT = "combat"
STATE_MENU = "menu"

# --- Transicao (fade) ---
FADE_SPEED = 12  # quanto o alpha muda por frame (maior = fade mais rapido)
