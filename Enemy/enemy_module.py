
### enemy_model.py

from Enemy.base_stats import Stats
from Enemy.enemy_leveling import EnemyLevelingMixin
from Enemy.enemy_combat import EnemyCombatMixin
from Enemy.enemy_info import EnemyInfoMixin
from Hooks.Event_Dispatch import EventDispatcher
from Enemy.enemy_passive_handler import Enemy_passive

class Enemy(EnemyLevelingMixin, EnemyCombatMixin, EnemyInfoMixin):
    def __init__(self, name, level_range, hp, atk, defense, agility, skill_name, skill_desc):
        self.name = name
        self.level_range = level_range
        self.level = None
        self.stats = Stats(hp, atk, defense, agility)
        self.skill_name = skill_name
        self.skill_desc = skill_desc
        self.buffs = {}
        self.debuffs = {}
        self.passive_skill_handler = Enemy_passive(self, EventDispatcher())

    @property
    def passive_skill_handler(self):
        return self._passive_skill_handler

    @passive_skill_handler.setter
    def passive_skill_handler(self, new_handler):
        self._passive_skill_handler = new_handler

    def mark_as_dead(self):
        self.passive_skill_handler.isDeath = True
