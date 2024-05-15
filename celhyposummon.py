import random
import cv2

from utils import check_pity, get_random_hero

celhypo_probs = [0.02, 0.0001, 0.0084, 0.0126, 0.0392, 0.032, 0.015, 0.09, 0.1932, 0.0562, 0.03, 0.0374, 0.135,
                 0.0501, 0.2808]
celhypo_folders = ["images/Celhypo/hero", "images/Celhypo/0.01", "images/Celhypo/0.07", "images/Celhypo/0.18",
                   "images/Celhypo/0.56", "images/Celhypo/0.80", "images/Celhypo/1.50", "images/Celhypo/2.25",
                   "images/Celhypo/2.76", "images/Celhypo/2.81", "images/Celhypo/3.00", "images/Celhypo/3.74",
                   "images/Celhypo/4.50", "images/Celhypo/5.01", "images/Celhypo/9.36"]


def celhypo_summon(celhypo_pity, name, choice):
    hit_pity = check_pity(celhypo_pity, name, 70)

    selected_heroes = []
    tiers = random.choices(celhypo_folders, weights=celhypo_probs, k=10)

    for tier in tiers:
        if tier == "images/Celhypo/hero":
            hero = "images/Celhypo/hero/" + choice + ".png"
        else:
            hero = get_random_hero(tier)
        selected_heroes.append(hero)

    if hit_pity:
        i = random.randint(0, 9)
        selected_heroes[i] = "images/Celhypo/hero/" + choice + ".png"
    elif "images/Celhypo/hero" in tiers:
        celhypo_pity[name] = 0

    images = []

    for image in selected_heroes:
        img = cv2.imread(image)
        img = cv2.resize(img, (100, 100))
        images.append(img)

    return images
