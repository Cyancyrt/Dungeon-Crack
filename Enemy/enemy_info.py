### enemy_info.py

import random

class EnemyInfoMixin:
    def display_basic_info(self):
        level = random.randint(*self.level_range)
        print(f"\nNama Musuh: {self.name}")
        print(f"Level: {level}")
        print(f"HP: {self.stats.hp}")
        return level

    def display_full_info(self):
        stats = self.to_dict()
        for key, value in stats.items():
            print(f"{key}: {value}")

    def to_dict(self):
        return {
            'name': self.name,
            'level': self.level,
            'hp': self.stats.hp,
            'atk': self.stats.attack,
            'defense': self.stats.defense,
            'agility': self.stats.agility,
            'skill_name': self.skill_name,
            'skill_desc': self.skill_desc
        }