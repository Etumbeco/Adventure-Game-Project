"""
Main Game Module

Runs the adventure game and connects the world map
to the monster battles and town menu.
"""

import gamefunctions


def main():
    """Run the adventure game."""

    character_health = 30
    character_gold = 10

    # Create the map once and maintain its state.
    map_state = gamefunctions.create_map()

    gamefunctions.print_welcome()

    while character_health > 0:

        gamefunctions.print_shop_menu(
            character_health,
            character_gold
        )

        choice = input("Enter your choice: ").strip()

        if choice == "1":

            # Open the world map.
            result = gamefunctions.map_interface(map_state)

            if result == "town":
                print("You are back in town!")

            elif result == "monster":

                # Start monster combat.
                character_health, character_gold = (
                    gamefunctions.fight_monster(
                        character_health,
                        character_gold
                    )
                )

                # Place a new monster after combat.
                if character_health > 0:
                    gamefunctions.move_monster(map_state)
                    print("A new monster has appeared!")
                    print("Returning to the world map...")

        elif choice == "2":

            character_health, character_gold = (
                gamefunctions.sleep(
                    character_health,
                    character_gold
                )
            )

        elif choice == "3":
            print("Thanks for playing!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    if character_health <= 0:
        print("Game over!")

    print("Game ended.")


if __name__ == "__main__":
    main()
