import os
import random

import cv2
import numpy as np
from multipledispatch import dispatch


def check_pity(pity, name, max_pity):
    if name not in pity:
        pity[name] = 0

    pity[name] = pity[name] + 10
    pity_count = pity[name]
    if pity_count < max_pity:
        return False
    else:
        pity[name] = 0
        return True


def get_random_hero(folder_path):
    try:
        images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.png'))]

        if not images:
            print(f"No images found in folder: {folder_path}")
            return None

        random_image = random.choice(images)
        return os.path.join(folder_path, random_image).replace('\\', '/')
    except OSError as e:
        print(f"Error reading folder: {folder_path}, {e}")
        return None


@dispatch(list, int)
def create_collage(images, rows=3):
    collage_width = 0
    image_rows = [images[i:i + rows] for i in range(0, len(images), rows)]
    image_heights = []
    for image_row in image_rows:
        collage_width = max(collage_width, sum([img.shape[1] for img in image_row]))
        image_heights.append(max([img.shape[0] for img in image_row]))

    collage_height = sum(image_heights)
    collage = np.zeros((collage_height, collage_width, 3), dtype=np.uint8)

    y = 0
    x = 0
    for i, image_row in enumerate(image_rows):
        for image in image_row:
            collage[y:y + image.shape[0], x:x + image.shape[1]] = image
            x += image.shape[1]
        y += image_heights[i]
        x = 0
    return collage


def stitch_images(images):
    random_number = random.randint(1, 100000)
    random_i = random.randint(0, 9)

    if random_number == 1:
        img = cv2.imread('images/gduck.png')
        img = cv2.resize(img, (100, 100))
        images[random_i] = img

    return create_collage(images, 2, 5)


@dispatch(list, int, int)
def create_collage(images, rows, cols):
    collage_height = images[0].shape[0] * rows
    collage_width = images[0].shape[1] * cols
    collage = np.zeros((collage_height, collage_width, 3), dtype=np.uint8)

    index = 0
    for i in range(rows):
        for j in range(cols):
            if index < len(images):
                image = images[index]
                collage[i * image.shape[0]:(i + 1) * image.shape[0], j * image.shape[1]:(j + 1) * image.shape[1],
                :] = image
                index += 1
    return collage


def is_not_leadership(roles, leadership_role_id):
    for role in roles:
        if role.id == leadership_role_id:
            return False
    return True