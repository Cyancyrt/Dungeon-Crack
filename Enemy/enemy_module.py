import random
import random
import math
from Hooks.Event_Dispatch import EventDispatcher
from collections import Counter
from Enemy.enemy_passive_handler import Enemy_passive

class Stats:
    def __init__(self, hp, attack, defense, agility):
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.agility = agility

class Enemy:
    def __init__(self, name, level_range, hp, atk, defense, agility, skill_name, skill_desc):
        self.name = name
        self.level_range = level_range
        self.level = None
        self.stats = Stats(hp, atk, defense, agility)
       
        self.skill_name = skill_name
        self.skill_desc = skill_desc
        self.buffs = {}
        self.debuffs = {}
        self.passive_skill_handler = Enemy_passive(self, EventDispatcher())

    @property
    def passive_skill_handler(self):
        return self._passive_skill_handler

    @passive_skill_handler.setter
    def passive_skill_handler(self, new_handler):
        self._passive_skill_handler = new_handler
    
    def mark_as_dead(self):
        self.passive_skill_handler.isDeath = True
    
    def set_level(self):
        if isinstance(self.level_range, list) and len(self.level_range) == 2:
            random_levels = [random.randint(self.level_range[0], self.level_range[1]) for _ in range(100)]
            level_counts = Counter(random_levels)
            most_common_level = level_counts.most_common(1)[0][0]
            self.level = most_common_level 

    def set_attributes(self):
        for attr in ['hp', 'attack', 'defense', 'agility']:
            if isinstance(getattr(self.stats, attr), list) and len(getattr(self.stats, attr)) == 2:
                value = random.randint(getattr(self.stats, attr)[0], getattr(self.stats, attr)[1])
                setattr(self.stats, attr, value)
                if attr == 'hp':
                    self.stats.max_hp = value  # Set max_hp sesuai dengan hp yang dipilih
    
    def defense_calc(self, player, damage):
        reduction_status = player.buffs.get("damage_reduction", {}).get("amount", 0)
        damage_reduction = math.ceil(player.stats.defense * (0.05 + reduction_status))
        damage_taken = max(damage - damage_reduction, 0)  # Pastikan damage tidak negatif
    
        return damage_taken
    def attack_player(self, player, is_defending=False):
    # Damage yang diterima pemain
        damage = self.stats.attack

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
            'hp': self.stats.hp,
            'atk': self.stats.attack,
            'defense': self.stats.defense,
            'agility': self.stats.agility,
            'skill_name': self.skill_name,
            'skill_desc': self.skill_desc
        }
    def display_full_info(self):
        # Menampilkan detail lengkap musuh
        stats = self.to_dict()
        stats.pop('level_range', None)
        for key, value in stats.items():
            print(f"{key}: {value}")
    



    

