"""
Adventure Game Functions

Contains game functions, player movement,
monster encounters, and the world map.
"""

import random


def print_welcome():
    """Display the welcome message."""
    print("Welcome to the Adventure Game!")


def print_shop_menu(character_health, character_gold):
    """Display the town menu."""
    print("\nYou are in town.")
    print(f"Current HP: {character_health}, "
          f"Current Gold: {character_gold}")
    print("What would you like to do?")
    print("1) Explore the world map")
    print("2) Sleep (Restore HP for 5 Gold)")
    print("3) Quit")


def random_monster():
    """Return a randomly selected monster."""
    monsters = [
        {"name": "Goblin", "health": 20, "attack": 5},
        {"name": "Vulture", "health": 15, "attack": 4},
        {"name": "Orc", "health": 30, "attack": 8}
    ]

    return random.choice(monsters)


def fight_monster(character_health, character_gold):
    """Fight a randomly selected monster."""
    monster = random_monster()

    print(f"\nA {monster['name']} appears!")

    while character_health > 0 and monster["health"] > 0:
        monster["health"] -= 10
        print("You attack the monster!")

        if monster["health"] <= 0:
            break

        character_health -= monster["attack"]
        print(f"The monster attacks! HP: {character_health}")

    if character_health > 0:
        print("You defeated the monster!")
        character_gold += 10
    else:
        print("You were defeated!")

    return character_health, character_gold


def sleep(character_health, character_gold):
    """Restore player health for five gold."""
    if character_gold >= 5:
        character_gold -= 5
        character_health = 30
        print("You rested and restored your health!")
    else:
        print("You don't have enough gold!")

    return character_health, character_gold


def create_map():
    """Create the initial 10x10 world map."""
    return {
        "player": (5, 9),
        "town": (5, 9),
        "monster": (5, 3),
        "left_town": False
    }


def display_map(map_state):
    """Display the world map using its current state."""
    print("\n========== WORLD MAP ==========")

    for y in range(10):
        row = []

        for x in range(10):
            position = (x, y)

            if position == map_state["player"]:
                row.append("P")
            elif position == map_state["town"]:
                row.append("T")
            elif position == map_state["monster"]:
                row.append("M")
            else:
                row.append(".")

        print(" ".join(row))

    print("\nP = Player")
    print("T = Town")
    print("M = Monster")
    print(". = Empty space")


def move_player(game_state, direction):
    """Move the player one space on the map."""
    x, y = game_state["player"]

    direction = direction.lower()

    if direction in ("up", "w"):
        y -= 1
    elif direction in ("down", "s"):
        y += 1
    elif direction in ("left", "a"):
        x -= 1
    elif direction in ("right", "d"):
        x += 1
    else:
        return "moved"

    # Check map boundaries.
    if not (0 <= x <= 9 and 0 <= y <= 9):
        print("You cannot move outside the map!")
        return "moved"

    game_state["player"] = (x, y)

    # Check if player returns to town.
    if game_state["player"] == game_state["town"]:
        if game_state["left_town"]:
            return "returned_to_town"

    else:
        game_state["left_town"] = True

    # Check monster location.
    if game_state["player"] == game_state["monster"]:
        return "monster_encounter"

    return "moved"


def map_interface(map_state):
    """Run the text-based world map."""
    while True:
        display_map(map_state)

        direction = input(
            "\nMove using W/A/S/D: "
        )

        result = move_player(map_state, direction)

        if result == "returned_to_town":
            print("You returned to town!")
            return "town"

        elif result == "monster_encounter":
            print("A monster appeared!")
            return "monster"


def move_monster(map_state):
    """Move the monster to a random unoccupied location."""
    while True:
        position = (
            random.randint(0, 9),
            random.randint(0, 9)
        )

        if (position != map_state["player"]
                and position != map_state["town"]):
            map_state["monster"] = position
            return
