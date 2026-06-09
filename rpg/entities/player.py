"""Classe do jogador."""

from .base import Entity


class Player(Entity):
    def __init__(self, name):
        super().__init__(name, health=100, strength=10, defense=5, evasion=10)
        self.level = 1
        self.experience = 0
        self.inventory = []

    def gain_experience(self, amount):
        self.experience += amount
        if self.experience >= 100:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience -= 100
        self.health += 10
        self.strength += 2
        self.defense += 1
