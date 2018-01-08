import numpy as np
from matplotlib import pyplot as plt
from math import sqrt

m = 2
k = 4


def fun(x, y):
    return k ** 2 * m * np.sin(m * x) * np.cos(m * x) + k * m * y * np.sin(
        m * x)


def theory(x):
    return np.e ** (-k * np.cos(m * x)) - k * np.cos(m * x) + 1


def euler(x, y0, n, delta):
    y = np.zeros(n)

    y[0] = y0
    for i in range(1, n):
        y[i] = delta * fun(x[i - 1], y[i - 1]) + y[i - 1]

    return x, y


def runge_kutta(x0, y0, x1, n):
    vx = [0] * (n + 1)
    vy = [0] * (n + 1)
    h = (x1 - x0) / (n - 1)
    vx[0] = x = x0
    vy[0] = y = y0
    for i in range(1, n + 1):
        k1 = h * fun(x, y)
        k2 = h * fun(x + 0.5 * h, y + 0.5 * k1)
        k3 = h * fun(x + 0.5 * h, y + 0.5 * k2)
        k4 = h * fun(x + h, y + k3)
        vx[i] = x = x0 + i * h
        vy[i] = y = y + (k1 + k2 + k2 + k3 + k3 + k4) / 6
    return vx, vy


def calculate_precision(x1, x2, points, filename):
    err_max = []
    err_sqr = []

    for i in range(len(x2)):
        d = abs(x1[i] - x2[i])
        err_max.append(d)
        err_sqr.append(d ** 2)

    n1 = max(err_max)
    n2 = sum(err_sqr) / len(x2)

    with open(filename, "a") as file:
        file.write(str(points) + " ")
        file.write(str(n1) + " ")
        file.write(str(n2) + "\n")


def main():
    for i in range(100, 25000, 1000):
        x0 = - np.pi / 4
        xn = 3 * np.pi / 2
        y0 = 2
        delta = (xn - x0) / i
        to_str = "{:.9f}".format(delta)
        title = "Rozwiązanie równania różniczkowego 1. rzędu dla kroku " \
                + to_str

        x = np.linspace(x0, xn, i)
        y = [theory(x) for x in x]

        x_e, y_e = euler(x, y0, i, delta)
        x_rk, y_rk = runge_kutta(x0, y0, xn, i)

        plt.plot(x, y, label="wartość dokładna")
        plt.plot(x_e, y_e, label="metoda Euler'a")
        plt.plot(x_rk, y_rk, label="metoda Runge-Kutta")
        plt.legend()
        plt.xlabel("x")
        plt.ylabel("y(x)")
        plt.title(title)
        plt.savefig("plots\\plot_" + str(i) + ".png")
        plt.close()

        calculate_precision(y_rk, y, delta, "results\\runge_kutta.txt")
        calculate_precision(y_e, y, delta, "results\\euler.txt")

        print("DONE for ", i, "points")


if __name__ == "__main__":
    main()
