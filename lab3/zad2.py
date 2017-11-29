from numpy import linalg, zeros, subtract, dot
from math import sqrt

from numpy.linalg import LinAlgError

EPSILON = 10 ** (-5)
SIZE = 3
MAX_ITER = 300


# Functions
def f(x1, x2, x3):
    return [[x1 ** 2 + x2 ** 2 - x3 ** 2 - 1],
            [x1 - 2 * (x2 ** 3) + 2 * (x3 ** 2) + 1],
            [2 * (x1 ** 2) + x2 - 2 * (x3 ** 2) - 1]]


# Deriveratives
def fp(x1, x2, x3):
    return [[2 * x1, 2 * x2, -2 * x3],
            [1, -6 * (x2 ** 2), 4 * x3],
            [4 * x1, 1, -4 * x3]]


def newton_method(starting_vector, stop):
    prev_x = starting_vector
    i = 0
    while True:
        f0 = f(prev_x[0][0], prev_x[1][0], prev_x[2][0])
        fp0 = fp(prev_x[0][0], prev_x[1][0], prev_x[2][0])

        inv_fp0 = linalg.inv(fp0)
        m = dot(inv_fp0, f0)
        next_x = subtract(prev_x, m)
        # print(prev_x)
        if stop(prev_x, next_x) or i > MAX_ITER:
            break

        prev_x = next_x
        i += 1

    return next_x, i


def distance(x, y):
    d = 0
    for i in range(SIZE):
        d += abs(x[i] - y[i]) ** 2

    return sqrt(d)


def stop_1():
    def end(old_x, new_x):
        return distance(old_x, new_x) <= EPSILON

    return end


def stop_2():
    def end(_, new_x):
        return distance(f(new_x[0][0], new_x[1][0], new_x[2][0]),
                        zeros(SIZE)) <= EPSILON

    return end


def test_newton(starting, filename1, filename2):
    with open(filename1, "a") as file:
        try:
            res, i = newton_method(starting, stop_1())
            x = [item for sublist in res for item in sublist]

            if i > MAX_ITER:
                return

            file.write("Starting vector: " +
                       str([item for sublist in starting for item in sublist]))
            file.write(" x= " + str(x) + "iterations: " + str(i) + "\n")
        except (LinAlgError, RuntimeError):
            return

    with open(filename2, "a") as file:
        try:
            res, i = newton_method(starting, stop_2())
            x = [item for sublist in res for item in sublist]

            if i > MAX_ITER:
                return

            file.write("Starting vector: " +
                       str([item for sublist in starting for item in sublist]))
            file.write(" x= " + str(x) + "iterations: " + str(i) + "\n")
        except (LinAlgError, RuntimeError):
            return


def main():
    x = -2.0
    for i in range(17):
        y = -2.0
        for j in range(17):
            z = -2.0
            for k in range(17):
                starting = [[x], [y], [z]]
                test_newton(starting, "results\\system1stop.txt",
                            "results\\system2stop.txt")

                s = [item for sublist in starting for item in sublist]
                print("DONE for starting: ", s)
                z += 0.25
            y += 0.25
        x += 0.25


if __name__ == "__main__":
    main()
