import math
from Settings import config

class Tetromino:
    def __init__(self, type):
        self.type = type
        self.points = []
        c = 5  # c for center
        self.rotationState = 0

        if self.type == 1:#'I'
            self.points.append((0, c))
            self.points.append((0,c+1))
            self.points.append((0, c - 2))
            self.points.append((0, c - 1))
        elif self.type == 2:#'O'
            self.points.append((0,c))
            self.points.append((0,c+1))
            self.points.append((-1,c))
            self.points.append((-1,c+1))
        elif self.type == 3:#'S'
            self.points.append((0,c))
            self.points.append((0,c-1))
            self.points.append((-1,c))
            self.points.append((-1,c+1))
        elif self.type == 4:#'Z'
            self.points.append((0,c))
            self.points.append((0,c+1))
            self.points.append((-1,c))
            self.points.append((-1,c-1))
        elif self.type == 5:#'J'
            self.points.append((0,c))
            self.points.append((0,c+1))
            self.points.append((0,c-1))
            self.points.append((-1,c-1))
        elif self.type == 6:#'L'
            self.points.append((0,c))
            self.points.append((0,c-1))
            self.points.append((0,c+1))
            self.points.append((-1,c+1))
        elif self.type == 7:#'T'
            self.points.append((-1,c))
            self.points.append((-1,c-1))
            self.points.append((-1,c+1))
            self.points.append((0,c))


    def getPoints(self):
        return self.points

    # moves tetromino down by amt, with error checking
    def moveDown(self, amt):
        # if already at bottom, can't go further down
        for i in range(len(self.points)):
            if self.points[i][1]+amt > config['rows']:
                return

        for i in range(len(self.points)):
            self.points[i] = (self.points[i][0]+amt, self.points[i][1])

    # moves tetromino to the side by amt, with error checking
    def moveX(self, amt):
        for i in range(len(self.points)):
            self.points[i] = (self.points[i][0], self.points[i][1]+amt)

        # check bounds and reverse if overstepped
        for point in self.points:
            if point[1] < 0 or point[1] >= config['cols']:
                for i in range(len(self.points)):
                    self.points[i] = (self.points[i][0], self.points[i][1] - amt)
                return False

    def getState(self):
        return [self.points.copy(), self.rotationState, self.type]

    def setState(self, state):
        self.points = state[0]
        self.rotationState = state[1]
        self.type = state[2]

    # rotates tetronimo
    def rotate(self, times):
        # some shapes only get rotated in some ways
        if self.type == 2:
            return
        if self.type == 1 and self.rotationState > 0:
            c = self.points[0][1]
            h = self.points[0][0]
            self.points = []
            self.rotationState = 0
            self.points.append((h, c))
            self.points.append((h, c + 1))
            self.points.append((h, c - 2))
            self.points.append((h, c - 1))
            return

        # update rotation state
        self.rotationState += times
        if self.rotationState > 3 or self.rotationState < 0:
            self.rotationState = self.rotationState % 4

        # use first point as center point
        centerR = self.points[0][0]
        centerC = self.points[0][1]

        for i in range(len(self.points)):
            if i != 0:
                # get distance and angle from center
                distanceR = centerR - self.points[i][0]
                distanceC = centerC - self.points[i][1]
                radius = math.hypot(distanceC, distanceR)
                angle = math.atan2(distanceR, distanceC)
                # subtract 45 degrees (clockwise) to angle to calculate each points' new location
                angle -= math.pi/2 * times
                new_r = round(radius*math.sin(angle))
                new_c = round(radius*math.cos(angle))
                self.points[i] = (new_r+centerR, new_c+centerC)
