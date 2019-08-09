class Carta:
    def __init__(self, valor, naipe, cor, hidden=True):
        self.valor = valor
        self.naipe = naipe
        self.cor = cor
        self.hidden = hidden

    def get_naipe(self):
        return self.naipe

    def get_valor(self):
        return self.valor

    def is_hidden(self):
        return self.hidden

    def change_hidden_state(self):
        self.hidden = not self.hidden

    def make_visible(self):
        self.hidden = False
