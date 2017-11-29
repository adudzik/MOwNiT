from numpy import zeros, array


def derivative(fun):
    eps = 10 ** (-7)

    def der(x):
        return (fun(x + eps) - fun(x)) / eps

    return der


def hermite_interpolation(x_exp, y_exp, fun):
    n = len(x_exp)
    fp = derivative(fun)

    points = zeros(shape=(2 * n + 1, 2 * n + 1))

    for i in range(0, 2 * n, 2):
        points[i][0] = x_exp[i // 2]
        points[i + 1][0] = x_exp[i // 2]
        points[i][1] = y_exp[i // 2]
        points[i + 1][1] = y_exp[i // 2]

    for i in range(2, 2 * n + 1):
        for j in range(1 + (i - 2), 2 * n):
            if i == 2 and j % 2 == 1:
                points[j][i] = fp(x_exp[j // 2])

            else:
                points[j][i] = (points[j][i - 1] - points[j - 1][i - 1]) / (
                    points[j][0] - points[(j - 1) - (i - 2)][0])

    def result_polynomial(x):
        val = 0
        for k in range(0, 2 * n):
            factor = 1
            l = 0
            while l < k:
                factor *= (x - x_exp[l // 2])
                if l + 1 != k:
                    factor *= (x - x_exp[l // 2])
                    l += 1
                l += 1
            val += factor * points[k][k + 1]
        return val

    return result_polynomial


def get_hermite_coefficients(x, y, fun):
    x.astype(float)
    y.astype(float)
    fp = derivative(fun)

    n = len(x)
    a = []

    for i in range(n):
        a.append(y[i])

    for j in range(1, n):
        p = 1
        for i in range(n - 1, j - 1, -1):
            if x[i] - x[i - j] != 0:
                a[i] = float(a[i] - a[i - 1]) / float(x[i] - x[i - j])
            else:
                a[i] = float(fp(a[i])) / p
        p += 1
    return array(a)


def get_hermite_values(a, x, r):
    x.astype(float)
    n = len(a) - 1
    temp = a[n]
    for i in range(n - 1, -1, -1):
        temp = temp * (r - x[i]) + a[i]
    return temp
