ascii_art.py script is used to convert videos/images to ascii art. If specified output file, including video, image, txt, html, converted ascii art will be saved in them, otherwise print out in terminal.

**PS:** <br>
1. Make sure resolution of input video is not large when converting from video to ascii art video <br>
2. If print out directly in terminal, adjust your terminal window size and font size first (in case of automatic wrapping) <br>

### Usage:
python ascii_art.py [-h] [--input INPUT] [--output OUTPUT] [--return_color] <br>
                    [--scale SCALE] [--method METHOD] <br>
                    [--html_bg_color HTML_BG_COLOR] <br>

#### optional arguments:
  -h, --help            show this help message and exit <br>
  --input INPUT         input image/video file <br>
  --output OUTPUT       output image/video/txt/html file <br>
  --return_color        convert image with origin color or to grayscale image <br>
  --scale SCALE         magnitude to scale image. For high resolution video or image, use fractional number like 0.3 <br>
  --method METHOD       choose module for image processing: opencv or pillow <br>
  --html_bg_color HTML_BG_COLOR when ouput is html file, set background color <br>

### Examples:
python ascii_art.py --input test.jpg --output out.txt <br>
python ascii_art.py --input test.mp4 --scale 0.4 --method opencv <br>