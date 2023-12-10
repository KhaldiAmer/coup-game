from colored import Fore, Back, Style


def colorize_text(text, action):
    if action == "tax":
        return f"{Fore.MAGENTA}{text}{Style.RESET}"
    elif action == "steal":
        return f"{Fore.BLUE}{text}{Style.RESET}"
    elif action == "exchange":
        return f"{Fore.GREEN}{text}{Style.RESET}"
    elif action == "assassinate":
        return f"{Fore.BLACK}{Back.WHITE}{text}{Style.RESET}"
    elif action == "income":
        return f"{Fore.YELLOW}{text}{Style.RESET}"
    elif action == "foreign_aid":
        return f"{Fore.YELLOW}{text}{Style.RESET}"
    elif action == "coup":
        return f"{Back.RED}{text}{Style.RESET}"


def colorize_card(card):
    if card == "duke":
        return f"{Fore.MAGENTA}{card}{Style.RESET}"
    elif card == "captain":
        return f"{Fore.BLUE}{card}{Style.RESET}"
    elif card == "ambassador":
        return f"{Fore.GREEN}{card}{Style.RESET}"
    elif card == "assassin":
        return f"{Fore.BLACK}{Back.WHITE}{card}{Style.RESET}"
    elif card == "contessa":
        return f"{Fore.RED}{card}{Style.RESET}"


def colorize_amount(amount):
    return f"{Fore.YELLOW}{amount}{Style.RESET}"
