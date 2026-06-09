"""Armas do jogo."""

from .base_item import BaseItem


class Weapon(BaseItem):
    def __init__(self, name, description, attack_bonus):
        super().__init__(name, description)
        self.attack_bonus = attack_bonus
