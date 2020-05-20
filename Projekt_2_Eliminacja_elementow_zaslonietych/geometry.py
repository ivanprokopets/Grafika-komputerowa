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

    @staticmethod
    def middle(points):
        middle_point = np.array([0, 0, 0], dtype=float)
        for point in points:
            middle_point = middle_point + point.point
        middle_point = middle_point / len(points)
        return Point(middle_point)

    @staticmethod
    def distance(point1, point2):
        distance = (point1[0] - point2[0])**2 + (point1[1] - point2[1])**2 + (
            point1[2] - point2[2])**2
        #print(distance**(1/2))
        return distance**(1 / 2)



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

        covers = []
        covers.append((points[0], points[1], points[2], points[3]))
        covers.append((points[4], points[5], points[6], points[7]))

        covers.append((points[0], points[1], points[5], points[4]))
        covers.append((points[2], points[3], points[7], points[6]))

        covers.append((points[1], points[5], points[6], points[2]))
        covers.append((points[0], points[3], points[7], points[4]))

        #divide covers to smaller parts
        divided_covers = []
        for cover in covers:
            center = Point.middle(cover)
            middle_points = [
                Point.middle((cover[0], cover[1])),
                Point.middle((cover[1], cover[2])),
                Point.middle((cover[2], cover[3])),
                Point.middle((cover[3], cover[0]))
            ]
            middle_points_reversed = [middle_points[-1]]
            middle_points_reversed.extend(middle_points[:-1])
            points.extend(middle_points)
            points.append(center)

            for cover_point, middle_normal, middle_moved in zip(
                    cover, middle_points, middle_points_reversed):
                divided_covers.append((cover_point, middle_normal, center,
                                       middle_moved))

        self.covers = divided_covers

    def __iter__(self):
        return iter(self.edges)


if __name__ == "__main__":
    #tests
    cube = Cube((0, 0, 0), 10)

    points = []
    points.append(Point((0, 0, 0)))
    points.append(Point((1, 2, 2)))
    print(Point.middle(points))