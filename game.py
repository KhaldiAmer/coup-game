
from controller import GameController


def main():
    controller = GameController()
    controller.view.display_welcome_message()

    # Ask for human player name
    player_name = controller.view.ask_for_player_name()
    controller.players[0].name = player_name

    while not controller.is_game_over():
        controller.view.display_state(
            controller.players,
            controller.current_player_index
        )

        # Step 1: Choose an action and target
        current_player = controller.current_player
        action, target = controller.choose_action()

        # Step 2: Challenge or block if necessary
        can_perform_action = controller.challenge_or_block(
            action,
            current_player,
            target,
        )

        # Step 3: Perform the action
        if can_perform_action:
            controller.perform_action(action, current_player, target)

        # Step 4: Check if game is over
        if controller.is_game_over():
            winner = controller.get_winner()
            controller.view.display_game_over(winner)
            if controller.view.ask_to_play_again():
                controller = GameController()
                controller.view.display_welcome_message()
                continue
            else:
                break

        controller.next_turn()


if __name__ == "__main__":
    main()
