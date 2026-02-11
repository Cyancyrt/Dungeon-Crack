
import os, re

def check_enemy_status(enemy, dispatch_event, passive_skill_handler):
    """Menampilkan status musuh berdasarkan persentase HP yang tersisa."""
    if enemy.stats.hp <= 0:
        return "enemy_died"
    # if not isinstance(passive_skill_handler.passive_skills, list):
    #     passive_skill_handler.passive_skills = [passive_skill_handler.passive_skills]
    thresshold = 0
    for skill in passive_skill_handler.passive_skills:
        if "enemy_hp_threshold" in skill.activation_condition:
            thresshold = skill.activation_condition["enemy_hp_threshold"]
            
    hp_percentage = (enemy.stats.hp / enemy.stats.max_hp) * 100  # Menghitung persentase HP tersisa
    if (enemy.stats.hp / enemy.stats.max_hp) * 100 <= thresshold:
        dispatch_event("enemy_hp_threshold")

    if hp_percentage <= 20:
        print(f"\n{enemy.name} hampir tumbang! ({hp_percentage:.0f}% HP tersisa)")
    elif hp_percentage <= 50:
        print(f"\n{enemy.name} mulai terlihat kelelahan! ({hp_percentage:.0f}% HP tersisa)")

def clear_screen():
    """Membersihkan layar cmd."""
    os.system('cls' if os.name == 'nt' else 'clear')

def naik_lantai(player, current_level):
    print("Apakah Anda ingin naik ke lantai berikutnya? (Y/N)")
    choice = input("\nPilih aksi (Y untuk naik, N untuk tetap): ").lower()
    if choice == 'y':
        player.floor_up()
    else:
        print(f"{player.name} memilih untuk tetap di lantai {current_level}.")

def get_stat_from_effect(effect_type):
    """Mencari stat dasar dari nama efek menggunakan pola regex"""
    patterns = {
        "attack": r"attack",     # Semua efek yang mengandung "attack"
        "defense": r"defense",   # Semua efek yang mengandung "defense"
        "speed": r"speed",       # Jika ada efek kecepatan
        "crit_chance": r"crit_chance|critical_chance",  # Bisa menangkap "crit_up", "critical_increase"
        "crit_damage": r"crit_damage|critical_damage",  # Bisa menangkap "crit_up", "critical_increase"
        "hp": r"hp|health",      # Bisa menangkap "hp_boost", "health_regen"
        "accuracy": r"accuracy", # Semua efek yang mengandung "accuracy"
        "agility": r"agility"    # Semua efek yang mengandung "agility"
    }

    for stat, pattern in patterns.items():
        if re.search(pattern, effect_type):
            return stat  # Kembalikan nama stat yang sesuai

    return None

def effect_display(target,effect_type, effect_value):
    """Menampilkan efek skill"""
    if effect_type == "mana_restore":
        print(f"🔵 {target.name} merasakan energi sihir mengalir! +{effect_value['amount']} MP!")
    elif effect_type == "hp_restore":
        print(f"❤️ {target.name} memulihkan kesehatannya! +{effect_value['amount']} HP!")
    elif effect_type == "burn":
        print(f"🔥 {target.name} terbakar! Kehilangan {effect_value['amount']} HP!")
    elif effect_type == "poison":
        print(f"☠️ {target.name} terkena racun! Kehilangan {effect_value['amount']} HP!")

def after_effect(target, effect_type, effect_value):
    """Menerapkan efek setelah efek utama diterapkan"""
    if effect_type not in target.buffs and effect_type not in target.debuffs:
        return  # Jika efek tidak ada, langsung keluar
    if effect_type in target.buffs:
        if effect_type == "mana_restore":
            target.stats.mp = min(target.stats.max_mp, max(0, target.stats.mp + effect_value["amount"]))  # Memulihkan mana
        elif effect_type == "hp_restore":
            target.stats.hp = min(target.stats.max_hp, max(0, target.stats.hp + effect_value["amount"]))
        effect_display(target, effect_type, effect_value)
    elif effect_type in target.debuffs:
        if effect_type == "burn":
            target.stats.hp = max(0, target.stats.hp - effect_value["amount"])
        elif effect_type == "poison":
            target.stats.hp = max(0, target.stats.hp - effect_value["amount"])
        effect_display(target, effect_type, effect_value)

def remove_effect(player, effect_type):
    """Menghapus efek dari buffs atau debuffs sesuai tipe efek."""
    target_dict = None

    if effect_type in player.buffs:
        target_dict = player.buffs
    elif effect_type in player.debuffs:
        target_dict = player.debuffs
    else:
        return  # Efek tidak ditemukan, keluar

    bonus = target_dict[effect_type].get("amount", 0)
    stat_attr = get_stat_from_effect(effect_type)
    if stat_attr is not None:
        player.stats.__dict__[stat_attr] -= bonus  # Kurangi efek yang diberikan

    # Hapus efek dari buffs/debuffs
    del target_dict[effect_type]

