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
        self.filled = True
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
        self.render()

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
        #print(transform)

    def zoom(self, close):
        if close:
            self.distance = self.distance + 50
            #print(scene.distance)
        else:
            self.distance = self.distance - 50
        #print(scene.distance)

    def turn(self, axis, direction):
        angle = direction * 10 * np.pi / 180.

        transform = np.array(
            [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
            dtype=float)

        if axis == 'x':
            transform[1:3, 1:3] = np.array([[np.cos(angle), -np.sin(angle)],
                                            [np.sin(angle),
                                             np.cos(angle)]])
        elif axis == 'y':
            transform[0:3, 0:3] = np.array([[np.cos(angle), 0,
                                             np.sin(angle)], [0, 1, 0],
                                            [-np.sin(angle), 0,
                                             np.cos(angle)]])
        else:
            transform[0:2, 0:2] = np.array([[np.cos(angle), -np.sin(angle)],
                                            [np.sin(angle),
                                             np.cos(angle)]])

        for poly in self.scene_data:
            for point in poly.points:
                point.transform(transform)
        #print(transform)

    def distance_from_camera(self, edge):
        edge_middle = Point.middle((edge.point1, edge.point2))
        #print(edge_middle)
        return Point.distance(edge_middle, self.start_point)

    def distance_from_camera_cover(self, cover):
        middle = Point.middle(cover.points)
        #print(middle)
        return Point.distance(middle, self.start_point)

    def render(self):
        cw = canvas.winfo_width()
        ch = canvas.winfo_height()
        if cw == 1:
            cw = 1284
            ch = 724
        canvas.delete(ALL)

        if self.filled:
            polygons = []
            Polygon = namedtuple('Polygon', ['points', 'color'])

            for cube in self.scene_data:
                for cover in cube.covers:
                    visible = True
                    for point in cover:
                        visible = visible and point[2] > self.start_point[2]
                    if visible:
                        polygons.append(Polygon(cover, cube.color))
            polygons.sort(key=self.distance_from_camera_cover, reverse=True)
            #print(polygons)
            for polygon in polygons:
                points = [
                    point.project(self.distance, (cw, ch))
                    for point in polygon.points
                ]
                #print(points)
                canvas.create_polygon(
                    points, fill=polygon.color, outline='black')
            print(points)
        else:
            edges = []
            Edge = namedtuple('Edge', ['point1', 'point2', 'color'])
            for cube in self.scene_data:
                for edge in cube:
                    if edge[0][2] > self.start_point[2] and edge[1][
                            2] > self.start_point[2]:
                        edges.append(Edge(edge[0], edge[1], cube.color))
                    else:
                        break
            edges.sort(key=self.distance_from_camera, reverse=True)

            for edge in edges:
                p0 = edge.point1.project(self.distance, (cw, ch))
                p1 = edge.point2.project(self.distance, (cw, ch))
                canvas.create_line(p0, p1, fill=edge.color, smooth=True)


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
    elif event.keycode == 32:
        scene.filled = not scene.filled
        scene.render()
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