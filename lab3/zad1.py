from math import exp
from matplotlib import pyplot as plt
from numpy import linspace

MAX_ITER = 500
EPSILON = 0

n = 10
m = 40

a = -0.6
b = 1.5


def f(x):
    return m * x * exp(-m) - m * exp(-n * x) + 1 / (n * m)


def derivative(fun):
    global EPSILON

    def der(x):
        return (fun(x + EPSILON) - fun(x)) / EPSILON

    return der


def stop_1(_):
    global EPSILON

    def end(old_x, new_x):
        return abs(old_x - new_x) < EPSILON

    return end


def stop_2(fun):
    global EPSILON

    def end(_, new_x):
        return abs(fun(new_x)) < EPSILON

    return end


def secant_method(x1, x2, stop):
    global EPSILON

    f1 = f(x1)
    f2 = f(x2)
    i = 0

    while (not stop(x2, x1)) and i <= MAX_ITER:
        i += 1
        if abs(f1 - f2) < EPSILON:
            break

        x0 = x1 - f1 * (x1 - x2) / (f1 - f2)
        f0 = f(x0)
        x2 = x1
        x1 = x0
        f2 = f1
        f1 = f0

    return x1, i


def newton_method(x0, stop):
    global EPSILON

    fp = derivative(f)

    f0 = f(x0)
    x1 = x0 - 1
    i = 0

    while (not stop(x1, x0)) and i <= MAX_ITER:
        i += 1
        f1 = fp(x0)

        if abs(f1) < EPSILON:
            break

        x1 = x0
        x0 -= f0 / f1
        f0 = f(x0)

    return x0, i


def test_secant(filename):
    with open(filename, "w+") as file:
        file.write("Changing b: \n")
        c = b
        file.write("1st stop\n")
        while c > a:
            res1, iterations1 = secant_method(a, c, stop_1(f))

            file.write(str(res1) + " " + str(iterations1) + "\n")

            c -= 0.1

        file.write("2nd stop\n")
        c = b
        while c > a:
            res2, iterations2 = secant_method(a, c, stop_2(f))

            file.write(str(res2) + " " + str(iterations2) + "\n")
            c -= 0.1

        file.write("\nChanging a: \n")

        file.write("1st stop\n")
        c = a
        while c < b:
            res1, iterations1 = secant_method(c, b, stop_1(f))

            file.write(str(res1) + " " + str(iterations1) + "\n")

            c += 0.1

        file.write("2nd stop\n")
        c = a
        while c < b:
            res2, iterations2 = secant_method(c, b, stop_2(f))

            file.write(str(res2) + " " + str(iterations2) + "\n")
            c += 0.1


def test_newton(filename):
    with open(filename, "w+") as file:
        file.write("1st stop\n")
        c = a
        while c < b + 0.1:
            res1, iterations1 = newton_method(c, stop_1(f))

            file.write(str(res1) + " " + str(iterations1) + "\n")

            c += 0.1

        file.write("2nd stop\n")
        c = a
        while c < b + 0.1:
            res2, iterations2 = newton_method(c, stop_2(f))

            file.write(str(res2) + " " + str(iterations2) + "\n")
            c += 0.1


def main():
    global EPSILON

    for i in range(9):
        k = i + 4
        EPSILON = 10 ** (-k)
        if k % 2 == 0:
            filename1 = "results\\newton_eps" + str(k) + ".txt"
            print("DONE newton for epsilon", EPSILON)
            filename2 = "results\\secant_eps" + str(k) + ".txt"
            print("DONE secant for epsilon", EPSILON)
            test_newton(filename1)
            test_secant(filename2)

    xs = linspace(-0.6, 1.5, 100)
    y = [f(x) for x in xs]

    plt.plot(xs, y)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title("Wykres funkcji f(x)")
    plt.savefig("wykres.png", bbox_inches='tight')


if __name__ == "__main__":
    main()
