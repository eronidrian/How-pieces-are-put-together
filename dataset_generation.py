#!/usr/bin/env python3

import cv2
from random import randint
import numpy as np
import math
import os
import argparse

# the speed of the change throughout the sets
PIXELATED_SPEED = [16, 19, 23, 28, 33, 39, 46, 53, 60, 70, 80, 90]
WAVY_SPEED = [300, 200, 150, 125, 115, 100, 82, 75, 62, 50, 30, 20]
JIGSAW_SPEED = [50, 46, 42, 34, 30, 24, 22, 20, 18, 16, 14, 10]


# generate pixelated set from image "img" and save the result with the name "name"
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


# generate wavy set from image "img" and save the result with the name "name"
def wave(image, name):
    height, width = image.shape[:2]

    print("\t[+] Generating wavy set")
    for num, intensity in enumerate(WAVY_SPEED):
        output = image.copy()
        print(f"\t\t[+] Image {num + 1}/{len(WAVY_SPEED)}")
        for i in range(height):
            for j in range(width):
                try:
                    output[i + int(intensity * math.sin(j / int(width / 30))), j] = image[i, j]
                except:
                    output[i + int(intensity * math.sin(j / int(width / 30))) - height, j] = image[i, j]
        cv2.imwrite(f'wavy/{name}{num}-{intensity}.jpg', output)


# generate jigsaw set from image "img" and save the result with the name "name"
def jigsaw(img, name):
    img = cv2.resize(img, (1150, 1150))
    height, width = img.shape[:2]
    print("\t[+] Generating jigsaw set")
    for num, square_num in enumerate(JIGSAW_SPEED):
        print(f"\t\t[+] Image {num + 1}/{len(JIGSAW_SPEED)}")
        output = np.zeros((height, width, 3), dtype=np.uint8)
        occupied = []
        square_size = int(width / square_num)
        for i in range(0, width - square_size + 1, square_size):
            for j in range(0, height - square_size + 1, square_size):
                position = (randint(0, square_num - 1) * square_size, randint(0, square_num - 1) * square_size)
                while position in occupied:
                    position = (randint(0, square_num - 1) * square_size, randint(0, square_num - 1) * square_size)
                occupied.append(position)
                section = img[j: j + square_size, i:i + square_size]
                output[position[0]: position[0] + square_size, position[1]:position[1] + square_size] = section

        cv2.imwrite(f'jigsaw/{name}{num}-{square_num}.jpg', output)


def run(args):
    directory = args.source_directory
    if args.all:
        os.mkdir("pixelated")
        os.mkdir("wavy")
        os.mkdir("jigsaw")
    else:
        if args.pixelated:
            os.mkdir("pixelated")
        if args.wavy:
            os.mkdir("wavy")
        if args.jigsaw:
            os.mkdir("jigsaw")
    num_of_img = len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])

    for i, filename in enumerate(os.listdir(directory)):
        print(f"[+] Running generation for image {i + 1}/{num_of_img}")
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            img = cv2.imread(f)
            if args.all:
                pixelate(img, os.path.splitext(filename)[0])
                wave(img, os.path.splitext(filename)[0])
                jigsaw(img, os.path.splitext(filename)[0])
            else:
                if args.pixelated:
                    pixelate(img, os.path.splitext(filename)[0])
                if args.wavy:
                    wave(img, os.path.splitext(filename)[0])
                if args.jigsaw:
                    jigsaw(img, os.path.splitext(filename)[0])


parser = argparse.ArgumentParser(prog="Dataset generator")
parser.add_argument('source_directory', help="The directory, where the source images are located")
parser.add_argument('-a', '--all', action="store_true",
                    help="Generate all the types of distortion (alternative to -w -j -p)")
parser.add_argument('-w', '--wavy', action="store_true", help="Generate wavy images")
parser.add_argument('-j', '--jigsaw', action="store_true", help="Generate jigsaw images")
parser.add_argument('-p', '--pixelated', action="store_true", help="Generate pixelated images")
parser.set_defaults(all=False, wavy=False, jigsaw=False, pixelated=False)
args = parser.parse_args()
if not (args.all or args.wavy or args.jigsaw or args.pixelated):
    parser.error('No action requested, specify the type of distortion with one or more option from (-w -j -p -a)')

run(args)
