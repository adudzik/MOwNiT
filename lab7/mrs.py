import numpy as np
from matplotlib import pyplot as plt


m = 2
a = 0
b = np.pi + 1


def theory(x):
    return np.cos(m * x) - x * np.sin(m * x)


def mrs(n, h):
    x = np.linspace(a, b, n, endpoint=True)
    a_arr = np.zeros((n, n))
    b_vec = np.zeros(n)

    for i in range(1, n-1):
        a_arr[i][i-1] = 1
        a_arr[i][i] = 4 * (h ** 2) - 2
        a_arr[i][i+1] = 1

    a_arr[0][0] = 1
    a_arr[-1][-1] = 1

    for i in range(1, n-1):
        b_vec[i] = (h ** 2) * (-2) * m * np.cos(m * x[i])

    b_vec[0] = 1
    b_vec[-1] = theory(b)

    y_vec = np.linalg.solve(a_arr, b_vec)

    return x, y_vec


def calculate_precision(x1, x2, step, points, filename):
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
        file.write(str(step) + " ")
        file.write(str(n1) + " ")
        file.write(str(n2) + "\n")


def main():

    for n in range(10, 500, 15):
        h = (b - a) / n
        x_mrs, y_mrs = mrs(n, h)

        x = np.linspace(a, b, n, endpoint=True)
        y = [theory(arg) for arg in x]

        plt.plot(x, y, label="wartość dokładna")
        plt.plot(x_mrs, y_mrs, label="MRS")
        plt.title("Rozwiązanie problemu brzegowego dla " + str(n) + " punktów")
        plt.xlabel("x")
        plt.ylabel("y(x)")
        plt.legend()
        plt.savefig("mrs\\plot_" + str(n) + ".png", bbox_inches="tight")
        plt.close()

        calculate_precision(y, y_mrs, h, n, "mrs\\mrs.txt")

        print("DONE for n:", n)


if __name__ == "__main__":
    main()