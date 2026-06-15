# RPG — Masmorra em Python

Projeto de Programação I 

## Estrutura

```
rpg_projeto/
│
├── main.py              # Versão original (terminal simples, sem cores)
├── funcoes_jogo.py      # Toda a lógica do jogo (combate, inventário, save...)
├── dados.json           # Monstros, itens, armas, armaduras, poções
├── main_ui.py           # ★ Versão com interface ASCII
│
└── interface/           # Módulo da interface TUI
    ├── __init__.py
    └── ui.py            # Classe UI — renderização com curses (cores, bordas, barras)
```

## Como executar

```bash
python main_ui.py
```

> Requer terminal com suporte a cores (qualquer terminal moderno no Linux/Mac).
> Tamanho mínimo recomendado: **80 colunas × 24 linhas**.

## Funcionalidades da interface

- Bordas góticas com caracteres Unicode (╔═╗║╚╝)
- Barras de vida coloridas (verde → amarelo → vermelho conforme HP)
- Tela de combate com painel duplo (herói vs inimigo) e log de batalha
- Tela de inventário com status completo
- Tela de menu com arte ASCII
- Tela de game over/vitória
- Efeito de flash para mensagens importantes
