from itertools import zip_longest
import numpy as np


def quadratic_interpolation(x_nodes, y_nodes, points_num, start_cond):
    n = len(x_nodes)

    h = []
    for i in range(1, n, 1):
        h.append(x_nodes[i] - x_nodes[i - 1])

    b = []
    for i in range(1, n):
        b.append((y_nodes[i] - y_nodes[i - 1]) * 2 / h[i - 1])

    # boundary conditions
    if start_cond:
        # derivative of starting point = 0
        b = [0] + b
        for i in range(1, n):
            b[i] -= b[i - 1]
    else:
        # derivative of ending point = 0
        b += [0]
        for i in range(n - 1, 0, -1):
            b[i - 1] -= b[i]

    a = []
    for i in range(1, n):
        a.append((b[i] - b[i - 1]) / (2 * h[i - 1]))

    c = []
    for i in range(n - 1):
        c.append(y_nodes[i])

    b = b[:-1]

    result = list(zip_longest(a, b, c, x_nodes[:]))

    return get_values(result, points_num)


def get_values(coefficients, plot_points_num):
    n = len(coefficients)

    x_int, y_int = [], []
    for i in range(n - 1):
        a, b, c, x = coefficients[i]
        x1 = coefficients[i + 1][3]

        for point in np.linspace(x, x1, plot_points_num // n):
            x_int.append(point)
            y_int.append(a * (point - x) ** 2 + b * (point - x) + c)

    return x_int, y_int
