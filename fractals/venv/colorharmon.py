#!/usr/bin/python
'''    Spectral Harmonographs   Copyright 2014 Alan Richmond (Tuxar.uk)

    Trace of 4 decaying sine waves, 2 per axis (x & y)(i.e. 2-pendula), with rainbow colour.
    I did this in Java some decades ago (Encyclogram; I no longer have the source), this
    version is in Python, with PyGame.
    It randomly generates a sequence of harmonographs. It's fast, and can be set to go
    much faster (or slower) if you want.
    Tip: set the display window to fullscreen. On KDE Ubuntu right-click on the title bar,
    select More Actions -> Fullscreen
'''
print(
    "Quit: q key, Screenshot: spacebar")

'''The MIT License (MIT)

Copyright (c) 2014 Alan Richmond (Tuxar.uk)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''

import pygame, sys, random as r
from pygame.locals import *
from math import pi, sin, cos, exp


def check_event():
    global save
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_q:
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_SPACE:
            save = True
            print
            "Saving when finished..."


def color_harmon():
    #                        EDIT THESE:
    width, height = 1280, 720  # YouTube HD
    width, height = 1920, 1080  # my left monitor
    width, height = 1280, 1024  # my right monitor
    # width,height=2560,1440      # YT channel art
    dd = 0.99995  # decay factor
    dt = 0.02  # time increment
    speed = 500  # yes, speed
    hui = 57 * 2  # Hue increment
    hue, sat, val, aaa = 0, 100, 100, 0
    sd = 0.005  # frequency spread (from integer)
    mx = 4  # max range for amplitudes & frequencies

    steps = 0
    pygame.init()
    pygame.event.set_allowed([QUIT, KEYDOWN])
    screen = pygame.display.set_mode((width, height), DOUBLEBUF)
    screen.set_alpha(None)
    fg = pygame.Color(0, 0, 0, 0)
    save = False
    while True:
        while True:
            ax1, ax2 = r.randint(-mx, mx), r.randint(-mx, mx)
            maxx = abs(ax1) + abs(ax2)
            if maxx > 0: break
        xscale = width / (2 * maxx)
        while True:
            ay1, ay2 = r.randint(0, mx), r.randint(0, mx)
            maxy = abs(ay1) + abs(ay2)
            if maxy > 0: break
        yscale = height / (2 * maxy)
        fx1, fx2 = r.randint(1, mx) + r.gauss(0, sd), r.randint(1, mx) + r.gauss(0, sd)
        fy1, fy2 = r.randint(1, mx) + r.gauss(0, sd), r.randint(1, mx) + r.gauss(0, sd)
        px1, px2 = r.uniform(0, 2 * pi), r.uniform(0, 2 * pi)
        py1, py2 = r.uniform(0, 2 * pi), r.uniform(0, 2 * pi)
        print(
            ax1, ax2, ay1, ay2)
        print(
            fx1, fx2, fy1, fy2)
        print(
            px1, px2, py1, py2)

        dec = 1.0
        t = 0.0  # angle for sin
        first = True
        while dec > 0.015:
            # calculate next x,y point along line
            x = xscale * dec * (ax1 * sin(t * fx1 + px1) + ax2 * sin(t * fx2 + px2)) + width / 2
            y = yscale * dec * (ay1 * cos(t * fy1 + py1) + ay2 * cos(t * fy2 + py2)) + height / 2
            dec *= dd  # decay
            if not first:  # ignore any complaint about prev_x,y being undefined
                fg.hsva = (hue, sat, val, aaa)
                hue = (hue + dt * hui) % 360  # cycle hue
                pygame.draw.aaline(screen, fg, (x, y), (prev_x, prev_y), 1)
            else:
                first = False

            prev_x = x  # save x,y for next line segment start
            prev_y = y
            if steps % speed == 0: pygame.display.update()
            steps += 1
            t += dt  # increment angle for sin
            check_event()

        if save:
            pars = 'shg-{0}_{1}-{2}_{3}-{4}_{5}'.format(ax1, ax2, fx1, fx2, px1, px2)
            pygame.image.save(screen, pars + '.jpg')
            print(
                "Saved as " + pars + '.jpg')
            save = False

        screen.fill((0, 0, 0))


if __name__ == "__main__":
    main()
