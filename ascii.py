import PIL
from PIL import Image
import math

# ascii characters
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]
N = len(ASCII_CHARS)

#resize image
def resize_image(image, new_width):
    width, height = image.size
    ratio = height/width
    new_height = int(ratio*new_width)
    resized_image = image.resize((new_width,new_height))
    return resized_image

# convert pixels
def grayify(image):
    return image.convert("L")

def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = ""
    for pixel in pixels:
        characters += ASCII_CHARS[pixel//math.floor(255/(N-1))]
    return characters

def main():
    new_width = int(input("Enter a new width for the output:\n"))
    path = input("Enter a valid pathname to an image:\n")
    # path = "/Users/paulcoste/Desktop/bur/img.png"
    try:
        image = PIL.Image.open(path)
    except:
        print(path, "is not a valid pathname to an image")
    new_image_data = pixels_to_ascii(grayify(resize_image(image,new_width)))
    for i in range(len(new_image_data)):
        if new_image_data[i] == ".":
            new_image_data = new_image_data[:i]+" "+new_image_data[i+1:]
    pixel_count = len(new_image_data)
    ascii_image = "\n".join([new_image_data[i:(i+new_width)] for i in range(0,pixel_count, new_width)])
    print(ascii_image)
    with open("ascii_image.txt","w") as f:
        f.write(ascii_image)
        
main()
