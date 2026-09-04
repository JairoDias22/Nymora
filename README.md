# Nymora

Um RPG de exploração em 2D, inspirado nos Zelda clássicos (*A Link to the Past*, *Link's Awakening*), mas com uma virada: em vez de combate em tempo real, os encontros são resolvidos em **batalhas por turno**.

## Sobre o jogo

Nymora propõe misturar duas sensações que normalmente não andam juntas: a liberdade de explorar um mundo dividido em salas conectadas — encontrando caminhos, itens e segredos no seu próprio ritmo — com a tensão estratégica de um combate por turno, onde cada decisão (atacar, usar item, fugir) importa.

A ideia não é ser "mais um clone de Zelda", e sim pegar o que faz a exploração desses jogos ser gostosa (mundo conectado, descoberta, progressão através de itens) e substituir a ação em tempo real por um sistema de combate mais pausado e estratégico, no estilo de RPGs clássicos como Chrono Trigger e EarthBound.

## Gameplay

- **Exploração:** o mundo é dividido em salas/telas conectadas por portas — sem mundo aberto contínuo, sem scroll suave. Ao atravessar uma porta, a tela some em fade e reaparece já na sala seguinte, no estilo dos Zelda 2D clássicos.
- **Combate:** ao encontrar um inimigo, a ação entra em modo turno. Jogador e inimigos se revezam executando ações (atacar, usar item, fugir), sem pressão de tempo real.
- **Progressão:** a exploração é a espinha dorsal do jogo — novos caminhos e áreas se abrem conforme o jogador avança (itens, habilidades, chaves), no espírito metroidvania.

## Estado atual do projeto

🚧 **Em desenvolvimento inicial (protótipo/base técnica).** O que já está implementado:

- [x] Máquina de estados do jogo (Overworld / Combate / Menu)
- [x] Transição em fade entre estados e entre salas
- [x] Sistema de salas com colisão (paredes) e portas conectando áreas
- [x] Movimentação do personagem pelo mundo
- [x] Tela de combate (placeholder, ainda sem lógica de batalha)

O que ainda **não** existe:

- [ ] Sistema de combate em turno funcional (ações, dano, fila de turno)
- [ ] Sprites e tiles definitivos (o visual atual é só placeholder em cores sólidas)
- [ ] Mapas de verdade feitos no Tiled (as salas atuais são geradas por código, só pra teste)
- [ ] Itens, inventário e progressão
- [ ] Inimigos com IA e sistema de encontros
- [ ] Sistema de save/load

## Tecnologias

- **Python 3** + **Pygame** para o motor do jogo
- **Tiled** + **pytmx** (planejado) para os mapas
- Assets visuais gerados com apoio de IA (Gemini) e desenvolvimento assistido por IA (Claude)

## Como rodar

```bash
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install pygame
python main.py
```

**Controles (versão atual):**
- Setas / WASD — mover
- Encostar na borda amarela de uma sala — trocar de sala
- ESPAÇO — simular um encontro de combate (demo)
- ESC (dentro do combate) — voltar para a exploração (demo)
