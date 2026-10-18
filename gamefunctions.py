import random


def purchase_item(itemPrice, startingMoney, quantityToPurchase=1):
    max_affordable = startingMoney // itemPrice
    num_purchased = min(quantityToPurchase, max_affordable)
    leftover_money = startingMoney - (num_purchased * itemPrice)

    return num_purchased, leftover_money


def new_random_monster():
    monsters = [
        {
            "name": "A goblin",
            "description": "This is a lone goblin. When it notices you, it rushes at you quickly with a sharp dagger drawn.",
            "health_range": (5, 10),
            "power_range": (2, 5),
            "money_range": (10, 50)
        },
        {
            "name": "Vulture",
            "description": "You discover a vulture eating the remains of two orcs that appear to have killed each other.",
            "health_range": (1, 3),
            "power_range": (1, 4),
            "money_range": (100, 1500)
        },
        {
            "name": "Orc",
            "description": "A large orc blocks your path. It carries a heavy club and looks ready for a fight.",
            "health_range": (15, 25),
            "power_range": (5, 10),
            "money_range": (50, 200)
        }
    ]

    monster = random.choice(monsters)

    return {
        "name": monster["name"],
        "description": monster["description"],
        "health": random.randint(*monster["health_range"]),
        "power": random.randint(*monster["power_range"]),
        "money": random.randint(*monster["money_range"])
    }


# Test purchase_item three times

num_purchased, leftover_money = purchase_item(123, 1000, 3)
print(num_purchased, leftover_money)

num_purchased, leftover_money = purchase_item(123, 201, 3)
print(num_purchased, leftover_money)

num_purchased, leftover_money = purchase_item(341, 2112)
print(num_purchased, leftover_money)


# Test new_random_monster three times

print(new_random_monster())
print(new_random_monster())
print(new_random_monster())
