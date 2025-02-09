from UI.Hooks import get_stat_from_effect
# ========== Handler untuk Passive Skill ========== #

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

    
    def reset_cooldown_and_duration(self):
        """Reset cooldown & durasi skill menjadi 0"""
        self.remaining_cooldown = 0
        self.remaining_duration = 0
    
    def _remove_effect(self, player):
        """Menghapus efek yang diberikan oleh skill"""
        for effect_type, bonuses in player.buffs.items():
            stat_attr = get_stat_from_effect(effect_type)
            
            if stat_attr is None:
                continue  # Lewati jika tidak dikenali

            for bonus in bonuses:
                player.stats.__dict__[stat_attr] -= bonus["value"]  # Kurangi efek yang disimpan

            # Kosongkan daftar buff yang sudah dihapus
            player.buffs[effect_type] = []

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
        self.event_dispatcher.register_event("turn_end", self.on_turn_end)
        self.event_dispatcher.register_event("battle_end", self._on_battle_end)

    def _on_game_start(self, **kwargs):
        """Trigger ketika game dimulai"""
        self._apply_skill_effect("on_battle_start", **kwargs)
        self.player.skill_handler.activate_passive()  # Aktifkan skill pasif pemain

    def _on_enemy_defeat(self, **kwargs):
        """Trigger ketika musuh mati"""
        self._apply_skill_effect("enemy_defeat", **kwargs)

    def _on_player_hit(self, **kwargs):
        """Trigger ketika pemain terkena serangan musuh"""
        self._apply_skill_effect("player_hit", **kwargs)
    
    def _on_battle_end(self, **kwargs):
        """Menonaktifkan semua skill pasif setelah pertarungan berakhir"""
        self.player.skill_handler.reset_passive(self.player)
        # Reset efek yang diterapkan oleh skill
        

    def on_turn_end(self, **kwargs):
        """Update semua passive skill yang masih aktif"""
        if not isinstance(self.passive_skills, list):
            self.passive_skills = [self.passive_skills]
        active_skills = [skill for skill in self.passive_skills if skill.is_active]
        if not active_skills:
            return
        if self.event_dispatcher.is_event_triggered("battle_end"):  # 🔥 Cek apakah battle sudah selesai
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
                handler(**effect_data,effect_type=effect_type, **kwargs)
            else:
                # Jika hanya berupa angka langsung, tetap panggil handler
                handler(effect_data,effect_type=effect_type, **kwargs)

    def _restore_mana(self, amount, effect_type, restore_type="flat"):
        if restore_type == "percentage":
            restored_mana = round((self.player.stats.max_mp * amount) / 100)
        else:
            restored_mana = amount
        self.player.stats.mp = min(self.player.stats.mp + restored_mana, self.player.stats.max_mp)


    def _boost_attack(self, amount, effect_type,bonus_type="flat",**kwargs):
        if bonus_type == "percentage":
            bonus_value = round((self.player.stats.attack * amount) / 100)  # 🔥 Hitung berdasarkan persen
        else:
            bonus_value = amount  # 🔥 Tambahkan nilai tetap

        if effect_type not in self.player.buffs:
            self.player.buffs[effect_type] = []

        self.player.buffs[effect_type].append({
            "amount": amount,
            "bonus_type": bonus_type,
            "value": bonus_value
        })
        self.player.stats.attack += bonus_value
        
    def _boost_def(self, amount,effect_type, bonus_type="flat",**kwargs):
        if bonus_type == "percentage":
            bonus_value = round((self.player.stats.defense * amount) / 100)  # 🔥 Hitung berdasarkan persen
        else:
            bonus_value = amount  # 🔥 Tambahkan nilai tetap
            
        if effect_type not in self.player.buffs:
            self.player.buffs[effect_type] = []

        self.player.buffs[effect_type].append({
            "amount": amount,
            "bonus_type": bonus_type,
            "value": bonus_value
        })
        self.player.stats.defense += bonus_value
        