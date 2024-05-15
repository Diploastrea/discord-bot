import random

import cv2

from utils import check_pity, get_random_hero

faction_probs = [0.5169, 0.4370, 0.0461]

lb_folders = ["images/Lightbearer/common", "images/Lightbearer/rare", "images/Lightbearer/elite"]
mauler_folders = ["images/Mauler/common", "images/Mauler/rare", "images/Mauler/elite"]
wilder_folders = ["images/Wilder/common", "images/Wilder/rare", "images/Wilder/elite"]
gb_folders = ["images/Graveborne/common", "images/Graveborne/rare", "images/Graveborne/elite"]


def faction_summon(faction_pity, name, faction):
    faction = faction.lower()
    hit_pity = check_pity(faction_pity, name, 30)

    selected_heroes = []
    tiers = []
    if faction == 'lb' or faction == 'lightbearer':
        tiers = random.choices(lb_folders, weights=faction_probs, k=10)
    elif faction == 'mauler':
        tiers = random.choices(mauler_folders, weights=faction_probs, k=10)
    elif faction == 'wilder':
        tiers = random.choices(wilder_folders, weights=faction_probs, k=10)
    elif faction == 'gb' or faction == 'graveborn':
        tiers = random.choices(gb_folders, weights=faction_probs, k=10)

    for tier in tiers:
        hero = get_random_hero(tier)
        selected_heroes.append(hero)

    if hit_pity:
        i = random.randint(0, 9)
        if faction == 'lb' or faction == 'lightbearer':
            selected_heroes[i] = get_random_hero("images/Lightbearer/elite")
        elif faction == 'mauler':
            selected_heroes[i] = get_random_hero("images/Mauler/elite")
        elif faction == 'wilder':
            selected_heroes[i] = get_random_hero("images/Wilder/elite")
        elif faction == 'gb' or faction == 'graveborne':
            selected_heroes[i] = get_random_hero("images/Graveborne/elite")
    elif "images/Lightbearer/elite" in tiers or\
            "images/Mauler/elite" in tiers or\
            "images/Wilder/elite" in tiers or\
            "images/Graveborne/elite" in tiers:
        faction_pity[name] = 0

    images = []
    for image in selected_heroes:
        img = cv2.imread(image)
        img = cv2.resize(img, (100, 100))
        images.append(img)

    return images
