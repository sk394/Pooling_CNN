# Project 1- Suman Khadka -Pooling


import numpy as np
import sys



# @param: .pgm filename
# @return: a tuple (header, image array, pixel size) # image array - numpy array
def readpgm(name):
    with open(name) as f:
        lines = f.readlines()
    for l in list(lines):
        if l[0] == '#':  # for comments
            lines.remove(l)
    assert lines[0].strip() == 'P2'  # checks if the first line has P2 string
    data = []
    for line in lines[1:]:
        data.extend([int(c) for c in
                     line.split()])  # converts the split strings into ints and add to the end of the data array
    return (np.array(data[3:]), (data[1], data[0]), data[
        2])  # returns numpy array containing pixel values, width, height, and maximum pixel value of the image


# @param: image array; image header; name of the processed image
# return: NaN
def image_save(output_header, image_array, fileName):
    """
        Save the processed image to a PGM file.
        Returns:
        None
    """
    # Unpack the header information
    p2, comment, size, max_pixel = output_header

    # Open the file in write mode
    with open(fileName, 'w') as f:
        # Write the PGM header
        f.write(f"{p2}\n")
        f.write(f"# {comment}\n")
        f.write(f"{size[1]} {size[0]}\n")
        f.write(f"{int(max_pixel)}\n")

        # Flatten the 2D array to a 1D array
        flat_image = image_array.flatten()

        # Write the pixel values
        for i, pixel in enumerate(flat_image):
            f.write(str(int(pixel)))
            if( i + 1) % 125 ==0:
                f.write("\n")
            else:
                f.write("   ")
           

    print(f"Image saved as {fileName}")


# @param: image array, pool size
# @return: pooled array
def max_pooling(input_array, pool_size):
    """performs max pooling on the input image
         WE have the arguments:-> a 2D array representing the input image and the
         size of the pooling window
    """
    # output image size
    output_height = -(-input_array.shape[0]//pool_size)
    output_width = -(-input_array.shape[1]//pool_size)
    pooled_img = np.zeros((output_height, output_width))

    for i in range(output_height):
        for j in range(output_width):
            start_i, start_j = i * pool_size, j*pool_size
            end_i, end_j = min((i+1)*pool_size, input_array.shape[0]), min((j+1)*pool_size, input_array.shape[1])
            pooled_img[i,j]=np.max(input_array[start_i:end_i, start_j:end_j])
    return pooled_img


def median_pooling(input_array, pool_size):
    rows, cols = input_array.shape
    output_array = np.zeros((rows , cols ), dtype=np.uint8)

    for i in range(rows ):
        for j in range(cols ):
            # Extract the window
            window = input_array[i:i+pool_size, j:j+pool_size]

            # Calculate the median and assign to the output
            output_array[i, j] = np.median(window)

    return output_array

# @param: image array, pool size
# @return: oil painted image array
def oil_painting(image, pool_size):
    oil_array = median_pooling(image, pool_size)
    return oil_array

def main():
    # check if the correct number of arguments is passed
    if len(sys.argv)!=4:
        print("Incorrect cmd: run python main.py image.pgm pool_size max_poolOroil_paint(1/2)")
        sys.exit(1)

    # get the input image array, pool size and part
    img, pool_size, part = sys.argv[1], int(sys.argv[2]), sys.argv[3]

    # load the image
    data = readpgm(img)
    image = np.reshape(data[0],data[1])

    if part=="1":
        output_image = max_pooling(image, pool_size)
        fileName = f"{img.split('.')[0]}_pooled_{pool_size}.pgm"
    elif part=="2":
        output_image = oil_painting(image, pool_size)
        fileName = f"{img.split('.')[0]}_oil_painted_{pool_size}.pgm"
    else:
        print("Invalid output. Choose 1 or 2 for part.")
        sys.exit(1)

    # combine the header and image data to save the output
    # Save the processed image
    image_save(('P2', 'Suman Processed Image', output_image.shape, data[2]), output_image, fileName)


if __name__=='__main__':
    main()