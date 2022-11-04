import cv2
from random import randint, sample
import itertools
import numpy as np
import math
import os
from sklearn.cluster import KMeans

PIXELATED_SPEED = [8, 12, 14, 16, 18, 20, 25, 28, 32, 40, 50, 60]
BLURRED_SPEED = [200, 175, 150, 130, 120, 110, 100, 90, 80, 70, 60, 30]
DISTORTED_SPEED = [300, 200, 150, 125, 115, 100, 82, 75, 62, 50, 25, 10]
JIGSAW_SPEED = [42, 34, 28, 22, 20, 18, 16, 14, 12, 10, 6, 3]


def pixelate(img, name):
    height, width = img.shape[:2]
    print(f"\t[+] Generating pixelated set")
    for i, number_of_pixels in enumerate(PIXELATED_SPEED):
        print(f"\t\t[+] Image {i + 1}/{len(PIXELATED_SPEED)}")
        Z = np.float32(img).reshape(-1, 3)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
        K = 6
        ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        temp = center[label.flatten()]
        temp = temp.reshape(img.shape)

        temp = cv2.resize(temp, (number_of_pixels, number_of_pixels), interpolation=cv2.INTER_LINEAR)
        output = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)

        cv2.imwrite(f'pixelated/{name}{i}-{number_of_pixels}.jpg', output)


def blur(image, name):
    print(f"\t[+] Generating blurred set")
    for num, intensity in enumerate(BLURRED_SPEED):
        print(f"\t\t[+] Image {num + 1}/{len(BLURRED_SPEED)}")
        output = cv2.blur(image, (intensity, intensity))
        cv2.imwrite(f'blurred/{name}{num}-{intensity}.jpg', output)


def distort(image, name):
    height, width = image.shape[:2]

    print("\t[+] Generating distorted set")
    for num, intensity in enumerate(DISTORTED_SPEED):
        output = image.copy()
        print(f"\t\t[+] Image {num + 1}/{len(DISTORTED_SPEED)}")
        for i in range(height):
            for j in range(width):
                try:
                    output[i + int(intensity * math.sin(j / int(width / 30))), j] = image[i, j]
                except:
                    output[i + int(intensity * math.sin(j / int(width / 30))) - height, j] = image[i, j]
        cv2.imwrite(f'distorted/{name}{num}-{intensity}.jpg', output)


def jigsaw(img, name):
    height, width = img.shape[:2]
    print("\t[+] Generating jigsaw set")
    for num, square_num in enumerate(JIGSAW_SPEED):
        print(f"\t\t[+] Image {num + 1}/{len(JIGSAW_SPEED)}")
        output = img.copy()
        occupied = []
        square_size = int(width / square_num)
        count = 0
        for i in range(0, width - square_size, square_size):
            for j in range(0, height - square_size, square_size):
                position = (randint(0, square_num - 1) * square_size, randint(0, square_num - 1) * square_size)
                while position in occupied:
                    position = (randint(0, square_num - 1) * square_size, randint(0, square_num - 1) * square_size)
                occupied.append(position)
                section = img[j: j + square_size, i:i + square_size]
                output[position[0]: position[0] + square_size, position[1]:position[1] + square_size] = section

        cv2.imwrite(f'jigsaw/{name}{num}-{square_num}.jpg', output)


def run():
    directory = "src_images"
    # os.mkdir("pixelated")
    # os.mkdir("blurred")
    # os.mkdir("distorted")
    # os.mkdir("jigsaw")
    num_of_img = len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])

    for i, filename in enumerate(os.listdir(directory)):
        print(f"[+] Running generation for image {i + 1}/{num_of_img}")
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            img = cv2.imread(f)
            pixelate(img, os.path.splitext(filename)[0])
            # blur(img, os.path.splitext(filename)[0])
            # distort(img, os.path.splitext(filename)[0])
            # jigsaw(img, os.path.splitext(filename)[0])


run()
