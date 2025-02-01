import json
import random
import math
from Class_player import load_character_class

CLASSES = ["Swordsman", "Lancer", "Cleric", "Mage", "Rogue", "Archer", "Warrior"]


class Stats:
    def __init__(self, hp=100, mp=50, attack=25, defense=15, agility=15,luck=0, stamina=30, intelligence=25, accuracy=20, crit_damage=50,  max_hp=None, max_mp=None, max_stamina=None):
        self.hp = hp
        self.mp = mp
        self.attack = attack
        self.defense = defense
        self.agility = agility
        self.stamina = stamina
        self.intelligence = intelligence
        self.accuracy = accuracy
        self.crit_damage = crit_damage
        self.agility = agility
        self.luck = 0
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
            "intelligence": self.intelligence,
            "accuracy": self.accuracy,
            "crit_damage": self.crit_damage,
            "luck": self.luck,
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
    def __init__(self, name, player_class, stats, world, level=1, exp=0, level_up_exp=100, stat_points=0, inventory=None):
        self.name = name
        self.player_class = player_class
        self.stats = stats  # Use Stats instance
        self.world = world  # Use World instance
        self.level = level  # Tambahkan level
        self.exp = exp
        self.level_up_exp = level_up_exp
        self.stat_points = stat_points
        self.inventory = inventory if inventory is not None else []
        self.skill = load_character_class(player_class)



    def to_dict(self):
        """Mengonversi atribut pemain menjadi dictionary untuk disimpan"""
        return {
            "name": self.name,
            "player_class": self.player_class,
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
                   stats=stats,
                   world=world,
                   exp=data['exp'],
                   level_up_exp=data['level_up_exp'],
                   stat_points=data['stat_points'],
                   inventory=data['inventory'])
    
    
    def save_progress(self):
        with open("player_save.json", "w") as f:
            json.dump(self.to_dict(), f, indent=4)
        print("✅ Progress berhasil disimpan!")
    
    def display_class_info(self):
        # Muat data class berdasarkan player_class yang ada
        character_class = self.skill
        # Tampilkan informasi class
        character_class.display_info()

    def floor_up(self):
        self.world.current_level += 1  # Naik ke lantai berikutnya
        self.world.boss_defeated = False
        self.save_progress()
        print(f"\n\n{self.name} naik ke lantai {self.world.current_level}!")
        
    def display_stats(self):
        stats = self.to_dict()
        player_stats, world_info = stats.pop('stats', {}), stats.pop('world', {})

        # Format level info
        stats['level'] = f"{stats.get('level', 1)} ({stats.pop('exp', 0)}/{stats.pop('level_up_exp', 100)})"
        
        # Format player stats
        for attr in ['accuracy', 'crit_damage']:
            player_stats[attr] = f"{player_stats.get(attr, 0)}%"
        for attr in ['hp', 'mp', 'stamina']:
            player_stats[attr] = f"{player_stats.get(attr, 0)} / {player_stats.pop(f'max_{attr}', 0)}"
        
        # Format world info
        world_info['dungeon_level'] = f"{world_info.get('dungeon_level', 1)} - {world_info.pop('current_level', 1)}"
        
        # Hapus elemen yang tidak perlu
        for key in ['inventory', 'name']: stats.pop(key, None)  # Menghapus 'name' dari stats
        for key in ['boss_defeated', 'current_world']: world_info.pop(key, None)

        # Gabungkan semua statistik dan tampilkan
        stat_items = list({**stats, **player_stats, **world_info}.items())
        half = len(stat_items) // 2

        # Print stats with player name centered
        max_len = max(len(item[0]) for item in stat_items)  # Find the max length of stat names
        middle_len = len("player class") + len(self.name) + 2  # Calculate space for the player name

        # Calculate the total width of the display
        # Each column has a width of 15 (stat name) + 10 (stat value) + 4 (padding and separator)
        column_width = 15 + 10 + 4
        total_width = column_width * 2  # Total width of the display

        # Center the player name and title
        title = "=== STATUS PLAYER ==="
        title_padding = (total_width - len(title)) // 2
        name_padding = (total_width - len(self.name)) // 2

        print(f"{'':<{title_padding}}{title}{'':<{title_padding}}")
        print(f"{'':<{name_padding}}{self.name.upper()}{'':<{name_padding}}")

        for left, right in zip(stat_items[:half], stat_items[half:]):
            print(f"{left[0].replace('_', ' '):<15}: {left[1]:<10}  |  {right[0].replace('_', ' '):<15}: {right[1]}")
        if len(stat_items) % 2:
            print(f"{stat_items[-1][0].replace('_', ' '):<15}: {stat_items[-1][1]}")






    
    def gain_exp(self, enemy_level):
        """Menambahkan EXP berdasarkan level musuh dan naik level jika perlu"""
        base_exp = 15  # EXP dasar untuk mengalahkan musuh
        level_difference = enemy_level - self.level

        # Hitung EXP berdasarkan perbedaan level
        if level_difference > 0:  # Musuh lebih kuat
            exp_gained = round(base_exp + (level_difference * 2.5))
        elif level_difference < 0:  # Musuh lebih lemah
            exp_gained = round(max(5, base_exp + (level_difference * 5)))  # Minimum 10 EXP
        else:  # Level sama
            exp_gained = base_exp

        self.exp += exp_gained
        print(f"{self.name} mendapatkan {exp_gained} EXP!")
        self.save_progress()
        
        if  self.exp >= self.level_up_exp:
            self.level_up()

        
    def level_up(self):
        """Meningkatkan level pemain dan mengatur ulang EXP ke 0."""

        # Hitung batas EXP baru menggunakan formula
        while self.exp >= self.level_up_exp:  # Bisa naik beberapa level sekaligus
            self.stat_points += 3  # Tambahkan stat points
            self.exp -= self.level_up_exp  # Reset EXP kelebihan
            self.level += 1  # Naik 1 level
            self.level_up_exp = round(self.level_up_exp * 1.33)  # EXP naik 1.33x

            self.stats.restore()

            print(f"HP, MP, dan Stamina telah dipulihkan sepenuhnya.")
            print(f"Selamat! {self.name} naik ke level {self.level}!")

        
        print(f"EXP yang dibutuhkan untuk level berikutnya: {self.level_up_exp}")
        print(f"Stat Points tersedia: {self.stat_points}")
        self.save_progress()

    def add_to_inventory(self, item):
        self.inventory.append(item)
        self.save_progress()
        print(f"{item} telah ditambahkan ke inventory.")

    def active_skill(self):
        character_class = self.skill
        data_skill = character_class.to_dict().get('active_skill', {})
        return data_skill
    
    def passive_skill(self):
        character_class = self.skill
        data_skill = character_class.to_dict().get('passive_skill', {})
        return data_skill

    def crit_chance(self, damage):
        crit_c = min(round(self.stats.accuracy/4.5),85)
        if random.randint(1, 100) <= crit_c:
            crit_multiplier = self.stats.crit_damage / 100 
            damage *= (1 + crit_multiplier)  # Kalikan dengan bonus critical
            print("Critical Hit!")  # Indikasi serangan critical
        return damage
    def damage_calc(self, damage_mult):
        damage = self.stats.attack *  damage_mult # Hitung damage awal
        # Cek apakah serangan critical
        damage = self.crit_chance(damage)
        return round(damage)  # Bulatkan damage
    
    def defense_calc(self, damage):
        defense_factor = 1 - (math.log1p(self.stats.defense) / (math.log1p(1000)))  # Fungsi logaritmik
        damage *= round(defense_factor)
        return damage
    
    def skill_attack(self, enemy):
        damage_mult = self.skill.use_active_skill()
        damage_calc = self.damage_calc(damage_mult)
        damage_akhir = self.defense_calc(damage_calc)
        if damage_akhir < 0:
            damage_akhir = 0
        enemy.hp -= damage_akhir
        print(f"{self.name} menyerang {enemy.name} dan memberikan {damage_akhir} damage!")
        self.skill.active_skill.reduce_cooldown()
        # return
    def basic_attack(self, enemy):
        damage = self.stats.attack
        damage = self.damage_calc(damage)
        # Menghitung damage serangan ke musuh
        defense_factor = 1 - (math.log1p(enemy.defense) / (math.log1p(1000)))  # Fungsi logaritmik
        damage *= round(defense_factor)
        if damage < 0:
            damage = 0
        enemy.hp -= damage
        print(f"{self.name} menyerang {enemy.name} dan memberikan {damage} damage!")
    

    def allocate_stat_points(self):
        """Mengalokasikan stat points"""
        if self.stat_points <= 0:
            print(f"Maaf, {self.name}, Anda tidak memiliki poin untuk dialokasikan.")
            return

        print(f"\nKamu memiliki {self.stat_points} poin stat untuk dialokasikan.")
        stats_map = {
            "1": ("max_hp", 10), "2": ("max_mp", 10), "3": ("attack", 10), "4": ("defense", 10),
            "5": ("agility", 8), "6": ("stamina", 10), "7": ("intelligence", 8),
            "8": ("accuracy", 2)
        }

        while self.stat_points > 0:
            print("\nPilih stat yang ingin ditingkatkan:")
            for k, v in stats_map.items():
                print(f"{k}. {v[0].capitalize()}")
            print("10. Selesai alokasikan poin stat.")
            
            choice = input("Pilih (1-10): ")
            if choice == "10":
                break
            if choice in stats_map:
                attr, value = stats_map[choice]
                setattr(self.stats, attr, getattr(self.stats, attr) + value)
                self.stat_points -= 1
                print(f"{attr.replace('_', ' ').capitalize()} +{value}")
            else:
                print("Pilihan tidak valid! Coba lagi.")
        
        self.save_progress()
