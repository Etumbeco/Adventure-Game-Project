"""
Main Game Module

This module imports gamefunctions and runs
the adventure game.
"""

import gamefunctions


def new_game():
    """Create a new player and start a new game."""

    state = {
        "player_name": "Player",
        "player_health": 30,
        "player_gold": 1000,
        "player_inventory": [],
        "equipped_weapon": None
    }

    return state


def main():
    """Run the adventure game."""

    print("\n========== ADVENTURE GAME ==========")
    print("1. Start New Game")
    print("2. Load Previous Game")

    while True:
        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            state = new_game()
            print("\nStarting a new adventure!")
            break

        elif choice == "2":
            state = gamefunctions.load_game()

            if state is not None:
                break

            print("\nPlease choose again.")
            print("1. Start New Game")
            print("2. Load Previous Game")

        else:
            print("Invalid choice. Please enter 1 or 2.")

    gamefunctions.print_welcome()

    gamefunctions.main_menu_action(state)

    print("\nGame ended.")


if __name__ == "__main__":
    main()
