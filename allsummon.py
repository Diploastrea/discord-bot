import random
import cv2

from utils import check_pity, get_random_hero

all_faction_probs = [0.5169, 0.4360, 0.0441, 0.002, 0.001]
all_faction_folders = ["images/Common", "images/Rare", "images/4F", "images/Celhypo/hero", "images/Woke/hero"]


def all_summon(all_pity, name):
    hit_pity = check_pity(all_pity, name, 30)

    selected_heroes = []
    tiers = random.choices(all_faction_folders, weights=all_faction_probs, k=10)

    for tier in tiers:
        hero = get_random_hero(tier)
        selected_heroes.append(hero)

    if hit_pity:
        i = random.randint(0, 9)
        selected_heroes[i] = get_random_hero("images/4F")
    elif "images/4F" in tiers:
        all_pity[name] = 0

    images = []

    for image in selected_heroes:
        img = cv2.imread(image)
        img = cv2.resize(img, (100, 100))
        images.append(img)

    return images
