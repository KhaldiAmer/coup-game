import random
from time import sleep
from views import PlayerView


class Player:
    def __init__(self, name, is_ai, cards=None):
        self.name = name
        self.is_ai = is_ai
        self.coins = 2
        self.cards = cards if cards is not None else []
        self.revealed = []
        self.view = PlayerView()

    def reveal_card(self):
        if self.is_eliminated:
            raise Exception("Player has no more cards to reveal and is already eliminated.")

        # Choose a card to reveal
        card_index = 0
        if self.is_ai:
            self.view.print_ai_thinking_reveal(self)
            sleep(1)
            card_index = random.choice([0, 1]) if len(self.cards) > 1 else 0
        elif len(self.cards) > 1:
            card_index = self.view.get_card_to_reveal(self)

        revealed_card = self.cards.pop(card_index)
        self.revealed.append(revealed_card)
        self.view.display_player_revealed_card(self.name, revealed_card)

        # Check if the player is eliminated
        self.check_elimination()

    def check_elimination(self):
        if self.is_eliminated:
            self.view.display_player_eliminated(self.name)

    @property
    def is_eliminated(self):
        return len(self.cards) == 0
