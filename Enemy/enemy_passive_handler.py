from Hooks.Hooks import remove_effect, after_effect
class Enemy_passive:
    def __init__(self, enemy, event_dispatcher):
        self.enemy = enemy
        self.event_dispatcher = event_dispatcher
        self._register_event_handlers()
        self._isDeath = False
    
    # Getter
    @property
    def isDeath(self):
        return self._isDeath

    # Setter
    @isDeath.setter
    def isDeath(self, value: bool):
        self._isDeath = value


    def _register_event_handlers(self):
        """Mendaftarkan semua event dan handler yang relevan"""
        # self.event_dispatcher.register_event("game_start", self._on_game_start)
        # self.event_dispatcher.register_event("enemy_defeat", self._on_enemy_defeat)
        # self.event_dispatcher.register_event("player_hit", self._on_player_hit)
        # self.event_dispatcher.register_event("enemy_hit", self._on_enemy_hit)
        self.event_dispatcher.register_event("turn_end", self._on_turn_end)
        self.event_dispatcher.register_event("battle_end", self._on_battle_end)
        # self.event_dispatcher.register_event("turn_interval", self._on_turn_interval)
        # self.event_dispatcher.register_event("enemy_hp_threshold", self._on_enemy_hp_threshold)
    
    def _on_turn_end(self, **kwargs):
        if self.isDeath:
            return  # Musuh sudah mati, tidak perlu melanjutkan
        if self.enemy.buffs:
            for effect_type, bonus in self.enemy.buffs.items():
                if bonus.get("duration", 0) > 0:
                    after_effect(self.enemy, effect_type, bonus)
                    
        if self.enemy.debuffs:
            for effect_type, penalty in self.enemy.debuffs.items():
                if penalty.get("duration", 0) > 0:
                    after_effect(self.enemy, effect_type, penalty)

    def _on_battle_end(self, **kwargs):
        if self.isDeath:
            return  # Musuh sudah mati, tidak perlu membersihkan efek
        if self.enemy.buffs:
            for effect_type, bonus in self.enemy.buffs.items():
                if bonus.get("duration", 0) > 0:
                    remove_effect(self.enemy, effect_type)
                    
        if self.enemy.debuffs:
            for effect_type, penalty in self.enemy.debuffs.items():
                if penalty.get("duration", 0) > 0:
                    remove_effect(self.enemy, effect_type)

