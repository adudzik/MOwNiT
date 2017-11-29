from numpy import linspace, array
from matplotlib import pyplot as plt
from utils import get_chebyshev_zeros, get_equal_distance_nodes, \
    calculate_precision
from newton import get_newton_coefficients, get_newton_values
from lagrange import lagrange_interpolation
from hermite import hermite_interpolation, get_hermite_coefficients, get_hermite_values
from math import sin, pi, e

START = -10.0
END = 5.0

PATHS = ["hermite\\", "lagrange\\", "newton\\"]


def f(x):
    return sin(4 * x / pi) * e ** (-0.5 * x / pi)


def test(n, int_type, x_exp, y_exp, get_nodes, nodes_type):
    x_node = get_nodes(n, START, END)
    y_node = array([f(x) for x in x_node])
    y_int = []

    if nodes_type == 0:
        file_name_part_1 = "equal_"
        file_name_part_2 = "_equal"
    else:
        file_name_part_1 = "chebyshev_"
        file_name_part_2 = "_chebyshev"

    if int_type == 0:
        for i in range(len(x_exp)):
            y_int.append(lagrange_interpolation(x_node, y_node, x_exp[i]))

        title = "Interpolacja wielomianami Lagrange'a dla liczby węzłów: " \
                + str(n)

        plot_path = PATHS[1] + file_name_part_1 + str(n) + ".png"
        prec_path = PATHS[1] + file_name_part_2 + ".txt"

    elif int_type == 1:
        a = get_newton_coefficients(x_node, y_node)

        for i in range(len(x_exp)):
            y_int.append(get_newton_values(a, x_node, x_exp[i]))

        title = "Interpolacja wielomianami Newton'a dla liczby węzłów: " \
                + str(n)

        plot_path = PATHS[2] + file_name_part_1 + str(n) + ".png"
        prec_path = PATHS[2] + file_name_part_2 + ".txt"

    else:
        f_int = hermite_interpolation(x_node, y_node, f)

        title = "Interpolacja Hermite'a dla liczby wezłów: " + str(n)

        for i in range(len(x_exp)):
            y_int.append(f_int(x_exp[i]))

        plot_path = PATHS[0] + file_name_part_1 + str(n) + ".png"
        prec_path = PATHS[0] + file_name_part_2 + ".txt"

    plt.plot(x_exp, y_exp, c='#00035b', label='funkcja f')
    plt.plot(x_exp, y_int, c='#fd3c06', label='funkcja interpolująca')
    plt.scatter(x_node, y_node, marker='o', c='red', s=20,
                label='węzły interpolacji')
    plt.title(title)
    plt.legend(loc="upper center")

    plt.savefig(plot_path, bbox_inches='tight')
    plt.close()

    calculate_precision(y_exp, y_int, prec_path, n)


def main():
    x_exp = linspace(START, END, 100)
    y_exp = [f(x) for x in x_exp]

    for i in range(14):
        if i >= 10:
            n = 5 * ((i + 1) % 10) + 10
        else:
            n = 2 + i

        test(n, 0, x_exp, y_exp, get_equal_distance_nodes, 0)
        print("DONE Lagrange for type: equal, n: ", n)
        test(n, 1, x_exp, y_exp, get_equal_distance_nodes, 0)
        print("DONE Newton for type: equal, n: ", n)
        test(n, 2, x_exp, y_exp, get_equal_distance_nodes, 0)
        print("DONE Hermite for type: equal, n: ", n)
        test(n, 0, x_exp, y_exp, get_chebyshev_zeros, 1)
        print("DONE Lagrange for type: chebyshev, n: ", n)
        test(n, 1, x_exp, y_exp, get_chebyshev_zeros, 1)
        print("DONE Newton for type: chebyshev, n: ", n)
        test(n, 2, x_exp, y_exp, get_chebyshev_zeros, 1)
        print("DONE Hermite for type: chebyshev, n: ", n)


if __name__ == "__main__":
    main()
