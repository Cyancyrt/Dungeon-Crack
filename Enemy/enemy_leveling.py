### enemy_leveling.py

import random
from collections import Counter

class EnemyLevelingMixin:
    def set_level(self):
        if isinstance(self.level_range, list) and len(self.level_range) == 2:
            random_levels = [random.randint(*self.level_range) for _ in range(100)]
            level_counts = Counter(random_levels)
            self.level = level_counts.most_common(1)[0][0]

    def set_attributes(self):
        for attr in ['hp', 'attack', 'defense', 'agility']:
            stat = getattr(self.stats, attr)
            if isinstance(stat, list) and len(stat) == 2:
                value = random.randint(stat[0], stat[1])
                setattr(self.stats, attr, value)
                if attr == 'hp':
                    self.stats.max_hp = value
