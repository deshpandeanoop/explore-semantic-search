import csv
import random

place_templates = {
    "Pub": {
        "names": ["The Rusty Anchor", "Neon Underground", "Brew & Barrel", "Hop House", "The Speakeasy", "Skyline Lounge"],
        "descs": [
            "A bustling nightlife spot featuring craft beers on tap, live indie music, and artisan bar bites.",
            "Cozy subterranean pub with signature cocktails, quiet corners for conversation, and classic pub games.",
            "High-energy rooftop lounge serving craft cocktails with panoramic city views and weekly DJ sets."
        ],
        "genders": ["All", "M", "F"],
        "ages": ["Adult"]
    },
    "Temple": {
        "names": ["Sunridge Meditation Shrine", "Lotus Heritage Temple", "Grand Serenity Pagoda", "Starlight Sanctuary"],
        "descs": [
            "A peaceful ancient temple surrounded by serene gardens, ideal for quiet meditation, spiritual reflection, and morning prayers.",
            "Historic spiritual landmark offering morning chanting, tranquil lotus ponds, and traditional architecture tours.",
            "Quiet hilltop shrine surrounded by nature trails, providing a calm retreat from urban noise."
        ],
        "genders": ["All"],
        "ages": ["All", "Adult", "Aged"]
    },
    "Park": {
        "names": ["Oakwood Botanical Park", "Riverside Greenway", "Pine Valley Promenade", "Meadowbrook Gardens"],
        "descs": [
            "Expansive green park featuring shaded walking trails, open picnic lawns, duck ponds, and peaceful benches.",
            "Family-friendly waterfront park with paved stroller paths, community flower beds, and weekend food trucks.",
            "Sprawling urban forest featuring botanical exhibits, scenic jogging loops, and dedicated dog play zones."
        ],
        "genders": ["All"],
        "ages": ["All", "Kids", "Aged"]
    },
    "Museum": {
        "names": ["Town History Hall", "Science & Innovation Center", "Modern Vision Gallery", "Maritime Heritage Museum"],
        "descs": [
            "Interactive museum featuring hands-on science exhibits, space flight simulators, and kid-friendly experiments.",
            "Curated art gallery showcasing local contemporary artists, rotating sculpture displays, and quiet viewing halls.",
            "Historical archive housing regional artifacts, interactive timeline exhibits, and guided walking audio tours."
        ],
        "genders": ["All"],
        "ages": ["All", "Kids", "Adult"]
    },
    "Cafe": {
        "names": ["The Roasted Bean", "Urban Hideaway Cafe", "Pastry & Press", "Monochrome Coffee Co."],
        "descs": [
            "Quiet neighborhood coffee shop offering single-origin espresso, specialty matcha, fast Wi-Fi, and cozy reading nooks.",
            "Charming bakery cafe serving freshly baked croissants, artisan sandwiches, and outdoor patio seating.",
            "Trendy minimalist cafe popular for brunch, cold brews, and remote working spaces."
        ],
        "genders": ["All", "F", "M"],
        "ages": ["Adult", "All"]
    },
    "Adventure": {
        "names": ["Summit Rock Climbing", "River Bend Kayaking", "Apex Trampoline Park", "ZipLine Canopy Trails"],
        "descs": [
            "High-adrenaline indoor climbing gym with bouldering walls, harness routes, and beginner instruction classes.",
            "Guided kayaking and paddleboarding equipment rentals along scenic calm riverways.",
            "Action-packed indoor adventure park featuring obstacle courses, foam pits, and high-flying trampolines."
        ],
        "genders": ["All", "M"],
        "ages": ["Kids", "Adult"]
    }
}

areas = ["Downtown", "Old Town", "Westside", "North Hills", "Riverside", "East End"]

with open("data/town_pulse_dataset.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "target_gender", "age_group", "place_category", "place_name", "location_area", "description"])
    
    for i in range(1, 1001):
        cat = random.choice(list(place_templates.keys()))
        data = place_templates[cat]
        
        name = f"{random.choice(data['names'])} #{random.randint(1, 99)}"
        gender = random.choice(data["genders"])
        age = random.choice(data["ages"])
        area = random.choice(areas)
        desc = random.choice(data["descs"])
        
        writer.writerow([i, gender, age, cat, name, area, desc])

print("Generated town_pulse_dataset.csv with 1,000 rows successfully.")