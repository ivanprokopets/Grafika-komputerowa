import json
import numpy as np
import tkinter
from tkinter import *
from collections import namedtuple

from geometry import Cube, Point


class Scene(object):
    def __init__(self):
        self.distance = 1000
        self.start_point = Point((0, 0, 0))
        self.filled = False
        self.load_scene()

    def load_scene(self):
        scene = []
        scene.append(Cube((-10, -10, 40), 10, 'red'))
        scene.append(Cube((10, -10, 40), 10, 'green'))
        scene.append(Cube((10, -10, 60), 10, 'orange'))
        scene.append(Cube((-10, -10, 60), 10, 'Turquoise'))

        scene.append(Cube((-10, 10, 40), 10, 'Magenta'))
        scene.append(Cube((10, 10, 40), 10, 'Lime'))
        scene.append(Cube((10, 10, 60), 10, 'white'))
        scene.append(Cube((-10, 10, 60), 10, 'yellow'))

        self.scene_data = scene

    def move(self, axis, direction):
        transform = np.array(
            [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
            dtype=float)

        if axis == "x":
            transform[0, 3] = direction
        elif axis == "y":
            transform[1, 3] = direction
        else:
            transform[2, 3] = direction

        for poly in self.scene_data:
            for point in poly.points:
                point.transform(transform)
        print(transform)

    


window = Tk()
window.title("Projekt Grafika Komputerowa - Prakapets Ivan")
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

canvas = Canvas(window, width=1920, height=1080)

canvas.configure(background='black')
canvas.grid(column=0, row=0, sticky=(N, W, E, S))

scene = Scene()

print("Pierwotna wartos:",scene.distance)
# keysbinding
def key(event):
    if event.keycode == 13:
        scene.distance = 1000
        scene.load_scene()
    else:
        pressed_key = {
            'w': lambda: scene.move('y', 1),
            's': lambda: scene.move('y', -1),
            'a': lambda: scene.move('x', 1),
            'd': lambda: scene.move('x', -1),
            'q': lambda: scene.move('z', 1),
            'e': lambda: scene.move('z', -1),
            '8': lambda: scene.turn('x', -1),
            '2': lambda: scene.turn('x', 1),
            '4': lambda: scene.turn('y', 1),
            '6': lambda: scene.turn('y', -1),
            '7': lambda: scene.turn('z', -1),
            '9': lambda: scene.turn('z', 1),
            '+': lambda: scene.zoom(True),
            '-': lambda: scene.zoom(False),
        }.get(event.char)
        if pressed_key:
            pressed_key()
            scene.render()

window.bind('<Key>', key)
window.mainloop()
print(scene.distance)
