def get_newton_coefficients(x, y):
    n = len(x)
    a = []

    for i in range(n):
        a.append(y[i])

    for j in range(1, n):

        for i in range(n - 1, j - 1, -1):
            a[i] = (a[i] - a[i - 1]) / float(x[i] - x[i - j])

    return a


def get_newton_values(a, x, r):
    n = len(a)
    temp = a[-1]
    for i in range(n - 2, -1, -1):
        temp = temp * (r - x[i]) + a[i]
    return temp
