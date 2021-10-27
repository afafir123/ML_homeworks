import sys
import numpy as np
import math
import pygame
from random import randint

UNCLASSIFIED = False
NOISE = None
points = np.matrix('0; 0')
colors = []


def dist(p, q):
    return math.sqrt(np.power(p - q, 2).sum())


def neighborhood(p, q, eps):
    return dist(p, q) < eps


def get_seeds(m, point_id, eps):
    n_points = m.shape[1]
    seeds = []
    for i in range(0, n_points):
        if neighborhood(m[:, point_id], m[:, i], eps):
            seeds.append(i)
    return seeds


def expand_cluster(m, classifications, point_id, cluster_id, eps, min_points):
    seeds = get_seeds(m, point_id, eps)
    if len(seeds) < min_points:
        classifications[point_id] = NOISE
        return False
    else:
        classifications[point_id] = cluster_id
        for seed_id in seeds:
            classifications[seed_id] = cluster_id

        while len(seeds) > 0:
            current_point = seeds[0]
            results = get_seeds(m, current_point, eps)
            if len(results) >= min_points:
                for i in range(0, len(results)):
                    result_point = results[i]
                    if classifications[result_point] == UNCLASSIFIED or \
                            classifications[result_point] == NOISE:
                        if classifications[result_point] == UNCLASSIFIED:
                            seeds.append(result_point)
                        classifications[result_point] = cluster_id
            seeds = seeds[1:]
        return True


def dbscan(m, eps, min_points):
    cluster_id = 1
    n_points = m.shape[1]
    classifications = [UNCLASSIFIED] * n_points
    for point_id in range(0, n_points):
        if classifications[point_id] == UNCLASSIFIED:
            if expand_cluster(m, classifications, point_id, cluster_id, eps, min_points):
                cluster_id = cluster_id + 1
    return classifications

def add_point(x, y, curr_points):
    return np.append(curr_points, np.matrix([[x], [y]]), axis=1)


pygame.init()
FramePerSec = pygame.time.Clock()
# разрешение окошка
HEIGHT = 1000
WIDTH = 1000
surface = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("DBSCAN")

for i in range(1000):
    colors.append('#%06X' % randint(0, 0xFFFFFF))
game_loop = True
classification = []
while game_loop:
    surface.fill((255, 255, 255))

    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        game_loop = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            points = add_point(*pygame.mouse.get_pos(), curr_points=points)
            classification = dbscan(points, 15, 5)
            print(classification)
    n = points.shape[1]
    for i in range(0, n):
        point = points[:, i]
        color = 'red' if (classification.__len__() <= i or classification[i] is None) else colors[classification[i]]
        pygame.draw.circle(surface, color, (point.item(0), point.item(1)), 3)

    pygame.display.update()

pygame.quit()
sys.exit()
