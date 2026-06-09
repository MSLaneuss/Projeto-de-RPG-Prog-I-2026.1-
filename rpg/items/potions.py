"""Poções e consumíveis."""

from .base_item import BaseItem


class Potion(BaseItem):
    def __init__(self, name, description, heal_amount=0, mana_amount=0):
        super().__init__(name, description)
        self.heal_amount = heal_amount
        self.mana_amount = mana_amount

    def use(self, target):
        if self.heal_amount:
            target.health += self.heal_amount
        if self.mana_amount and hasattr(target, "mana"):
            target.mana += self.mana_amount
