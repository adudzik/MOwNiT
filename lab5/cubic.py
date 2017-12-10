from itertools import zip_longest
import numpy as np


def cubic_interpolation(x_nodes, y_nodes, points_number, is_natural, fp1, fp2):
    n = len(x_nodes)

    fd, h = [], []
    for i in range(1, n):
        h.append(x_nodes[i] - x_nodes[i - 1])
        fd.append((y_nodes[i] - y_nodes[i - 1]) / h[i - 1])

    if is_natural:
        # natural condition
        ftt = [0]
        for i in range(1, n - 1):
            ftt.append(3 * (fd[i] - fd[i - 1]) / (h[i] + h[i - 1]))
        ftt += [0]
    else:
        # second derivatives are equal
        ftt = [fp1]
        for i in range(1, n - 1):
            ftt.append(3 * (fd[i] - fd[i - 1]) / (h[i] + h[i - 1]))
        ftt += [fp2]

    a, b, c, d = [], [], [], []
    for i in range(n - 1):
        a.append((ftt[i + 1] - ftt[i]) / (6 * h[i]))
        b.append(ftt[i] / 2)
        c.append(fd[i] - h[i] * (ftt[i + 1] + 2 * ftt[i]) / 6)
        d.append(y_nodes[i])

    result = list(zip_longest(a, b, c, d, x_nodes[:]))

    return get_values(result, points_number)


def get_values(coefficients, plot_points_num):
    n = len(coefficients)

    x_int, y_int = [], []
    for i in range(n - 1):
        a, b, c, d, x = coefficients[i]
        x1 = coefficients[i + 1][4]

        for point in np.linspace(x, x1, plot_points_num // n):
            x_int.append(point)
            y_int.append(a * (point - x) ** 3 + b * (point - x) ** 2 + c * (
                point - x) + d)

    return x_int, y_int
