#! -*- coding: utf-8 -*-

from PIL import Image as PI
import matplotlib.pyplot as plt
import os
import argparse


class ASCIIArt():
    # Character ramp for grey scale pictures, from black to white
    STANDARD_CHAR_LIST = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
    ABBREVIATED_CHAR_LIST = list("@%#*+=-:. ")

    def __init__(self):
        pass


    def _read_image(self, image_path, return_color=True):
        try:
            assert os.path.exists(image_path)
        except:
            raise ValueError("Image file not found! Check your input path: {}".format(image_path))
        img = PI.open(image_path)
        # get grayscale image
        self.grey_image = img.convert("L")
        if return_color:
            self.color_image = img


    @staticmethod
    def _rgb_hex_code(R, G, B):
        return "#{:02x}{:02x}{:02x}".format(R, G, B)


    def convert_ascii(self, img_path, char_list=ABBREVIATED_CHAR_LIST, return_color=False, scale=1.0):
        """
        Convert origin image to black-white ascii art image
        :param char_list: sets of characters used for image pixel replacement (sort in descending order of grayscale)
        :param return_color: If true, return RGB value of each pixel
        :param scale: scale the output image size. Default: origin size
        :return: list of transformed ascii characters
        """
        # load image
        self._read_image(image_path=img_path, return_color=return_color)
        # scale the img
        try:
            assert scale > 0
        except:
            raise ValueError("scale argument must be larger than 0!")
        scaled_img_width = int(self.grey_image.size[0] * scale)
        scaled_img_height = int(self.grey_image.size[1] * scale)
        scaled_grey_img = self.grey_image.resize((scaled_img_width, scaled_img_height))
        char_list_length = len(char_list)
        ascii_img = [[None for i in range(scaled_img_width)] for j in range(scaled_img_height)]
        if return_color:
            scaled_color_img = self.color_image.resize((scaled_img_width, scaled_img_height))
            ascii_color = [x[:] for x in ascii_img]
        for i in range(scaled_img_height):
            for j in range(scaled_img_width):
                # brightness: the larger, the brighter, and later position in given char list
                brightness = scaled_grey_img.getpixel((j, i))
                ascii_img[i][j] = char_list[brightness * char_list_length / 256]
                if return_color:
                    R, G, B = scaled_color_img.getpixel((j, i))
                    ascii_color[i][j] = self._rgb_hex_code(R, G, B)
        if return_color:
            return ascii_img, ascii_color
        else:
            return ascii_img


    def draw_ascii(self, ascii_img, outfile, ascii_color=None, html_bg_color="white"):
        _, suffix = os.path.splitext(outfile)
        if suffix == '.txt':
            # output ascii art to text file
            with open(outfile, mode="wb") as of:
                for line in ascii_img:
                    of.write("{}\n".format("".join(line)))
            of.close()
        elif suffix == '.png':
            fig = plt.figure(figsize=(20, 20))
            if not ascii_color:
                ascii_color = [["#000000"] * len(ascii_img[0])] * len(ascii_img)
            plt.xlim(0, len(ascii_img[0]))
            plt.ylim(0, len(ascii_img))
            for j, line in enumerate(ascii_img):
                for i, symbol in enumerate(line):
                    plt.text(i, len(ascii_img) - j, symbol, fontsize=6, color=ascii_color[j][i])
            plt.axis('off')
            fig.savefig(outfile)
        elif suffix == '.html':
            with open(outfile, mode="wb") as of:
                of.write(r'<html><head><title>ASCII ART</title></head><body bgcolor={}>'.format(html_bg_color))
                if ascii_color:
                    of.write("<pre align=\"left\">\n")
                    for i, line in enumerate(ascii_img):
                        for j, symbol in enumerate(line):
                            of.write("<span style=\"color:{};\">{}</span>".format(ascii_color[i][j], symbol))
                        of.write("<br>")
                    of.write("</pre>\n")
                else:
                    for line in ascii_img:
                        of.write("<pre align=\"left\">{}</pre>\n".format("".join(line)))
                of.write("</body>\n")
                of.write("</html>")
            of.close()
        else:
            raise ValueError("Only .txt, .html, .png output file format accepted, but {} found".format(suffix))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str)
    parser.add_argument("--output", type=str)
    parser.add_argument("--return_color", action='store_true')
    parser.add_argument("--scale", type=float, default=1.0)
    parser.add_argument("html_bg_color", default="white")
    args = parser.parse_args()
    ascii_art_obj = ASCIIArt()
    ascii_img, ascii_color = ascii_art_obj.convert_ascii(img_path=args.input, return_color=args.return_color, scale=args.scale)
    ascii_art_obj.draw_ascii(ascii_img=ascii_img, ascii_color=ascii_color, outfile=args.output, html_bg_color=args.html_bg_color)
