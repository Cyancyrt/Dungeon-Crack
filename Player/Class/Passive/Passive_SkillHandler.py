from Hooks.Hooks import after_effect
from Core_Mechanics.Effect.buff_debuff import StatusHandler, Buff, Debuff
from Hooks.Hooks import remove_effect
from Exception.battle_exception import EventNotRegisteredError, InvalidSkillEffect, SkillHandlerNotFoundError

class PassiveSkillHandler:
    def __init__(self, player, event_dispatcher=None):
        self.player = player
        self.passive_skills = player.passive_skills
        self.ActivatedPassive = []
        self.cooldowns = {}
        self.durations = {}
        self.event_dispatcher = event_dispatcher

        if not self.event_dispatcher:
            raise EventNotRegisteredError("Event dispatcher must be provided to PassiveSkillHandler.")
        
        try:
            self._register_event_handlers()
        except Exception as e:
            raise EventNotRegisteredError(f"Failed to register events: {e}")

    def _register_event_handlers(self):
        self.event_dispatcher.register_event("battle_start", self._on_battle_start)
        self.event_dispatcher.register_event("enemy_defeat", self._on_enemy_defeat)
        self.event_dispatcher.register_event("player_hit", self._on_player_hit)
        self.event_dispatcher.register_event("enemy_hit", self._on_enemy_hit)
        self.event_dispatcher.register_event("turn_end", self._on_turn_end)
        self.event_dispatcher.register_event("battle_end", self._on_battle_end)
        self.event_dispatcher.register_event("turn_interval", self._on_turn_interval)
        self.event_dispatcher.register_event("enemy_hp_threshold", self._on_enemy_hp_threshold)

    def update_passive(self):
        """Perbarui durasi dan cooldown semua skill pasif serta hapus efek yang expired."""
        try:
            for skill in self.passive_skills:
                name = skill.name  # akses menggunakan dot notation

                # Kurangi durasi aktif
                if self.durations.get(name, 0) > 0:
                    self.durations[name] -= 1
                    if self.durations[name] == 0:
                        print(f"🔻Efek pasif {name} telah berakhir.")
                        self.cooldowns[name] = getattr(skill, "cooldown", 0)

                # Kurangi cooldown
                if self.cooldowns.get(name, 0) > 0:
                    self.cooldowns[name] -= 1

            for effect_type, bonus in list(self.player.buffs.items()):
                if bonus.get("duration", 0) > 0:
                    print(bonus.get("just_applied"))
                    if bonus.get("just_applied"):
                        bonus["just_applied"] = False  # Hanya set sekali
                    else :
                        bonus["duration"] -= 1
                        if bonus["duration"] == 0:
                            remove_effect(self.player, effect_type)

            for effect_type, bonus in list(self.player.debuffs.items()):
                if bonus.get("duration", 0) > 0:
                    bonus["duration"] -= 1
                    if bonus["duration"] == 0:
                        remove_effect(self.player, effect_type)

        except Exception as e:
            raise RuntimeError(f"[ERROR] Failed to update passive skills: {e}")
        

    def activate_passive(self, **kwargs):
        """Aktifkan semua passive skill yang siap digunakan."""
        try:
            for skill in self.passive_skills:
                name = skill.name
                self.cooldowns.setdefault(name, 0)
                self.durations.setdefault(name, 0)

                if self.cooldowns[name] == 0 and self.durations[name] == 0:
                    # Pakai getattr dengan nilai default sebagai pengganti .get()
                    self.durations[name] = getattr(skill, "duration", 1)

                    if "next_turn" in getattr(skill, "activation_condition", []):
                        self.durations[name] += 1

                    cooldown_val = getattr(skill, "cooldown", 0)
                    self.cooldowns[name] = cooldown_val + 1 if cooldown_val > 0 else 0

                    print(f"\n🔥Pasif {name} Aktif! {getattr(skill, 'description', '')}.")
                    self.ActivatedPassive.append(name)
                    self._apply_effects_from_skill(skill,**kwargs)

        except Exception as e:
            raise RuntimeError(f"[ERROR] Failed to activate passive skill '{name}': {e}")
        
    
    def _on_battle_start(self, **kwargs):
        try:
            self._apply_skill_effect("on_battle_start", **kwargs)
        except Exception as e:
            print(f"[ERROR] _on_battle_start failed: {e}")

    def _on_enemy_defeat(self, **kwargs):
        try:
            self._apply_skill_effect("enemy_defeat", **kwargs)
        except Exception as e:
            print(f"[ERROR] _on_enemy_defeat failed: {e}")

    def _on_player_hit(self, **kwargs):
        try:
            self._apply_skill_effect("on_player_hit", **kwargs)
        except Exception as e:
            print(f"[ERROR] _on_player_hit failed: {e}")

    def _on_enemy_hit(self, **kwargs):
        try:
            self._apply_skill_effect("on_enemy_hit", **kwargs)
        except Exception as e:
            print(f"[ERROR] _on_enemy_hit failed: {e}")

    def _on_turn_end(self, **kwargs):
        try:
            if not hasattr(self.player, "skill_handler"):
                raise SkillHandlerNotFoundError("Player has no skill_handler assigned.")

            self.update_passive()

            if self.player.debuffs:
                for effect_type, bonus in self.player.debuffs.items():
                    if bonus.get("duration", 0) > 0:
                        after_effect(self.player, effect_type, bonus)

            self._apply_skill_effect("turn_end", **kwargs)
        except Exception as e:
            print(f"[ERROR] _on_turn_end failed: {e}")

    def _on_enemy_hp_threshold(self, **kwargs):
        try:
            self._apply_skill_effect("enemy_hp_threshold", **kwargs)
        except Exception as e:
            print(f"[ERROR] _on_enemy_hp_threshold failed: {e}")

    def _on_turn_interval(self, turn, **kwargs):
        try:
            if not isinstance(self.passive_skills, list):
                self.passive_skills = [self.passive_skills]
            
            for skill in self.passive_skills:
                if "turn_interval" in skill.activation_condition:
                    interval = skill.activation_condition.get("turn_interval", 1)
                    if turn % interval == 0:
                        self._apply_skill_effect("turn_interval", **kwargs)
        except Exception as e:
            print(f"[ERROR] _on_turn_interval failed: {e}")

    def _on_battle_end(self, **kwargs):
        try:
            if not hasattr(self.player, "skill_handler"):
                raise SkillHandlerNotFoundError("Player has no skill_handler assigned.")
            
            self.update_passive(self.player)
        except Exception as e:
            print(f"[ERROR] _on_battle_end failed: {e}")

    def _apply_skill_effect(self, event_type, **kwargs):
        if not isinstance(self.passive_skills, list):
            self.passive_skills = [self.passive_skills]

        
        for skill in self.passive_skills:
            try:
                name = skill.name

                if event_type not in skill.activation_condition:
                    # print(f"[INFO] Event '{event_type}' tidak memicu skill '{name}'.")
                    continue

                if skill.is_stack:
                    # print(f"[INFO] Skill '{name}' bertipe stackable, dilewati dalam fase aktivasi pasif.")
                    continue

                # Inisialisasi jika belum ada
                self.cooldowns.setdefault(name, 0)
                self.durations.setdefault(name, 0)

                if self.cooldowns[name] == 0 and self.durations[name] == 0:
                    self.activate_passive(**kwargs)                
                else:
                    print(f"[INFO] Skill '{name}' dalam cooldown ({self.cooldowns[name]}) atau durasi habis ({self.durations[name]}).")

            except (InvalidSkillEffect, SkillHandlerNotFoundError) as e:
                print(f"[WARNING] Gagal menerapkan skill pasif '{name}': {e}")

    def _apply_effects_from_skill(self, skill, **kwargs):
        if not hasattr(self.player, "skill_handler"):
            raise SkillHandlerNotFoundError("Player has no skill_handler assigned.")
        
        for effect_type, effect_value in skill.effect.items():
            print(f"[INFO] Menerapkan efek dari skill '{skill.name}': {effect_type} = {effect_value}")
            self._handle_effect(effect_type, effect_value, **kwargs)


    def _handle_effect(self, effect_type, effect_value, **kwargs):
        buff_handlers = Buff._buff_dict()
        debuff_handlers = Debuff._debuff_dict()
        effect_handlers = StatusHandler._status_effect_dict()

        handler = buff_handlers.get(effect_type) or debuff_handlers.get(effect_type) or effect_handlers.get(effect_type)

        target = effect_value.get("target", self.player)

        for skill in self.passive_skills:
            if "duration" not in effect_value:
                effect_value["duration"] = skill.effect_duration

        if not handler:
            raise InvalidSkillEffect(f"No handler found for effect type '{effect_type}'.")

        if effect_value.get("stackable", "False") == "False" and effect_type in self.player.buffs:
            return

        try:
            handler(effect_type, effect_value, target=target, **kwargs)
        except Exception as e:
            raise InvalidSkillEffect(f"Failed to apply effect '{effect_type}': {e}")
