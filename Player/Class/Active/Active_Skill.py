class ActiveSkill:
    def __init__(self, name, description, cooldown, damage_multiplier=1.0, aoe=False, effects={},
                 mana_cost=0, stamina_cost=0, skill_type="physical"):
        self.name = name
        self.description = description
        self.cooldown = cooldown
        self.damage_multiplier = damage_multiplier
        self.aoe = aoe
        self.effect = effects  # 🔥 Menyimpan efek seperti "stun", "heal", dll.
        self.mana_cost = mana_cost
        self.stamina_cost = stamina_cost
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
    
