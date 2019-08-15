from carta import Carta
from estruturas import Fila, Pilha
import random
import tabulate
import copy

class Jogo:
    def __init__(self):
        self.draw_pile = self.gera_baralho_embaralhado()
        self.gera_baralho_embaralhado()
        self.tableau = self.gera_tableau()
        self.lista_cartas = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        temp_pilha = Pilha()
        self.build_piles = [["Ouros", copy.deepcopy(temp_pilha)], ["Copas", copy.deepcopy(temp_pilha)], ["Espadas", copy.deepcopy(temp_pilha)], ["Paus", copy.deepcopy(temp_pilha)]]

    def gera_baralho_embaralhado(self):
        baralho = []
        lista_cartas = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        lista_naipes = [("Paus", "p"), ("Ouros", "v"), ("Espadas", "p"), ("Copas", "v")]
        for naipe, cor in lista_naipes:
            for valor in lista_cartas:
                baralho.append(Carta(valor, naipe, cor))

        r = random.SystemRandom()
        r.shuffle(baralho)
        return Fila(baralho)

    def checa_vitoria(self):
        for _, pilha_build in self.build_piles:
            carta_top = pilha_build.get_top()
            if carta_top is None:
                return False
            if carta_top.valor != "K":
                return False
        return True

    def gera_tableau(self):
        tableau = []
        for i in range(1, 8):
            temp_pile = []
            for j in range(i):
                temp_pile.append(self.draw_pile.pop())
            tableau.append(temp_pile)
        for i in tableau:
            i[-1].change_hidden_state()
        return tableau

    def print_game(self):
        print("\n\n")
        print(10*"#"+ " BUILD PILES " + 10*"#")
        for i in self.build_piles:
            naipe = i[0]
            carta = i[1].get_top()
            if carta is not None:
                valor = carta.valor
                naipe = carta.naipe
                cor = carta.cor
                print(naipe + ": " + str((valor, naipe, cor)), end="| ")
            else:
                print(naipe + ": Empty", end="| ")

        print("\n\n")

        print(10 * "#" + " TABLEAU " + 10 * "#")
        temp_list = []
        for i in range(20):
            inside_temp_list = []
            for list_ in self.tableau:
                if len(list_) <= i:
                    inside_temp_list.append(" ")
                else:
                    carta = list_[i]
                    if carta.is_hidden():
                        inside_temp_list.append("Hidden")
                    else:
                        inside_temp_list.append((carta.valor, carta.naipe, carta.cor))
            temp_list.append(copy.copy(inside_temp_list))
        temp_list.insert(0, ["Lista A", "Lista B", "Lista C", "Lista D", "Lista E", "Lista F", "Lista G"])
        print(tabulate.tabulate(temp_list))

    def printa_lista(self, letra_lista):
        dic_index = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6}
        index_lista = dic_index[letra_lista]
        lista_especifica = self.tableau[index_lista]
        valid_indexes = []
        for index, value in enumerate(lista_especifica):
            if not value.is_hidden():
                print(index, "- [" + value.valor, "de", value.naipe, ";", value.cor + "]")
                valid_indexes.append(str(index))
            else:
                print("Hidden")
        return valid_indexes

    def get_last_tableau(self, index):
        dic_index = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6}
        index_lista = dic_index[index]
        if len(self.tableau[index_lista]) == 0:
            return None
        ultima_carta = self.tableau[index_lista].pop()    
        lista_especifica = self.tableau[index_lista]
        if len(lista_especifica) > 0:
            lista_especifica[-1].make_visible()
        return ultima_carta
    
    def compra_carta(self):
        return self.draw_pile.pop()

    def descarta(self, carta):
        carta.change_hidden_state()
        self.draw_pile.insert(carta)

    ###### BUILD PILES ########

    def check_prior_build_piles(self, carta_empilhada, carta_a_empilhar):
        if carta_empilhada is None:
            return carta_a_empilhar.valor == "A"
        index_empilhada = self.lista_cartas.index(carta_empilhada.valor)
        valor_esperado = self.lista_cartas[index_empilhada + 1]
        if valor_esperado != carta_a_empilhar.valor:
            return False
        return True

    def insere_build_piles(self, carta):
        dic_naipe = {"Ouros": 0, "Copas": 1, "Espadas": 2, "Paus": 3}
        naipe = carta.naipe
        build_pile_especifico = self.build_piles[dic_naipe[naipe]][1]
        top = build_pile_especifico.get_top()
        if self.check_prior_build_piles(top, carta):
            build_pile_especifico.insert(carta)
            return True
        else:
            print("Não é possivel inserir esta carta")
            return False

    def get_top_build_piles(self, naipe_index):
        try:
            return self.build_piles[naipe_index][1].get_top()
        except:
            return None

    def get_list_of_cards(self, letra_lista, card_index):
        dic_index = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6}
        index_lista = dic_index[letra_lista]
        lista_especifica = self.tableau[index_lista]
        list_cards = []
        since = False
        for index, value in enumerate(lista_especifica):
            if index == card_index:
                since = True
            if since:
                list_cards.append(value)
        lista_especifica = lista_especifica[:card_index]
        if len(lista_especifica) != 0:
            lista_especifica[-1].make_visible()
        self.tableau[index_lista] = lista_especifica

        return list_cards

    def check_prior_tableau(self, carta_listada, carta_a_listar):
        if carta_listada is None:
            return carta_a_listar.valor == "K"
        if carta_listada.valor == "A":
            return False
        if carta_listada.cor == carta_a_listar.cor:
            return False
        index_empilhada = self.lista_cartas.index(carta_listada.valor)
        valor_esperado = self.lista_cartas[index_empilhada - 1]
        if valor_esperado != carta_a_listar.valor:
            return False
        return True

    def insere_tableau(self, carta, letra_lista):
        letra_lista = letra_lista.upper()
        if letra_lista not in {"A", "B", "C", "D", "E", "F", "G"}:
            print("Letra invalida")
            return False
        dic_index = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6}
        index_lista = dic_index[letra_lista]
        lista_especifica = self.tableau[index_lista]
        if len(lista_especifica) == 0:
            lista_especifica.append(carta)
            return True
        ultimo_valor = lista_especifica[-1]
        if self.check_prior_tableau(ultimo_valor, carta):
            lista_especifica.append(carta)
            return True
        else:
            print("Não é possivel inserir esta carta")
            return False

    def insere_tableau_lista(self, cartas, letra_lista):
        for i in cartas:
            if not self.insere_tableau(i, letra_lista):
                return False
        return True


    def menu(self):
        while True:
            if self.checa_vitoria():
                print("Você ganhou o jogo! Parabens!")
                break
            self.print_game()
            print("\nSelecione um area do Tabuleiro: \n1 - Draw Pile\n2 - Build Pile\n3 - Tableau")
            opt = input("\nComando: ")
            if opt == "1":
                print("\nOpções: \n1 - Comprar")
                inside_opt = input("\nComando: ")
                if inside_opt == "1":
                    carta = self.compra_carta()
                    if carta is not None:
                        carta.change_hidden_state()
                        while True:
                            self.print_game()
                            print("\nVoce comprou a carta: [" + carta.valor, "de", carta.naipe, ";" ,carta.cor + "]")
                            print("\nOpções: \n1 - Descartar\n2 - Colocar no Build Piles\n3 - Colocar no Tableau")
                            inside_opt = input("\nComando: ")
                            if inside_opt == "1":
                                self.descarta(carta)
                                break
                            elif inside_opt == "2":
                                if self.insere_build_piles(carta):
                                    break
                            elif inside_opt == "3":
                                print("\nSelecione uma lista para inserir: (A - G)")
                                letra = input("\nLista: ")
                                if self.insere_tableau(carta, letra):
                                    break
                            else:
                                print("Comando Invalido")
                                continue

                    else:
                        print("Draw Pile vazio")
                else:
                    print("Comando Invalido")
                    continue
            elif opt == "2":
                print("\nOpções: \n1 - Mover Carta")
                inside_opt = input("\nComando: ")
                if inside_opt == "1":
                    print("\nSelecione o naipe: \n0 - Ouros\n1 - Copas\n2 - Espadas\n3 - Paus")
                    naipe = input("\nComando: ")
                    if naipe not in {"0", "1", "2", "3"}:
                        print("naipe_invalido")
                        continue
                    else:
                        carta = self.get_top_build_piles(int(naipe))
                        if carta is not None:
                            while True:
                                print("\nOpções:v\n1 - Colocar no Tableau")
                                inside_opt = input("\nComando: ")
                                if inside_opt == "1":
                                    print("\nSelecione uma lista para mover a carta: (A - G) ")
                                    letra = input("\nLista: ")
                                    if self.insere_tableau(carta, letra):
                                        break
                                else:
                                    print("Comando Invalido")
                                    continue
                        else:
                            print("Não há carta nessa pilha")
                            continue
                else:
                    print("Comando Invalido")
                    continue
            elif opt == "3":
                print("\nSelecione uma lista (A - G):")
                index_list = input("\nLista: ").upper()
                if index_list not in {"A", "B", "C", "D", "E", "F", "G"}:
                    print("Lista invalida")
                else:
                    print("\nOpções: \n1 - Mover carta para Build piles\n2 - Mover cartas para outra lista no Tableau")
                    place = input("\nOpções: ")
                    if place == "1":
                        carta = self.get_last_tableau(index_list)
                        self.insere_build_piles(carta)
                    elif place == "2":
                        while True:
                            valid_indexes = self.printa_lista(index_list)
                            print("\nSelecione a carta inicial da sequencia a ser movida: ")
                            card_index = input("\nCarta: ")
                            if card_index not in valid_indexes:
                                print("index invalido")
                                continue
                            list_cards = self.get_list_of_cards(index_list, int(card_index))
                            while True:
                                print("\nSelecione uma lista (A - G) para mover a sequencia de cartas:\n")
                                index_list = input("\nLista: ").upper()
                                if index_list not in {"A", "B", "C", "D", "E", "F", "G"}:
                                    print("Lista invalida")
                                    continue
                                break
                            self.insere_tableau_lista(list_cards, index_list)
                            break
                    else:
                        print("Comando Invalido")
                        continue
            else:
                print("Comando Invalido")
                continue





















