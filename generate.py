from PIL import Image

import argparse
import os

DATA_DIRECTORY = "data"
CARDS_FILE = "cards.txt"
TEMPLATE_IMAGE = "template.jpg"

OUT_DIRECTORY = "out"

class Card:

    def __init__(self, title, image, flavor):
        self.short = '_'.join([s.lower() for s in title.split(' ')])
        self.title = title
        self.image = image
        self.flavor = flavor

    def __repr__(self):
        return "<{}: {}>".format(self.title, self.flavor)

def parse_pack(pack):
    """
    Given the pack name, collects the relevant information from the CSV.

    Outputs a list of cards using the path information.
    """

    # TODO(harrison): Consider using the python library for manipulating paths instead of doing jank shit here.
    full_in_path = DATA_DIRECTORY + "/" + pack
    csv_path = full_in_path + "/" + CARDS_FILE

    cards = []
    with open(csv_path, 'r') as f:
        for line in f:
            tokens = line[:-1].split('\t')
            cards.append(Card(tokens[0], tokens[1], tokens[2]))

    return cards

def setup(full_out_dir):
    """
    Performs necessary setup work for the output.
    """
    try:
        print("Trying to make directory at: {}".format(full_out_dir))
        os.mkdir(full_out_dir)
    except:
        print("Directory at {} already exists!".format(full_out_dir))

def generate_images(cards, pack):
    """
    Given the input card tuples, saves images at the given path.

    Doesn't return anything.
    """
    full_out_dir = OUT_DIRECTORY + "/" + pack
    full_in_path = DATA_DIRECTORY + "/" + pack
    template_path = full_in_path + "/" + TEMPLATE_IMAGE
    setup(full_out_dir)

    im = Image.open(template_path)
    for card in cards:
        card_filename = full_out_dir + "/" + card.short + ".jpg"
        print("Printing: {}".format(card_filename))
        im.save(card_filename, "JPEG")

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Card generator. Will take the input information and generate cards.',
    )
    parser.add_argument(
        '--pack', 
        help='Input the pack that you want to generate cards for.',
        type=str,
        required=True,
    )

    args = parser.parse_args()
    pack = args.pack
    print("Working on the pack:", pack)

    cards = parse_pack(pack)
    print(cards)
    generate_images(cards, pack)
