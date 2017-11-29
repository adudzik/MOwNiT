from numpy import zeros
from math import sqrt
from random import randint, uniform

# Globals
it_1_stop = []
it_2_stop = []
err_1_stop = []
err_2_stop = []


# Generating arrays
def fill_array_a(n):
    k = 10
    m = 1
    a = zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i == j:
                a[i][j] = k
            elif j > i:
                a[i][j] = ((-1) ** (j + 1)) * m / (j + 1)
            elif j == i - 1:
                a[i][j] = m / (i + 1)
            else:
                a[i][j] = 0

    return a


def generate_x(n):
    x = zeros(n)

    for i in range(n):
        if randint(1, 100000) % 2 == 0:
            x[i] = -1
        else:
            x[i] = 1

    return x


def fill_array_b(a, x, n):
    b = zeros(n)

    for i in range(n):
        for j in range(n):
            b[i] += a[i][j] * x[j]

    return b


def generate_starting_vector(n):
    result = zeros(n)
    for i in range(n):
        result[i] = uniform(-5000, 5000)  # range o starting vector cords

    return result


# Operating on vectors
def rewrite_vector(x, n):
    result = zeros(n)

    for i in range(n):
        result[i] = x[i]

    return result


def distance(x, y, n):
    d = 0

    for i in range(n):
        d += abs(x[i] - y[i]) ** 2

    return sqrt(d)


# Solvers
def jacoby_method(a, b, x, n, epsilon):
    # Generating vectors
    next_x = zeros(n)
    starting_vector = generate_starting_vector(n)

    for stop_type in range(2):
        it_counter = 0
        prev_x = rewrite_vector(starting_vector, n)
        while True:
            it_counter += 1
            # Jacoby's method
            for i in range(n):
                suma = 0

                for j in range(n):
                    if i != j:
                        suma += a[i][j] * prev_x[j]

                next_x[i] = (b[i] - suma) / a[i][i]

            # First stop
            if stop_type == 0:
                err = distance(prev_x, next_x, n)
                if err < epsilon:
                    it_1_stop.append(it_counter)
                    break
                else:
                    prev_x = rewrite_vector(next_x, n)
            # Second stop
            elif stop_type == 1:
                new_b = fill_array_b(a, next_x, n)
                err = distance(new_b, b, n)
                if err < epsilon:
                    it_2_stop.append(it_counter)
                    break
                else:
                    prev_x = rewrite_vector(next_x, n)
            else:
                prev_x = rewrite_vector(next_x, n)

        if stop_type == 0:
            err_1_stop.append(distance(x, next_x, n))
        else:
            err_2_stop.append(distance(x, next_x, n))


def sor_solver(a, b, x, n, epsilon, omega):
    # Generating vectors
    next_x = zeros(n)
    gs_next = zeros(n)
    starting_vector = generate_starting_vector(n)

    for stop_type in range(2):
        it_counter = 0
        prev_x = rewrite_vector(starting_vector, n)
        while True:
            it_counter += 1
            # SOR method
            for i in range(n):
                suma = 0

                # Gauss-Seidel next iteration
                for j in range(n):
                    if j > i:
                        suma += a[i][j] * prev_x[j]
                    elif j < i:
                        suma += a[i][j] * next_x[j]

                gs_next[i] = (b[i] - suma) / a[i][i]

                # SOR next iteration
                next_x[i] = (1 - omega) * prev_x[i] + omega * gs_next[i]

            # First stop
            if stop_type == 0:
                err = distance(prev_x, next_x, n)
                if err < epsilon:
                    it_1_stop.append(it_counter)
                    break
                else:
                    prev_x = rewrite_vector(next_x, n)
            # Second stop
            elif stop_type == 1:
                new_b = fill_array_b(a, next_x, n)
                err = distance(new_b, b, n)
                if err < epsilon:
                    it_2_stop.append(it_counter)
                    break
                else:
                    prev_x = rewrite_vector(next_x, n)
            else:
                prev_x = rewrite_vector(next_x, n)

        if stop_type == 0:
            err_1_stop.append(distance(x, next_x, n))
        else:
            err_2_stop.append(distance(x, next_x, n))


# Test functions
def test_jacoby(n, tests):
    global it_1_stop, it_2_stop, err_1_stop, err_2_stop
    a = fill_array_a(n)
    x = generate_x(n)
    b = fill_array_b(a, x, n)

    for j in range(8):
        eps = 10 ** (-(j + 3))
        print("Precision: ", eps)
        for i in range(tests):
            jacoby_method(a, b, x, n, eps)

        maximum = max(it_1_stop)
        minimum = min(it_1_stop)
        avg = sum(it_1_stop) / len(it_1_stop)
        avq_err = sum(err_1_stop) / len(err_1_stop)

        print("Stop1 - min =", minimum, "avg =", avg, "max =", maximum,
              "average error =", avq_err)

        maximum = max(it_2_stop)
        minimum = min(it_2_stop)
        avg = sum(it_2_stop) / len(it_2_stop)
        avq_err = sum(err_2_stop) / len(err_2_stop)

        print("Stop2 - min =", minimum, "avg =", avg, "max =", maximum,
              "average error =", avq_err)

        it_1_stop, it_2_stop, err_1_stop, err_2_stop = [], [], [], []


def test_sor(n, tests):
    global it_1_stop, it_2_stop, err_1_stop, err_2_stop
    a = fill_array_a(n)
    x = generate_x(n)
    b = fill_array_b(a, x, n)
    omega = 0

    for j in range(7):
        omega += 0.25
        print("Omega: ", omega)
        for i in range(tests):
            sor_solver(a, b, x, n, 10 ** (-6), omega)

        maximum = max(it_1_stop)
        minimum = min(it_1_stop)
        avg = sum(it_1_stop) / len(it_1_stop)
        avq_err = sum(err_1_stop) / len(err_1_stop)

        print("Stop1 - min =", minimum, "avg =", avg, "max =", maximum,
              "average error =", avq_err)

        maximum = max(it_2_stop)
        minimum = min(it_2_stop)
        avg = sum(it_2_stop) / len(it_2_stop)
        avq_err = sum(err_2_stop) / len(err_2_stop)

        print("Stop2 - min =", minimum, "avg =", avg, "max =", maximum,
              "average error =", avq_err)

        it_1_stop, it_2_stop, err_1_stop, err_2_stop = [], [], [], []


def main():
    n = int(input("Problem's size = "))

    t = int(input("1. Jacoby \n2. SOR \n"))

    if t == 1:
        if n > 100:
            tests = 5
        else:
            tests = 50
        test_jacoby(n, tests)
    else:
        if n > 100:
            tests = 1
        else:
            tests = 10
        test_sor(n, tests)


if __name__ == "__main__":
    main()
