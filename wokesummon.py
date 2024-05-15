import random
import cv2

from utils import check_pity, get_random_hero

woke_probs = (0.02, 0.0001, 0.005, 0.04, 0.02, 0.015, 0.0199, 0.02, 0.1, 0.03, 0.1122, 0.135, 0.072, 0.2808, 0.14)
woke_folders = ["images/Woke/hero", "images/Woke/0.01", "images/Woke/0.50", "images/Woke/0.80", "images/Woke/1.00",
                "images/Woke/1.50", "images/Woke/1.99", "images/Woke/2.00", "images/Woke/2.25", "images/Woke/3.00",
                "images/Woke/3.74", "images/Woke/4.50", "images/Woke/7.20", "images/Woke/9.36", "images/Woke/14.00"]


def woke_summon(woke_pity, name, choice):
    hit_pity = check_pity(woke_pity, name, 70)

    selected_heroes = []
    tiers = random.choices(woke_folders, weights=woke_probs, k=10)
    for tier in tiers:
        if tier == "images/Woke/hero":
            hero = "images/Woke/hero/" + choice + ".png"
        else:
            hero = get_random_hero(tier)
        selected_heroes.append(hero)

    if hit_pity:
        i = random.randint(0, 9)
        selected_heroes[i] = "images/Woke/hero/" + choice + ".png"
    elif "images/Woke/hero" in tiers:
        woke_pity[name] = 0
    images = []

    for image in selected_heroes:
        img = cv2.imread(image)
        img = cv2.resize(img, (100, 100))
        images.append(img)

    return images
