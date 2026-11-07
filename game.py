"""
Main Game Module

This module imports gamefunctions and runs
the adventure game.
"""

import gamefunctions


def main():
    """Run the adventure game."""

    state = {
        "player_name": "Player",
        "player_health": 30,
        "player_gold": 1000,
        "player_inventory": [],
        "equipped_weapon": None
    }

    gamefunctions.print_welcome()

    gamefunctions.main_menu_action(state)

    print("Game ended.")


if __name__ == "__main__":
    main()
