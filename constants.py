from helpers import colorize_text

ACTION_LABELS = {
    "income": colorize_text("Income (Take 1 coin)", "income"),
    "foreign_aid": colorize_text("Foreign aid (Take 2 coins)", "foreign_aid"),
    "coup": colorize_text("Coup (Pay 7 coins to launch a coup)", "coup"),
    "tax": colorize_text("Tax (Take 3 coins as the Duke)", "tax"),
    "steal": colorize_text("Steal (Steal 2 coins as the Captain)", "steal"),
    "exchange": colorize_text("Exchange (Exchange cards with the Court Deck as the Ambassador)", "exchange"),
    "assassinate": colorize_text("Assassinate (Pay 3 coins to assassinate another player's influence)", "assassinate")
}

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

# constants
MAX_COINS_FOR_COUP = 10
MIN_PLAYERS = 2
MAX_PLAYERS = 6
