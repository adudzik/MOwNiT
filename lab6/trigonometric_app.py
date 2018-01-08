import numpy as np
from matplotlib import pyplot as plt

START = -10.0
END = 5.0


def f(x):
    return np.sin(4 * x / np.pi) * np.e ** (-0.5 * x / np.pi)


def approximate(deg, x_exp, y_exp):
    n = len(y_exp)
    a_0 = sum(y_exp) / n
    a_coefficients, b_coefficients = [], []

    t = 2 * np.pi / (n - 1)
    for j in range(1, deg + 1):
        a, b = 0.0, 0.0

        for i in range(n):
            a += y_exp[i] * np.cos(t * j * i)
            b += y_exp[i] * np.sin(t * j * i)

        a *= 2 / n
        b *= 2 / n

        a_coefficients.append(a)
        b_coefficients.append(b)

    length = x_exp[-1] - x_exp[0]
    mapping_a = 2 * np.pi / length
    mapping_b = (x_exp[-1] + x_exp[0]) / 2

    def get_values(x):
        x = mapping_a * (x - mapping_b) + np.pi
        result = a_0

        for k in range(len(a_coefficients)):
            result += a_coefficients[k] * np.cos((k + 1) * x) + \
                      b_coefficients[k] * np.sin((k + 1) * x)

        return result

    return get_values


def calculate_precision(x1, x2, points, filename):
    err_max = []
    err_sqr = []

    for i in range(len(x1)):
        d = abs(x1[i] - x2[i])
        err_max.append(d)
        err_sqr.append(d ** 2)

    n1 = max(err_max)
    n2 = sum(err_sqr) / len(x2)

    with open(filename, "a") as file:
        file.write(str(points) + " ")
        file.write(str(n1) + " ")
        file.write(str(n2) + "\n")


def test(deg, norm_file):
    nodes = 2 * deg + 1

    x_app = np.linspace(START, END, 150)
    for i in range(nodes, 101, 5):
        x_nodes = np.linspace(START, END, i)
        y_nodes = [f(x) for x in x_nodes]
        fun = approximate(deg, x_nodes, y_nodes)

        y_app = [fun(x) for x in x_app]
        y_f = [f(x) for x in x_app]

        plt.plot(x_app, y_f, c='red', label='funkcja f')
        plt.plot(x_app, y_app, c='blue', label='funkcja aproksymująca')
        if i < 30:
            plt.scatter(x_nodes, y_nodes, c='green', s=25, label='węzły')
        plt.title(
            "Aproksymacja trygonometryczna dla " + str(
                i) + " punktów i wielomianów stopnia " + str(
                deg))
        plt.legend(loc="upper center")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.savefig("plots_trig\\eq_" + str(deg) + "_" + str(i) + ".png",
                    bbox_inches='tight')
        plt.close()

        calculate_precision(y_app, y_f, i, norm_file)


def main():
    for deg in range(2, 10, 1):
        test(deg, "results_trig\\res_" + str(deg) + ".txt")
        print("DONE for deg:", deg)

    for deg in range(10, 26, 5):
        test(deg, "results_trig\\res_" + str(deg) + ".txt")
        print("DONE for deg:", deg)


if __name__ == "__main__":
    main()
