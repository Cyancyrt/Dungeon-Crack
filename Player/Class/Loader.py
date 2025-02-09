import json

def load_json(filename):
    """Memuat data dari file JSON."""
    with open(filename, "r") as file:
        return json.load(file)

def load_class():
    """Memuat data class dari file JSON."""
    return load_json("data/class_player.json")

def load_active_skills():
    """Memuat data skill aktif dari file JSON."""
    return load_json("data/active_skills.json")

def load_passive_skills():
    """Memuat data skill pasif dari file JSON."""
    return load_json("data/passive_skills.json")