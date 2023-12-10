
from controller import GameController


def main():
    controller = GameController()
    controller.view.display_welcome_message()

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

        if controller.is_game_over():
            controller.view.display_game_over()
            if controller.view.ask_to_play_again():
                controller = GameController()
                controller.view.display_welcome_message()
            else:
                break

        controller.next_turn()


if __name__ == "__main__":
    main()
