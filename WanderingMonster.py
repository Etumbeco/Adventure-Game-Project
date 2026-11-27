import random


class WanderingMonster:
    """Represent a monster that moves around the game map."""

    def __init__(self, x, y, monster_type, color, hp):
        self.x = int(x)
        self.y = int(y)
        self.monster_type = str(monster_type)
        self.color = list(color)
        self.hp = int(hp)

    @classmethod
    def random_spawn(cls, occupied, forbidden, grid_w, grid_h):
        """Create a monster at a random available location."""

        available_positions = []

        for x in range(grid_w):
            for y in range(grid_h):
                position = (x, y)

                if position not in occupied and position not in forbidden:
                    available_positions.append(position)

        if not available_positions:
            raise ValueError("No available location to spawn monster.")

        x, y = random.choice(available_positions)

        monster_types = [
            ("Goblin", [0, 255, 0], 20),
            ("Orc", [255, 0, 0], 30),
            ("Vulture", [128, 128, 128], 15)
        ]

        monster_type, color, hp = random.choice(monster_types)

        return cls(x, y, monster_type, color, hp)

    @classmethod
    def from_dict(cls, data):
        """Create a monster from saved dictionary data."""

        return cls(
            data["x"],
            data["y"],
            data["monster_type"],
            data["color"],
            data["hp"]
        )

    def to_dict(self):
        """Convert monster information into JSON-safe data."""

        return {
            "x": self.x,
            "y": self.y,
            "monster_type": self.monster_type,
            "color": list(self.color),
            "hp": self.hp
        }

    def move(self, occupied, forbidden, grid_w, grid_h):
        """Move one space in a random available direction."""

        directions = [
            (0, -1),
            (0, 1),
            (-1, 0),
            (1, 0)
        ]

        random.shuffle(directions)

        for dx, dy in directions:
            new_x = self.x + dx
            new_y = self.y + dy

            new_position = (new_x, new_y)

            if (
                0 <= new_x < grid_w
                and 0 <= new_y < grid_h
                and new_position not in occupied
                and new_position not in forbidden
            ):
                self.x = new_x
                self.y = new_y
                return True

        return False
