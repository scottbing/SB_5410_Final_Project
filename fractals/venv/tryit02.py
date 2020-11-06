#! /usr/bin/env python
#
# Copyright (c) 2013, Luke Southam <luke@devthe.com>
# All rights reserved.
# http://opensource.org/licenses/BSD-3-Clause

import os
import sys
from subprocess import call
import errno
import shutil
import glob
import tempfile

IS_PYPY = '__pypy__' in sys.builtin_module_names

# import numpy
_numpy_name = 'num' + ('pypy' if IS_PYPY else 'py')
numpy = __import__(_numpy_name)

WIDTH, HEIGHT = 1920, 1080  # 1080p
REAL_MIN, REAL_MAX = -2.0, 2.0
IMAGINE_MIN, IMAGINE_MAX = -2.0, 2.0
FRAMESTEP = 0.01


class JuliaSet(object):
    """
    Creates Julia Sets based off the function suplied at JuliaSet.z
    """

    def __init__(self, width, height, rmin, rmax, imin, imax):
        print("Starting up ...")


        self.real_range = numpy.arange(rmin, rmax,
                                       (rmax - rmin) / width)
        self.imagine_range = numpy.arange(imax, imin,
                                          (imin - imax) / HEIGHT)

        self.height = height
        self.width = width
        self.rmin = rmin
        self.rmax = rmax
        self.imin = imin
        self.imax = imax

    def compute(self, real, imagine, c_imagine):
        """
        This is where the magic happends ;)
        """
        z = complex(real, imagine)
        c = complex(0.0, c_imagine)
        n = 255
        while abs(z) < 10 and n >= 5:
            z = self.z(z, c, n)  # z**2 + c
            n = n - 5
        return str(n)

    def generate_anim(self, framestep):
        """
        Creates Julia Set animation of self.z
        """

        print(
            "Generating animation %ix%i with %i frames:" % (self.width,
                                                            self.height,
                                                            1.0 / framestep))

        self.comp = lambda imagine, c_imagine: (lambda re:
                                                self.compute(re, imagine, c_imagine))

        frameslen = len(str(1. / framestep))

        frame = 0
        sys.stdout.write(' Proccessing frames: 0%')
        for c_imagine in numpy.arange(0.0, 1.0, framestep):
            frame += 1
            filename = ("{0:0%id}.pgm" % frameslen).format(frame)

            self.generate_pic(c_imagine, filename)
            sys.stdout.write('\r')
            sys.stdout.flush()
            sys.stdout.write(' Proccessing frames: %f%%' %
                             (frame * framestep * 100))
        print()

        print(
        " Creating gif ...")
        #call("convert -delay 10 *.pgm julia.gif".split())

    def generate_pic(self, c_imagine, filename):
        """
        Creates Julia Set image of self.z
        """
        with open(filename, 'w') as f:
            f.write('P2\n# Julia Set image\n'
                    + str(self.width)
                    + ' '
                    + str(self.height)
                    + '\n255\n')

            # Generate pixel values
            for imagine in self.imagine_range:
                data = map(self.comp(imagine, c_imagine), self.real_range)
                f.write(' '.join(data) + '\n')


def get_temp():
    TEMPDIR = os.path.join(TEMP, 'julia')
    try:
        os.makedirs(TEMPDIR)
    except OSError as exc:
        pass
    return TEMPDIR


if __name__ == '__main__':
    CWD = os.getcwd()
    TEMP = tempfile.gettempdir()
    TEMPDIR = get_temp()
    os.chdir(TEMPDIR)

    js = JuliaSet(WIDTH, HEIGHT,
                  REAL_MIN, REAL_MAX,
                  IMAGINE_MIN, IMAGINE_MAX)
    js.z = lambda z, c, n: z ** 2 + c
    js.generate_anim(FRAMESTEP)

    print(
    " Storing gif ..."
    shutil.copy("julia.gif", "%s/julia.gif" % CWD))

    print(
    " Cleaning up ..."
    os.chdir(CWD)
    if os.path.exists(TEMPDIR):
        shutil.rmtree(TEMPDIR))

    print("DONE!")
