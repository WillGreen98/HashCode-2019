import os
from image import Image

files_list = ["a_example.txt", "b_lovely_landscapes.txt", "c_memorable_moments.txt","d_pet_pictures.txt", "e_shiny_selfies.txt"]
path = os.path.abspath("~/Desktop/Programming/Google/HashCode/HashCode-2019/Qualification-Round/Material/")

relPath = "Material/"

def open_file():
    with open(path + files_list, 'r') as file:
        data = file.read()
        line = file.readline()
        #print(data)
        #print(line)
    file.closed

def open_single_file(file_name):
    img_arr = []

    testFile = relPath + file_name
    with open(testFile, 'r') as file:
        lines = int(file.readline())
        for i in range(lines):
            line = file.readline().split(" ")
            orientation = line[0]
            if orientation == "V":
                orientation = "V"
            elif orientation == "H":
                orientation = "H"
            else:
                print("ERROR WHILE PARSING")
            #create image
            tags = line[2:-1] + [line[-1][:-1]]
            newImage = Image(i,tags,orientation)
            #print(f"img{i}:{orientation}:{tags}")
            img_arr.append(newImage)
    file.closed
    return img_arr

def write_file(name, out):
    with open(name, 'w+') as file_out:
        file_out.write(out)

if __name__ == '__main__':
    print("test")
    print(open_single_file(files_list[0]))
