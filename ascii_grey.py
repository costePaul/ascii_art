from __future__ import annotations
# import PIL
from PIL import Image
# from PIL.Image import core.ImagingCore
from PIL.Image import Image as TypeImage
import math
import argparse
import os

# ascii characters
# ASCII_CHARS: list[str] = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]
ASCII_CHARS: list[str] = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", ".", " "] # adding the space " " as an "empty" value to 
N:int = len(ASCII_CHARS)
step:int = math.floor(255/(N-1))

# resize image
def resize_image(image:TypeImage, new_width:int) -> TypeImage:
    width: int
    height: int
    width, height = image.size
    ratio:float = height/width
    new_height:int = int(ratio*new_width)
    resized_image:TypeImage = image.resize((new_width,new_height))
    return resized_image

# convert to shades of grey
def grayify(image:TypeImage) -> TypeImage:
    return image.convert("L")

# converts a shade of grey image into a string of ascii characters
def pixels_to_ascii(image:TypeImage, inversion:bool) -> str:
    pixels = image.getdata() # sequence object (=iterable) containing pixel values
    characters:str = ""
    pixel:int
    for pixel in pixels:
        if inversion:
            pixel = 255-pixel
        characters += ASCII_CHARS[pixel//step]
    return characters

def get_image_directory_and_name(path): # to replace by os.path.split(path)
    last_slash_index = 0
    last_dot_index = 0
    n = len(path)
    for i in range(n):
        if path[i]=='/':
            last_slash_index = i
    for i in range(last_slash_index,n):
        if path[i]=='.':
            last_dot_index = i
    if last_dot_index==0:
        return path[:last_slash_index],path
    else :
        return path[:last_slash_index],path[last_slash_index+1:last_dot_index]

def write_image_to_disc(ascii_image, path, output_file, _print=False):
    if result_path := output_file:
        pass
    else:
        dir:str
        name:str
        dir, name = os.path.split(path)
        result_path:str = dir+'/'+os.path.splitext(name)[0]+'.txt'
    with open(result_path, 'w') as f:
        f.write(ascii_image)
    if _print:
        print(ascii_image)
    print("Result stored in ",result_path)

def treat_image(image:TypeImage, new_width:int, inversion:bool) -> str:
    new_image_data:str = pixels_to_ascii(grayify(resize_image(image,new_width)), inversion)
    
    pixel_count:int = len(new_image_data)
    ascii_image:str = "\n".join([new_image_data[i:(i+new_width)] for i in range(0,pixel_count, new_width)])
    return  ascii_image

def main(parser):
    args = parser.parse_args()
    # Width
    if new_width := args.width:
       pass
    else:
        new_width = int(input("Enter a new width for the output:\n"))
    # Path
    if path := args.path:
        pass
    else:
        path = input("Enter a valid pathname to an image:\n")
    # open image
    try:
        image = Image.open(path)
    except:
        print(path, "is not a valid pathname to an image")
    
    ascii_image = treat_image(image, new_width, args.inversion)
    write_image_to_disc(ascii_image, path, args.output_file, _print=args.print)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--width", dest="width", type=int, help="output width")
    parser.add_argument("-p", "--path", dest="path", type=str, help="image path")
    parser.add_argument("-o", "--output-file", dest="output_file", type=str, help="output file path")
    parser.add_argument("-i", "--inversion", dest="inversion", type=bool, default=False, help="black white inversion")
    parser.add_argument("--print", dest="print", type=bool, default=False, help="If you wish to print the result in the console")
    print(type(parser))
    # main(parser)
