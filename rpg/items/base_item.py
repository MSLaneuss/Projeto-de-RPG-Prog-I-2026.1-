"""Classe base para itens."""

class BaseItem:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def use(self, target):
        raise NotImplementedError("Use method must be implemented by subclasses")
