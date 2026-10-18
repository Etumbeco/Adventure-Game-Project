"""
Main Game Module

This module imports gamefunctions and runs a simple adventure game.
"""

import gamefunctions


def main():
    """Run the adventure game."""
    name = input("What is your name, adventurer? ")

    print(f"\nWelcome, {name}!")
    gamefunctions.print_welcome()
    gamefunctions.print_shop_menu()

    choice = input("\nWould you like to purchase an item? (yes/no): ")

    if choice.lower() == "yes":
        gamefunctions.purchase_item()
    else:
        print("You decided not to buy anything.")

    gamefunctions.random_monster()
    print(f"\nThank you for playing, {name}!")


if __name__ == "__main__": def print_welcome():
    """Display the welcome message."""
    print("Welcome to the Adventure Game!")


def print_shop_menu():
    """Display the shop menu."""
    print("\n--- Shop Menu ---")
    print("1. Buy an item")
    print("2. Return to the adventure")


def random_monster():
    """Select and return a random monster."""
    return new_random_monster()
    main()
