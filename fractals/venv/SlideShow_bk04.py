from random import randrange
import tkinter
import pygame
import cmath
import sys

def display(width=800, height=600, fullscreen=False, colour=(0, 0, 0)):
    size = width, height
    # if fullscreen:
    #     screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    # else:
    #     screen = pygame.display.set_mode(size)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Tikolu Fractal Display")
    screen.fill(colour)
    pygame.display.update()
    return (screen)


def generate(screen, iterations=15, power=2, hue=(2, 2, 2), darkmode=False, updatemode=1):
    width, height = screen.get_size()
    w2 = width / 2
    h2 = height / 2
    w4 = width / 4
    h4 = height / 4
    y = 0
    while y < height:
        x = -1
        while x < width:
            x += 1
            offset = complex((x - w2) / w4, (y - h2) / h4)
            cpoint = complex(0, 0) + offset
            i = 0
            while i < iterations:
                try:
                    cpoint = (cpoint ** power) + offset
                except ZeroDivisionError:
                    cpoint = ((cpoint + 1) ** power) + offset
                if abs(cpoint.real) > 2 or abs(cpoint.imag) > 2:
                    break
                i += 1
            i = 255 * (i / iterations)
            if darkmode == False:
                i = abs(i - 255)
            colour = i / hue[0], i / hue[1], i / hue[2]
            point = round((offset.real * w4) + w2), round((offset.imag * h4) + h2)
            screen.set_at(point, colour)
        if updatemode != 0:
            if y % updatemode == 0:
                pygame.display.update()
        pygame.display.set_caption("Generating Fractal... " + str(round((y / height) * 100)) + "%")
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                sys.exit()
        y += 1
    pygame.display.update()

def tikolu(h, w, um):
    #taken from: https://github.com/Tikolu/fractal.py
    #def main():

    pygame.init()

    print("Fractal Screensaver. Click to Exit.")
    #width = int(input("Width: "))
    width = w
    #height = int(input("Height: "))
    height = h
    #updatemode = int(input("Update Frequency: "))
    updatemode = um

    d = display(width, height, True)

    while True:
        iterations = randrange(5, 25)
        power = randrange(-5, 5)

        r = randrange(1, 8)
        g = randrange(1, 8)
        b = randrange(1, 8)
        hue = r, g, b

        darkmode = randrange(0, 2)

        generate(d, iterations, power, hue, darkmode, updatemode)

