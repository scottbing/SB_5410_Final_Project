# BSSD Midterm Project
# Scott Bing
# Image Analysis

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageDraw, ImageTk, ImageOps, ImageEnhance, ImageFont
import matplotlib.pyplot as plt
from MandlebrotSet import *
from Julia import *
from RectSierpinski import *
from Tricircle import *
from Carpet import *
from SlideShow import *
from AnimateSierpinski import *
from AnimateDragon import *
from HilbertCurve import *
import tkinter.font as font
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

        # used when calling slideshow
        # pygame.init()

        # reverse_btn = Button(self)
        self.color_to_change = None
        self.color1_to_change = None
        self.color2_to_change = None
        self.color3_to_change = None

        # Menu taken from:     https://www.tutorialspoint.com/python/tk_menu.htm
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
        # open the application frame
        self.create_widgets()
        # self.create_initial_screen()

    # end application constructor

    def openFile(self):
        """Process the Open File Menu"""
        self.fileName = askopenfilename(parent=self, initialdir="C:/", title='Choose an image.')
        print(self.fileName)

        self.putImage(self.fileName)

        # open the application frame
        self.create_widgets()

    # end def openFile(self):

    def donothing(self):
        """Placeholder for inactive menu items"""
        pass

    # end def donothing(self):

    def clearScreen(self):
        """Clears the screen"""
        # clear checkboxes
        self.is_mandlebrot.set(False)
        self.is_julia.set(False)
        self.is_cubistic.set(False)
        self.is_symcolored.set(False)
        self.is_tricircle.set(False)
        self.is_carpet.set(False)

        # clear the colors
        # reverse_btn = Button(self)
        self.color_to_change = None
        self.color1_to_change = None
        self.color2_to_change = None
        self.color3_to_change = None

        # # clear text boxes
        # self.height_ent.delete(0, 'end')
        # self.width_ent.delete(0, 'end')
        # self.angle_ent.delete(0, 'end')
        #
        # # clear labels
        # self.err2show.set("")
        #
        # # deselect radio buttons
        # self.flipValue.set(None)
        #
        # # initialize sliders
        # self.bright_value.set(1.0)
        # self.contrast_value.set(1.0)
        # self.sharpness_value.set(1.0)

    # end def clearScreen(self):

    # function to be called when mouse is clicked
    def getcoords(self, event):
        # outputting x and y coords to console
        """Captures currrent screen coordinates
        using mouse clicks"""
        self.selected_pixels.append((event.x, event.y))
        print("Selected Pixels: ", self.selected_pixels)
        print(event.x, event.y)
        return (event.x, event.y)

    # end def getcoords(self, event):

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

    # end def putImage(self, fileName):

    def create_initial_screen(self):
        """Create the opening screen"""
        self.lblFont = font.Font(weight="bold")
        self.lblFont = font.Font(size=16)

        Label(self,
              text="Use the 'File -> Open' menu above to select an image file to process:",
              wraplength=300,
              font=self.lblFont
              ).grid(row=0, column=0, sticky=NSEW, pady=7)

    # end def create_initial_screen(self):

    def create_widgets(self):
        """ Create and place screen widgets in the
        main application frame"""
        self.lblFont = font.Font(weight="bold")
        self.lblFont = font.Font(size=20)

        Label(self,
              text="AMAZING FRACTALS",
              wraplength=300,
              font=self.lblFont
              ).grid(row=0, column=0, columnspan=3, sticky=NSEW, pady=7)

        ttk.Separator(self,
                      orient=HORIZONTAL
                      ).grid(row=1, column=0, columnspan=2, sticky=EW, pady=5, padx=5)

        animFont = font.Font(weight="bold")
        animFont = font.Font(size=21)

        Label(self,
              text="Static:",
              font=animFont
              ).grid(row=2, column=0, columnspan=2, sticky=W)

        # process mandlebrot set
        self.is_mandlebrot = BooleanVar()
        Checkbutton(self,
                    text="Mandelbrot Set",
                    variable=self.is_mandlebrot
                    ).grid(row=3, column=0, sticky=W)

        Label(self,
              text="Theme:"
              ).grid(row=3, column=1, sticky=W)

        self.theme = StringVar()
        self.themes = ttk.Combobox(self,
                                   width=10,
                                   textvariable=self.theme)

        # Adding combobox drop down list
        self.themes['values'] = ('ocean',
                                 'twilight',
                                 'inferno',
                                 'Purples_r',
                                 'prism',
                                 'rainbow',
                                 'autumn',
                                 'cubehelix',
                                 'copper_r',
                                 'gist_earth',
                                 'nipy_spectral',
                                 'Pastell')

        self.themes.grid(row=3, column=1, padx=57, sticky=W)

        # Shows ocean as a default value
        self.themes.current(0)

        # process julia set
        self.is_julia = BooleanVar()
        Checkbutton(self,
                    text="Julia",
                    variable=self.is_julia
                    ).grid(row=4, column=0, sticky=W)

        # process Cubistic Sierpinski Synthesis
        self.is_cubistic = BooleanVar()
        Checkbutton(self,
                    text="Cubistic Sierpinski",
                    variable=self.is_cubistic
                    ).grid(row=5, column=0, sticky=W)

        Label(self,
              text="Iterations:",
              ).grid(row=5, column=1, padx=157, sticky=W)

        self.itercube = IntVar()
        self.itercube.set(7)
        self.iter = Spinbox(self,
                            from_=1,
                            to=7,
                            width=3,
                            textvariable=self.itercube
                            # variable=self.iterations
                            ).grid(row=5, column=1, padx=230, sticky=W)

        # Process Randomly Colored Sierpinski Triangle
        self.is_symcolored = BooleanVar()
        Checkbutton(self,
                    text="Sierpinski Triangle",
                    variable=self.is_symcolored
                    ).grid(row=6, column=0, sticky=W)

        Label(self,
              text="Iterations:",
              ).grid(row=6, column=1, padx=157, sticky=W)

        self.itersym = IntVar()
        self.itersym.set(5)
        self.iter = Spinbox(self,
                            from_=1,
                            to=7,
                            width=3,
                            textvariable=self.itersym
                            # variable=self.iterations
                            ).grid(row=6, column=1, padx=230, sticky=W)

        # process tricircle
        self.is_tricircle = BooleanVar()
        Checkbutton(self,
                    text="Tricircle",
                    variable=self.is_tricircle
                    ).grid(row=7, column=0, sticky=W)

        # Process carpet
        self.is_carpet = BooleanVar()
        Checkbutton(self,
                    text="Carpet",
                    variable=self.is_carpet
                    ).grid(row=8, column=0, sticky=W)

        # create a colorized image button
        self.color_carpet_btn = Button(self,
                                       text="Select Colors",
                                       command=self.three_colors,
                                       highlightbackground='#2E4149',
                                       ).grid(row=8, column=1, sticky=W)

        Label(self,
              text="Iterations:",
              ).grid(row=8, column=1, padx=157, sticky=W)

        self.itercarp = IntVar()
        self.itercarp.set(5)
        self.iter_sp_carp = Spinbox(self,
                                    from_=1,
                                    to=7,
                                    width=3,
                                    textvariable=self.itercarp
                                    ).grid(row=8, column=1, padx=230, sticky=W)

        btnFont = font.Font(weight="bold")
        btnFont = font.Font(size=19)

        # create a the generate button
        self.generate_btn = Button(self,
                                   text="Generate",
                                   command=self.processSelections,
                                   highlightbackground='#3E4149',
                                   font=btnFont
                                   ).grid(row=9, column=0, sticky=W, pady=10, padx=5)

        # create a the clear screen button
        self.clear_btn = Button(self,
                                text="Clear",
                                command=self.clearScreen,
                                highlightbackground='#2E4149',
                                font=btnFont
                                ).grid(row=9, column=1, sticky=W, pady=10, padx=5)

        ttk.Separator(self,
                      orient=HORIZONTAL
                      ).grid(row=10, column=0, columnspan=2, sticky=NSEW, pady=5, padx=5)

        animFont = font.Font(weight="bold")
        animFont = font.Font(size=21)

        Label(self,
              text="Animated:",
              font=animFont
              ).grid(row=11, column=0, columnspan=2, sticky=W)

        # create a the animate sierpinski button
        self.sierpinski_btn = Button(self,
                                     text="Sierpinski",
                                     command=self.anim_sierpinski,
                                     highlightbackground='#3E4149',
                                     ).grid(row=12, column=0, sticky=W, padx=20, pady=5)

        # process animated sierpinski color
        self.color_sierpinski_btn = Button(self,
                                           text="Select Color",
                                           command=self.colorize,
                                           highlightbackground='#2E4149',
                                           ).grid(row=12, column=1, sticky=W)

        Label(self,
              text="Iterations:",
              ).grid(row=12, column=1, padx=157, sticky=W)

        self.itersier = IntVar()
        self.itersier.set(5)
        self.iter_sp_sier = Spinbox(self,
                                    from_=1,
                                    to=8,
                                    width=3,
                                    textvariable=self.itersier
                                    ).grid(row=12, column=1, padx=230, sticky=W)

        # create a the animate dragon button
        self.dragon_btn = Button(self,
                                 text="Dragon",
                                 command=self.anim_dragon,
                                 highlightbackground='#3E4149',
                                 ).grid(row=13, column=0, sticky=W, padx=20, pady=5)

        # process animated dragon color
        self.color_dragon_btn = Button(self,
                                       text="Select Color",
                                       command=self.colorize,
                                       highlightbackground='#2E4149',
                                       ).grid(row=13, column=1, sticky=W)

        Label(self,
              text="Iterations:",
              ).grid(row=13, column=1, padx=157, sticky=W)

        self.iterdrgn = IntVar()
        self.iterdrgn.set(5)
        self.iter_sp_drgn = Spinbox(self,
                                    from_=1,
                                    to=10,
                                    width=3,
                                    textvariable=self.iterdrgn
                                    ).grid(row=13, column=1, padx=230, sticky=W)

        # create a the animate hilbert button
        self.hilbert_btn = Button(self,
                                  text="Hilbert Curve",
                                  command=self.anim_hilbert,
                                  highlightbackground='#3E4149',
                                  ).grid(row=14, column=0, sticky=W, padx=20, pady=5)

        # process animated hilbert color
        self.color_hilbert_btn = Button(self,
                                        text="Select Color",
                                        command=self.colorize,
                                        highlightbackground='#2E4149',
                                        ).grid(row=14, column=1, sticky=W)

        Label(self,
              text="Iterations:",
              ).grid(row=14, column=1, padx=157, sticky=W)

        self.iterhlb = IntVar()
        self.iterhlb.set(5)
        self.iter_sp_hlb = Spinbox(self,
                                   from_=1,
                                   to=6,
                                   width=3,
                                   textvariable=self.iterhlb
                                   ).grid(row=14, column=1, padx=230, sticky=W)

        # create a the animate slideshow button
        self.slideshow_btn = Button(self,
                                    text="Fractal Slide Show",
                                    command=tikolu,
                                    highlightbackground='#3E4149',
                                    ).grid(row=15, column=0, sticky=W, padx=20, pady=5)

        Label(self,
              text="Height:"
              ).grid(row=15, column=1, sticky=W)
        self.height_ent = Entry(self, width=10)
        self.height_ent.grid(row=15, column=1, padx=55, sticky=W)
        Label(self,
              text="Width:"
              ).grid(row=15, column=1, padx=157, sticky=W)
        self.width_ent = Entry(self, width=10)
        self.width_ent.grid(row=15, column=1, padx=210, sticky=W)

        Label(self,
              text="Frequency:"
              ).grid(row=16, column=1, sticky=W)

        self.iterfrq = IntVar()
        self.iterfrq.set(5)
        self.iter_sp_frq = Spinbox(self,
                                   from_=1,
                                   to=20,
                                   width=3,
                                   textvariable=self.iterfrq
                                   ).grid(row=16, column=1, padx=75, sticky=W)

        Label(self,
              text="seconds"
              ).grid(row=16, column=1, padx=100, sticky=W)

        # create a filler
        Label(self,
              text=" "
              ).grid(row=17, column=0, sticky=W)

        self.errFont = font.Font(weight="bold")
        self.errFont = font.Font(size=20)
        self.err2show = StringVar()
        Label(self,
              textvariable=self.err2show,
              foreground="red",
              font=self.errFont,
              wraplength=200
              ).grid(row=19, column=0, sticky=NSEW, pady=4)

    # end def create_widgets(self):

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

    def three_colors(self):
        '''process color selections'''
        self.lblFont = font.Font(weight="bold")
        self.lblFont = font.Font(size=16)

        self.colorFrame = Toplevel(self)
        self.colorFrame.wm_title("Colorize Settings")

        Label(self.colorFrame,
              text="Select three colors using the RGB sliders and press Generate.",
              wraplength=200,
              font=self.lblFont
              ).grid(row=0, column=0, sticky=W, columnspan=3, padx=10, pady=10)

        Label(self.colorFrame,
              text="Color #1",
              wraplength=200,
              font=self.lblFont
              ).grid(row=1, column=0, sticky=W, columnspan=3, padx=10, pady=10)

        self.red_value1 = DoubleVar()
        Scale(self.colorFrame,
              variable=self.red_value1,
              from_=0, to=255,
              resolution=1,
              label="Red",
              orient=HORIZONTAL
              ).grid(row=2, column=0, sticky=NSEW, padx=10, pady=10)
        self.red_value1.set(0)

        self.green_value1 = DoubleVar()
        Scale(self.colorFrame,
              variable=self.green_value1,
              from_=0, to=255,
              resolution=1,
              label="Green",
              orient=HORIZONTAL
              ).grid(row=3, column=0, sticky=NSEW, padx=10, pady=10)
        self.green_value1.set(0)

        self.blue_value1 = DoubleVar()
        Scale(self.colorFrame,
              variable=self.blue_value1,
              from_=0, to=255,
              resolution=1,
              label="Blue",
              orient=HORIZONTAL
              ).grid(row=4, column=0, sticky=NSEW, padx=10, pady=10)
        self.blue_value1.set(0)

        Label(self.colorFrame,
              text="Color #2",
              wraplength=200,
              font=self.lblFont
              ).grid(row=1, column=1, sticky=W, columnspan=3, padx=10, pady=10)

        self.red_value2 = DoubleVar()
        Scale(self.colorFrame,
              variable=self.red_value2,
              from_=0, to=255,
              resolution=1,
              label="Red",
              orient=HORIZONTAL
              ).grid(row=2, column=1, sticky=NSEW, padx=10, pady=10)
        self.red_value2.set(0)

        self.green_value2 = DoubleVar()
        Scale(self.colorFrame,
              variable=self.green_value2,
              from_=0, to=255,
              resolution=1,
              label="Green",
              orient=HORIZONTAL
              ).grid(row=3, column=1, sticky=NSEW, padx=10, pady=10)
        self.green_value2.set(0)

        self.blue_value2 = DoubleVar()
        Scale(self.colorFrame,
              variable=self.blue_value2,
              from_=0, to=255,
              resolution=1,
              label="Blue",
              orient=HORIZONTAL
              ).grid(row=4, column=1, sticky=NSEW, padx=10, pady=10)
        self.blue_value2.set(0)

        Label(self.colorFrame,
              text="Color #3",
              wraplength=200,
              font=self.lblFont
              ).grid(row=1, column=2, sticky=W, columnspan=3, padx=10, pady=10)

        self.red_value3 = DoubleVar()
        Scale(self.colorFrame,
              variable=self.red_value3,
              from_=0, to=255,
              resolution=1,
              label="Red",
              orient=HORIZONTAL
              ).grid(row=2, column=2, sticky=NSEW, padx=10, pady=10)
        self.red_value3.set(0)

        self.green_value3 = DoubleVar()
        Scale(self.colorFrame,
              variable=self.green_value3,
              from_=0, to=255,
              resolution=1,
              label="Green",
              orient=HORIZONTAL
              ).grid(row=3, column=2, sticky=NSEW, padx=10, pady=10)
        self.green_value3.set(0)

        self.blue_value3 = DoubleVar()
        Scale(self.colorFrame,
              variable=self.blue_value3,
              from_=0, to=255,
              resolution=1,
              label="Blue",
              orient=HORIZONTAL
              ).grid(row=4, column=2, sticky=NSEW, padx=10, pady=10)
        self.blue_value3.set(0)

        # create a the generate button
        self.gen_colorize_btn = Button(self.colorFrame,
                                       text="Generate",
                                       command=self.processThreeColors,
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

    # end def three_colors(self):

    def processThreeColors(self):
        """ Gets three color values """
        # get color #1
        red1 = (int(self.red_value1.get()))
        green1 = (int(self.green_value1.get()))
        blue1 = (int(self.blue_value1.get()))

        # convert RGB color to hexadecimal value
        self.color1_to_change = '#{:02x}{:02x}{:02x}'.format(red1, green1, blue1)

        # get color #2
        red2 = (int(self.red_value2.get()))
        green2 = (int(self.green_value2.get()))
        blue2 = (int(self.blue_value2.get()))

        # convert RGB color to hexadecimal value
        self.color2_to_change = '#{:02x}{:02x}{:02x}'.format(red2, green2, blue2)

        # get color #3
        red3 = (int(self.red_value3.get()))
        green3 = (int(self.green_value3.get()))
        blue3 = (int(self.blue_value3.get()))

        # convert RGB color to hexadecimal value
        self.color3_to_change = '#{:02x}{:02x}{:02x}'.format(red3, green3, blue3)

        self.colorFrame.destroy()

    # end def processThreeColors(self):

    def colorize(self):
        '''process color selections'''
        self.lblFont = font.Font(weight="bold")
        self.lblFont = font.Font(size=16)

        self.colorFrame = Toplevel(self)
        self.colorFrame.wm_title("Colorize Settings")

        Label(self.colorFrame,
              text="Select a color using the RGB sliders and press Generate.",
              wraplength=200,
              font=self.lblFont
              ).grid(row=0, column=0, sticky=W, padx=10, pady=10)

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

        self.errFont = font.Font(weight="bold")
        self.errFont = font.Font(size=20)
        self.cerr2show = StringVar()
        Label(self.colorFrame,
              textvariable=self.cerr2show,
              foreground="red",
              font=self.errFont,
              wraplength=200
              ).grid(row=6, column=0, sticky=NSEW, pady=4)

    # end def colorize(self):

    def processColorize(self):
        """ Adds a user selected color to the image """
        # get select color
        red = (int(self.red_value.get()))
        green = (int(self.green_value.get()))
        blue = (int(self.blue_value.get()))

        # convert RGB color to hexadecimal value
        self.color_to_change = '#{:02x}{:02x}{:02x}'.format(red, green, blue)

        self.colorFrame.destroy()

    # end def processColorize(self):

    def anim_slideshow(self):
        # taken from: https://github.com/Tikolu/fractal.py

        update_iddletasks()

        print("Fractal Screensaver. Click to Exit.")
        width = int(input("Width: "))
        height = int(input("Height: "))
        updatemode = int(input("Update Frequency: "))

        d = fractal.display(width, height, True)

        while True:
            iterations = randrange(5, 25)
            power = randrange(-5, 5)

            r = randrange(1, 8)
            g = randrange(1, 8)
            b = randrange(1, 8)
            hue = r, g, b

            darkmode = randrange(0, 2)

            fractal.generate(d, iterations, power, hue, darkmode, updatemode)

    def anim_hilbert(self):
        # Global parameters

        width = 450

        title = "Hilbert-Curve-II"
        axiom = "X"
        rules = {"X": "XFYFX+F+YFXFY-F-XFYFX", "Y": "YFXFY-F-XFYFX+F+YFXFY"}
        iterations = 4  # TOP: 6
        angle = 90
        y_offset = -190
        angle_offset = 0

        if self.color_to_change == None:
            self.color_to_change = 'maroon'

        hilbert_curve(iterations, axiom, rules, angle, aspect_ratio=1, width=width,
                      offset_angle=angle_offset, y_offset=y_offset, color=self.color_to_change)
        # end def anim_hilbert(self):

    def anim_dragon(self):
        # Global parameters

        width = 450

        title = "TerDragon-Curve"
        axiom = "F"
        rules = {"F": "F-F+F"}
        iterations = 7  # TOP: 10
        angle = 120
        # c = 'purple'

        offset_angle = 90 - 30 * iterations
        correction_angle = 180 - 30 * iterations

        if self.color_to_change == None:
            self.color_to_change = 'magenta'

        animate_dragon(iterations, axiom, rules, angle, correction_angle=correction_angle,
                       offset_angle=offset_angle, width=width, height=width, color=self.color_to_change)

    def anim_sierpinski(self):
        # Global parameters

        width = 450

        title = "Siepinski-Sieve"
        axiom = "FXF--FF--FF"
        rules = {"F": "FF", "X": "--FXF++FXF++FXF--"}
        iterations = self.itersier.get()  # TOP: 8
        angle = 60

        if self.color_to_change == None:
            self.color_to_change = 'navy'

        animate_sierpinski(iterations, axiom, rules, angle, aspect_ratio=1, width=width, color=self.color_to_change)

    # end anim_sierpinski(self):

    def carpet(self):
        a = np.array([0, 0])
        b = np.array([3, 0])
        c = np.array([3, 3])
        d = np.array([0, 3])

        # set the iterations
        iterations = self.itercarp.get()

        # set the colors
        if self.color1_to_change is None:
            c1 = 'maroon'
        else:
            c1 = self.color1_to_change

        if self.color2_to_change is None:
            c2 = (random.random(), random.random(), random.random())
        else:
            c2 = self.color2_to_change

        if self.color3_to_change is None:
            c3 = (random.random(), random.random(), random.random())
        else:
            c3 = self.color3_to_change

        plt.figure(figsize=(20, 20))

        plt.fill([a[0], b[0], c[0], d[0]], [a[1], b[1], c[1], d[1]], color=c1, alpha=0.8)
        # plt.hold(True)

        carpet(a, b, c, d, iterations, c2, c3)

        plt.title("Randomly Colored Sierpinski Carpet (iterations = " + str(iterations) + ")")
        plt.axis('equal')
        plt.axis('off')
        plt.show()
        self.clearScreen()

    # end def carpet(self):

    def tricircle(self):

        triangle = [(0, 0), (1, 0), (0.5, np.sqrt(3) / 2.)]  # [(-2,-2),(0,2),(2,0)]

        # triangle = [(0,0), (1,0), (0,1)]

        radius_limit = 0.005
        fig = plt.figure(figsize=(18, 18))
        ax = fig.add_subplot(1, 1, 1)
        ax.set_xlim((0, 1))  # ((-3,3))
        ax.set_ylim((0, 1))  # ((-3,3))

        draw_triangle_fractal(ax, triangle, radius_limit)

        plt.title(
            "Randomly Colored Sierpinski Triangle With Embedded Circles")
        plt.axis('off')
        plt.show()
        self.clearScreen()

    # end def tricircle(self):

    def symcoloredsierpinski(self):
        a = np.array([0, 0])
        b = np.array([1, 0])
        c = np.array([0.5, np.sqrt(3) / 2.])

        k = 5

        plt.figure(figsize=(15, 15))

        iterations = self.itersym.get()

        Sierpinski(a, b, c, k, iterations)

        plt.title(
            "Asymmetrical (cut at 1/5) Randomly Colored Sierpinski Triangle (iterations = " + str(iterations) + ")")
        plt.axis('equal')
        plt.axis('off')
        plt.show()
        self.clearScreen()

    # end def symcoloredsierpinski(self):

    def rectSierpinski(self):
        h = np.sqrt(3)

        a1 = np.array([0, 0])
        b1 = np.array([3, 0])
        c1 = np.array([1.5, h])
        a1u = np.array([0, 2 * h])
        b1u = np.array([3, 2 * h])
        c1u = np.array([1.5, h])

        a2 = np.array([0, 0])
        b2 = np.array([0, 2 * h])
        c2 = np.array([1.5, h])
        a2r = np.array([3, 0])
        b2r = np.array([3, 2 * h])
        c2r = np.array([1.5, h])

        k1 = 3
        k1u = 5
        k2 = 4
        k2r = 6

        fig, ax = plt.subplots(1, figsize=(15, 15))

        iter = self.itercube.get()
        Sierpinski(a1, b1, c1, k1, iteration=iter)
        # plt.hold(True)
        Sierpinski(a1u, b1u, c1u, k1u, iteration=iter)
        # plt.hold(True)
        Sierpinski(a2, b2, c2, k2, iteration=iter)
        # plt.hold(True)
        Sierpinski(a2r, b2r, c2r, k2r, iteration=iter)
        # plt.hold(True)

        plt.title("Randomly Colored Cubistic Sierpinski Synthesis (iterations = " + str(iter) + ")")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        plt.axis('equal')
        plt.axis('off')
        plt.show()
        self.clearScreen()

    # end def rectSierpinski(self):

    def manderbrot(self):
        n = 1000
        img = plotter(n, thresh=4, max_steps=50)
        # plt.imshow(img, cmap="inferno")
        plt.imshow(img, cmap=self.theme.get())
        plt.axis("off")
        plt.show()
        self.clearScreen()

    # end def manderbrot(self):

    # process user selections
    def processSelections(self):
        """Processes user screen selections"""
        # Mandelbrot Set
        if self.is_mandlebrot.get() == True:
            self.manderbrot()
        elif self.is_julia.get() == True:
            julia()
            self.clearScreen()
        elif self.is_cubistic.get() == True:
            self.rectSierpinski()
        elif self.is_symcolored.get() == True:
            self.symcoloredsierpinski()
        elif self.is_tricircle.get() == True:
            self.tricircle()
        elif self.is_carpet.get() == True:
            self.carpet()
    # end def processSelections(self):


# main
"""Application Entry Point - the main
driver code for the BSSD5410 Midterm Project"""
root = Tk()
root.resizable(height=None, width=None)
root.title("BSSD 5410 Midterm Scott Bing")
app = Application(root)
root.mainloop()
