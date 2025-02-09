from UI.Hooks import get_stat_from_effect, EventDispatcher
# ========== Kelas untuk Skill ========== #

class ActiveSkill:
    def __init__(self, name, description, cooldown, damage_multiplier=1.0, aoe=False, 
                 mana_cost=0, stamina_cost=0, effect=None, skill_type="physical"):
        self.name = name
        self.description = description
        self.cooldown = cooldown
        self.damage_multiplier = damage_multiplier
        self.aoe = aoe
        self.mana_cost = mana_cost
        self.stamina_cost = stamina_cost
        self.effect = effect or {}  # 🔥 Menyimpan efek seperti "stun", "heal", dll.
        self.skill_type = skill_type  # 🔥 Bisa "physical", "magical", atau "hybrid"

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "cooldown": self.cooldown,
            "damage_multiplier": self.damage_multiplier,
            "aoe": self.aoe,
            "mana_cost": self.mana_cost,
            "stamina_cost": self.stamina_cost,
            "effect": self.effect,
            "skill_type": self.skill_type
        }

    @staticmethod
    def from_dict(data):
        return ActiveSkill(**data)
    
class ActiveSkillHandler:
    def __init__(self, player, event_dispatcher=None):
        self.player = player
        self.active_skills = player.active_skills  # List skill aktif yang dimiliki pemain
        self.cooldowns = {}  # 🔥 Menyimpan cooldown setiap skill
        self.event_dispatcher = event_dispatcher
        self._register_event_handlers()
        
    

    def _register_event_handlers(self):
        """Mendaftarkan semua event dan handler yang relevan"""
        self.event_dispatcher.register_event("enemy_defeat", self._on_enemy_defeat)
        self.event_dispatcher.register_event("turn_end", self._on_turn_end)

    def _on_enemy_defeat(self, **kwargs):
        """Trigger ketika musuh mati"""
        for skill_name in self.cooldowns:
            if self.cooldowns[skill_name] > 0:
                self.cooldowns[skill_name] = 0
        # self._apply_skill_effect("enemy_defeat", **kwargs)

    def _on_turn_end(self, **kwargs):
        self.reduce_cooldown()
        # self._apply_skill_effect("turn_end", **kwargs)

    def use_skill(self, skill_name, target=None):
        """Menggunakan skill aktif pada target"""
        if not isinstance(self.active_skills, list):
             self.active_skills = [self.active_skills]
        
        skill = next((s for s in self.active_skills if s.name == skill_name), None)


        # if not skill:
        #     print(f"Skill {skill_name} tidak ditemukan!")
        #     return False

        if self.cooldowns.get(skill_name, 0) > 0:
            print(f"Skill {skill_name} masih cooldown {self.cooldowns[skill_name]} turn lagi!")
            return False

        if self.player.stats.mp < skill.mana_cost:
            print(f"MP tidak cukup untuk menggunakan {skill_name}!")
            return False

        # # 🔥 Gunakan skill
        # self._apply_skill_effect(skill, target)
        self.cooldowns[skill_name] = skill.cooldown + 1  # Set cooldown setelah penggunaan
        return True

    def _apply_skill_effect(self, skill, target=None):
        """Menerapkan efek skill ke target"""
        damage = self.player.stats.attack * skill.damage_multiplier
        target.stats.hp -= damage
        print(f"{target.name} menerima {damage} damage dari {skill.name}!")

        # 🔥 Jika ada efek tambahan, terapkan
        for effect_type, effect_value in skill.effect.items():
            self._handle_effect(target, effect_type, effect_value)

    def _handle_effect(self, target, effect_type, effect_value):
        """Menangani efek skill seperti stun, heal, dll."""
        if effect_type == "stun":
            target.stunned = True
            print(f"{target.name} terkena stun selama {effect_value} turn!")
        elif effect_type == "heal":
            target.stats.hp = min(target.stats.hp + effect_value, target.stats.max_hp)
            print(f"{target.name} mendapatkan {effect_value} HP!")
        elif effect_type == "buff":
            target.buffs.append(effect_value)
            print(f"{target.name} mendapatkan buff {effect_value}!")

    
    def reduce_cooldown(self):
        """Mengurangi cooldown setiap turn"""
        for skill_name in self.cooldowns:
            if self.cooldowns[skill_name] > 0:
                self.cooldowns[skill_name] -= 1

# class ActiveSkill:
#     def __init__(self, name, description, cooldown, damage_multiplier=1.0, aoe=False, mana_cost=0, stamina_cost=0):
#         self.name = name
#         self.description = description
#         self.cooldown = cooldown
#         self.remaining_cooldown = 0
#         self.damage_multiplier = damage_multiplier
#         self.aoe = aoe
#         self.mana_cost = mana_cost
#         self.stamina_cost = stamina_cost

#     def use(self):
#         if self.remaining_cooldown == 0:
#             self.remaining_cooldown = self.cooldown
#             return self.damage_multiplier
#         else:
#             print(f"❌ Skill {self.name} masih cooldown {self.remaining_cooldown} turn lagi.")
#             return False

#     def reduce_cooldown(self):
#         if self.remaining_cooldown > 0:
#             self.remaining_cooldown -= 1
#     def reset_cooldown(self):
#         self.remaining_cooldown = 0

#     def to_dict(self):
#         return {
#             "name": self.name,
#             "description": self.description,
#             "cooldown": self.cooldown,
#             "damage_multiplier": self.damage_multiplier,
#             "aoe": self.aoe
#         }

#     @staticmethod
#     def from_dict(data):
#         return ActiveSkill(**data)

