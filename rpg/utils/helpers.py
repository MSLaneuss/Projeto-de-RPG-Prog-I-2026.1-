"""Funções utilitárias e pequenas animações."""

import os
import sys
import time


def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def typewriter(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()
