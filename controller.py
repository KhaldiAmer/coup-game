import random
from time import sleep
from view import GameView, PlayerView

# Characters
CHARACTERS = ["duke", "assassin", "captain", "ambassador", "contessa"]

# Rules config for each action
COUP_RULES_CONFIG = {
    "tax": {
        "performed_by": "duke",
        "income": 3,
        "cost": 0,
        "blocked_by": [],
        "can_be_challenged": True
    },
    "steal": {
        "performed_by": "captain",
        "amount": 2,
        "cost": 0,
        "income": 0,
        "blocked_by": ["captain", "ambassador"],
        "can_be_challenged": True
    },
    "assassinate": {
        "performed_by": "assassin",
        "cost": 3,
        "income": 0,
        "blocked_by": ["contessa"],
        "can_be_challenged": True
    },
    "exchange": {
        "performed_by": "ambassador",
        "income": 0,
        "cost": 0,
        "blocked_by": [],  # Exchange cannot be blocked
        "can_be_challenged": True
    },
    "foreign_aid": {
        "performed_by": None,
        "income": 2,
        "cost": 0,
        "blocked_by": ["duke"],
        "can_be_challenged": False
    },
    "income": {
        "performed_by": None,
        "income": 1,
        "cost": 0,
        "blocked_by": [],  # Income cannot be blocked
        "can_be_challenged": False
    },
    "coup": {
        "performed_by": None,
        "income": 0,
        "cost": 7,  # The cost to perform a coup
        "blocked_by": [],  # Coup cannot be blocked
        "can_be_challenged": False
    }
}
MAX_COINS_FOR_COUP = 10
MIN_PLAYERS = 2
MAX_PLAYERS = 6


class Player:
    def __init__(self, name, is_ai, cards=None):
        self.name = name
        self.is_ai = is_ai
        self.coins = 2
        self.cards = cards if cards is not None else []
        self.revealed = []
        self.view = PlayerView()

    def reveal_card(self):
        if len(self.cards) == 0:
            raise Exception(
                "Player has no more cards to reveal. and is already eliminated."
            )

        if len(self.cards) == 1:
            self.view.display_player_revealed_card(self.name, self.cards[0])
            self.revealed.extend([self.cards.pop()])
            # Check if the player is eliminated
            self.check_elimination()
            return

        if self.is_ai:
            sleep(1)
            # AI logic to choose a random card to reveal
            card_index = random.choice([0, 1])
        else:
            card_index = self.view.get_card_to_reveal(self)

        self.view.display_player_revealed_card(self.name, self.cards[card_index])
        self.revealed.extend([self.cards.pop(card_index)])

        # Check if the player is eliminated
        self.check_elimination()

    def check_elimination(self):
        if len(self.cards) == 0:
            self.view.display_player_eliminated(self.name)

    @property
    def is_eliminated(self):
        return len(self.cards) == 0


class GameController:
    def __init__(self, number_of_players=3):
        # Validation
        if number_of_players < 2 or number_of_players > 6:
            raise ValueError("Number of players must be between 2 and 6")

        # Setup the deck
        self.deck = CHARACTERS * 3
        self.reshuffle_deck()

        # Setup the players
        self.players = [Player("Human", False, self.deck[:2])]
        self.deck = self.deck[2:]  # Remove the cards taken by the human player
        for i in range(1, number_of_players):
            self.players.append(Player(f"AI {i}", True, self.deck[:2]))
            self.deck = self.deck[2:]  # Remove the cards taken by AI players

        # Set the current player to the first player
        self.current_player_index = 0
        self.actions = COUP_RULES_CONFIG.keys()

        # Setup the view, we could pass the view as a parameter to the constructor
        self.view = GameView()

    @property
    def current_player(self):
        return self.players[self.current_player_index]

    @property
    def blockable_actions(self):
        # loop through COUP_RULES_CONFIG and return a list of actions that can be blocked
        blockable_actions = []
        for action in self.actions:
            if COUP_RULES_CONFIG[action]["blocked_by"]:
                blockable_actions.append(action)
        return blockable_actions

    # Deck methods
    def reshuffle_deck(self, cards=[]):
        # Put the cards back to the deck and shuffle
        self.deck.extend(cards)
        random.shuffle(self.deck)

    def take_card_from_deck(self):
        # Take a card from the deck
        if len(self.deck) == 0:
            self.view.print_error("Not enough cards in the deck.")
            raise Exception("Not enough cards in the deck.")
        card = self.deck.pop()
        self.reshuffle_deck()
        return card

    # Game methods
    def choose_action(self):
        """
        Choose an action and target for the current player.
        Return a tuple of (action, target).
        """
        current_player = self.current_player
        target = None
        if current_player.is_ai:
            sleep(1)
            # AI logic to choose an action
            player_options = self.player_available_actions(
                current_player
            )
            action = random.choice(player_options)
        else:
            player_options = self.player_available_actions(
                current_player
            )
            action = self.view.get_player_action(
                current_player,
                player_options
            )
        if action in ["assassinate", "steal", "coup"]:
            possible_targets = self.get_other_players(
                current_player
            )
            if current_player.is_ai:
                target = random.choice(possible_targets)
            else:
                target = self.view.get_player_target(
                    possible_targets,
                    current_player
                )
        else:
            target = None
        return action, target

    def challenge_or_block(self, action: str, current_player: Player, target: Player = None):
        """
        Loop through the players and ask them if they want to challenge or block.
        If a player decides to challenge or block, call the corresponding method and return the result.
        """
        can_be_challenged = COUP_RULES_CONFIG[action].get("can_be_challenged", False)
        can_be_blocked = COUP_RULES_CONFIG[action].get("blocked_by", [])

        players_to_ask = self.get_other_players(current_player)

        for player in players_to_ask:
            is_target = player == target
            if player != current_player:
                # Handle challenge
                if can_be_challenged and self.ask_challenge(player, current_player, action, target):
                    challenge_successful = self.handle_challenge(player, current_player, action)
                    return not challenge_successful

                # Handle block
                if is_target and can_be_blocked and self.ask_block(player, action, target):
                    block_successful = self.handle_block(player, action, target)
                    return not block_successful

        # No challenge or block occurred
        return True

    def ask_challenge(self, player, current_player, action, target):
        if player.is_ai:
            return self.ai_decide_to_challenge(player, current_player, action)
        else:
            return self.view.get_challenge_decision(player, current_player, action, target)

    def ask_block(self, player, action, target):
        if player.is_ai:
            return self.ai_decide_to_block(player, action)
        else:
            return self.view.get_block_decision(player, action, target)

    def handle_challenge(self, challenger: Player, challenged: Player, action: str):
        """
        return True if the challenge succeeds, False otherwise.
        """
        claimed_card = COUP_RULES_CONFIG[action]["performed_by"]

        # Check if the challenged player has the claimed card
        if claimed_card in challenged.cards:
            # Challenge fails; challenger loses an influence
            self.view.challenge_failed(challenger, challenged, claimed_card)
            self.resolve_influence_loss(challenger)
            # Reshuffle and replace the challenged player's card
            self.replace_player_card(challenged, claimed_card)
            return False
        else:
            # Challenge succeeds; challenged player loses an influence
            self.view.challenge_succeeded(challenger, challenged, claimed_card)
            self.resolve_influence_loss(challenged)
            return True

    def replace_player_card(self, challenged: Player, claimed_card: str):
        challenged.cards.remove(claimed_card)
        card = self.take_card_from_deck()
        challenged.cards.append(card)

    def resolve_influence_loss(self, player: Player):
        player.reveal_card()

    def handle_block(self, player: Player, action: str, target: Player = None):
        """
        Handle a block attempt.
        - blocker: The player attempting to block.
        - action: The action being blocked.
        - action_player: The player who initiated the action.
        return True if the block is successful, False otherwise.
        """
        # If the action player decides to challenge the block
        if player.is_ai:
            challenge_decision = self.ai_decide_to_challenge(player, target, action)
        else:
            challenge_decision = self.view.get_challenge_decision(player, target, action, target)

        if challenge_decision:
            # Handle the challenge to the block
            return self.handle_challenge(target, player, action)

        # If there's no challenge to the block, or the challenge to the block fails
        self.view.block_successful(target, action)
        return True  # The block is successful, and the action does not proceed

    # Methods for player actions
    def income(self, player):
        player.coins += COUP_RULES_CONFIG["income"]["income"]  # Take 1 coin from the treasury

    def foreign_aid(self, player):
        player.coins += COUP_RULES_CONFIG["foreign_aid"]['income']

    def coup(self, player: Player, target: Player):
        cost = COUP_RULES_CONFIG["coup"]['cost']
        if player.coins < cost:
            raise Exception("Not enough coins to perform a coup.")
        player.coins -= cost
        # Target player loses an influence card
        if not target.is_eliminated:
            target.reveal_card()

    def tax(self, player):
        player.coins += COUP_RULES_CONFIG["tax"]['income']

    def assassinate(self, player: Player, target: Player):
        cost = COUP_RULES_CONFIG["assassinate"]['cost']
        if player.coins < cost:
            raise Exception("Not enough coins to perform an assassination.")
        if len(player.cards) < 1:
            raise Exception("Player has no more cards to lose.")
        player.coins -= cost
        # Target player loses an influence card
        target.reveal_card()

    def exchange(self, player):
        # Exchange cards with the deck
        if len(self.deck) < 2:
            self.view.print_error("Not enough cards in the deck.")
            raise Exception("Not enough cards in the deck.")

        # Take 2 cards from the deck
        cards_to_choose_from = player.cards + [self.take_card_from_deck(), self.take_card_from_deck()]

        # Choose 2 cards to keep
        if player.is_ai:
            cards_to_keep = random.sample(cards_to_choose_from, 2)
        else:
            cards_to_keep = self.view.choose_cards_to_exchange(player, cards_to_choose_from)

        # Set new player cards
        # and remove the remaining cards
        # to keep from the cards to choose from
        player.cards = cards_to_keep
        for card in cards_to_keep:
            cards_to_choose_from.remove(card)

        # Put the cards to choose from back to the deck
        self.reshuffle_deck(cards_to_choose_from)

    def steal(self, player, target):
        # Take 2 coins from the target player
        steal_amount = COUP_RULES_CONFIG["steal"]['amount']
        if target.coins < steal_amount:
            player.coins += target.coins
            target.coins = 0
        else:
            player.coins += steal_amount
            target.coins -= steal_amount

    #  AI player methods
    def ai_decide_to_challenge(self, player, target, action):
        # TODO: Finish this method
        # Randomly decide to challenge or not
        sleep(1)
        return False  # random.choice([True, False])

    def ai_decide_to_block(self, player, action):
        # TODO: Finish this method
        sleep(1)
        return False  # random.choice([True, False])

    # Helper methods
    def player_available_actions(self, player):
        # Return a list of available actions for the player
        actions = []
        if player.coins >= MAX_COINS_FOR_COUP:
            actions.append("coup")
            return actions
        for action in self.actions:
            coup_rules_for_action = COUP_RULES_CONFIG[action]
            # Check if the player has enough coins to perform the action
            if player.coins >= coup_rules_for_action["cost"]:
                actions.append(action)
        return actions

    def next_turn(self):
        # Skip eliminated players
        while True:
            self.current_player_index = (
                (self.current_player_index + 1) % len(self.players)
            )
            if not self.players[self.current_player_index].is_eliminated:
                break

    def perform_action(self, action, player, target=None):
        # Dispatch the action to the corresponding method
        if action == "income":
            self.income(player)
            self.view.print_income(player)
        elif action == "foreign_aid":
            self.foreign_aid(player)
            self.view.print_foreign_aid(player)
        elif action == "coup" and target:
            self.coup(player, target)
            self.view.print_coup(player, target)
        elif action == "tax":
            self.tax(player)
            self.view.print_tax(player)
        elif action == "assassinate" and target:
            self.assassinate(player, target)
            self.view.print_assassinate(player, target)
        elif action == "exchange":
            self.exchange(player)
            self.view.print_exchange(player)
        elif action == "steal" and target:
            self.steal(player, target)
            self.view.print_steal(player, target)
        else:
            raise Exception("Unknown action.")

    def get_other_players(self, player):
        # Return a list of possible targets for the player
        possible_targets = []
        for index, player in enumerate(self.players):
            is_valid_target = not player.is_eliminated
            same_player = index == self.current_player_index
            if not is_valid_target or same_player:
                continue
            possible_targets.append(player)
        return possible_targets

    def is_game_over(self):
        # The game is over when only one player is left not eliminated
        active_players = [
            player for player in self.players if not player.is_eliminated
        ]
        return len(active_players) == 1

    def get_winner(self):
        # Return the winner of the game
        active_players = [
            player for player in self.players if not player.is_eliminated
        ]
        if len(active_players) != 1:
            raise Exception("The game is not over yet.")

        return active_players[0]

    def reset(self):
        # Prompt the user for number of players
        number_of_players = int(input("Enter number of players: "))
        while number_of_players < MIN_PLAYERS or number_of_players > MAX_PLAYERS:
            self.view.print_error(
                "Number of players must be between 2 and 6. Please try again."
            )
            self.reset()
