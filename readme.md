ascii_art.py script is used to convert videos/images to ascii art. If specified output file, including video, image, txt, html, converted ascii art will be saved in them, otherwise print out in terminal.

**PS:**
1. Make sure resolution of input video is not large when converting from video to ascii art video
2. If print out directly in terminal, adjust your terminal window size and font size first (in case of automatic wrapping)

### Usage:
python ascii_art.py [-h] [--input INPUT] [--output OUTPUT] [--return_color]
                    [--scale SCALE] [--method METHOD]
                    [--html_bg_color HTML_BG_COLOR]

#### optional arguments:
  -h, --help            show this help message and exit
  --input INPUT         input image/video file
  --output OUTPUT       output image/video/txt/html file
  --return_color        convert image with origin color or to grayscale image
  --scale SCALE         magnitude to scale image. For high resolution video or image, use fractional number like 0.3
  --method METHOD       choose module for image processing: opencv or pillow
  --html_bg_color HTML_BG_COLOR when ouput is html file, set background color

### Examples:
python ascii_art.py --input test.jpg --output out.txt
python ascii_art.py --input test.mp4 --scale 0.4 --method opencv