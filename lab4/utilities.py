from math import cos, pi
from numpy import linspace, array


def get_chebyshev_zeros(k, start, end):
    result = []

    for j in range(1, k + 1, 1):
        result.append((start + end) / 2 + (end - start) / 2 *
                      cos(pi * (2 * j - 1) / (2 * k)))

    return array(result)


def get_equal_distance_nodes(n, start, end):
    return linspace(start, end, n)


def calculate_precision(x1, x2, filename):
    err_max = []
    err_sqr = []

    for i in range(len(x1)):
        d = abs(x1[i] - x2[i])
        err_max.append(d)
        err_sqr.append(d ** 2)

    n1 = max(err_max)
    n2 = sum(err_sqr) / len(x2)

    with open(filename, "a") as file:
        file.write(str(n1) + " ")
        file.write(str(n2) + "\n")
