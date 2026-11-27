"""
Main Game Module

Runs the adventure game and connects
the world map, wandering monsters, and town menu.
"""

import gamefunctions


def main():
    """Run the adventure game."""

    character_health = 30
    character_gold = 10

    # Create the initial game state.
    state = gamefunctions.create_map()

    gamefunctions.print_welcome()

    while character_health > 0:

        # Display the town menu.
        gamefunctions.print_shop_menu(
            character_health,
            character_gold
        )

        choice = input("Enter your choice: ").strip()

        if choice == "1":

            # Explore the world map.
            result, character_health, character_gold = (
                gamefunctions.map_interface(
                    state,
                    character_health,
                    character_gold
                )
            )

            if result == "game_over":
                break

            if result == "town":
                print("You are back in town!")

        elif choice == "2":

            # Restore player health.
            character_health, character_gold = (
                gamefunctions.sleep(
                    character_health,
                    character_gold
                )
            )

        elif choice == "3":

            # Save the game.
            gamefunctions.save_game(
                state,
                character_health,
                character_gold
            )

        elif choice == "4":

            # Load the saved game.
            loaded_game = gamefunctions.load_game()

            if loaded_game is not None:
                state, character_health, character_gold = loaded_game

        elif choice == "5":

            print("Thanks for playing!")
            break

        else:

            print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")

    if character_health <= 0:
        print("Game over!")

    print("Game ended.")


if __name__ == "__main__":
    main()
