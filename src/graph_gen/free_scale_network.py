from itertools import product
import numpy as np


def generate_free_scale_graph(n, k, labels, reverse_edges=False):
    g = {i: [(j, np.random.choice(labels)) for j in range(k)] for i in range(k)}
    degree = np.array([3] * k)

    for i in range(k, n):
        p = degree / np.sum(degree)
        to_vertices = np.random.choice(range(i), k,  p=p)

        g[i] = []
        degree = np.append(degree, 0)
        for to in to_vertices:
            label = np.random.choice(labels)
            g[i].append((to, label))
            degree[to] += 1
            degree[i] += 1

            if reverse_edges:
                g[to].append((i, label))
    return g
