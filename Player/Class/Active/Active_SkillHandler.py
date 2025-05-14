from Core_Mechanics.Effect.buff_debuff import StatusHandler, Buff, Debuff
from Player.Class.Loader import load_active_skills
from Exception.battle_exception import SkillNotFound, InsufficientMP, SkillOnCooldown, InvalidSkillEffect, InvalidTargetForEffect

class ActiveSkillHandler:
    def __init__(self, player, event_dispatcher=None):
        self.player = player
        self.active_skills = player.active_skills  # List skill aktif yang dimiliki pemain
        self.cooldowns = {}  # 🔥 Menyimpan cooldown setiap skill
        self.event_dispatcher = event_dispatcher
        self._register_event_handlers()
        
    def _register_event_handlers(self):
        """Mendaftarkan semua event dan handler yang relevan"""
        self.event_dispatcher.register_event("skill_activated", self._on_skill_activated)
        self.event_dispatcher.register_event("turn_end", self._on_turn_end)
        self.event_dispatcher.register_event("battle_end", self._on_battle_end)
    
    def _on_skill_activated(self, **kwargs):
        try:
            active_skills = load_active_skills()

            # Pastikan self.active_skills adalah list
            if not isinstance(self.active_skills, list):
                self.active_skills = [self.active_skills]

            for name, data in active_skills.items():
                # Mencari skill aktif milik player yang cocok namanya
                skill = next((s for s in self.active_skills if s.name == name), None)
                if skill:
                    self._apply_skill_effect(skill)
        except Exception as e:
            print(f"[ERROR] _on_enemy_hit: {str(e)}")
            raise e

    def _on_turn_end(self, **kwargs):
        try:
            self.reduce_cooldown()
        except Exception as e:
            print(f"[ERROR] _on_turn_end: {str(e)}")
            raise e
    
    def _on_battle_end(self, **kwargs):
        try:
            self.reset_cooldown()
        except Exception as e:
            print(f"[ERROR] _on_battle_end: {str(e)}")
            raise e

    def _check_active_skill(self, skill_name, skill):
        """Cek apakah skill bisa digunakan"""
        try:
            if self.cooldowns.get(skill_name, 0) > 0:
                raise SkillOnCooldown(f"Skill {skill_name} masih cooldown {self.cooldowns[skill_name]} turn lagi!")
            
            if self.player.stats.mp < skill.mana_cost:
                raise InsufficientMP(f"MP tidak cukup untuk menggunakan {skill_name}!")
                
            return True
        except (SkillOnCooldown, InsufficientMP) as e:
            print(f"[ERROR] _check_active_skill: {str(e)}")
            return False

    def use_skill(self, skill_name, enemy):
        """Menggunakan skill aktif pada target"""
        try:
            if not isinstance(self.active_skills, list):
                self.active_skills = [self.active_skills]
            if enemy:
                self.enemy = enemy
            
            skill = next((s for s in self.active_skills if s.name == skill_name), None)
            if not skill:
                raise SkillNotFound(f"Skill {skill_name} tidak ditemukan!")

            check = self._check_active_skill(skill_name, skill)
            if not check:
                return False

            if skill.effect:
                self._apply_skill_effect(skill)

            # 🔥 Gunakan skill
            self.cooldowns[skill_name] = skill.cooldown  # Menggunakan cooldown yang sudah benar tanpa tambahan +1
            return skill.damage_multiplier
        except SkillNotFound as e:
            print(f"[ERROR] use_skill: {str(e)}")
        except Exception as e:
            print(f"[ERROR] use_skill: {str(e)}")


    def _apply_skill_effect(self, skill):
        """Menerapkan efek skill ke target"""
        try:
            if isinstance(skill, str):
                raise InvalidSkillEffect(f"Skill yang diteruskan adalah string, bukan objek skill yang valid.")

            if not hasattr(skill, 'effect'):
                raise InvalidSkillEffect(f"Skill {skill.name} tidak memiliki efek yang valid.")

            for effect_type, effect_value in skill.effect.items():
                self._handle_effect(effect_type, effect_value)
        except InvalidSkillEffect as e:
            print(f"[ERROR] _apply_skill_effect: {str(e)}")
            raise e
        except Exception as e:
            print(f"[ERROR] _apply_skill_effect: {str(e)}")
            raise e

    def _handle_effect(self, effect_type, effect_value, **kwargs):
        """Menangani efek skill seperti stun, heal, dll."""
        try:
            buff_handlers = Buff._buff_dict()
            debuff_handlers = Debuff._debuff_dict()
            effect_handlers = StatusHandler._status_effect_dict()
            handler = buff_handlers.get(effect_type) or debuff_handlers.get(effect_type) or effect_handlers.get(effect_type)
            
            if not handler:
                raise InvalidTargetForEffect(f"Target efek skill {effect_type} tidak ditemukan.")

            target = effect_value.get("target", self.player)  # Default ke self.player jika tidak ada target
            if target == "enemy":
                target = self.enemy
            if handler:
                if not effect_value.get("stackable") and effect_type in self.player.buffs:
                    return
                handler(effect_type, effect_value, target=target, **kwargs)
        except InvalidTargetForEffect as e:
            print(f"[ERROR] _handle_effect: {str(e)}")
        except Exception as e:
            print(f"[ERROR] _handle_effect: {str(e)}")
            raise e

    def reset_cooldown(self):
        """Reset cooldown setiap turn"""
        try:
            for skill in self.cooldowns:
                self.cooldowns[skill] = 0
        except Exception as e:
            print(f"[ERROR] reset_cooldown: {str(e)}")
            raise e
        
    def reduce_cooldown(self):
        """Mengurangi cooldown setiap turn"""
        try:
            for skill_name in list(self.cooldowns.keys()):  # Menggunakan list untuk menghindari perubahan pada dictionary saat iterasi
                if self.cooldowns[skill_name] > 0:
                    self.cooldowns[skill_name] -= 1
                # Menghapus skill dari cooldown jika cooldown-nya sudah habis
                if self.cooldowns[skill_name] == 0:
                    del self.cooldowns[skill_name]
        except Exception as e:
            print(f"[ERROR] reduce_cooldown: {str(e)}")
            raise e
