from colored import Fore, Back, Style
from helpers import colorize_card, colorize_text, colorize_amount
from constants import ACTION_LABELS


class PlayerView:
    def __init__(self):
        pass

    def get_card_to_reveal(self, player):
        for index, card in enumerate(player.cards):
            print(f"{index + 1}. {card}")
        card_index = int(input("Enter card number: ")) - 1
        return card_index

    def display_player_eliminated(self, player_name):
        print(f"{Fore.RED}{player_name} has been eliminated from the game.{Style.RESET}")

    def display_player_revealed_card(self, player_name, card):
        print(f"{Fore.RED}{player_name} revealed {card}{Style.RESET}")

    def print_ai_thinking_reveal(self):
        print(f"{Fore.DARK_CYAN}AI thinking about what to reveal...{Style.RESET}")


class GameView:
    def __init__(self):
        pass

    def display_welcome_message(self):
        print(f"{Fore.GREEN}Welcome to Coup - Command Line Edition{Style.RESET}")

    def display_state(self, players, current_player_index):
        print(f"{Fore.GREEN}======================================={Style.RESET}")
        current_player = players[current_player_index]
        is_ai = current_player.is_ai
        if is_ai:
            print(f"{Fore.DARK_CYAN}{current_player.name}'s turn {Style.RESET}")
        else:
            print("Other players:")
            for i, player in enumerate(players):
                if i == current_player_index:
                    continue
                revealed_cards = " ".join([
                    f"[{colorize_card(card)}]" for card in player.revealed
                ])
                print(f"{i + 1}. {player.name} ({len(player.cards)} cards) {revealed_cards} - {colorize_amount(player.coins)} coins")
            print(f"{Fore.GREEN}======================================={Style.RESET}")
            print(f"Player {current_player.name}'s turn (Human)" if current_player.is_ai is False else f"{Fore.YELLOW}AI's turn{Style.RESET}")
            print(f"Coins: {colorize_amount(current_player.coins)}")
            cards = " ".join([f"[{colorize_card(card)}]" for card in current_player.cards])
            print(f"Cards: {cards}\n")
            if current_player.revealed:
                revealed_cards = " ".join([
                    f"[{colorize_card(card)}]" for card in current_player.revealed
                ])
                print(f"Revealed cards: {revealed_cards}\n")
        print(f"{Fore.GREEN}======================================={Style.RESET}")

    def print_error(self, error):
        print(f"{Fore.RED}{error}{Style.RESET}")

    def announce_action(self, player, action, character="", target=None):
        """
        Format the action based on the character and action:
        """
        character_text = f"by [{colorize_card(character)}]" if character else ""
        target_name_text = f" on {target.name}" if target else ""
        text = f"{player.name} choose to perform [{colorize_text(action, action)}] {colorize_text(character_text, action)}{target_name_text}"
        if action == "income":
            print(f"{Fore.YELLOW}{text}{Style.RESET}")
        elif action == "foreign_aid":
            print(f"{Fore.YELLOW}{text}{Style.RESET}")
        elif action == "coup":
            print(f"{Back.RED}{text}{Style.RESET}")
        elif character == "assassin":
            print(f"{Fore.BLACK}{Back.WHITE}{text}{Style.RESET}")
        elif character == "ambassador":
            print(f"{Fore.GREEN}{text}{Style.RESET}")
        elif character == "captain":
            print(f"{Fore.BLUE}{text}{Style.RESET}")
        elif character == "duke":
            print(f"{Fore.MAGENTA}{text}{Style.RESET}")
        elif character == "contessa":
            print(f"{Fore.RED}{text}{Style.RESET}")
        else:
            print(text)

    def print_steal(self, player, target):
        self.announce_action(player, "steal", "captain", target)

    def print_income(self, player):
        self.announce_action(player, "income")
        print(f"{player.name} has {colorize_amount(player.coins)} coins now.")

    def print_foreign_aid(self, player):
        self.announce_action(player, "foreign_aid")
        print(f"{player.name} has {colorize_amount(player.coins)} coins now.")

    def print_coup(self, player, target):
        self.announce_action(player, "coup", target=target)

    def print_tax(self, player):
        self.announce_action(player, "tax", "duke")
        print(f"{player.name} has {colorize_amount(player.coins)} coins now.")

    def print_assassinate(self, player, target):
        self.announce_action(player, "assassinated", "assassin", target=target)

    def print_exchange(self, player):
        self.announce_action(player, "exchange", "ambassador")

    def get_player_action(self, player, options):
        """
        Display the options available to the player
        and return the option selected by the player
        """
        print(f"What would you like to do, {player.name}?")
        for i, option in enumerate(options):
            print(f"{i + 1}. {ACTION_LABELS[option]}")
        option_number = input("Enter the number of your choice: ")
        # validate option number
        if not option_number.isdigit():
            self.print_error("Invalid option. Try again.")
            return self.get_player_action(player, options)
        option_number = int(option_number)
        if option_number > len(options) or option_number < 1:
            self.print_error("Invalid option. Try again.")
            return self.get_player_action(player, options)
        return options[int(option_number) - 1]

    def get_player_target(self, players, player):
        """
        Display the players available to the player
        and return the player selected by the player

        @param players: a list of Player objects
        @param player: a Player object
        returns a Player object
        """
        print(f"Who would you like to target, {player.name}?")
        for i, player in enumerate(players):
            print(f"{i + 1}. {player.name}")
        player_number = int(input("Enter the number of your target: "))
        if player_number > len(players) or player_number < 1:
            self.print_error("Invalid player. Try again.")
            return self.get_player_target(players, player)
        return players[int(player_number) - 1]

    def announce_eliminated_player(self, player):
        print(f"{Fore.RED}{player.name} has been eliminated from the game.{Style.RESET}")
    # Additional methods for displaying information and results

    @staticmethod
    def display_game_over(winner):
        print(f"{Fore.GREEN}{winner.name.capitalize()} won the game!{Style.RESET}")
        print(f"{Fore.GREEN}Game Over{Style.RESET}")
        # Display the winner and final state of the game

    def ask_to_play_again(self):
        print("Would you like to play again?")
        decision = input("Enter 'y' for yes or 'n' for no: ")
        if decision == "y":
            return True
        elif decision == "n":
            return False
        else:
            self.print_error("Invalid decision. Try again.")
            return self.ask_to_play_again()

    def test_announce_action(self):
        # with all possible options:
        class Player:
            name = "player"
        player = Player()
        self.print_assassinate(player, "target")
        self.print_tax(player)
        self.print_exchange(player)
        self.print_steal(player, "target")
        self.print_income(player)
        self.print_foreign_aid(player)
        self.print_coup(player, "target")

    def challenge_failed(self, challenger, challenged, claimed_card):
        print(f"{Back.RED}Challenge failed. {challenged.name} did have a {claimed_card}.{Style.RESET}")

    def challenge_succeeded(self, challenger, challenged, claimed_card):
        print(f"{Fore.GREEN}Challenge succeeded. {challenged.name} did not have a/an {claimed_card}.{Style.RESET}")

    def get_challenge_decision(
        self, challenger, challenged, action, target=None
    ):
        """
        Return True if the player decides to challenge
        Return False if the player decides not to challenge
        """
        target_text = ""
        if target is challenger:
            target_text = f" on you."
        elif target:
            target_text = f" on {target.name}."

        print(f"{challenger.name}, would you like to challenge {challenged.name}?")
        print(f"{challenged.name} is performing a/an {colorize_text(action, action)}{target_text}.")
        decision = input("Enter 'y' to challenge and 'n' to allow: ")
        if decision == "y":
            return True
        elif decision == "n":
            return False
        else:
            self.print_error("Invalid decision. Try again.")
            return self.get_challenge_decision(
                challenger, challenged, action
            )

    def get_block_decision(self, blocker, blocked_player, action):
        """
        Return True if the player decides to block
        Return False if the player decides not to block
        """
        print(f"{blocker.name}, would you like to block?")
        print(f"{blocked_player.name} is performing a/an {colorize_text(action, action)}.")
        # Print the cards that the challenger player has
        print("you have the following cards:")
        print(" ".join([f"[{colorize_card(card)}]" for card in blocker.cards]))
        decision = input("Enter 'y' to block or 'n' to allow: ")
        if decision == "y":
            return True
        elif decision == "n":
            return False
        else:
            self.print_error("Invalid decision. Try again.")
            return self.get_block_decision(blocker, blocked_player, action)

    def block_successful(self, blocker, blocked_player, action):
        print(f"{blocker.name} blocked {blocked_player.name}'s {action}.")

    def choose_cards_to_exchange(self, player, cards):
        """
        Return a list of cards to exchange
        """
        print(f"{player.name}, choose cards to keep.")
        for i, card in enumerate(cards):
            print(f"{i + 1}. {card}")
        cards_to_keep = []
        # Choose n cards to exchange depending on player's number of cards
        num_cards_to_exchange = len(player.cards)
        for i in range(num_cards_to_exchange):
            card_index = int(input("Enter card number: ")) - 1
            # Validate card index
            if card_index > len(cards) or card_index < 0:
                self.print_error("Invalid card. Try again.")
                return self.choose_cards_to_exchange(player, cards)
            cards_to_keep.append(cards[card_index])

        return cards_to_keep

    def print_ai_thinking(self, about=""):
        about_text = f" about {about}" if about else ""
        print(f"{Fore.DARK_CYAN}AI thinking{about_text}...{Style.RESET}")

    def ask_for_player_name(self):
        return input("Enter your name: ") or "Human"
