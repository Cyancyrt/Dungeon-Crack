from Player.Class.Active_Skill import ActiveSkill
from Player.Class.Passive_skill import PassiveSkill
from Player.Class.Loader import load_class, load_active_skills, load_passive_skills



# ========== Kelas untuk CharacterClass ========== #
class CharacterClass:
    def __init__(self, name, active_skill, passive_skill):
        self.name = name
        self.active_skill = active_skill
        self.passive_skill = passive_skill

    

    def display_info(self):
        """Menampilkan informasi karakter dan skill"""
        if not isinstance(self.passive_skill, list):
            self.passive_skill = [self.passive_skill] 
        separator = "=" * 40
        
        print(f"\n{separator}\nCLASS INFO\n{separator}")
        print(f"Class           : {self.name}\n")
        
        print(f"{separator}\nACTIVE SKILL\n{separator}")
        print(f"Skill Name      : {self.active_skill.name}")
        print(f"Description     : {self.active_skill.description}")
        print(f"Cooldown        : {self.active_skill.cooldown} turn(s)")
        print(f"AOE             : {'Yes' if self.active_skill.aoe else 'No'}")
        print(f"Damage Multiplier : {self.active_skill.damage_multiplier * 100}%\n")
        for skill in self.passive_skill:
            print(f"{separator}\nPASSIVE SKILL\n{separator}")
            print(f"Skill Name      : {skill.name}")
            print(f"Description     : {skill.description}")
            print(f"Effect Duration : {skill.effect_duration} turn(s)")
            print(f"Cooldown        : {skill.cooldown} turn(s)")

    
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
        active_skill = ActiveSkill(**data['active_skill'])
        passive_skill = PassiveSkill(**data['passive_skill'])
        return CharacterClass(data['name'], active_skill, passive_skill)

    
# ========== Fungsi untuk Memuat Data dari JSON ========== #
def load_character_class(class_name):
    """Memuat class karakter beserta skill aktif dan pasifnya."""
    class_data = load_class()["classes"].get(class_name)
    if not class_data:
        raise ValueError(f"Class {class_name} tidak ditemukan!")

    # Memuat data skill dari file terpisah
    active_skills = load_active_skills()
    passive_skills = load_passive_skills()

    # Ambil skill aktif berdasarkan nama
    active_skill_name = class_data["active_skill"]
    active_skill_data = active_skills.get(active_skill_name)
    if not active_skill_data:
        raise ValueError(f"Skill aktif {active_skill_name} tidak ditemukan!")

    # Ambil skill pasif berdasarkan nama
    passive_skill_name = class_data["passive_skill"]
    passive_skill_data = passive_skills.get(passive_skill_name)
    if not passive_skill_data:
        raise ValueError(f"Skill pasif {passive_skill_name} tidak ditemukan!")

    # Buat objek skill
    active_skill = ActiveSkill(
        active_skill_name,
        active_skill_data["description"],
        active_skill_data["cooldown"],
        active_skill_data["damage_multiplier"],
        active_skill_data["aoe"],
        mana_cost=active_skill_data.get("mana_cost", 0),  # Pastikan default ke 0
        stamina_cost=active_skill_data.get("stamina_cost", 0)  # Pastikan default ke 0
    )

    passive_skill = PassiveSkill(
        passive_skill_name,
        passive_skill_data.get("description", ""),  # Jika tidak ada, default ""
        passive_skill_data.get("duration", 0),  # Jika tidak ada, default 0
        passive_skill_data.get("cooldown", 0),  # Jika tidak ada, default 0
        passive_skill_data.get("activation_condition", []),  # Perbaikan di sini! 🛠
        passive_skill_data.get("effect", {})  # Jika tidak ada, default {}
    )



    return CharacterClass(class_name, active_skill, passive_skill)
