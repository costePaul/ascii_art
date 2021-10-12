import PIL
from PIL import Image
import math
import numpy as np
import matplotlib

# Global variables
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]
N = len(ASCII_CHARS)
list_of_colors = ['grey','red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
list_of_rgb = [[128,128,128],[255,0,0],[0,255,0],[255,255,0],[0,0,255],[255,0,255],[0,255,255],[255,255,255]]
number_of_colors = len(list_of_colors)

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

# get closest color for the pixel in list_of_colors
def get_closest_color(pixel):
    distances = []
    for number in range(number_of_colors):
        distance = 0
        for i in range(3):
            distance += (pixel[i]-list_of_rgb[number][i])**2        
        distances.append(distance)
    return list_of_colors[np.argmin(np.array(distances))]

# stores pixels color info
def pixels_to_color_name(image):
    pixels = image.getdata()
    color_info = []
    for pixel in pixels:
        color_info.append(get_closest_color(pixel))
    return np.array(color_info)

# converts a shade of grey image into a string of ascii characters
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
    
    grey_image = grayify(resized_image)
    color_info = pixels_to_color_name(resized_image)

    new_image_data = pixels_to_ascii(grey_image)
    for i in range(len(new_image_data)):
        if new_image_data[i] == ".":
            new_image_data = new_image_data[:i]+" "+new_image_data[i+1:]
    pixel_count = len(new_image_data)
    
    counter = 0
    for i in range(pixel_count):
        if color_info[i] == list_of_colors[0]:
            pixel = "\033[1;30;40m "+new_image_data[i]+"\033[0m"
        elif color_info[i] == list_of_colors[1]:
            pixel = "\033[1;31;40m "+new_image_data[i]+"\031[0m"
        elif color_info[i] == list_of_colors[2]:
            pixel = "\033[1;32;40m "+new_image_data[i]+"\031[0m"
        elif color_info[i] == list_of_colors[3]:
            pixel = "\033[1;33;40m "+new_image_data[i]+"\031[0m"
        elif color_info[i] == list_of_colors[4]:
            pixel = "\033[1;34;40m "+new_image_data[i]+"\031[0m"
        elif color_info[i] == list_of_colors[5]:
            pixel = "\033[1;35;40m "+new_image_data[i]+"\031[0m"
        elif color_info[i] == list_of_colors[6]:
            pixel = "\033[1;36;40m "+new_image_data[i]+"\031[0m"
        else:
            pixel = "\033[1;37;40m "+new_image_data[i]
        if counter%new_width == 0:
            print(pixel)
        else:
            print(pixel,end='')
        counter += 1

main()