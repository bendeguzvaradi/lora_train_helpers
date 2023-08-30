"""LORA traing preprocess and normalisation steps."""
import os
from PIL import Image
from argparse import ArgumentParser
from pathlib import Path
from tqdm import tqdm
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("img_folder", type=str)
    parser.add_argument("--size", default=512)
    parser.add_argument("--bkg_to_white", type=bool, default=False)
    parser.add_argument("--overwrite", default=False)
    args = parser.parse_args()
    return vars(args)


def resize(image_pil, width, height):
    '''
    Resize PIL image keeping ratio and using white background.
    '''
    ratio_w = width / image_pil.width
    ratio_h = height / image_pil.height
    if ratio_w < ratio_h:
        # It must be fixed by width
        resize_width = width
        resize_height = round(ratio_w * image_pil.height)
    else:
        # Fixed by height
        resize_width = round(ratio_h * image_pil.width)
        resize_height = height
    image_resize = image_pil.resize((resize_width, resize_height), Image.ANTIALIAS)
    background = Image.new('RGBA', (width, height), (255, 255, 255, 255))
    offset = (round((width - resize_width) / 2), round((height - resize_height) / 2))
    background.paste(image_resize, offset)
    return background


if __name__ == "__main__":
    args = parse_args()
    for path_in in tqdm(Path(args["img_folder"]).glob('*.png'), total=len(os.listdir(args["img_folder"]))):
        path_out = path_in.parent / f"{path_in.stem}-out.png"
        # no point processing images that have already been done!
        if path_out.exists():
            continue
        with Image.open(path_in) as img:
            out = resize(img, width=int(args["size"]), height=int(args["size"]))
            if args["overwrite"]:
                out.save(path_in)
            else:
                out.save(path_out)
            