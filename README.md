# Masmorra (Projeto Programação 2026.1)

Projeto de Programação I 

## Estrutura

```
rpg_projeto/
│
├── funcoes_jogo.py      # Toda a lógica do jogo (combate, inventário, save...)
├── dados.json           # Valores de monstros, itens, armas, armaduras, poções
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

