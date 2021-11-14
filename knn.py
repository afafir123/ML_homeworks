import operator
import random
import numpy as np
import pygame
import math


def dist(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def generateData(numberOfClassEl, numberOfClasses):
    radius = 50
    data = []
    for classNum in range(numberOfClasses):
        # Choose random center of 2-dimensional gaussian
        centerX, centerY = random.randint(radius, 600 - radius), random.randint(radius, 400 - radius)
        # Choose numberOfClassEl random nodes with RMS=0.5
        for rowNum in range(numberOfClassEl):
            data.append([[random.gauss(centerX, radius / 2), random.gauss(centerY, radius / 2)], classNum])
    return data


def KNN(point, k):
    sorted_points = sort_by_distance(point)
    k_neighbors = get_k_neighbors(sorted_points, k)
    color = get_most_frequent_color(k_neighbors)
    point[1] = color

def calculate_k_results(point):
    sorted_points = sort_by_distance(point)
    for k in range(1, len(k_res)):
        k_neighbors = get_k_neighbors(sorted_points, k)
        color_for_current_K = get_most_frequent_color(k_neighbors)
        if point[1] == color_for_current_K:
            k_res[k] += 1


def get_best_k():
    best_k = max(k_res)
    print("best k is ", k_res.index(best_k))
    return k_res.index(best_k)



def get_k_neighbors(sorted_points, k):
    return sorted_points[:k]


def sort_by_distance(point):
    distances = []
    for p in points:
        if p == point:
            continue
        distance = dist(p[0], point[0])
        distances.append((p, distance))
    distances.sort(key=operator.itemgetter(1))
    return [i[0] for i in distances]


def get_most_frequent_color(points):
    print(points)
    return max(set([i[1] for i in points]), key=colors.count)


def draw_pygame():
    screen = pygame.display.set_mode((600, 400))
    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    test_points.append([[event.pos[0], event.pos[1]], -1])

                if event.button == 3:
                    point = [[event.pos[0], event.pos[1]], -1]
                    KNN(point, get_best_k())
                    points.append(point)

            if event.type == pygame.KEYDOWN:
                if len(test_points) > 0:
                    if event.key == pygame.K_1:
                        test_points[-1][-1] = 0
                        points.append(test_points[-1])
                        calculate_k_results(test_points[-1])
                        del test_points[-1]

                    if event.key == pygame.K_2:
                        test_points[-1][-1] = 1
                        points.append(test_points[-1])
                        calculate_k_results(test_points[-1])
                        del test_points[-1]
                    if event.key == pygame.K_3:
                        test_points[-1][-1] = 2
                        points.append(test_points[-1])
                        calculate_k_results(test_points[-1])
                        del test_points[-1]
                    print(k_res)
        for point in points:
            pygame.draw.circle(screen, colors[point[1]], point[0], 3)
        for point in test_points:
            pygame.draw.circle(screen, colors[point[1]], point[0], 3)

        pygame.display.update()


if __name__ == '__main__':
    n, cl = 50, 3
    colors = ['red', 'green', 'blue', 'white']
    points = generateData(n, cl)
    test_points = []
    #suppose that k range from 1 to sqrt(n)
    max_k = math.floor(math.sqrt(n))
    k_res = [0 for i in range(max_k)]

    draw_pygame()
