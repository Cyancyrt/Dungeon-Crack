# ========== Handler untuk Passive Skill ========== #

class PassiveSkill:
    def __init__(self, name, description, effect_duration, cooldown, activation_condition, effect):
        self.name = name
        self.description = description
        self.duration = effect_duration
        self.cooldown = cooldown
        self.activation_condition = activation_condition
        self.effect = effect  # Simpan semua efek dalam dictionary
        self.is_active = False
        self.is_stack = False

    
    def reset_cooldown_and_duration(self):
        """Reset cooldown & durasi skill menjadi 0"""
        self.is_stack = False
        self.remaining_cooldown = 0
        self.remaining_duration = 0
    

            

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
    

    
