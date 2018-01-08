import numpy as np
from matplotlib import pyplot as plt

START = -10.0
END = 5.0


def f(x):
    return np.sin(4 * x / np.pi) * np.e ** (-0.5 * x / np.pi)


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


def approximate(deg, x_exp, y_exp):
    n = len(x_exp)
    m = deg + 1

    left_side = []
    right_side = []

    for k in range(m):
        temp = 0
        for j in range(n):
            temp += y_exp[j] * x_exp[j] ** k

        right_side.append(temp)

        left_vector = []
        for i in range(m):
            temp = 0
            for j in range(n):
                temp += x_exp[j] ** (i + k)
            left_vector.append(temp)

        left_side.append(left_vector)

    a_val = np.linalg.solve(left_side, right_side)

    def get_value(x):
        result, i = 0, 0
        for a in a_val:
            result += a * x ** i
            i += 1
        return result

    return get_value


def test(deg, norm_file):
    x_app = np.linspace(START, END, 150)

    if deg < 10:
        for i in range(deg + 1, 10, 1):
            x_nodes = np.linspace(START, END, i)
            y_nodes = [f(x) for x in x_nodes]

            fun = approximate(deg, x_nodes, y_nodes)

            y_app = [fun(x) for x in x_app]
            y_f = [f(x) for x in x_app]

            plt.plot(x_app, y_f, c='red', label='funkcja aproksymowana')
            plt.plot(x_app, y_app, c='blue', label='funkcja aproksymująca')

            if i < 30:
                plt.scatter(x_nodes, y_nodes, c='green', s=25,
                            label='punkty aproksymacji')

            plt.title(
                "Aproksymacja dla " + str(i) + " punktów i wielomianu stopnia "
                + str(deg))
            plt.legend(loc="upper center")
            plt.xlabel("x")
            plt.ylabel("f(x)")
            plt.savefig("plots\\eq_" + str(deg) + "_" + str(i) + ".png",
                        bbox_inches='tight')
            plt.close()

            # calculate_precision(y_app, y_f, i, norm_file)

        for i in range(10, 101, 10):
            x_nodes = np.linspace(START, END, i)
            y_nodes = [f(x) for x in x_nodes]
            fun = approximate(deg, x_nodes, y_nodes)

            y_app = [fun(x) for x in x_app]
            y_f = [f(x) for x in x_app]

            plt.plot(x_app, y_f, c='red', label='funkcja aproksymowana')
            plt.plot(x_app, y_app, c='blue', label='funkcja aproksymująca')

            if i < 30:
                plt.scatter(x_nodes, y_nodes, c='green', s=25,
                            label='punkty aproksymacji')

            plt.title(
                "Aproksymacja dla " + str(i) + " punktów i wielomianu stopnia "
                + str(deg))
            plt.legend(loc="upper center")
            plt.xlabel("x")
            plt.ylabel("f(x)")
            plt.savefig("plots\\eq_" + str(deg) + "_" + str(i) + ".png",
                        bbox_inches='tight')
            plt.close()

            # calculate_precision(y_app, y_f, i, norm_file)
    else:
        for i in range(deg, 101, 10):
            x_nodes = np.linspace(START, END, i)
            y_nodes = [f(x) for x in x_nodes]
            fun = approximate(deg, x_nodes, y_nodes)

            y_app = [fun(x) for x in x_app]
            y_f = [f(x) for x in x_app]

            plt.plot(x_app, y_f, c='red', label='funkcja aproksymowana')
            plt.plot(x_app, y_app, c='blue', label='funkcja aproksymująca')

            if i < 30:
                plt.scatter(x_nodes, y_nodes, c='green', s=25,
                            label='punkty aproksymacji')

            plt.title(
                "Aproksymacja dla " + str(i) + " punktów i wielomianu stopnia "
                + str(deg))
            plt.legend(loc="upper center")
            plt.xlabel("x")
            plt.ylabel("f(x)")
            plt.savefig("plots\\eq_" + str(deg) + "_" + str(i) + ".png",
                        bbox_inches='tight')
            plt.close()

            # calculate_precision(y_app, y_f, i, norm_file)


def main():
    for deg in range(2, 10, 1):
        test(deg, "results\\res_" + str(deg) + ".txt")
        print("DONE for deg:", deg)

    for deg in range(10, 26, 5):
        test(deg, "results\\res_" + str(deg) + ".txt")
        print("DONE for deg:", deg)


if __name__ == "__main__":
    main()
