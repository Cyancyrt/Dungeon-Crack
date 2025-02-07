import random
import random
import math
from collections import Counter

class Enemy:
    def __init__(self, name, level_range, hp, atk, defense, agility, skill_name, skill_desc):
        self.name = name
        self.level_range = level_range
        self.level = None
        self.hp = hp
        self.max_hp = hp
        self.atk = atk
        self.defense = defense
        self.max_defense = defense
        self.agility = agility
        self.skill_name = skill_name
        self.skill_desc = skill_desc
    
    def set_level(self):
        if isinstance(self.level_range, list) and len(self.level_range) == 2:
            random_levels = [random.randint(self.level_range[0], self.level_range[1]) for _ in range(100)]
            level_counts = Counter(random_levels)
            most_common_level = level_counts.most_common(1)[0][0]
            self.level = most_common_level 

    def set_attributes(self):
        for attr in ['hp', 'atk', 'defense', 'agility']:
            if isinstance(getattr(self, attr), list) and len(getattr(self, attr)) == 2:
                value = random.randint(getattr(self, attr)[0], getattr(self, attr)[1])
                setattr(self, attr, value)
                if attr == 'hp':
                    self.max_hp = value  # Set max_hp sesuai dengan hp yang dipilih
    
    def defense_calc(self, player, damage):
        damage_reduction = math.ceil(player.stats.defense * 0.25)
        damage_taken = max(damage - damage_reduction, 0)  # Pastikan damage tidak negatif
    
        return damage_taken
    def attack_player(self, player, is_defending=False):
    # Damage yang diterima pemain
        damage = self.atk

        # kurangi damage dengan persentase berdasarkan defense
        defense_factor = self.defense_calc(player, damage)
        # Pastikan damage tidak kurang dari 0
        damage = max(0, defense_factor)

        # Kurangi HP pemain
        player.stats.hp -= damage
        print(f"{self.name} menyerang {player.name}, mengurangi {damage} HP!")
    
    def display_basic_info(self):
        # Menentukan level musuh secara acak dalam range yang ditentukan
        level = random.randint(*self.level_range)
        # Menampilkan nama, HP, dan level
        print(f"\nNama Musuh: {self.name}")
        print(f"Level: {level}")
        print(f"HP: {self.hp}")
        return level
    def to_dict(self):
        # Mengonversi objek Enemy ke dalam bentuk kamus
        return {
            'name': self.name,
            'level': self.level,
            'hp': self.hp,
            'atk': self.atk,
            'defense': self.defense,
            'agility': self.agility,
            'skill_name': self.skill_name,
            'skill_desc': self.skill_desc
        }
    def display_full_info(self):
        # Menampilkan detail lengkap musuh
        stats = self.to_dict()
        stats.pop('level_range', None)
        for key, value in stats.items():
            print(f"{key}: {value}")
    
    

