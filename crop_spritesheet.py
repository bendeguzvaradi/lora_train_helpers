from argparse import ArgumentParser
from PIL import Image
from tqdm import tqdm
import math
import os


def parse_args():
    """Sets arguments."""
    parser = ArgumentParser()
    parser.add_argument("input_path", type=str)
    parser.add_argument("output_path", type=str)
    args = parser.parse_args()
    return vars(args)


def color_distance(color1, color2):
    return math.sqrt((color1[0] - color2[0])**2 + (color1[1] - color2[1])**2 + (color1[2] - color2[2])**2)


def crop_turquoise_edges(input_path, output_path, turquoise_color=(129,128,255), tolerance=300):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for filename in tqdm(os.listdir(input_path)):
        if filename.endswith(".png"):
            input_file = os.path.join(input_path, filename)
            output_file = os.path.join(output_path, filename)

            image = Image.open(input_file)
            image_data = image.load()

            left, top, right, bottom = image.width, image.height, 0, 0

            for x in range(image.width):
                if any(color_distance(image_data[x, y], turquoise_color) > tolerance for y in range(image.height)):
                    left = x
                    break

            for x in reversed(range(image.width)):
                if any(color_distance(image_data[x, y], turquoise_color) > tolerance for y in range(image.height)):
                    right = x + 1
                    break

            for y in range(image.height):
                if any(color_distance(image_data[x, y], turquoise_color) > tolerance for x in range(image.width)):
                    top = y
                    break

            for y in reversed(range(image.height)):
                if any(color_distance(image_data[x, y], turquoise_color) > tolerance for x in range(image.width)):
                    bottom = y + 1
                    break
            
            cropped_image = image.crop((left, top, right, bottom))
            cropped_image.save(output_file)


if __name__ == "__main__":
    args = parse_args()
    input_directory = args["input_path"]
    output_directory = args["output_path"]
    crop_turquoise_edges(input_directory, output_directory)