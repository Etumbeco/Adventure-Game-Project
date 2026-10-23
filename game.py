"""
Main Game Module

This module imports gamefunctions and runs a simple adventure game.
"""

import gamefunctions


def main():
    """Run the adventure game."""
    character_health = 30
    character_gold = 10

    gamefunctions.print_welcome()

    while character_health > 0:
        gamefunctions.print_shop_menu(
            character_health, character_gold
        )

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            character_health, character_gold = (
                gamefunctions.fight_monster(
                    character_health, character_gold
                )
            )
        elif choice == "2":
            character_health, character_gold = (
                gamefunctions.sleep(
                    character_health, character_gold
                )
            )
        elif choice == "3":
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    print("Game ended.")


if __name__ == "__main__":
    main()
