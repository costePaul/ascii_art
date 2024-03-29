import PIL
from PIL import Image
import math
import argparse

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

# converts a shade of grey image into a string of ascii characters
def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = ""
    for pixel in pixels:
        characters += ASCII_CHARS[pixel//math.floor(255/(N-1))]
    return characters

def get_image_directory_and_name(path):
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

def main(parser):
    args = parser.parse_args()
    if not args.width:
        new_width = int(input("Enter a new width for the output:\n"))
    else:
        new_width = args.width
    if not args.path:
        path = input("Enter a valid pathname to an image:\n")
    else:
        path = args.path
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
    
    # print(ascii_image)
    if not args.output_file:
        dir,name = get_image_directory_and_name(path)
        result_path = dir+'/'+name+'.txt'
    else:
        result_path = args.output_file
    with open(result_path, 'w') as f:
        f.write(ascii_image)
    print("Result stored in ",result_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--width", dest="width", type=int, help="output width")
    parser.add_argument("-p", "--path", dest="path", type=str, help="image path")
    parser.add_argument("-o", "--output-file", dest="output_file", type=str, help="output file path")
    main(parser)
