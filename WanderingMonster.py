import random


class WanderingMonster:

    def __init__(self, x, y, monster_type, color, hp):
        self.x = int(x)
        self.y = int(y)
        self.monster_type = str(monster_type)
        self.color = list(color)
        self.hp = int(hp)

    @classmethod
    def random_spawn(cls, occupied, forbidden, grid_w, grid_h):

        available_positions = []

        for x in range(grid_w):
            for y in range(grid_h):
                if ((x, y) not in occupied and
                        (x, y) not in forbidden):
                    available_positions.append((x, y))

        if not available_positions:
            return None

        x, y = random.choice(available_positions)

        monster_types = ["Goblin", "Orc", "Vulture"]

        monster_type = random.choice(monster_types)

        colors = {
            "Goblin": [0, 255, 0],
            "Orc": [255, 0, 0],
            "Vulture": [128, 128, 128]
        }

        hit_points = {
            "Goblin": 20,
            "Orc": 40,
            "Vulture": 15
        }

        return cls(
            x,
            y,
            monster_type,
            colors[monster_type],
            hit_points[monster_type]
        )

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["x"],
            data["y"],
            data["monster_type"],
            data["color"],
            data["hp"]
        )

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "monster_type": self.monster_type,
            "color": list(self.color),
            "hp": self.hp
        }

    def move(self, occupied, forbidden, grid_w, grid_h):

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

            if not (0 <= new_x < grid_w):
                continue

            if not (0 <= new_y < grid_h):
                continue

            if (new_x, new_y) in occupied:
                continue

            if (new_x, new_y) in forbidden:
                continue

            self.x = new_x
            self.y = new_y
            return
