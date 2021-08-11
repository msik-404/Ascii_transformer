from PIL import Image
import numpy as np
from txt_to_image import TxtToImage


def intensity_to_iter_index(pixel_val, iterable):
    """
    Maps pixel intensity value to index of iterable. Usually a list of ascii symbols with decreasing intensity.

    :param pixel_val: 0-255 int corresponding to intensity of greyscale of a pixel
    :param iterable: list of ascii symbols with decreasing intensity
    :return: index of a ascii symbol corresponding to pixel intensity value
    """
    index = int(pixel_val // (255 / len(iterable)))
    if index == len(iterable):
        index -= 1
    return index


class AsciiTransformer:
    def __init__(self):
        self.image = None
        self.symbols_list = [i for i in "@%#*+=-:. "]
        self.new_width = None
        self.new_height = None

    def load_image(self, path):
        """
        Load image from the path.

        :param path: Path of the image to be transformed
        :return: Returns nothing
        """
        self.image = Image.open(path)

    def set_symbols(self, symbols_str=None):
        """
        Adds characters that will be used in ascii image.

        :param symbols_str: List of letters
        :return: Returns nothing
        """
        symbols_list = []
        if symbols_str:
            for i in symbols_str:
                symbols_list.append(i)
            self.symbols_list = symbols_list

    def resize_image(self, new_width):
        """
        Resizes image. Each pixel corresponds to letter.

        :param new_width: Desired width of the resized image
        :return: Returns nothing
        """
        width, height = self.image.size
        aspect_ratio = width / height
        self.new_width = new_width
        self.new_height = int(new_width * aspect_ratio)
        self.image = self.image.resize((self.new_width, self.new_height))

    def convert_to_grayscale(self):
        """
        Converts image to grayscale.

        :return: Returns nothing
        """
        self.image = self.image.convert("L")

    def convert_to_ascii(self):
        """
        Converts pixels from image to letters based on pixel value.

        :return: 2d numpy_array of letters with proper dimensions
        """
        self.convert_to_grayscale()
        pixels = self.image.getdata()
        new_pixels = [self.symbols_list[intensity_to_iter_index(pixel, self.symbols_list)] for pixel in pixels]
        symbols_array = np.array(new_pixels)
        symbols_array = np.reshape(symbols_array, (self.new_height, self.new_width))
        return symbols_array

    def save_txt(self):
        """
        Saves ascii art to txt file.
        :return: Returns nothing
        """
        symbols_array = self.convert_to_ascii()
        with open("ascii_image.txt", "w") as f:
            for line in symbols_array:
                f.write("".join(line))
                f.write("\n")

    def save_image(self):
        """
        Saves ascii art to image.

        :return: Returns nothing
        """
        symbols_array = self.convert_to_ascii()
        converter = TxtToImage()
        converter.load_data(symbols_array)
        converter.imgfy_ascii()
