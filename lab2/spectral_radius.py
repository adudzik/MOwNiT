from numpy import zeros, linalg, dot, subtract
from jacoby import fill_array_a


# Spectral radius
def find_spectral_radius(a, n):
    spectral_radius = 0

    # Creating iterations matrix B = I - M^-1 * A
    i_m = zeros((n, n))
    for j in range(n):
        i_m[j][j] = 1

    m = zeros((n, n))
    for i in range(n):
        m[i][i] = 1.0 / a[i][i]

    b = subtract(i_m, dot(m, a))

    e_values = linalg.eigvals(b)

    for i in range(n):
        if spectral_radius < abs(e_values[i]):
            spectral_radius = abs(e_values[i])

    return spectral_radius


def main():
    n = int(input("Problem's size = "))
    a = fill_array_a(n)
    print("n = ", n, "    radius=", find_spectral_radius(a, n))


if __name__ == "__main__":
    main()
