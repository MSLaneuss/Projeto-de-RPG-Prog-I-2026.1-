"""Classe base para entidades do jogo."""

class Entity:
    def __init__(self, name, health, strength, defense, evasion):
        self.name = name
        self.health = health
        self.strength = strength
        self.defense = defense
        self.evasion = evasion

    def is_alive(self):
        return self.health > 0

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)
