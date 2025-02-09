
from Player.Player_Handler import StatHandler, LevelHandler, SkillHandler, CombatHandler, InventoryHandler
from Player.Class.Class_player import load_character_class
from Player.Class.Active_Skill import ActiveSkillHandler
from Player.Class.Passive_skill import PassiveSkillHandler
from UI.Hooks import EventDispatcher


CLASSES = ["Swordsman", "Lancer", "Cleric", "Mage", "Rogue", "Archer", "Warrior"]


class Stats:
    def __init__(self, hp=100, mp=50, attack=25, defense=15, agility=15, luck=0, stamina=30, accuracy=20, crit_damage=50,  max_hp=None, max_mp=None, max_stamina=None):
        self.hp = hp
        self.mp = mp
        self.attack = attack
        self.defense = defense
        self.agility = agility
        self.stamina = stamina
        self.accuracy = accuracy
        self.crit_damage = crit_damage
        self.agility = agility
        self.luck = luck
        # Pastikan max_hp, max_mp, dan max_stamina menerima nilai yang diberikan
        self.max_hp = max_hp if max_hp is not None else hp
        self.max_mp = max_mp if max_mp is not None else mp
        self.max_stamina = max_stamina if max_stamina is not None else stamina

    def restore(self):
        self.hp = self.max_hp
        self.mp = self.max_mp
        self.stamina = self.max_stamina

    def to_dict(self):
        return {
            "hp": self.hp,
            "mp": self.mp,
            "attack": self.attack,
            "defense": self.defense,
            "agility": self.agility,
            "stamina": self.stamina,
            "luck": self.luck,
            "accuracy": self.accuracy,
            "crit_damage": self.crit_damage,
            "max_hp": self.max_hp,
            "max_mp": self.max_mp,
            "max_stamina": self.max_stamina
        }

class World:
    def __init__(self, current_world=1, current_level=1, boss_defeated=False):
        self.current_world = current_world
        self.current_level = current_level
        self.boss_defeated = boss_defeated

    def advance_level(self):
        self.current_level += 1
        self.boss_defeated = False  # Reset after advancing

    def to_dict(self):
        return {
            "current_world": self.current_world,
            "current_level": self.current_level,
            "boss_defeated": self.boss_defeated
        }

class Player:
    def __init__(self, name, player_class, stats, world,event_dispatcher, level=1, exp=0, level_up_exp=100, stat_points=0, inventory=None):
        self.name = name
        self.player_class = load_character_class(player_class)
        self.stats = stats  # Instance dari Stats
        self.world = world  # Instance dari World
        self.level = level
        self.exp = exp
        self.level_up_exp = level_up_exp
        self.stat_points = stat_points
        self.inventory = inventory if inventory is not None else []
        self.active_skills = self.player_class.active_skill
        self.passive_skills = self.player_class.passive_skill  # Sekarang bisa punya banyak skill pasif
        self.event_dispatcher = event_dispatcher

         # 🔥 Tambahkan handler untuk active dan passive skill
        self.active_skill_handler = ActiveSkillHandler(self,event_dispatcher)



        self.buffs = {}
        # 🔥 Handler untuk mengelompokkan fitur
        self.stat_handler = StatHandler(self)
        self.level_handler = LevelHandler(self)
        self.skill_handler = SkillHandler(self)
        self.combat_handler = CombatHandler(self)
        self.inventory_handler = InventoryHandler(self)

    def to_dict(self):
        return {
            "name": self.name,
            "player_class": self.player_class.name,
                'stats': self.stats.to_dict(),  # Jika Stats adalah objek, pastikan juga ada to_dict() di kelas Stats
                'world': self.world.to_dict(),  # Jika World adalah objek, pastikan juga ada to_dict() di kelas World
                "level" : self.level,
                "exp": self.exp,
                "level_up_exp": self.level_up_exp,
                "stat_points": self.stat_points,
                "inventory": self.inventory,
            }
            
    @classmethod
    def from_dict(cls, data):
        # Ambil data untuk Stats dan World
        stats_data = data.get('stats', {})
        stats = Stats(**stats_data)  # Membuat objek Stats dari data yang ada
        world_data = data.get('world', {})
        world = World(**world_data)  # Membuat objek World dari data yang ada
        return cls(name=data['name'],
                player_class=data['player_class'],
                event_dispatcher=EventDispatcher(),
                stats=stats,
                level=data['level'],
                world=world,
                exp=data['exp'],
                level_up_exp=data['level_up_exp'],
                stat_points=data['stat_points'],
                inventory=data['inventory'])

    def display_stats(self):
        self.stat_handler.display_stats()

    def allocate_stat_points(self):
        self.stat_handler.allocate_stat_points()
    
    def gain_exp(self, enemy_level):
        self.level_handler.gain_exp(enemy_level)

    def level_up(self):
        self.level_handler.level_up()

    def add_to_inventory(self, item):
        self.inventory_handler.add_item(item)

    def basic_attack(self, enemy):
        self.combat_handler.basic_attack(enemy)

    def activate_skill_attack(self, enemy):
        self.combat_handler.activate_skill_attack(enemy)





        

        
