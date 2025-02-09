import random
import math
from UI.Hooks import clear_screen
import UI.Menu as menu


class StatHandler:
    def __init__(self, player):
        self.player = player
    def display_class_info(self):
        # Muat data class berdasarkan player_class yang ada
        character_class = self.player.player_class
        # Tampilkan informasi class
        character_class.display_info()

    
    def display_stats(self):
        stats = self.player.to_dict()
        player_stats, world_info = stats.pop('stats', {}), stats.pop('world', {})
        # Format level info
        stats['level'] = f"{stats.get('level', 1)} ({stats.pop('exp', 0)}/{stats.pop('level_up_exp', 100)})"
        
        # Hitung Crit Chance
        n = player_stats.get('accuracy', 0) / 10
        player_stats['crit_chance'] = f"{round((n * (n + 1)) // 1.5)}%"
        
        # Format player stats
        for attr in ['accuracy', 'crit_damage']:  
            player_stats[attr] = f"{round(float(player_stats.get(attr, 0)))}%"
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

        # Each column has a width of 15 (stat name) + 10 (stat value) + 4 (padding and separator)
        column_width = 15 + 10 + 4
        total_width = column_width * 2  # Total width of the display

        # Center the player name and title
        title = "=== STATUS PLAYER ==="
        title_padding = (total_width - len(title)) // 2
        name_padding = (total_width - len(self.player.name)) // 2

        print(f"{'':<{title_padding}}{title}{'':<{title_padding}}")
        print(f"{'':<{name_padding}}{self.player.name.upper()}{'':<{name_padding}}")

        for left, right in zip(stat_items[:half], stat_items[half:]):
            print(f"{left[0].replace('_', ' '):<15}: {left[1]:<15}  |  {right[0].replace('_', ' '):<15}: {right[1]}")
        if len(stat_items) % 2:
            print(f"{stat_items[-1][0].replace('_', ' '):<15}: {stat_items[-1][1]}")

    def allocate_stat_points(self):
        """Mengalokasikan stat points ke atribut utama"""
        if self.player.stat_points <= 0:
            print(f"Maaf, {self.player.name}, Anda tidak memiliki poin untuk dialokasikan.")
            input("\nTekan Enter untuk melanjutkan...")
            clear_screen()
            return

        print(f"\nKamu memiliki {self.player.stat_points} poin stat untuk dialokasikan.")
        
        stats_map = {
            "1": ("strength", "STR - Meningkatkan Attack & Crit chance"), 
            "2": ("vitality", "VIT - Meningkatkan Max HP & Defense"), 
            "3": ("dexterity", "DEX - Meningkatkan Agility, Accuracy & Luck"), 
            "4": ("intelligence", "INT - Meningkatkan Max MP & Stamina")
        }
        
        temp_allocations = {"strength": 0, "vitality": 0, "dexterity": 0, "intelligence": 0}

        while self.player.stat_points > 0:
            print("\nPilih atribut utama yang ingin ditingkatkan:")
            for k, v in stats_map.items():
                print(f"{k}. {v[1]}")
            print("5. Selesai alokasikan poin stat.")

            choice = input("Pilih (1-5): ")
            if choice == "5":
                break
            if choice in stats_map:
                attr, name = stats_map[choice]
                temp_allocations[attr] += 1
                self.player.stat_points -= 1
                print(f"{name} telah ditingkatkan!")
            else:
                print("Pilihan tidak valid! Coba lagi.")

        # Update stat turunan berdasarkan alokasi sementara
        self.apply_stat_changes(temp_allocations)
        menu.save_player(self.player)

    def apply_stat_changes(self, allocations):
        """Menerapkan perubahan stat dari alokasi sementara"""
        stat_effects = {
            "vitality": {"max_hp": 10, "defense": 2},
            "intelligence": {"max_mp": 10, "attack": 2},
            "strength": {"attack": 2, "accuracy": 3, "crit_damage": 0.5},
            "dexterity": {"agility": 2, "accuracy": 2, "luck": 1, "stamina": 2}
        }

        for attr, points in allocations.items():
            for stat, multiplier in stat_effects[attr].items():
                setattr(self.player.stats, stat, (getattr(self.player.stats, stat) + points * multiplier))  # Update stats sesuai alokasi

class LevelHandler:
    def __init__(self, player):
        self.player = player
    def floor_up(self):
        self.player.world.current_level += 1  # Naik ke lantai berikutnya
        self.player.world.boss_defeated = False
        menu.save_player(self.player)
        print(f"\n\n{self.player.name} naik ke lantai {self.player.world.current_level}!")  
      
    def gain_exp(self, enemy_level):
        base_exp = 10  # EXP dasar untuk mengalahkan musuh
        base_exp = round(base_exp + (enemy_level-1) * 2.5)
        level_difference = enemy_level - self.player.level

        # Hitung EXP berdasarkan perbedaan level
        if level_difference > 0:  # Musuh lebih kuat
            exp_gained = round(base_exp + (level_difference * 2.5))
        elif level_difference < 0:  # Musuh lebih lemah
            exp_gained = round(max(base_exp, base_exp + (level_difference * 5)))  # Minimum 10 EXP
        else:  # Level sama
            exp_gained = base_exp

        self.player.exp += exp_gained
        print(f"{self.player.name} mendapatkan {exp_gained} EXP!")
        menu.save_player(player=self.player)
        
        if  self.player.exp >= self.player.level_up_exp:
            self.level_up()


    def level_up(self):
        """Meningkatkan level pemain dan mengatur ulang EXP ke 0."""

        # Hitung batas EXP baru menggunakan formula
        while self.player.exp >= self.player.level_up_exp:
            self.player.stat_points += 3
            self.player.exp -= self.player.level_up_exp
            self.player.level += 1
            self.player.level_up_exp = round(self.player.level_up_exp * 1.33)

            self.player.stats.restore()

            print(f"\nHP, MP, dan Stamina telah dipulihkan sepenuhnya.")
            print(f"Selamat! {self.player.name} naik ke level {self.player.level}!")

        
        print(f"\nEXP yang dibutuhkan untuk level berikutnya: {self.player.level_up_exp}")
        print(f"Stat Points tersedia: {self.player.stat_points}")
        menu.save_player(self.player)

class SkillHandler:
    def __init__(self, player):
        self.player = player
        self.passive_skill = player.passive_skills
        self.active_skill = player.active_skills

    def use_active_skill(self):
        return self.player.active_skill_handler.use_skill(self.active_skill.name)
    
    def update_active(self):
        return self.player.active_skill_handler.reduce_cooldown()
    
    def reset_passive(self, player):
        if not isinstance(self.passive_skill, list):
            self.passive_skill = [self.passive_skill]  # Ubah menjadi list jika hanya satu skill

        # Loop untuk mereset semua skill pasif
        for skill in self.passive_skill:
            if not skill.effect_removed:  # 🔥 Pastikan efek hanya dihapus sekali
                skill._remove_effect(player)
                skill.effect_removed = True
            skill.is_active = False
            skill.reset_cooldown_and_duration()
    
    def update_passive(self, player):
        if not isinstance(self.passive_skill, list):
            self.passive_skill = [self.passive_skill]  # Ubah menjadi list jika hanya satu skill

        # Loop untuk memperbarui semua skill pasif
        for skill in self.passive_skill:
            skill.update(player)

    def activate_passive(self):
        if not isinstance(self.passive_skill, list):
            self.passive_skill = [self.passive_skill]  # Ubah menjadi list jika hanya satu skill

        # Loop untuk mengaktifkan semua skill pasif
        for skill in self.passive_skill:
            skill.activate()



class InventoryHandler:
    def __init__(self, player):
        self.player = player

    def add_item(self, item):
        self.player.inventory.append(item)
        print(f"{item} telah ditambahkan ke inventory.")

class CombatHandler:
    def __init__(self, player):
        self.player = player

    def crit_chance(self, damage):
        n = self.player.stats.accuracy / 10
        crit_c = round((n * (n + 1)) // 1.5)
        if random.randint(1, 100) <= crit_c:
            crit_multiplier = self.player.stats.crit_damage / 100 
            damage *= (1 + crit_multiplier)  # Kalikan dengan bonus critical
            print("Critical Hit!")  # Indikasi serangan critical
        return damage
    
    def damage_calc(self, damage_mult=1):
        damage = self.player.stats.attack *  damage_mult # Hitung damage awal
        # Cek apakah serangan critical
        damage = self.crit_chance(damage)
        return round(damage)  # Bulatkan damage
    

    def defense_calc(self, enemy, damage):
        damage_reduction = math.ceil(enemy.defense * 0.25)
        damage_taken = max(damage - damage_reduction, 0)  # Pastikan damage tidak negatif
    
        return damage_taken
    
    def activate_skill_attack(self, enemy):
        damage_mult = self.player.skill_handler.use_active_skill()
        if damage_mult:
        # Kurangi mana jika ada mana_cost
            if self.player.active_skills.mana_cost > 0:
                self.player.stats.mp -= self.player.active_skills.mana_cost
            
            # Kurangi stamina jika ada stamina_cost
            if self.player.active_skills.stamina_cost > 0:
                self.player.stats.stamina -= self.player.active_skills.stamina_cost
                
        damage_calc = self.damage_calc(damage_mult)
        damage_akhir = self.defense_calc(enemy,damage_calc)
        if damage_akhir < 0:
            damage_akhir = 0
        enemy.hp -= damage_akhir
        print(f"{self.player.name} menyerang {enemy.name} dan memberikan {damage_akhir} damage!")


    def basic_attack(self, enemy):
        damage_calc = self.damage_calc()
        # Menghitung damage serangan ke musuh
        damage_akhir = self.defense_calc(enemy,damage_calc)
        if damage_akhir < 0:
            damage_akhir = 0
        enemy.hp -= damage_akhir
        print(f"{self.player.name} menyerang {enemy.name} dan memberikan {damage_akhir} damage!")
    
