import numpy as np
from matplotlib import pyplot as plt
from cubic import cubic_interpolation
from quadratic import quadratic_interpolation
from utilities import get_equal_distance_nodes, get_chebyshev_zeros, \
    calculate_precision

START = -10.0
END = 5.0

PATHS = ["cub\\", "quad\\"]


def f(x):
    return np.sin(4 * x / np.pi) * np.e ** (-0.5 * x / np.pi)


def fp(fun):
    h = 10 ** (-4)

    def der(x, i):
        if i == 1:
            return (fun(x + h) - fun(x - h)) / h / 2
        return (der(x + h, i - 1) - der(x - h, i - 1)) / h / 2

    return der


def test(x_exp, y_exp, n, int_type, cond_type):
    x_node = np.linspace(START, END, n)
    y_node = [f(x) for x in x_node]

    if int_type == 2:
        x_int, y_int = quadratic_interpolation(x_node, y_node, 150, cond_type)
        title = "Interpolacja funkcjami sklejanymi 2-go stopnia dla " \
                + str(n - 1) + " przedziałów"

        t = "_start" if cond_type else "_end"
        plot_path = PATHS[1] + "q_" + str(n) + t + ".png"
        prec_path = PATHS[1] + "q" + t + ".txt"
    else:
        fp1, fp2 = 0, 0

        if int_type == 3 and not cond_type:
            fp1 = (fp(f)(START, 2))
            fp2 = (fp(f)(END, 2))

        x_int, y_int = cubic_interpolation(x_node, y_node, 150, cond_type, fp1,
                                           fp2)

        title = "Interpolacja funkcjami sklejanymi 3-go stopnia dla " \
                + str(n - 1) + " przedziałów"

        t = "_natural" if cond_type else "_esd"
        plot_path = PATHS[0] + "c_" + str(n) + t + ".png"
        prec_path = PATHS[0] + "c" + t + ".txt"

    plt.plot(x_exp, y_exp, c='#00035b', label='funkcja f')
    plt.plot(x_int, y_int, c='#fd3c06', label='funkcja sklejana')
    plt.scatter(x_node, y_node, marker='o', c='green', s=25,
                label="węzły interpolacji")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title(title)
    plt.legend(loc="upper center")
    plt.savefig(plot_path, bbox_inches='tight')
    plt.close()

    f_x = [f(x) for x in x_int]
    calculate_precision(n, f_x, y_int, prec_path)


def main():
    x_exp = np.linspace(START, END, 150)
    y_exp = np.array([f(x) for x in x_exp])

    for i in range(2, 11, 1):
        test(x_exp, y_exp, i, 2, True)
        print("DONE for quadratic n:", i, "stop: 1")
        test(x_exp, y_exp, i, 2, False)
        print("DONE for quadratic n:", i, "stop: 2")
        test(x_exp, y_exp, i, 3, True)
        print("DONE for cubic n:", i, "stop: 1")
        test(x_exp, y_exp, i, 3, False)
        print("DONE for cubic n:", i, "stop: 2")

    for i in range(15, 41, 5):
        test(x_exp, y_exp, i, 2, True)
        print("DONE for quadratic n:", i, "stop: 1")
        test(x_exp, y_exp, i, 2, False)
        print("DONE for quadratic n:", i, "stop: 2")
        test(x_exp, y_exp, i, 3, True)
        print("DONE for cubic n:", i, "stop: 1")
        test(x_exp, y_exp, i, 3, False)
        print("DONE for cubic n:", i, "stop: 2")


if __name__ == "__main__":
    main()
