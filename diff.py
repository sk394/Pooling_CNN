import numpy as np
import sys


# @param: .pgm filename
# @return: a tuple (header, image array) # image array - numpy array
def pgmFileRead(fileName):
    # Open the file in read mode; Read all lines into a list
    with open(fileName, 'r') as file:
        lines = file.readlines()

    img_header = [lines.pop(0)]  # P2
    while lines[0][0] == "#":  # comments
        img_header += [lines.pop(0)]

    width_height = lines.pop(0)
    width, height = tuple(map(int, width_height.split()))  # aspect ratio
    img_header += [width_height]
    img_header += [lines.pop(0)]  # gray scale levels
    img = np.array([int(n) for line in lines for n in line.split()])  # pixel values
    return img_header, img.reshape(height, width)


def compareImages(myProcessedFile, studentProcessedFile):
    info = ""
    img_header1, img1 = pgmFileRead(myProcessedFile)
    img_header2, img2 = pgmFileRead(studentProcessedFile)
    size1 = np.array(list(map(int, img_header1[-2].split())))
    size2 = np.array(list(map(int, img_header2[-2].split())))

    if img_header1[0] != img_header2[0]:
        info += "Different: format is different!\n"
    elif sum(abs(size1 - size2)) > 0:
        info += 'Different: image size!\n'
    elif img_header1[-1] != img_header2[-1]:
        info += "Different: gray scale level!\n"
    elif sum(sum(abs(img1-img2))) > 0:
        info += "Different: some pixel values!\n"
    return info


def main():
    myProcessedFile, studentProcessedFile = sys.argv[1:3]
    print('\nmyProcessedFile:', myProcessedFile,
          '\nstudentProcessedFile:', studentProcessedFile, "\n")
    info = compareImages(myProcessedFile, studentProcessedFile)
    if len(info) > 0:
        print(info)
    else:
        print("Same image!")


if __name__ == '__main__':
    main()
