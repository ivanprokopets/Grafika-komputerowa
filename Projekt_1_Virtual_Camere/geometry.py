import numpy as np


class Point:
    def __init__(self, values):
        self.point = np.array(values, np.float)

    def __repr__(self):
        return 'Point({0}, {1}, {2})'.format(*self.point)

    def __getitem__(self, index):
        return self.point[index]

    def __add__(self, y):
        if len(y) == 3:
            self.point = self.point + y
            return Point(self.point)
        else:
            raise NotImplementedError

    def transform(self, matrix):
        result = np.matmul(matrix, np.insert(self.point, 3, 1))
        self.point = result[:3]

    def project(self, distance, window_size):
        x = window_size[0] / 2 + distance * self.point[0] / self.point[2]
        y = window_size[1] / 2 + distance * self.point[1] / self.point[2]
        return (x, y)





class Cube:
    def __init__(self, pos, size=1, color="white"):
        self.color = color

        points = []
        points.append(Point(pos))
        points.append(Point(pos) + (size, 0, 0))
        points.append(Point(pos) + (size, 0, size))
        points.append(Point(pos) + (0, 0, size))

        points.append(Point(pos) + (0, size, 0))
        points.append(Point(pos) + (size, size, 0))
        points.append(Point(pos) + (size, size, size))
        points.append(Point(pos) + (0, size, size))

        self.points = points

        edges = []
        edges.append((points[0], points[1]))
        edges.append((points[0], points[3]))
        edges.append((points[0], points[4]))

        edges.append((points[2], points[1]))
        edges.append((points[2], points[3]))
        edges.append((points[2], points[6]))

        edges.append((points[5], points[1]))
        edges.append((points[5], points[4]))
        edges.append((points[5], points[6]))

        edges.append((points[7], points[3]))
        edges.append((points[7], points[4]))
        edges.append((points[7], points[6]))

        self.edges = edges


    def __iter__(self):
        return iter(self.edges)

