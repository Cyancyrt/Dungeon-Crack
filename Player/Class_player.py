import json
import time


def load_json(filename):
    """Memuat data dari file JSON."""
    with open(filename, "r") as file:
        return json.load(file)

def load_class():
    """Memuat data class dari file JSON."""
    return load_json("data/class_player.json")

def load_active_skills():
    """Memuat data skill aktif dari file JSON."""
    return load_json("data/active_skills.json")

def load_passive_skills():
    """Memuat data skill pasif dari file JSON."""
    return load_json("data/passive_skills.json")

# ========== Kelas untuk Skill ========== #
class Skill:
    def __init__(self, name, description, cooldown, damage_multiplier=1.0, aoe=False, mana_cost=0, stamina_cost=0):
        self.name = name
        self.description = description
        self.cooldown = cooldown
        self.remaining_cooldown = 0
        self.damage_multiplier = damage_multiplier
        self.aoe = aoe
        self.mana_cost = mana_cost
        self.stamina_cost = stamina_cost

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
    def reset_cooldown(self):
        self.remaining_cooldown = 0

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


class PassiveSkill:
    def __init__(self, name, description, effect_duration, cooldown, activation_condition, effect):
        self.name = name
        self.description = description
        self.effect_duration = effect_duration
        self.cooldown = cooldown
        self.activation_condition = activation_condition
        self.remaining_duration = 0
        self.remaining_cooldown = 0
        self.effect = effect  # Simpan semua efek dalam dictionary
        self.is_active = False
        self.effect_removed = False

    def activate(self):
        """Aktifkan skill jika cooldown sudah selesai."""
        print(self.remaining_cooldown, self.remaining_duration)
        if self.remaining_cooldown == 0 and self.remaining_duration == 0:
            self.is_active = True
            self.effect_removed = False 
            self.remaining_duration = self.effect_duration  # Set durasi efek skill
            self.remaining_cooldown = self.cooldown  # Set cooldown segera setelah aktivasi
            print(f"🔥 Pasif {self.name} Aktif! {self.description}.")

    def update(self, player):
        """Perbarui durasi & cooldown skill setiap turn."""

        if not self.is_active:
            print(f"Skill {self.name} tidak aktif.")
            return  # Jika skill tidak aktif, tidak ada perubahan
        
        if self.remaining_duration > 0:
            self.remaining_duration -= 1
            
            if self.remaining_duration == 0:  # Jika durasi habis, mulai cooldown
                self.is_active = False
                self.remaining_cooldown = self.cooldown
                if not self.effect_removed:  # 🔥 Pastikan efek hanya dihapus sekali
                    self._remove_effect(player)
                    self.effect_removed = True  # Set flag agar tidak dihapus lagi
        
        if self.remaining_cooldown > 0:
            self.remaining_cooldown -= 1  # Kurangi cooldown setiap turn
        else:
            print(f"  Cooldown sudah selesai.")

    
    def reset_cooldown_and_duration(self):
        """Reset cooldown & durasi skill menjadi 0"""
        self.remaining_cooldown = 0
        self.remaining_duration = 0
    
    def _remove_effect(self, player):
        """Menghapus efek yang diberikan oleh skill"""
        for effect_type, value in self.effect.items():
            if effect_type == "attack_bonus":
                player.stats.attack -= value  # Kembalikan attack ke semula
            elif effect_type == "defense_bonus":
                player.stats.defense -= value  # Kembalikan defense ke semula

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "effect_duration": self.effect_duration,
            "cooldown": self.cooldown,
            "activation_condition": self.activation_condition,
            "effect": self.effect
        }

    @staticmethod
    def from_dict(data):
        return PassiveSkill(
            data["name"],
            data["description"],
            data["effect_duration"],
            data["cooldown"],
            data["activation_condition"],
            data["effect"]
        )

# ========== Handler untuk Passive Skill ========== #
class PassiveSkillHandler:
    def __init__(self, player, event_dispatcher):
        self.player = player
        self.passive_skills = player.passive_skills
        self.event_dispatcher = event_dispatcher
        self._register_event_handlers()

    def _register_event_handlers(self):
        """Mendaftarkan semua event dan handler yang relevan"""
        self.event_dispatcher.register_event("game_start", self._on_game_start)
        self.event_dispatcher.register_event("enemy_defeat", self._on_enemy_defeat)
        self.event_dispatcher.register_event("player_hit", self._on_player_hit)
        self.event_dispatcher.register_event("battle_end", self._on_battle_end)

    def _on_game_start(self, **kwargs):
        """Trigger ketika game dimulai"""
        self._apply_skill_effect("on_battle_start", **kwargs)
        self.player.activate_passive_skill()  # Aktifkan skill pasif pemain

    def _on_enemy_defeat(self, **kwargs):
        """Trigger ketika musuh mati"""
        self._apply_skill_effect("enemy_defeat", **kwargs)

    def _on_player_hit(self, **kwargs):
        """Trigger ketika pemain terkena serangan musuh"""
        self._apply_skill_effect("player_hit", **kwargs)
    
    def _on_battle_end(self, **kwargs):
        """Menonaktifkan semua skill pasif setelah pertarungan berakhir"""
        self.player.skill.reset_passive(self.player)
        self.player.reset_skill_cooldown()
        # Reset efek yang diterapkan oleh skill
        

    def update_all_skills(self, event_dispatcher):
        """Update semua passive skill yang masih aktif"""
        if not isinstance(self.passive_skills, list):
            self.passive_skills = [self.passive_skills]
        active_skills = [skill for skill in self.passive_skills if skill.is_active]
        if not active_skills:
            return
        if event_dispatcher.is_event_triggered("battle_end"):  # 🔥 Cek apakah battle sudah selesai
            for skill in self.passive_skills:
                skill.reset_passive(self.player)
            return
        
        for skill in active_skills:
            skill.update(self.player)

    def _apply_skill_effect(self, event_type, **kwargs):
        """Apply skill effects berdasarkan event"""
        # Pastikan passive_skills adalah list, meskipun hanya satu skill
        if not isinstance(self.passive_skills, list):
            self.passive_skills = [self.passive_skills]  # Ubah menjadi list jika hanya satu skill

        # Loop untuk banyak skill
        for skill in self.passive_skills:
            if event_type in skill.activation_condition:  # Cek apakah event_type ada dalam activation_condition
                effect = skill.effect
                for effect_type, effect_value in effect.items():
                    if isinstance(effect_value, dict):  # Jika efek memiliki struktur dictionary (nested)
                        self._handle_effect(effect_type, effect_value, **kwargs)
                  

    def _handle_effect(self, effect_type, effect_data, **kwargs):
        """Menangani berbagai efek skill berdasarkan jenis efek dan data yang diberikan"""
        
        effect_handlers = {
            "mana_restore": self._restore_mana,
            "attack_bonus": self._boost_attack,
            "defense_bonus": self._boost_def,
            # "hp_regeneration": self._regenerate_hp,
            # "critical_chance_boost": self._increase_crit_chance,
            # Tambahkan efek lainnya di sini jika diperlukan
        }

        handler = effect_handlers.get(effect_type)  # Ambil fungsi berdasarkan effect_type
        if handler:
            if isinstance(effect_data, dict):
                # Jika `effect_data` adalah dictionary, gunakan detail spesifik
                handler(**effect_data, **kwargs)
            else:
                # Jika hanya berupa angka langsung, tetap panggil handler
                handler(effect_data, **kwargs)

    def _restore_mana(self, amount, restore_type="flat"):
        mana_used = self.player.skill.active_skill.mana_cost
        if restore_type == "percentage":
            restored_mana = round((mana_used * amount) / 100)
        else:
            restored_mana = amount

        self.player.stats.mp = min(self.player.stats.mp + restored_mana, self.player.stats.max_mp)


    def _boost_attack(self, amount, bonus_type="flat",**kwargs):
        if bonus_type == "percentage":
            bonus_value = round((self.player.stats.attack * amount) / 100)  # 🔥 Hitung berdasarkan persen
        else:
            bonus_value = amount  # 🔥 Tambahkan nilai tetap

        self.player.stats.attack += bonus_value
        print(f"⚔️ Attack naik: {bonus_value} ({bonus_type})")
        
    def _boost_def(self, amount, bonus_type="flat",**kwargs):
        if bonus_type == "percentage":
            bonus_value = round((self.player.stats.defense * amount) / 100)  # 🔥 Hitung berdasarkan persen
        else:
            bonus_value = amount  # 🔥 Tambahkan nilai tetap

        self.player.stats.defense += bonus_value
        print(f"🛡️ Defense naik: {bonus_value} ({bonus_type})")
        




# ========== Kelas untuk CharacterClass ========== #
class CharacterClass:
    def __init__(self, name, active_skill, passive_skill):
        self.name = name
        self.active_skill = active_skill
        self.passive_skill = passive_skill

    def use_active_skill(self):
        return self.active_skill.use()

    def activate_passive(self):
        if not isinstance(self.passive_skill, list):
            self.passive_skill = [self.passive_skill]  # Ubah menjadi list jika hanya satu skill

        # Loop untuk mengaktifkan semua skill pasif
        for skill in self.passive_skill:
            skill.activate()

    def update_passive(self, player):
        if not isinstance(self.passive_skill, list):
            self.passive_skill = [self.passive_skill]  # Ubah menjadi list jika hanya satu skill

        # Loop untuk memperbarui semua skill pasif
        for skill in self.passive_skill:
            skill.update(player)

    def reset_passive(self, player):
        if not isinstance(self.passive_skill, list):
            self.passive_skill = [self.passive_skill]  # Ubah menjadi list jika hanya satu skill

        # Loop untuk mereset semua skill pasif
        for skill in self.passive_skill:
            if not skill.effect_removed:  # 🔥 Pastikan efek hanya dihapus sekali
                skill._remove_effect(player)
                skill.effect_removed = True
            skill.is_active = False
            skill.reset_cooldown_and_duration()

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
        active_skill = Skill(**data['active_skill'])
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
    active_skill = Skill(
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