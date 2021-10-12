import PIL
from PIL import Image
import math
import numpy as np
import webcolors

# ascii characters
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]
N = len(ASCII_CHARS)

# resize image
def resize_image(image, new_width):
    width, height = image.size
    ratio = height/width
    new_height = int(ratio*new_width)
    resized_image = image.resize((new_width,new_height))
    return resized_image

# convert to shades of grey
def grayify(image):
    return image.convert("L")

# stores pixels color info
def pixels_to_color_name(pixels):
    color_info = []
    for pixel in pixels:
        color_info.append(webcolors.rgb_to_name(pixel))
    return np.array(color_info)

def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = ""
    for pixel in pixels:
        characters += ASCII_CHARS[pixel//math.floor(255/(N-1))]
    return characters

def main():
    new_width = int(input("Enter a new width for the output:\n"))
    path = input("Enter a valid pathname to an image:\n")
    try:
        image = PIL.Image.open(path)
    except:
        print(path, "is not a valid pathname to an image")
    resized_image = resize_image(image,new_width)
    
    grey_image = grayify(image)
    color_info = pixels_to_color_name(image)

    new_image_data = pixels_to_ascii(grey_image)
    for i in range(len(new_image_data)):
        if new_image_data[i] == ".":
            new_image_data = new_image_data[:i]+" "+new_image_data[i+1:]
    pixel_count = len(new_image_data)
    ascii_image = "\n".join([new_image_data[i:(i+new_width)] for i in range(0,pixel_count, new_width)])
    print(ascii_image)
        
main()
