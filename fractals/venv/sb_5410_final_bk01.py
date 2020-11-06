# BSSD Midterm Project
# Scott Bing
# Image Analysis

from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageDraw, ImageTk, ImageOps, ImageEnhance, ImageFont
import tkinter.font as font
from SortFunctions import selectionSort
from SortFunctions import quickSortIterative
from SearchFunctions import binarySearchSub
from PixelFunctions import *
import numpy as np
import colorsys
import os

TOGGLE_SLICE = False
TOLERENCE = False
RED = 183
GREEN = 198
BLUE = 144


class Application(Frame):
    """ GUI application that displays the image processing
        selections"""

    def __init__(self, master):
        """ Initialize Frame - application constructor"""
        super(Application, self).__init__(master)

        Frame.__init__(self, master)
        self.master = master

        # reverse_btn = Button(self)

        #Menu taken from:     https://www.tutorialspoint.com/python/tk_menu.htm
        # create menu
        menu = Menu(self.master)
        self.master.config(menu=menu)

        fileMenu = Menu(menu, tearoff=0)
        fileMenu.add_command(label="New", command=self.donothing)
        fileMenu.add_command(label="Open", command=self.openFile)
        fileMenu.add_command(label="Save", command=self.donothing)
        fileMenu.add_command(label="Save as...", command=self.donothing)
        fileMenu.add_command(label="Close", command=self.donothing)

        fileMenu.add_separator()

        fileMenu.add_command(label="Exit", command=root.quit)
        menu.add_cascade(label="File", menu=fileMenu)
        editMenu = Menu(menu, tearoff=0)
        editMenu.add_command(label="Undo", command=self.donothing)

        editMenu.add_separator()

        editMenu.add_command(label="Cut", command=self.donothing)
        editMenu.add_command(label="Copy", command=self.donothing)
        editMenu.add_command(label="Paste", command=self.donothing)
        editMenu.add_command(label="Delete", command=self.donothing)
        editMenu.add_command(label="Select All", command=self.donothing)

        menu.add_cascade(label="Edit", menu=editMenu)
        helpMenu = Menu(menu, tearoff=0)
        helpMenu.add_command(label="Help Index", command=self.donothing)
        helpMenu.add_command(label="About...", command=self.donothing)
        menu.add_cascade(label="Help", menu=helpMenu)

        self.selected_pixels = []  # list of tuples [()]

        self.grid()
        self.create_initial_screen()

    #end application constructor

    def openFile(self):
        """Process the Open File Menu"""
        self.fileName = askopenfilename(parent=self, initialdir="C:/", title='Choose an image.')
        print(self.fileName)

        self.putImage(self.fileName)

        # open the application frame
        self.create_widgets()

    #end def openFile(self):

    def donothing(self):
        """Placeholder for inactive menu items"""
        pass

    #end def donothing(self):

    def clearScreen(self):
        """Clears the screen"""
        # clear checkboxes
        self.is_resize.set(False)
        self.is_reverse.set(False)
        self.is_rotate.set(False)
        self.is_reverse.set(False)
        self.is_flip.set(False)
        self.is_bright.set(False)
        self.is_contrast.set(False)
        self.is_sharpness.set(False)

        # clear text boxes
        self.height_ent.delete(0, 'end')
        self.width_ent.delete(0, 'end')
        self.angle_ent.delete(0, 'end')

        # clear lables
        self.err2show.set("")

        # deselect radio buttons
        self.flipValue.set(None)

        # initialize sliders
        self.bright_value.set(1.0)
        self.contrast_value.set(1.0)
        self.sharpness_value.set(1.0)

    #end def clearScreen(self):

    # function to be called when mouse is clicked
    def getcoords(self, event):
        # outputting x and y coords to console
        """Captures currrent screen coordinates
        using mouse clicks"""
        self.selected_pixels.append((event.x, event.y))
        print("Selected Pixels: ", self.selected_pixels)
        print(event.x, event.y)
        return (event.x, event.y)

    #end def getcoords(self, event):

    def putImage(self, fileName):
        """Get the image from the Open menu and
            place it on the main applicaiton frame """
        # Show the user selected image
        # set up orginal story frame
        imageFrame = LabelFrame(self, text="Original Story")
        imageFrame.grid(row=0, column=0, columnspan=3, sticky="nsew")

        self.image = Image.open(self.fileName)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas = Canvas(imageFrame, bd=0, width=self.photo.width(), height=self.photo.height())
        self.canvas.grid(row=0, column=0, sticky=N + S + E + W)

        # handle mouse clicks
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
        self.canvas.bind("<Button 1>", self.getcoords)

        print("Current Image Size: ", self.image.size)

        # this lines UNPACKS values
        # of variable a
        (h, w) = self.image.size

        # create a label and text entry for the name of a person
        Label(self,
              text="Current Image Size: " + str(h) + "x" + str(w)
              ).grid(row=1, column=0, sticky=W)

    #end def putImage(self, fileName):

    def create_initial_screen(self):
        """Create the opening screen"""
        self.lblFont = font.Font(weight="bold")
        self.lblFont = font.Font(size=16)



        Label(self,
              text="Use the 'File -> Open' menu above to select an image file to process:",
              wraplength=300,
              font=self.lblFont
              ).grid(row=0, column=0, sticky=NSEW, pady=7)

    #end def create_initial_screen(self):

    def create_widgets(self):
        """ Create and place screen widgets in the
        main application frame"""
        # # create resize check button
        self.is_resize = BooleanVar()
        Checkbutton(self,
                    text="Resize",
                    variable=self.is_resize
                    ).grid(row=2, column=0, sticky=W)
        Label(self,
              text="Height:"
              ).grid(row=2, column=0, sticky=E)
        self.height_ent = Entry(self, width=10)
        self.height_ent.grid(row=2, column=1, sticky=W)
        Label(self,
              text="Width:"
              ).grid(row=2, column=1, sticky=E)
        self.width_ent = Entry(self, width=10)
        self.width_ent.grid(row=2, column=2, sticky=W)

        # Rotate Check button
        self.is_rotate = BooleanVar()
        Checkbutton(self,
                    text="Rotate Image",
                    variable=self.is_rotate
                    ).grid(row=3, column=0, sticky=W)
        Label(self,
              text="Angle:"
              ).grid(row=3, column=0, sticky=E)
        self.angle_ent = Entry(self, width=10)
        self.angle_ent.grid(row=3, column=1, sticky=W)

        # Flip image button
        self.is_flip = BooleanVar()
        Checkbutton(self,
                    text="Flip Image",
                    variable=self.is_flip
                    ).grid(row=4, column=0, sticky=W)

        self.flipValue = IntVar()

        self.is_vertical = Radiobutton(self,
                    text='Vertical',
                    variable=self.flipValue, value=1
                    ).grid(row=4, column=0, sticky=E)

        self.is_horizontal = Radiobutton(self,
                    text='Horizontal',
                    variable=self.flipValue, value=2
                    ).grid(row=4, column=1, sticky=W)

        # Reverse image button
        self.is_reverse = BooleanVar()
        Checkbutton(self,
                    text="Reverse Image",
                    variable=self.is_reverse
                    ).grid(row=5, column=0, sticky=W)

        # create a CheckBox and text entry for a Brightness
        # Brightness setting button
        self.is_bright = BooleanVar()
        Checkbutton(self,
                    text="Brightness",
                    variable=self.is_bright
                    ).grid(row=7, column=0, sticky=W)

        self.bright_value = DoubleVar()
        Scale(self,
              variable=self.bright_value,
              from_ = .5, to = 2,
              resolution=0.5,
              orient = HORIZONTAL
              ).grid(row=7, column=0, sticky=E)
        self.bright_value.set(1.0)

        # create a filler
        Label(self,
              text="1 - original; gt. 1 - Bright; lt. 1 Dark"
              ).grid(row=7, column=1, sticky=W)

        # create a CheckBox and text entry for a Contrast
        # Contrast setting button
        self.is_contrast = BooleanVar()
        Checkbutton(self,
                    text="Contrast",
                    variable=self.is_contrast
                    ).grid(row=8, column=0, sticky=W)

        self.contrast_value = DoubleVar()
        Scale(self,
              variable=self.contrast_value,
              from_=.5, to=2,
              resolution=0.5,
              orient=HORIZONTAL
              ).grid(row=8, column=0, sticky=E)
        self.contrast_value.set(1.0)

        # create a filler
        Label(self,
              text="1 - original; gt. 1 - more Contrast; lt. 1 less Contrast"
              ).grid(row=8, column=1, sticky=W)

        # create a CheckBox and text entry for a Sharpness
        # Sharpness setting button
        self.is_sharpness = BooleanVar()
        Checkbutton(self,
                    text="Sharpness",
                    variable=self.is_sharpness
                    ).grid(row=9, column=0, sticky=W)

        self.sharpness_value = DoubleVar()
        Scale(self,
              variable=self.sharpness_value,
              from_=.5, to=2,
              resolution=0.5,
              orient=HORIZONTAL
              ).grid(row=9, column=0, sticky=E)
        self.sharpness_value.set(1.0)

        # create a filler
        Label(self,
              text="1 - original; gt. 1 - more Sharpness; lt. 1 less Sharpness"
              ).grid(row=9, column=1, sticky=W)

        btnFont = font.Font(weight="bold")
        btnFont = font.Font(size=19)

        # create a the sort pixels button
        self.sort_btn = Button(self,
                                   text="Sort Pixels",
                                   command=self.sortPixels,
                                   # bg='blue',
                                   # fg='#ffffff',
                                   highlightbackground='#3E4149',
                                   ).grid(row=10, column=0, sticky=W, padx=20, pady=5)

        # create a the scramble pixels button
        self.scramble_btn = Button(self,
                               text="Scramble",
                               command=self.scramblePixels,
                               # bg='blue',
                               # fg='#ffffff',
                               highlightbackground='#3E4149',
                               ).grid(row=11, column=0, sticky=W, padx=20, pady=5)

        # create a thumbnail image button
        self.thumbnail_btn = Button(self,
                                    text="Thumbnail",
                                    command=self.thumbnail,
                                    # bg='blue',
                                    # fg='#ffffff',
                                    highlightbackground='#3E4149',
                                    ).grid(row=13, column=0, sticky=W, padx=20, pady=5)

        # create a watermark on an image button
        self.watermark_btn = Button(self,
                                    text="Watermark",
                                    command=self.watermark,
                                    highlightbackground='#3E4149',
                                    ).grid(row=14, column=0, sticky=W, padx=20, pady=5)


        # create a colorized image button
        self.colorize_btn = Button(self,
                                   text="Adjust Tolerance",
                                   command=self.colorize,
                                   highlightbackground='#3E4149',
                                   ).grid(row=15, column=0, sticky=W, padx=20, pady=5)

        # create a colorized image button
        self.capture_btn = Button(self,
                                   text="Crop Image",
                                   command=self.capture,
                                   highlightbackground='#3E4149',
                                   ).grid(row=16, column=0, sticky=W, padx=20, pady=5)

        # create a filler
        Label(self,
              text=" "
              ).grid(row=17, column=0, sticky=W)

        # create a the clear screen button
        self.clear_btn = Button(self,
                                text="Clear",
                                command=self.clearScreen,
                                highlightbackground='#3E4149',
                                font=btnFont
                                ).grid(row=18, column=0, sticky=E, pady=10, padx=5)

        # create a the generate button
        self.generate_btn = Button(self,
                                   text="Generate",
                                   command=self.processSelections,
                                   highlightbackground='#3E4149',
                                   font=btnFont
                                   ).grid(row=18, column=1, sticky=W, pady=10, padx=5)

        self.errFont = font.Font(weight="bold")
        self.errFont = font.Font(size=20)
        self.err2show = StringVar()
        Label(self,
              textvariable=self.err2show,
              foreground="red",
              font=self.errFont,
              wraplength=200
              ).grid(row=19, column=0, sticky=NSEW, pady=4)

    #end def create_widgets(self):


    # Check for numeric and -1-255
    # Taken from:
    # https://stackoverflow.com/questions/31684082/validate-if-input-string-is-a-number-between-0-255-using-regex
    # numeric validation
    def is_number(self, n):
        try:
            int(n)
            return True
        except ValueError:
            return False

    # end def is_number(n):

    def capture(self):
        """Creates image from selected pixel range
        The Crop Image routine"""
        # get current image
        im = Image.open(self.fileName)
        pixels = im.load()
        #pixels = storePixels(im)  # store rgb pixels
        # manipulate file name for save process
        baseFile = self.fileName.split('/')
        length = len(baseFile)
        base = baseFile[len(baseFile) - 1]
        print(baseFile[len(baseFile) - 1])
        print("len(self.selected_pixels): ", len(self.selected_pixels))

        # grab the selected pixes
        if len(self.selected_pixels) >= 1:
            pixel1 = self.selected_pixels[len(self.selected_pixels)-1]
            print("First pixel: ", pixel1)
            pixel2 = self.selected_pixels[len(self.selected_pixels)-2]
            print("Second pixel: ", pixel2)

            x1, y1 = pixel1
            print("x1: ", x1)
            print("y1: ", y1)

            x2, y2 = pixel2
            print("x2: ", x2)
            print("y2: ", y2)

            size = (abs(x1-x2), abs(y1-y2))
            print("Image Size = ", size)

            # Create output image
            out = Image.new("RGB", size)
            draw = ImageDraw.Draw(out)

            print("out.width: ", out.width)
            print("out.height: ", out.height)

            # flip the x's
            if x1 < x2:
                tmpx = x1
                x1 = x2
                x2 = tmpx


            # Cropped image of above dimension
            # (It will not change orginal image)
            out = im.crop((x2, y2, x1, y1))

            # Shows the image in image viewer
            out.show()

            # save reversed image
            out.save('new_image-' + base)
            print("file new_image-" + base + " saved")
            self.clearScreen()

    #end def capture(self):

    def watermark(self):
        # Taken from https://medium.com/analytics-vidhya/some-interesting-tricks-in-python-pillow-8fe5acce6084
        """mark the picture with a watermark"""
        # open image to apply watermark to
        im = Image.open(self.fileName)
        # manipulate file name for save process
        baseFile = self.fileName.split('/')
        length = len(baseFile)
        base = baseFile[len(baseFile) - 1]
        print(baseFile[len(baseFile) - 1])
        im.convert("RGB")
        # get image size
        im_width, im_height = im.size
        # 5 by 4 water mark grid
        wm_size = (int(im_width * 0.20), int(im_height * 0.25))
        wm_txt = Image.new("RGBA", wm_size, (255, 255, 255, 0))
        # set text size, 1:40 of the image width
        font_size = int(im_width / 40)
        # load font e.g. gotham-bold.ttf
        font = ImageFont.truetype('/Library/Fonts/Arial.ttf', 20)

        d = ImageDraw.Draw(wm_txt)
        wm_text = "Scott Bing"
        # centralize text
        left = (wm_size[0] - font.getsize(wm_text)[0]) / 2
        top = (wm_size[1] - font.getsize(wm_text)[1]) / 2
        # RGBA(0, 0, 0, alpha) is black
        # alpha channel specifies the opacity for a colour
        alpha = 75
        # write text on blank wm_text image
        d.text((left, top), wm_text, fill=(0, 0, 0, alpha), font=font)
        # uncomment to rotate watermark text
        # wm_txt = wm_txt.rotate(15,  expand=1)
        # wm_txt = wm_txt.resize(wm_size, Image.ANTIALIAS)
        for i in range(0, im_width, wm_txt.size[0]):
            for j in range(0, im_height, wm_txt.size[1]):
                im.paste(wm_txt, (i, j), wm_txt)

        im.save('watermark-' + base)
        print("file watermark-" + base + " saved")

        self.clearScreen()

    #end def watermark(self):

    def thumbnail(self):
        # Taken from https://medium.com/analytics-vidhya/some-interesting-tricks-in-python-pillow-8fe5acce6084
        """make a thumbnail from the originally user
            selected image"""
        im = Image.open(self.fileName)
        # manipulate file name for save process
        baseFile = self.fileName.split('/')
        length = len(baseFile)
        base = baseFile[len(baseFile) - 1]
        print(baseFile[len(baseFile) - 1])
        # set the maximum width and height for the thumbnail
        max_thumbnail_size = (50, 50)
        # applying size for thumbnail
        im.thumbnail(max_thumbnail_size)
        # creating thumbnail
        im.save('thumbnail-' + base)
        print("file thumbnail-" + base + " saved")

        self.clearScreen()

    # show image in preview
        im.show()

    #end of def thumbnail(self):

    def colorize(self):
        '''process tolerance'''
        self.lblFont = font.Font(weight="bold")
        self.lblFont = font.Font(size=16)

        self.colorFrame = Toplevel(self)
        self.colorFrame.wm_title("Colorize Settings")

        Label(self.colorFrame,
              text="Select a Tolerance value and a color using the RGB sliders and press Generate.",
              wraplength=200,
              font=self.lblFont
              ).grid(row=0, column=0, sticky=W, padx=10, pady=10)

        Label(self.colorFrame,
              text="Tolerance:"
              ).grid(row=1, column=0, sticky=W, padx=10, pady=10)
        self.tolerance_ent = Entry(self.colorFrame, width=10)
        self.tolerance_ent.grid(row=1, column=0, sticky=E, padx=10, pady=10)

        self.red_value = DoubleVar()
        Scale(self.colorFrame,
              variable=self.red_value,
              from_=0, to=255,
              resolution=1,
              label="Red",
              orient=HORIZONTAL
              ).grid(row=2, column=0, sticky=NSEW, padx=10, pady=10)
        self.red_value.set(0)

        self.green_value = DoubleVar()
        Scale(self.colorFrame,
              variable=self.green_value,
              from_=0, to=255,
              resolution=1,
              label="Green",
              orient=HORIZONTAL
              ).grid(row=3, column=0, sticky=NSEW, padx=10, pady=10)
        self.green_value.set(0)

        self.blue_value = DoubleVar()
        Scale(self.colorFrame,
              variable=self.blue_value,
              from_=0, to=255,
              resolution=1,
              label="Blue",
              orient=HORIZONTAL
              ).grid(row=4, column=0, sticky=NSEW, padx=10, pady=10)
        self.blue_value.set(0)

        # create a the generate button
        self.gen_colorize_btn = Button(self.colorFrame,
                                   text="Generate",
                                   command=self.processColorize,
                                   highlightbackground='#3E4149',
                                   font=self.lblFont
                                   ).grid(row=5, column=0, sticky=E, pady=10, padx=5)

        self.cerr2show = StringVar()
        Label(self.colorFrame,
              textvariable=self.cerr2show,
              foreground="red",
              font=self.errFont,
              wraplength=200
              ).grid(row=6, column=0, sticky=NSEW, pady=4)

    #end def colorize(self):

    # Taken from: https://www.codingame.com/playgrounds/2524/basic-image-manipulation/colors
    # Square distance between 2 colors
    def distance2(self, color1, color2):
        """square distance between 2 colors"""
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        return (r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2

    #end distance2(self, color1, color2):

    # Taken from: https://www.codingame.com/playgrounds/2524/basic-image-manipulation/colors
    def processColorize(self):
        """ Adds a user selected color to the image """
        # read each pixel into memory as the image object im
        err = False
        im = Image.open(self.fileName)
        pixels = im.load()
        #pixels = storePixels(im)
        print("stored")
        # manipulate file name for save process
        baseFile = self.fileName.split('/')
        length = len(baseFile)
        base = baseFile[len(baseFile) - 1]
        print(baseFile[len(baseFile) - 1])

        # Create output image
        out = Image.new("RGB", im.size)
        draw = ImageDraw.Draw(out)

        # get select color
        red = (int(self.red_value.get()))
        green = (int(self.green_value.get()))
        blue = (int(self.blue_value.get()))
        color_to_change = (red, green, blue)

        # check threshold
        try:
            t = int(self.tolerance_ent.get())
        except Exception as e:
            err = True
            self.cerr2show.set("Colorize Tolerance value is missing or invalid")

        if err == False:
            # get tolerance value
            threshold = (int(self.tolerance_ent.get()))

            # Generate image
            for x in range(im.width):
                for y in range(im.height):
                    r, g, b = pixels[x, y]
                    if self.distance2(color_to_change, pixels[x, y]) < threshold ** 2:
                        r = int(r * (red/255))
                        g = int(g * (green/255))
                        b = int(b * (blue/255))
                    draw.point((x, y), (r, g, b))

            out.save("output.png")
            out.save('colorized-' + base)
            print("file colorized-" + base + " saved")

            self.colorFrame.destroy()

        #end def processColorize(self):

    # taken from here: https://ehmatthes.github.io/pcc_2e/beyond_pcc/pillow/#examining-multiple-pixels
    def scramblePixels(self):
        """ Randomly scrambles the pixel values """
        # read each pixel into memory as the image object im
        im = Image.open(self.fileName)
        pixels = storePixels(im)
        print("stored")
        # manipulate file name for save process
        baseFile = self.fileName.split('/')
        length = len(baseFile)
        base = baseFile[len(baseFile) - 1]
        print(baseFile[len(baseFile) - 1])
        # Taken from:
        # https: // stackoverflow.com / questions / 36468530 / changing - pixel - color - value - in -pil
        rr, gg, bb = im.split()
        rr = rr.point(lambda p: 0 if p == 0 else np.random.randint(256))
        gg = gg.point(lambda p: 0 if p == 0 else np.random.randint(256))
        bb = bb.point(lambda p: 0 if p == 0 else np.random.randint(256))
        out_img = Image.merge("RGB", (rr, gg, bb))
        out_img.getextrema()
        out_img.show()

        out_img.save('scrambled-' + base)
        print("sorted-" + base + " saved")

    #end def scramblePixels(self):

    def sortPixels(self):
        """ Sorts the image pixels and writes
            out a new image """
        # read each pixel into memory as the image object im
        im = Image.open(self.fileName)
        pixels = storePixels(im)
        print("stored")
        # manipulate file name for save process
        baseFile = self.fileName.split('/')
        length = len(baseFile)
        base = baseFile[len(baseFile) - 1]
        print(baseFile[len(baseFile) - 1])

    #end def sortPixels(self):

        ### sort copy of pixels ###
        sorted_pixels = pixels.copy()
        quickSortIterative(sorted_pixels, 0, len(sorted_pixels) - 1, comparePixels)
        print("sorted")
        sorted_im = pixelsToImage(im, sorted_pixels)
        sorted_im.save('sorted-' + base)
        print("sorted-" + base + " saved")

    def brightness(self):
        """brightens or darkens the image"""
        # get current image
        im = Image.open(self.fileName)
        # manipulate file name for save process
        baseFile = self.fileName.split('/')
        length = len(baseFile)
        base = baseFile[len(baseFile) - 1]
        print(baseFile[len(baseFile) - 1])

        # image brightness enhancer
        enhancer = ImageEnhance.Brightness(im)
        factor = (float(self.bright_value.get()))
        im_out = enhancer.enhance(factor)
        if factor == 1:
            im_out.save('brt_original-' + base)
            print("file brt_original-" + base + " saved")
        elif factor < 1:
            im_out.save('brt_darkened-' + base)
            print("file brt_darkened-" + base + " saved")
        elif factor > 1:
            im_out.save('brt_brightened-' + base)
            print("file brt_brightened-" + base + " saved")
        self.clearScreen()

    #end def brightness(self):

    def constrast(self):
        """sets the contrast factor for the image"""
        # get current image
        im = Image.open(self.fileName)
        # manipulate file name for save process
        baseFile = self.fileName.split('/')
        length = len(baseFile)
        base = baseFile[len(baseFile) - 1]
        print(baseFile[len(baseFile) - 1])

        # image contrast enhancer
        enhancer = ImageEnhance.Contrast(im)
        factor = (float(self.contrast_value.get()))
        im_out = enhancer.enhance(factor)
        if factor == 1:
            im_out.save('ctr_original-' + base)
            print("file ctr_original-" + base + " saved")
        elif factor < 1:
            im_out.save('ctr_less-' + base)
            print("file ctr_less-" + base + " saved")
        elif factor > 1:
            im_out.save('ctr_more-' + base)
            print("file ctr_more-" + base + " saved")
        self.clearScreen()

    #end def constrast(self):

    def sharpness(self):
        """sets the sharpness factor for the image"""
        # get current image
        im = Image.open(self.fileName)
        # manipulate file name for save process
        baseFile = self.fileName.split('/')
        length = len(baseFile)
        base = baseFile[len(baseFile) - 1]
        print(baseFile[len(baseFile) - 1])

        # image contrast enhancer
        enhancer = ImageEnhance.Sharpness(im)
        factor = (float(self.sharpness_value.get()))
        im_out = enhancer.enhance(factor)
        if factor == 1:
            im_out.save('shp_original-' + base)
            print("file shp_original-" + base + " saved")
        elif factor < 1:
            im_out.save('shp_less-' + base)
            print("file shp_less-" + base + " saved")
        elif factor > 1:
            im_out.save('shp_more-' + base)
            print("file shp_more-" + base + " saved")
        self.clearScreen()

    #end def sharpness(self):

    # reverse the image
    def reverse(self):
        """converts an image ot grayscale"""
        # get current image
        im = Image.open(self.fileName)
        pixels = storePixels(im)  # store rgb pixels
        # manipulate file name for save process
        baseFile = self.fileName.split('/')
        length = len(baseFile)
        base = baseFile[len(baseFile) - 1]
        print(baseFile[len(baseFile) - 1])
        grayScale(im, pixels)  # grayscale pixels in place
        # save reversed image
        im.save('reverse-' + base)
        print("file reverse-" + base + " saved")
        self.clearScreen()

    #def reverse(self):

    # flip image on vertical axis
    def flip_vertical(self):
        """Flips an image vertically"""
        # get current image
        im = Image.open(self.fileName)
        # manipulate file name for save process
        baseFile = self.fileName.split('/')
        length = len(baseFile)
        base = baseFile[len(baseFile) - 1]
        print(baseFile[len(baseFile) - 1])
        # flip image vertiical
        out = im.transpose(Image.FLIP_TOP_BOTTOM)
        # save flipped image
        out.save('fl_vertical-' + base)
        print("file fl_vertical-" + base + " saved")
        self.clearScreen()

    #end def flip_vertical(self):

    # flip image on horizontal axis
    def flip_horizontal(self):
        """Flips an image horizontally"""
        # get current image
        im = Image.open(self.fileName)
        baseFile = self.fileName.split('/')
        # manipulate file name for save process
        length = len(baseFile)
        base = baseFile[len(baseFile) - 1]
        print(baseFile[len(baseFile) - 1])
        # flip image horizontal
        out = im.transpose(Image.FLIP_LEFT_RIGHT)
        # save flipped image
        out.save('fl_horizontal-' + base)
        print("file fl_horizontal-" + base + " saved")
        self.clearScreen()

    #end def flip_horizontal(self):

    # rotate an image
    def rotate(self):
        """Rotates and image based on a given angle
            0 - 360 degrees"""
        err = False
        # get current image
        im = Image.open(self.fileName)
        baseFile = self.fileName.split('/')
        # manipulate file name for save process
        length = len(baseFile)
        base = baseFile[len(baseFile) - 1]
        print(baseFile[len(baseFile) - 1])

        # check angle
        try:
            a = int(self.angle_ent.get())
        except Exception as e:
            err = True
            self.err2show.set("Rotate Angle value is missing or invalid")

        if err == False:
            # get angle
            angle = (int(self.angle_ent.get()))
            print("angle: ", angle)
            self.angle_ent['text'] = ""
            root.update()
            # rotate image
            out = im.rotate(angle)
            # save rotated image
            out.save('rotated-' + base)
            print("file rotated-" + base + " saved")
            self.clearScreen()

    #end def rotate(self):

    # resize an image
    def resize(self):
        """Resizes an image using dimensions
            entered by the user"""
        err = False
        # get current image
        im = Image.open(self.fileName)
        baseFile = self.fileName.split('/')
        # manipulate file name for save process
        length = len(baseFile)
        base = baseFile[len(baseFile) - 1]
        print(baseFile[len(baseFile) - 1])
        # if type(self.height_ent.get()) is not int:
        #     raise TypeError("Height either left blank or invalid")

        # check height
        try:
            h = int(self.height_ent.get())
        except Exception as e:
            err = True
            self.err2show.set("Resize Height value is missing or invalid")

        # check width
        try:
            w = int(self.width_ent.get())
        except Exception as e:
            err = True
            self.err2show.set("Resize Width value is missing or invalid")

        if err == False:
            size = (h, w)
            print("size: ", size)
            # resize image
            out = im.resize(size)
            # save resized image
            out.save('resized-' + base)
            print("file resized-" + base + " saved")
            self.clearScreen()

    #end def resize(self):

    # process user selections
    def processSelections(self):
        """Processes user screen selections"""
        if self.is_resize.get() == True:
            self.resize()
        elif self.is_rotate.get() == True:
            self.rotate()
        elif self.is_flip.get() == True:
            if self.flipValue.get() == 1:
                self.flip_vertical()
            elif self.flipValue.get() == 2:
                self.flip_horizontal()
        elif self.is_reverse.get() == True:
            self.reverse()
        elif self.is_bright.get() == True:
            self.brightness()
        elif self.is_contrast.get() == True:
            self.constrast()
        elif self.is_sharpness.get() == True:
            self.sharpness()

#end def processSelections(self):


# main
"""Application Entry Point - the main
driver code for the BSSD5410 Midterm Project"""
root = Tk()
root.resizable(height = None, width = None)
root.title("BSSD 5410 Midterm Scott Bing")
app = Application(root)
root.mainloop()
