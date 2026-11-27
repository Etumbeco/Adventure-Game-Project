"""
Adventure Game Functions

Handles player movement, monster encounters,
combat, map display, and JSON save/load.
"""

import json
import os

from WanderingMonster import WanderingMonster


GRID_W = 10
GRID_H = 10
SAVE_FILE = "savegame.json"


def print_welcome():
    print("Welcome to the Adventure Game!")


def print_shop_menu(character_health, character_gold):
    print("\nYou are in town.")
    print(f"Current HP: {character_health}")
    print(f"Current Gold: {character_gold}")
    print("1) Explore the world map")
    print("2) Sleep (Restore HP for 5 Gold)")
    print("3) Save game")
    print("4) Load game")
    print("5) Quit")


def create_map():
    """Create the initial game state with one monster."""

    state = {
        "player": (5, 9),
        "town": (5, 9),
        "left_town": False,
        "monsters": []
    }

    monster = WanderingMonster.random_spawn(
        occupied=[],
        forbidden=[state["player"], state["town"]],
        grid_w=GRID_W,
        grid_h=GRID_H
    )

    if monster is not None:
        state["monsters"].append(monster)

    return state


def draw_map(state):
    """Display the map using the current game state."""

    print("\n========== WORLD MAP ==========")

    monster_positions = {}

    for monster in state["monsters"]:
        monster_positions[(monster.x, monster.y)] = monster

    for y in range(GRID_H):
        row = []

        for x in range(GRID_W):

            position = (x, y)

            if position == state["player"]:
                row.append("P")

            elif position == state["town"]:
                row.append("T")

            elif position in monster_positions:
                row.append("M")

            else:
                row.append(".")

        print(" ".join(row))

    print("\nP = Player")
    print("T = Town")
    print("M = Monster")
    print(". = Empty space")


def spawn_monsters(state, number):
    """Spawn monsters at valid random locations."""

    for _ in range(number):

        occupied = [
            (monster.x, monster.y)
            for monster in state["monsters"]
        ]

        forbidden = [
            state["player"],
            state["town"]
        ]

        monster = WanderingMonster.random_spawn(
            occupied,
            forbidden,
            GRID_W,
            GRID_H
        )

        if monster is not None:
            state["monsters"].append(monster)


def move_monsters(state):
    """Move each monster once after the player moves."""

    for monster in state["monsters"]:

        occupied = [
            (other.x, other.y)
            for other in state["monsters"]
            if other is not monster
        ]

        forbidden = [
            state["player"],
            state["town"]
        ]

        monster.move(
            occupied,
            forbidden,
            GRID_W,
            GRID_H
        )


def move_player(state, direction):
    """Move the player one grid space."""

    x, y = state["player"]

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
        print("Invalid direction.")
        return "invalid"

    if not (0 <= x < GRID_W and 0 <= y < GRID_H):
        print("You cannot move outside the map!")
        return "invalid"

    state["player"] = (x, y)

    if state["player"] != state["town"]:
        state["left_town"] = True

    return "moved"


def fight_monster(character_health, character_gold, monster):
    """Fight the monster encountered by the player."""

    attacks = {
        "Goblin": 5,
        "Orc": 8,
        "Vulture": 4
    }

    monster_attack = attacks.get(monster.monster_type, 5)

    print(f"\nA {monster.monster_type} appears!")

    while character_health > 0 and monster.hp > 0:

        monster.hp -= 10

        print("You attack the monster!")

        if monster.hp <= 0:
            break

        character_health -= monster_attack

        print(
            f"The monster attacks! "
            f"Your HP: {character_health}"
        )

    defeated = monster.hp <= 0

    if defeated and character_health > 0:

        print("You defeated the monster!")

        character_gold += 10

    elif character_health <= 0:

        print("You were defeated!")

    return character_health, character_gold, defeated


def sleep(character_health, character_gold):
    """Restore player health for five gold."""

    if character_gold >= 5:

        character_gold -= 5
        character_health = 30

        print("You rested and restored your health!")

    else:

        print("You don't have enough gold!")

    return character_health, character_gold


def save_game(state, character_health, character_gold):
    """Save the game and convert monsters into JSON dictionaries."""

    save_data = {
        "player": list(state["player"]),
        "town": list(state["town"]),
        "left_town": state["left_town"],
        "character_health": character_health,
        "character_gold": character_gold,
        "monsters": [
            monster.to_dict()
            for monster in state["monsters"]
        ]
    }

    with open(SAVE_FILE, "w", encoding="utf-8") as file:
        json.dump(save_data, file, indent=4)

    print("Game saved successfully!")


def load_game():
    """Load the game and reconstruct monster objects."""

    if not os.path.exists(SAVE_FILE):
        print("No saved game was found.")
        return None

    with open(SAVE_FILE, "r", encoding="utf-8") as file:
        save_data = json.load(file)

    state = {
        "player": tuple(save_data["player"]),
        "town": tuple(save_data["town"]),
        "left_town": save_data["left_town"],
        "monsters": [
            WanderingMonster.from_dict(monster_data)
            for monster_data in save_data["monsters"]
        ]
    }

    character_health = save_data["character_health"]
    character_gold = save_data["character_gold"]

    print("Game loaded successfully!")

    if not state["monsters"]:
        spawn_monsters(state, 2)

    return state, character_health, character_gold


def map_interface(state, character_health, character_gold):
    """Handle player movement, combat, and monster movement."""

    while character_health > 0:

        draw_map(state)

        direction = input(
            "\nMove using W/A/S/D: "
        )

        result = move_player(state, direction)

        if result == "invalid":
            continue

        # Check player position before monsters move.
        encountered = None

        for monster in state["monsters"]:

            if (monster.x, monster.y) == state["player"]:
                encountered = monster
                break

        # Start combat if a monster is found.
        if encountered is not None:

            character_health, character_gold, defeated = (
                fight_monster(
                    character_health,
                    character_gold,
                    encountered
                )
            )

            if defeated:
                state["monsters"].remove(encountered)

        if character_health <= 0:
            draw_map(state)
            return "game_over", character_health, character_gold

        # Spawn two monsters if none remain.
        if not state["monsters"]:
            print("No monsters remain!")
            print("Two new monsters have appeared!")

            spawn_monsters(state, 2)

        # Monsters move once after each valid player move.
        # move_monsters(state)

        
        

        if state["player"] == state["town"] and state["left_town"]:
            print("You returned to town!")

            return "town", character_health, character_gold

    return "game_over", character_health, character_gold
