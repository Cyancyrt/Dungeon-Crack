import random
import random
import math

class Enemy:
    def __init__(self, name, level_range, hp, atk, defense, agility, skill_name, skill_desc):
        self.name = name
        self.level_range = level_range
        self.hp = hp
        self.max_hp = hp
        self.atk = atk
        self.defense = defense
        self.max_defense = defense
        self.agility = agility
        self.skill_name = skill_name
        self.skill_desc = skill_desc
        
    def attack_player(self, player, is_defending=False):
    # Damage yang diterima pemain
        damage = self.atk

        # kurangi damage dengan persentase berdasarkan defense
        defense_factor = 1 - (math.log1p(player.stats.defense) / (math.log1p(1000)))  # Fungsi logaritmik
        damage *= round(defense_factor)
        # Pastikan damage tidak kurang dari 0
        damage = max(0, damage)

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
            'level_range': self.level_range,
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
        stats["level"] = stats.pop("level_range", stats.get("level", "Unknown"))
        for key, value in stats.items():
            print(f"{key}: {value}")
    
    

