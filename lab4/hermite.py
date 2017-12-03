def derivative(fun):
    h = 10 ** (-4)

    def der(x, i):
        if i == 1:
            return (fun(x + h) - fun(x - h)) / h / 2
        return (der(x + h, i - 1) - der(x - h, i - 1)) / h / 2

    return der


def get_hermite_coefficients(x, y, fun):
    n = len(x)
    a = []

    fp = derivative(fun)

    for i in range(n):
        a.append(y[i])

    p = 1
    for j in range(1, n):
        p *= j
        for i in range(n - 1, j - 1, -1):
            if x[i] == x[i - j]:
                a[i] = fp(x[i], j) / p
            else:
                a[i] = (a[i] - a[i - 1]) / float(x[i] - x[i - j])
    return a


def get_hermite_values(a, x, r):
    n = len(x)
    temp = a[-1]
    for i in range(n - 2, -1, -1):
        temp = temp * (r - x[i]) + a[i]
    return temp
