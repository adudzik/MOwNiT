from numpy import zeros, linalg


def fill_matrix_1(n):
    a = zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i == 0:
                a[i][j] = 1.0
            else:
                a[i][j] = 1.0 / (i + j + 1.0)
    return a


def fill_matrix_2(n):
    a = zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i <= j:
                a[i][j] = 2.0 * (i + 1.0) / (j + 1.0)
            else:
                a[i][j] = a[j][i]
    return a


def find_conditions(a, n):
    rows_a = zeros(n)
    rows_inv_a = zeros(n)

    inv_a = linalg.inv(a)

    for i in range(n):
        for j in range(n):
            rows_a[i] += abs(a[i][j])
            rows_inv_a[i] += abs(inv_a[i][j])

    return max(rows_a) * max(rows_inv_a)


def main():
    for i in range(8):
        a = fill_matrix_1(i + 3)
        print("zad1 n =", i + 3, "cond(A)=", find_conditions(a, i + 3))

    for i in range(8):
        b = fill_matrix_2(i + 3)
        print("zad2 n =", i + 3, "cond(A)=", find_conditions(b, i + 3))


if __name__ == "__main__":
    main()
