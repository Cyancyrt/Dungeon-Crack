
### enemy_combat.py

import math

class EnemyCombatMixin:
    def evade_chance(self, player):
        if player.buffs.get("invisible", False):
            print(f"{player.name} menghindari semua serangan karena invisible!")
            return 0
        return 1

    def defense_calc(self, player, damage):
        reduction_status = player.buffs.get("damage_reduction", {}).get("amount", 0)
        damage_reduction = math.ceil(player.stats.defense * (0.05 + reduction_status))
        return max(damage - damage_reduction, 0)

    def attack_player(self, player, is_defending=False):
        if self.evade_chance(player) == 0:
            print(f"{player.name} evaded the attack!")
            return 0
        damage = self.stats.attack
        damage = self.defense_calc(player, damage)
        if "barrier" in player.buffs:
            barrier = player.buffs["barrier"]
            if barrier["amount"] >= damage:
                barrier["amount"] -= damage
                damage = 0
            else:
                damage -= barrier["amount"]
                barrier["amount"] = 0

        player.stats.hp -= damage
        print(f"{self.name} menyerang {player.name}, mengurangi {damage} HP!")
