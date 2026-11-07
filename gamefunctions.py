"""
Functions for the adventure game.

This module manages the shop, inventory, combat,
equipment, and player actions.
"""

import random


def print_welcome():
    """Display the welcome message."""
    print("\nWelcome to the Adventure Game!")


def print_shop_menu(state):
    """Display the main town menu."""
    print("\n========== ADVENTURE GAME ==========")
    print(f"Player: {state['player_name']}")
    print(f"Health: {state['player_health']}")
    print(f"Gold: {state['player_gold']}")
    print("\n1. Fight Monster")
    print("2. Sleep")
    print("3. Visit Shop")
    print("4. View Inventory")
    print("5. Equip Weapon")
    print("6. Quit")


def random_monster():
    """Choose a random monster."""
    monsters = [
        {"name": "Goblin", "hp": 10, "damage": 3, "gold": 5},
        {"name": "Vulture", "hp": 12, "damage": 4, "gold": 5},
        {"name": "Orc", "hp": 20, "damage": 5, "gold": 8}
    ]

    return random.choice(monsters).copy()


def display_fight_statistics(state, monster):
    """Display current fight statistics."""
    print("\nYour HP:", state["player_health"])
    print(monster["name"], "HP:", monster["hp"])


def show_inventory(state):
    """Display all items in the player's inventory."""
    print("\n========== INVENTORY ==========")

    if not state["player_inventory"]:
        print("Your inventory is empty.")
        return

    for index, item in enumerate(state["player_inventory"], 1):
        print(f"{index}. {item['name']} ({item['type']})")

        if item["type"] == "weapon":
            print(
                f"   Durability: "
                f"{item['currentDurability']}/"
                f"{item['maxDurability']}"
            )

        if item.get("equipped", False):
            print("   EQUIPPED")


def visit_shop(state):
    """Allow the player to purchase shop items."""
    shop_items = [
        {
            "name": "sword",
            "type": "weapon",
            "price": 50,
            "maxDurability": 10,
            "currentDurability": 10,
            "equipped": False
        },
        {
            "name": "shield",
            "type": "shield",
            "price": 30,
            "maxDurability": 10,
            "currentDurability": 10,
            "equipped": False
        },
        {
            "name": "magic_bomb",
            "type": "misc",
            "price": 40,
            "note": "Defeats one monster instantly."
        }
    ]

    print("\n========== SHOP ==========")

    for index, item in enumerate(shop_items, 1):
        print(f"{index}. {item['name']} - {item['price']} gold")

    print("4. Return")

    choice = input("Choose an item to purchase: ").strip()

    if choice == "4":
        return

    if choice not in ("1", "2", "3"):
        print("Invalid choice.")
        return

    item = shop_items[int(choice) - 1]

    if state["player_gold"] < item["price"]:
        print("You do not have enough gold!")
        return

    state["player_gold"] -= item["price"]

    purchased_item = item.copy()
    purchased_item.pop("price")

    state["player_inventory"].append(purchased_item)

    print(f"You purchased {item['name']} successfully!")


def equip_weapon(state):
    """Allow the player to equip a weapon."""
    weapons = [
        item for item in state["player_inventory"]
        if item["type"] == "weapon"
        and item["currentDurability"] > 0
    ]

    print("\n========== EQUIP WEAPON ==========")

    for index, weapon in enumerate(weapons, 1):
        print(f"{index}. {weapon['name']}")

    print("0. Unequip weapon")

    if not weapons:
        print("You have no usable weapons.")

    choice = input("Choose a weapon: ").strip()

    if choice == "0":
        for item in state["player_inventory"]:
            if item["type"] == "weapon":
                item["equipped"] = False

        state["equipped_weapon"] = None
        print("You unequipped your weapon.")
        return

    if not choice.isdigit():
        print("Invalid choice.")
        return

    number = int(choice)

    if number < 1 or number > len(weapons):
        print("Invalid choice.")
        return

    for item in state["player_inventory"]:
        if item["type"] == "weapon":
            item["equipped"] = False

    selected = weapons[number - 1]
    selected["equipped"] = True
    state["equipped_weapon"] = selected

    print(f"You equipped your {selected['name']}!")


def fight_monster(state):
    """Fight a monster using inventory items."""
    monster = random_monster()

    print(f"\nA {monster['name']} appeared!")

    while state["player_health"] > 0 and monster["hp"] > 0:

        display_fight_statistics(state, monster)

        bombs = [
            item for item in state["player_inventory"]
            if item["name"] == "magic_bomb"
        ]

        if bombs:
            choice = input(
                "Use magic bomb to defeat the monster? (y/n): "
            ).strip().lower()

            if choice == "y":
                state["player_inventory"].remove(bombs[0])
                monster["hp"] = 0
                print("Your magic bomb defeated the monster instantly!")
                break

        action = input("1. Fight\n2. Run away\nChoose: ").strip()

        if action == "1":
            damage = random.randint(4, 8)

            weapon = state["equipped_weapon"]

            if weapon and weapon["currentDurability"] > 0:
                damage += 5
                weapon["currentDurability"] -= 1

                print("Your sword increases your damage!")

                if weapon["currentDurability"] == 0:
                    weapon["equipped"] = False
                    state["equipped_weapon"] = None
                    print("Your sword broke!")

            monster["hp"] -= damage
            print(f"You dealt {damage} damage!")

            if monster["hp"] > 0:
                state["player_health"] -= monster["damage"]
                print(
                    f"The {monster['name']} dealt "
                    f"{monster['damage']} damage!"
                )

        elif action == "2":
            print("You ran away!")
            return

        else:
            print("Invalid choice.")

    if state["player_health"] <= 0:
        state["player_health"] = 0
        print("You passed out! Game over.")

    elif monster["hp"] <= 0:
        print(f"You defeated the {monster['name']}!")
        state["player_gold"] += monster["gold"]
        print(f"You earned {monster['gold']} gold!")


def sleep(state):
    """Restore player health for five gold."""
    if state["player_gold"] < 5:
        print("You need at least 5 gold to sleep.")

    elif state["player_health"] == 30:
        print("Your health is already full!")

    else:
        state["player_gold"] -= 5
        state["player_health"] = 30
        print("You rested and restored your health to 30 HP.")


def main_menu_action(state):
    """Run the player's selected main menu action."""
    while True:
        print_shop_menu(state)

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            fight_monster(state)

        elif choice == "2":
            sleep(state)

        elif choice == "3":
            visit_shop(state)

        elif choice == "4":
            show_inventory(state)

        elif choice == "5":
            equip_weapon(state)

        elif choice == "6":
            print("Thanks for playing!")
            break

        else:
            print("Invalid choice. Please try again.")

        if state["player_health"] <= 0:
            break
