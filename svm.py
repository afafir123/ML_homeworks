import random

import numpy as np
import pygame
from sklearn.svm import SVC
width, height = 600, 400

def generateData(numberOfClassEl, numberOfClasses):
    radius = 50
    data = []
    for classNum in range(numberOfClasses):
        centerX, centerY = random.randint(radius, 600 - radius), random.randint(radius, 400 - radius)
        for rowNum in range(numberOfClassEl):
            data.append([[random.gauss(centerX, radius / 2), random.gauss(centerY, radius / 2)], classNum])
    return data

def get_line_points(svc):
    w = svc.coef_[0]
    a = -w[0] / w[1]
    xx = np.array([0, width])
    yy = a * xx - (svc.intercept_[0]) / w[1]

    return [xx[0], yy[0]], [xx[-1], yy[-1]]


def draw_pygame():
    screen = pygame.display.set_mode((width, height))
    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = list(event.pos)
                cls = svc.predict([pos])[0]
                points.append([pos, cls])

        for point in points:
            pygame.draw.circle(screen, colors[point[1]], point[0], 3)

        pygame.draw.line(screen, 'white', p1, p2, 2)

        pygame.display.update()


if __name__ == '__main__':
    points = generateData(10, 2)
    colors = {0: 'red', 1: 'blue'}
    x_coords = np.array(list(map(lambda p: p[0], points)))
    y_coords = np.array(list(map(lambda p: p[1], points)))
    svc = SVC(kernel='linear')
    svc.fit(x_coords, y_coords)
    p1, p2 = get_line_points(svc)
    draw_pygame()
