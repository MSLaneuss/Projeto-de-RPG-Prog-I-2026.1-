"""Sistema de combate e turnos."""

from random import randint


def calculate_damage(attacker, defender):
    base = attacker.strength - defender.defense
    return max(1, base + randint(-2, 2))


def attack(attacker, defender):
    if randint(1, 100) <= defender.evasion:
        return 0
    return calculate_damage(attacker, defender)
