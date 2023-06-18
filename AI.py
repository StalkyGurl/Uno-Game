"""
This file contains AI class
"""

from Player import *
from random import choice, randint


class AI(Player):
    def __init__(self):
        super().__init__('')
        self.nick = self.generate_nickname()

    # Function to generate random nickname for AI
    @staticmethod
    def generate_nickname():

        # English

        eng_male_prefixes = ["mister", "master", "funny", "crazy", "lord", "dr", "desperate",
                             "incredible", "cheesy", "sneaky", "king", "stalky"]
        eng_male_names = ["pizza", "doggo", "ghost", "killer", "cousin", "teddy", "potato",
                          "spaghetti", "cheese", "slayer", "dragon", "donut", "icecream", "boy", "boi"]

        eng_female_prefixes = ["lady", "miss", "queen", "cute", "stalky", "little", "annoying", "humble"]
        eng_female_names = ["kitten", "panda", "girl", "gurl", "mom", "grandma", "sister",
                            "granny", "latte", "coffee", "avocado"]

        # Polish

        pl_male_prefixes = ["szybki", "niezawodny", "wielki", "potężny", "zabawny", "anonimowy", "królewski",
                            "fatalny", "męski", "nieśmiertelny", "król", "książę", "doktor", "inżynier",
                            "technik", "hrabia"]
        pl_male_names = ["pies", "chomik", "smok", "misiek", "pepe", "Seba", "Brzęczyszczykiewicz",
                         "Kuba", "wampir", "kanarek", "brat", "ojciec", "syn", "rycerz", "informatyk"]

        pl_female_prefixes = ["piękna", "królowa", "księżniczka", "delikatna", "zabawna", "szalona", "niesamowita",
                              "niezależna", "gadatliwa", "pasywno-agresywna", "nadnaturalna"]
        pl_female_names = ["kapibara", "psiara", "koniara", "kociara", "szynszyla", "Julka", "rywalka",
                           "zawodniczka", "usterka", "dziewczyna", "polonistka", "podżegaczka"]

        # Russian

        rus_male_prefixes = ["Царь", "Князь", "Мастер", "Дядя", "Товарищ", "Отец", "Дед", "Доктор",
                             "Беспонтовый", "Непостижимый", "Важный"]
        rus_male_names = ["Иван", "Григорий", "Василий", "Леонид", "Максим", "Пёс", "Пирожок", "Кекс", "Чёрт"]

        rus_female_prefixes = ["Царица", "Княжна", "Спец", "Тётя", "Мать", "Бабка", "Доктор", "Быстрая",
                               "Могучая", "Скучная"]
        rus_female_names = ["Елена", "Марина", "Фаина", "Зинаида", "Ксения", "Псина", "Булка", "Сковорода",
                            "Фига", "Кость", "Хворь"]

        numbers = "0123456789"
        symbols = "_- "

        language = choice(["eng", "pl", "rus"])
        gender = choice(["male", "female"])

        nick = ''
        if randint(0, 3) < 3:
            if language == "eng" and gender == "male":
                nick += choice(eng_male_prefixes)
            elif language == "eng" and gender == "female":
                nick += choice(eng_female_prefixes)
            elif language == "pl" and gender == "male":
                nick += choice(pl_male_prefixes)
            elif language == "pl" and gender == "female":
                nick += choice(pl_female_prefixes)
            elif language == "rus" and gender == "male":
                nick += choice(rus_male_prefixes)
            elif language == "rus" and gender == "female":
                nick += choice(rus_female_prefixes)
            nick += symbols[randint(0, 2)]

        if language == "eng" and gender == "male":
            nick += choice(eng_male_names)
        elif language == "eng" and gender == "female":
            nick += choice(eng_female_names)
        elif language == "pl" and gender == "male":
            nick += choice(pl_male_names)
        elif language == "pl" and gender == "female":
            nick += choice(pl_female_names)
        elif language == "rus" and gender == "male":
            nick += choice(rus_male_names)
        elif language == "rus" and gender == "female":
            nick += choice(rus_female_names)

        if language != "rus" and len(nick) < 19:
            for _ in range(randint(0, 3)):
                nick += numbers[randint(0, 9)]

        return nick

    # Function to generate random AI move
    def make_ai_move(self, board, gamestate):
        wilds = []
        made_move = False
        if self.has_placeable_card(board):
            for card in self.hand:
                # If the card is wild, save it for later
                if isinstance(card, Cards.SpecialCard) and card.wild:
                    wilds.append(card)
                elif self.check_card(card, board):
                    self.make_move(card, board, gamestate)
                    made_move = True
                    gamestate.log.append("[Log] " + self.nick + " put " + card.translate_card() + " card.")
                    if len(self.hand) == 1:
                        gamestate.log.append(self.nick + ": UNO!")
                    break
            # Use wild card
            if not made_move:
                self.make_move(wilds[0], board, gamestate)
                gamestate.log.append("[Log] " + self.nick + " put " + wilds[0].translate_card() + " card.")
                if len(self.hand) == 1:
                    gamestate.log.append(self.nick + ": UNO!")
        else:
            # Pick a card if there is no card to place
            self.pick_card(board)
            gamestate.log.append("[Log] " + self.nick + " picked a card from a pile.")
            if self.check_card(self.hand[-1], board):
                self.make_move(self.hand[-1], board, gamestate)
                gamestate.log.append("[Log] " + self.nick + " put picked card (" +
                                     board.discard_pile[-1].translate_card() + ")")
                if len(self.hand) == 1:
                    gamestate.log.append(self.nick + ": UNO!")
