
"""Functions for the adventure game."""

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
    print("1) Leave town (Fight Monster)")
    print("2) Sleep (Restore HP for 5 Gold)")
    print("3) Quit")


def random_monster():
    """Choose a random monster."""
    monsters = [
        {"name": "Goblin", "hp": 10, "damage": 3, "gold": 3},
        {"name": "Vulture", "hp": 12, "damage": 4, "gold": 5},
        {"name": "Orc", "hp": 20, "damage": 5, "gold": 8}
    ]
    return random.choice(monsters)


def display_fight_statistics(character_health, monster):
    """Display current fight statistics."""
    print(f"\nYour HP: {character_health}")
    print(f"{monster['name']} HP: {monster['hp']}")


def get_user_fight_action():
    """Ask the player to fight or run away."""
    print("\n1) Fight")
    print("2) Run away")
    return input("Enter your choice: ").strip()


def fight_monster(character_health, character_gold):
    """Fight a monster and return updated health and gold."""
    monster = random_monster()
    print(f"\nA {monster['name']} appeared!")

    while character_health > 0 and monster["hp"] > 0:
        display_fight_statistics(character_health, monster)
        action = get_user_fight_action()

        if action == "1":
            damage = random.randint(4, 8)
            monster["hp"] -= damage
            print(f"You dealt {damage} damage!")

            if monster["hp"] > 0:
                character_health -= monster["damage"]
                print(
                    f"The {monster['name']} dealt "
                    f"{monster['damage']} damage!"
                )

        elif action == "2":
            print("You ran away!")
            break

        else:
            print("Invalid choice. Enter 1 or 2.")

    if character_health <= 0:
        character_health = 0
        print("You passed out! Game over.")
    elif monster["hp"] <= 0:
        print(f"You defeated the {monster['name']}!")
        character_gold += monster["gold"]
        print(f"You earned {monster['gold']} gold!")

    return character_health, character_gold


def sleep(character_health, character_gold):
    """Restore health for 5 gold."""
    if character_gold < 5:
        print("You need at least 5 gold to sleep.")
    elif character_health == 30:
        print("Your health is already full!")
    else:
        character_gold -= 5
        character_health = 30
        print("You rested and restored your health to 30 HP.")

    return character_health, character_gold

