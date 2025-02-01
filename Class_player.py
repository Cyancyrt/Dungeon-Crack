import json
import time

# ========== Kelas untuk Skill ========== #
class Skill:
    def __init__(self, name, description, cooldown, damage_multiplier=1.0, aoe=False):
        self.name = name
        self.description = description
        self.cooldown = cooldown
        self.remaining_cooldown = 0
        self.damage_multiplier = damage_multiplier
        self.aoe = aoe

    def use(self):
        if self.remaining_cooldown == 0:
            self.remaining_cooldown = self.cooldown
            return self.damage_multiplier
        else:
            print(f"❌ Skill {self.name} masih cooldown {self.remaining_cooldown} turn lagi.")
            return False

    def reduce_cooldown(self):
        if self.remaining_cooldown > 0:
            self.remaining_cooldown -= 1


    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "cooldown": self.cooldown,
            "damage_multiplier": self.damage_multiplier,
            "aoe": self.aoe
        }

    @staticmethod
    def from_dict(data):
        return Skill(**data)


# ========== Kelas untuk Passive Skill ========== #
class PassiveSkill:
    def __init__(self, name, description, effect_duration, cooldown, strength_bonus=0, defense_bonus=0):
        self.name = name
        self.description = description
        self.effect_duration = effect_duration
        self.cooldown = cooldown
        self.remaining_duration = effect_duration
        self.remaining_cooldown = 0
        self.strength_bonus = strength_bonus
        self.defense_bonus = defense_bonus

    def activate(self):
        if self.remaining_cooldown == 0:
            self.remaining_duration = self.effect_duration
            print(f"🔥 Pasif {self.name} Aktif! (+{self.strength_bonus}% STR, +{self.defense_bonus} DEF) selama {self.effect_duration} turn.")
        else:
            print(f"❌ Pasif {self.name} dalam cooldown {self.remaining_cooldown} turn.")

    def update(self):
        if self.remaining_duration > 0:
            self.remaining_duration -= 1
            if self.remaining_duration == 0:
                print(f"🛑 Efek pasif {self.name} berakhir.")
                self.remaining_cooldown = self.cooldown
        elif self.remaining_cooldown > 0:
            self.remaining_cooldown -= 1

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "effect_duration": self.effect_duration,
            "cooldown": self.cooldown,
            "strength_bonus": self.strength_bonus,
            "defense_bonus": self.defense_bonus
        }

    @staticmethod
    def from_dict(data):
        return PassiveSkill(**data)


# ========== Kelas untuk CharacterClass ========== #
class CharacterClass:
    def __init__(self, name, active_skill, passive_skill):
        self.name = name
        self.active_skill = active_skill
        self.passive_skill = passive_skill

    def use_active_skill(self):
        return self.active_skill.use()

    def activate_passive(self):
        self.passive_skill.activate()

    def update_passive(self):
        self.passive_skill.update()
    def display_info(self):
        """Menampilkan informasi karakter dan skill"""
        separator = "=" * 40
        
        print(f"\n{separator}\nCLASS INFO\n{separator}")
        print(f"Class           : {self.name}\n")
        
        print(f"{separator}\nACTIVE SKILL\n{separator}")
        print(f"Skill Name      : {self.active_skill.name}")
        print(f"Description     : {self.active_skill.description}")
        print(f"Cooldown        : {self.active_skill.cooldown} turn(s)")
        print(f"AOE             : {'Yes' if self.active_skill.aoe else 'No'}")
        print(f"Damage Multiplier : {self.active_skill.damage_multiplier * 100}%\n")
        
        print(f"{separator}\nPASSIVE SKILL\n{separator}")
        print(f"Skill Name      : {self.passive_skill.name}")
        print(f"Description     : {self.passive_skill.description}")
        print(f"Effect Duration : {self.passive_skill.effect_duration} turn(s)")
        print(f"Cooldown        : {self.passive_skill.cooldown} turn(s)")
        print(f"Strength Bonus  : {self.passive_skill.strength_bonus}%")
        print(f"Defense Bonus   : {self.passive_skill.defense_bonus}\n")

    
    def to_dict(self):
        # Mengonversi karakter class ke dalam dictionary yang dapat diserialisasi
        return {
            "name": self.name,
            "active_skill": self.active_skill.to_dict(),
            "passive_skill": self.passive_skill.to_dict(),
        }

    @staticmethod
    def from_dict(data, class_data):
        # Memuat class dari dictionary
        active_skill = Skill(**data['active_skill'])
        passive_skill = PassiveSkill(**data['passive_skill'])
        return CharacterClass(data['name'], active_skill, passive_skill)

    
def load_class():
    """Memuat data class dari file JSON."""
    with open("class_player.json", "r") as file:
        class_data = json.load(file)  # Membaca file JSON dan memuatnya ke dalam dictionary
    return class_data

# ========== Fungsi untuk Memuat Data dari JSON ========== #
def load_character_class(class_name):
    """Memuat class karakter dari JSON."""
    data = load_class()
    class_data = data["classes"].get(class_name)
    if not class_data:
        raise ValueError(f"Class {class_name} tidak ditemukan!")

    active_skill_data = class_data["active_skill"]
    passive_skill_data = class_data["passive_skill"]

    active_skill = Skill(
        active_skill_data["name"],
        active_skill_data["description"],
        active_skill_data["cooldown"],
        active_skill_data["damage_multiplier"],
        active_skill_data["aoe"]
    )

    passive_skill = PassiveSkill(
        passive_skill_data["name"],
        passive_skill_data["description"],
        passive_skill_data["effect_duration"],
        passive_skill_data["cooldown"],
        passive_skill_data["strength_bonus"],
        passive_skill_data["defense_bonus"]
    )

    return CharacterClass(class_name, active_skill, passive_skill)