import random
import json
import random

class Enemy:
    def __init__(self, name, level_range, hp, atk, defense, agility, skill_name, skill_desc):
        self.name = name
        self.level_range = level_range
        self.hp = hp
        self.atk = atk
        self.defense = defense
        self.agility = agility
        self.skill_name = skill_name
        self.skill_desc = skill_desc
        
    def attack_player(self, player, is_defending=False):
    # Damage yang diterima pemain
        damage = self.atk

        # Jika pemain sedang bertahan, kurangi damage dengan persentase berdasarkan defense
        if is_defending:
            damage *= (1 - (player.defense / 100))  # Misalnya, defense mengurangi 50% damage

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
    
    

