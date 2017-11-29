from numpy import array


def get_newton_coefficients(x, y):
    x.astype(float)
    y.astype(float)
    n = len(x)
    a = []
    for i in range(n):
        a.append(y[i])

    for j in range(1, n):

        for i in range(n - 1, j - 1, -1):
            a[i] = float(a[i] - a[i - 1]) / float(x[i] - x[i - j])

    return array(a)


def get_newton_values(a, x, r):
    x.astype(float)
    n = len(a) - 1
    temp = a[n]
    for i in range(n - 1, -1, -1):
        temp = temp * (r - x[i]) + a[i]
    return temp
