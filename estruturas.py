import random

class Fila:
    def __init__(self, fila=[]):
        self.fila = fila

    def insert(self, e):
        self.fila.insert(0, e)

    def pop(self):
        if len(self.fila) == 0:
            return None
        return self.fila.pop()



class Pilha:
    def __init__(self, pilha=[]):
        self.pilha = pilha

    def insert(self, e):
        self.pilha.append(e)

    def pop(self):
        if len(self.pilha) == 0:
            return None
        return self.pilha.pop()

    def get_top(self):
        if len(self.pilha) == 0:
            return None
        return self.pilha[-1]
