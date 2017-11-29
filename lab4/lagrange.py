def lagrange_interpolation(xs, ys, x):
    y = 0.0

    for i in range(len(xs)):
        t = 1.0
        for j in range(len(xs)):
            if j != i:
                t *= (x - xs[j]) / (xs[i] - xs[j])

        y += t * ys[i]

    return y
