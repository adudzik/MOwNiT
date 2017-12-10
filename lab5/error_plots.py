from matplotlib import pyplot as plt


def read_file(filename):
    with open(filename) as file:
        read_data = file.readlines()

    x, y1, y2 = [], [], []
    for line in read_data:
        elements = line.split(' ')
        x.append(float(elements[0]))
        y1.append(float(elements[1]))
        y2.append(float(elements[2]))

    return x, y1, y2


def create_plots():
    filename1 = "cub\\c_esd.txt"
    filename2 = "cub\\c_natural.txt"
    filename3 = "quad\\q_end.txt"
    filename4 = "quad\\q_start.txt"

    x_ce, y_cem, y_ceq = read_file(filename1)
    x_cn, y_cnm, y_cnq = read_file(filename2)
    x_qe, y_qem, y_qeq = read_file(filename3)
    x_qs, y_qsm, y_qsq = read_file(filename4)

    plt.plot(x_cn, y_cnm, c="blue", label="3. stopień - 1. warunek brzegowy")
    plt.plot(x_ce, y_cem, c="orange", label="3. stopień - 2. warunek brzegowy")
    plt.plot(x_qs, y_qsm, c="red", label="2. stopień - 1. warunek brzegowy")
    plt.plot(x_qe, y_qem, c="green", label="2. stopień - 2. warunek brzegowy")
    plt.xlabel("liczba węzłów interpolacyjnych")
    plt.ylabel("błąd interpolacji")
    plt.title("Błąd w metryce maksimum dla funkcji sklejanych "
              "2-go i 3-go stopnia")
    plt.legend()
    plt.semilogy()
    plt.savefig("max.png", bbox_inches='tight')
    plt.close()

    plt.plot(x_cn, y_cnq, c="blue", label="3. stopień - 1. warunek brzegowy")
    plt.plot(x_ce, y_ceq, c="orange", label="3. stopień - 2. warunek brzegowy")
    plt.plot(x_qs, y_qsq, c="red", label="2. stopień - 1. warunek brzegowy")
    plt.plot(x_qe, y_qeq, c="green", label="2. stopień - 2. warunek brzegowy")
    plt.xlabel("liczba węzłów interpolacyjnych")
    plt.ylabel("błąd interpolacji")
    plt.title("Błąd w metryce średniokwadratowej dla funkcji sklejanych "
              "2-go i 3-go stopnia")
    plt.legend()
    plt.semilogy()
    plt.savefig("avg.png", bbox_inches='tight')
    plt.close()


def main():
    create_plots()


if __name__ == "__main__":
    main()
