#! -*- coding: utf-8 -*-

from PIL import Image as PI
import numpy as np
import matplotlib.pyplot as plt
try:
    import skvideo.io
    import cv2
except:
    print "opencv method and video input are not allowed"
import os
import argparse
import sys
import time
import subprocess


class ASCIIArt():
    # Character ramp for grey scale pictures, from black to white
    STANDARD_CHAR_LIST = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
    ABBREVIATED_CHAR_LIST = list("@%#*+=-:. ")

    def __init__(self, method="pillow", return_color=True):
        # method: choose method to read and process image. Only pillow or opencv acceptable now
        # return_color: If true, return RGB value of each pixel
        self.method = method
        self.return_color = return_color
        self.image_format = [".png", ".jpg", ".bmp", ".pbm", ".pgm", ".ppm", ".sr", ".ras", ".tiff", ".tif", ".jpeg"]
        self.video_format = [".mp4", ".avi", ".yuv"]
        self.clear_console = 'clear' if os.name == 'posix' else 'CLS'

    def _read_image(self, image_path):
        try:
            assert os.path.exists(image_path)
        except:
            raise ValueError("Image file not found! Check your input path: {}".format(image_path))
        if self.method == "pillow":
            img = PI.open(image_path)
            # get grayscale image
            grey_image = img.convert("L")
            if self.return_color:
                self.color_image = img
        elif self.method == "opencv":
            img = cv2.imread(image_path)
            grey_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            raise ValueError("Current input method could only be pillow or opencv!")
        if self.return_color:
            return grey_image, img
        else:
            return grey_image


    def _read_video(self, video_path):
        try:
            assert os.path.exists(video_path)
        except:
            raise ValueError("Video file not found! Check your input path: {}".format(video_path))
        # videogen: generator to return video frame by frame
        videogen = skvideo.io.vreader(video_path)
        for frame in videogen:
            grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if self.return_color:
                yield grey_frame, frame
            else:
                yield grey_frame


    @staticmethod
    def _rgb_hex_code(R, G, B):
        return "#{:02x}{:02x}{:02x}".format(R, G, B)


    def _img2ascii(self, grey_image, color_image=None, char_list=ABBREVIATED_CHAR_LIST, scale=1.0):
        """
        Convert origin image to black-white ascii art image
        :param char_list: sets of characters used for image pixel replacement (sort in descending order of grayscale)
        :param scale: scale the output image size. Default: origin size
        :return: list of transformed ascii characters
        """
        # scale the img
        try:
            assert scale > 0
        except:
            raise ValueError("Argument scale must be larger than 0!")
        try:
            assert self.method in ["pillow", "opencv"]
        except:
            raise ValueError("Argument method must be pillow or opencv!")
        if self.method == 'pillow':
            scaled_img_width = int(grey_image.size[0] * scale)
            scaled_img_height = int(grey_image.size[1] * scale)
            scaled_grey_img = grey_image.resize((scaled_img_width, scaled_img_height))
            if self.return_color:
                scaled_color_img = color_image.resize((scaled_img_width, scaled_img_height))
        elif self.method == 'opencv':
            scaled_grey_img = cv2.resize(grey_image, None, fx=scale, fy=scale)
            scaled_img_width = len(scaled_grey_img[0])
            scaled_img_height = len(scaled_grey_img)
            if self.return_color:
                scaled_color_img = cv2.resize(color_image, None, fx=scale, fy=scale)
        char_list_length = len(char_list)
        ascii_img = [[None for i in range(scaled_img_width)] for j in range(scaled_img_height)]
        ascii_color = [x[:] for x in ascii_img]
        for i in range(scaled_img_height):
            for j in range(scaled_img_width):
                if self.method == "pillow":
                    # brightness: the larger, the brighter, and later position in given char list
                    brightness = scaled_grey_img.getpixel((j, i))
                    if self.return_color:
                        R, G, B = scaled_color_img.getpixel((j, i))
                        ascii_color[i][j] = self._rgb_hex_code(R, G, B)
                elif self.method == "opencv":
                    brightness = scaled_grey_img[i, j]
                    if self.return_color:
                        R, G, B = scaled_color_img[i][j]
                        ascii_color[i][j] = (int(R), int(G), int(B))
                ascii_img[i][j] = char_list[brightness * char_list_length / 255]
        if self.return_color:
            return ascii_img, ascii_color
        else:
            return ascii_img

    @staticmethod
    def _cv_image(ascii_img, ascii_color):
        output_img = np.array(
            [[[255, 255, 255] for m in range(len(ascii_img[0])) * 10] for n in range(len(ascii_img)) * 10]).astype(np.uint8)
        font = cv2.FONT_HERSHEY_SIMPLEX
        for j, line in enumerate(ascii_img):
            for i, symbol in enumerate(line):
                try:
                    cv2.putText(output_img, symbol, (i * 10, j * 10), font, 0.4, ascii_color[j][i], 1)
                except:
                    raise MemoryError("Input image is too large to convert. Try a smaller one, like 300 x 300 ...")
        return output_img


    def draw_ascii(self, input, output=None, char_list=ABBREVIATED_CHAR_LIST, scale=1.0, html_bg_color="white"):
        _, in_suffix = os.path.splitext(input)
        try:
            _, out_suffix = os.path.splitext(output)
        except:
            out_suffix = None
        if in_suffix in self.image_format:
            if self.return_color:
                grey_image, color_image = self._read_image(input)
                ascii_img, ascii_color = self._img2ascii(grey_image=grey_image, color_image=color_image, char_list=char_list, scale=scale)
            else:
                grey_image = self._read_image(input)
                ascii_img = self._img2ascii(grey_image=grey_image, char_list=char_list, scale=scale)
                ascii_color = [["#000000"] * len(ascii_img[0])] * len(ascii_img)
            if out_suffix == '.txt':
                # output ascii art to text file
                with open(output, mode="wb") as of:
                    for line in ascii_img:
                        of.write("{}\n".format("".join(line)))
                of.close()
            elif out_suffix == '.png' or out_suffix == '.jpg':
                if self.method == 'pillow':
                    fig = plt.figure(figsize=(20, 20))
                    plt.xlim(0, len(ascii_img[0]))
                    plt.ylim(0, len(ascii_img))
                    for j, line in enumerate(ascii_img):
                        for i, symbol in enumerate(line):
                            plt.text(i, len(ascii_img) - j, symbol, fontsize=6, color=ascii_color[j][i])
                    plt.axis('off')
                    fig.savefig(output)
                elif self.method == 'opencv':
                    output_img = self._cv_image(ascii_img=ascii_img, ascii_color=ascii_color)
                    cv2.imwrite(output, output_img)
            elif out_suffix == '.html':
                with open(output, mode="wb") as of:
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
            elif out_suffix == None:
                output_str = ""
                for line in ascii_img:
                    output_str += "".join(line) + "\n"
                os.system(self.clear_console)
                sys.stdout.write(output_str)
            else:
                raise ValueError("Only .txt, .html, {} output file format accepted, but {} found".format("".join(self.image_format), out_suffix))
        elif in_suffix in self.video_format:
            if out_suffix in self.video_format:
                writer = skvideo.io.FFmpegWriter(output)
                if self.return_color:
                    for grey_frame, color_frame in self._read_video(video_path=input):
                        ascii_img, ascii_color = self._img2ascii(grey_image=grey_frame, color_image=color_frame,
                                                                        char_list=char_list, scale=scale)
                        output_img = self._cv_image(ascii_img=ascii_img, ascii_color=ascii_color)
                        writer.writeFrame(output_img)
                else:
                    for grey_frame in self._read_video(video_path=input):
                        ascii_img = self._img2ascii(grey_image=grey_frame, char_list=char_list, scale=scale)
                        ascii_color = [[(255, 255, 255)] * len(ascii_img[0])] * len(ascii_img)
                        output_img = self._cv_image(ascii_img=ascii_img, ascii_color=ascii_color)
                        writer.writeFrame(output_img)
                writer.close()
            elif out_suffix == None:
                total_video = []
                self.return_color = False
                video_temp_file = input + ".temp"
                if not os.path.exists(video_temp_file):
                    with open(video_temp_file, "wb") as of:
                        first_frame = True
                        for grey_frame in self._read_video(video_path=input):
                            ascii_img = self._img2ascii(grey_image=grey_frame, char_list=char_list, scale=scale)
                            output_str = ""
                            for line in ascii_img:
                                output_str += "".join(line) + "\n"
                            total_video.append(output_str)
                            if first_frame:
                                of.write("{}\n".format(len(ascii_img)))
                                first_frame = False
                            of.write(output_str)
                    of.close()
                else:
                    row = 1
                    frame_str = ""
                    with open(video_temp_file, "rb") as fi:
                        frame_row = int(fi.readline().strip())
                        for line in fi:
                            frame_str += line
                            if row % frame_row == 0:
                                total_video.append(frame_str)
                                frame_str = ""
                            row += 1
                    fi.close()
                for frame in total_video:
                    #os.system(self.clear_console)
                    sys.stdout.write(frame)
                    sys.stdout.flush()
                    sys.stdout.write("\x1b[0;0H")
                    time.sleep(0.015)
        else:
            raise ValueError("Only image or video input file are accepted, but {} found!".format(in_suffix))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help="input image/video file")
    parser.add_argument("--output", type=str, default=None, help="output image/video/txt/html file")
    parser.add_argument("--return_color", action='store_true', help="convert image with origin color or to grayscale image")
    parser.add_argument("--scale", type=float, default=1.0, help="magnitude to scale image. For high resolution video or image, use fractional number like 0.3")
    parser.add_argument("--method", default="pillow", help="choose module for image processing: opencv or pillow")
    parser.add_argument("--html_bg_color", default="white", help="when ouput is html file, set background color")
    if len(sys.argv[1:]) == 0 or sys.argv[1] == '--help':
        parser.print_help()
        parser.exit()
    args = parser.parse_args()
    ascii_art_obj = ASCIIArt(method=args.method, return_color=args.return_color)
    ascii_art_obj.draw_ascii(input=args.input, output=args.output, html_bg_color=args.html_bg_color, scale=args.scale)