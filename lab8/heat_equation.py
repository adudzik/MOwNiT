import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt

a = 2
A = 1
B = -1
alpha = 1
l = 3 * np.pi / 2
tc = 5


def phi(x):
    return A * np.sin(alpha * x)


def forward(x_val, m, n):
    h = l / n
    k = tc / m

    coef = (a ** 2) * k / (h ** 2)
    print(coef)
    u_array = np.zeros((m + 1, n + 1))

    for i in range(n + 1):
        u_array[0][i] = phi(x_val[i])

    for j in range(m + 1):
        u_array[j][0] = 0
        u_array[j][-1] = B

    for i in range(0, m):
        for j in range(1, n):
            u_array[i + 1][j] = coef * (u_array[i][j + 1] - 2 * u_array[i][j]
                                        + u_array[i][j - 1]) + u_array[i][j]

    return u_array


def backward(x_val, m, n):
    h = l / n
    k = tc / m

    coef = (h ** 2) / (a ** 2) / k
    print(1 / coef)
    u_array = np.zeros((m + 1, n + 1))

    # boundary conditions
    for i in range(n + 1):
        u_array[0][i] = phi(x_val[i])

    for j in range(m + 1):
        u_array[j][0] = 0
        u_array[j][-1] = B

    a_arr = np.zeros((n + 1, n + 1))

    # fill array a
    for i in range(1, n):
        a_arr[i][i - 1] = -1
        a_arr[i][i] = 2 + coef
        a_arr[i][i + 1] = -1

    a_arr[0][0] = 1
    a_arr[-1][-1] = 1

    for j in range(1, m + 1):
        b = np.zeros(n + 1)

        b[0] = 0
        b[-1] = B

        for i in range(1, n):
            b[i] = u_array[j - 1][i] * coef

        x = thomas(a_arr, b, n + 1)
        u_array[j] = x

    return u_array


def thomas(a_arr, b_vec, n):
    result = np.zeros(n)
    aa = np.zeros(n)
    b = np.zeros(n)
    c = np.zeros(n)
    beta = np.zeros(n)
    gamma = np.zeros(n)

    for i in range(n):
        if i == 0:
            b[i] = a_arr[i][i]
            c[i] = a_arr[i][i + 1]
            continue
        if i == n - 1:
            aa[i] = a_arr[i][i - 1]
            b[i] = a_arr[i][i]
            continue

        aa[i] = a_arr[i][i - 1]
        b[i] = a_arr[i][i]
        c[i] = a_arr[i][i + 1]

    beta[0] = (-1) * c[0] / b[0]
    gamma[0] = b_vec[0] / b[0]

    for i in range(1, n):
        beta[i] = (-1) * c[i] / (aa[i] * beta[i - 1] + b[i])
        gamma[i] = (b_vec[i] - aa[i] * gamma[i - 1]) / (
            aa[i] * beta[i - 1] + b[i])

    result[n - 1] = gamma[n - 1]

    for i in range(n - 2, -1, -1):
        result[i] = beta[i] * result[i + 1] + gamma[i]

    return result


def test_coef():
    for n in range(5, 51, 5):
        for m in range(10, 1000, 50):
            h = l / n
            k = tc / m

            coef = (a ** 2) * k / (h ** 2)

            with open("./test.txt", "a") as file:
                file.write(str(m) + " ")
                file.write(str(n) + " ")
                file.write(str(coef) + "\n")


def main():
    # test_coef()
    # return
    m = 10
    n = 50

    x_val = np.linspace(0, l, n + 1)
    t_val = np.linspace(0, tc, m + 1)

    x, y = np.meshgrid(x_val, t_val)

    # u = forward(x_val, m, n)
    u = backward(x_val, m, n)

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_surface(x, y, u)
    ax.set_xlabel("x")
    ax.set_ylabel("czas (t)")
    ax.set_zlabel("u(x,t)")
    plt.show()


if __name__ == "__main__":
    main()
