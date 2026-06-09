"""Classe de inimigos e IA simples."""

from .base import Entity


class Enemy(Entity):
    def __init__(self, name, health, strength, defense, evasion):
        super().__init__(name, health, strength, defense, evasion)

    def choose_action(self):
        return "attack"
