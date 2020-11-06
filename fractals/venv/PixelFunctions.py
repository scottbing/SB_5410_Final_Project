from PIL import Image, ImageDraw
#from SortFunctions import selectionSort
#from SortFunctions import quickSort
#from SearchFunctions import binarySearchSub


def comparePixels(pix1, pix2):
    return pix1[0][0] > pix2[0][0]
# end def comparePixels(pix1,pix2):

def storePixels(im):
    width = int(im.size[0])
    height = int(im.size[1])

    # store ppixels inout double tuple format.
    pixel_array = []

    for i in range(width):  # for loop for x position
        for j in range(height):  # for loop for y position
            # get r and g and b values of pixel at position
            r, g, b = im.getpixel((i, j))
            pixel_array.append([(r, g, b), (i, j)])
        # end for j
    # end for i
    return pixel_array
# end def storePixels(im):

def pixelsToImage(im, pixels):
    outimg = Image.new("RGB", im.size)
    outimg.putdata([p[0] for p in pixels])
    outimg.show()
    return outimg
# end def pixelsToImage(im, pixels):

def pixelsToPoints(im, pixels):
    #defualt bakground color is black
    #outimg = Image.new("RGB",  size)
    for p in pixels:
        im.putpixel(p[1], p[0])
    im.show()
    #return outimg
# enddef pixelsToPoints(im, pixels):

def grayScale(im, pixels):
    draw = ImageDraw.Draw(im)
    for px in pixels:
        gray_av = int((px[0][0] + px[0][1] + px[0][2])/3)
        draw.point(px[1], (gray_av, gray_av, gray_av))
#end of def grayScale(im, pixels):
