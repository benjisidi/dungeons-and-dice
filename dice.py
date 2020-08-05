import math
from typing import List, Tuple
import matplotlib.pyplot as plt
import numpy as np
import random
import timeit


def roll(n, f):
    return [random.randint(1, f) for i in range(n)]


def roll_cluster(cluster, n=1):
    return [[roll(n, f) for (n, f) in cluster] for i in range(n)]


def expected_result(cluster):
    return [n * (f + 1) / 2 for (n, f) in cluster]


def powerset(n, f):
    return np.polynomial.polynomial.polypow([0, *[1 for i in range(f)]], n)


def N(t, n, f):
    if t > n * f or t < n:
        return 0
    if t == n * f or t == n:
        return 1
    return powerset[t]


def p(t, n, f):
    return N(t, n, f) / (f ** n)


def handful_N_set(clusters):
    overall_powerset = [1]
    for cluster in clusters:
        overall_powerset = np.polynomial.polynomial.polymul(
            overall_powerset, powerset(*cluster)
        )
    return overall_powerset


def handful_p_set(clusters):
    ni = clusters[:, 0]
    fi = clusters[:, 1]
    total = np.product([np.power(f, ni[i], dtype=float) for (i, f) in enumerate(fi)])
    return handful_N_set(clusters) / total


def handful_N(clusters, t):
    return handful_N_set(clusters)[t]


def handful_p(clusters, t):
    return handful_p_set(clusters)[t]


def plot_N(n, f):
    data = [N(i, n, f) for i in range(n, n * f + 1)]
    x = range(n, n * f + 1)
    plt.scatter(x, data)
    plt.ylabel(f"N({n},d,{f})")
    plt.xlabel("t")
    plt.title(f"Outcome distribution for {n}d{f}")
    plt.show()


def plot_p(n, f, cumulative=False):
    data = [p(i, n, f) for i in range(n, n * f + 1)]
    if cumulative:
        data = np.cumsum(data)
    x = range(n, n * f + 1)
    plt.scatter(x, data)
    plt.ylabel(f"p(t, {n}, {f})")
    plt.xlabel("t")
    plt.title(
        f"{'Cumulative probability' if cumulative else 'Probability'} distribution for {n}d{f}"
    )
    plt.show()


def plot_handful_n(clusters):
    ni = clusters[:, 0]
    fi = clusters[:, 1]
    data = np.trim_zeros(handful_N_set(clusters))
    x = range(np.sum(ni), np.sum(ni * fi) + 1)
    plt.scatter(x, data)
    plt.ylabel("# of ways of rolling t")
    plt.xlabel("t")
    plt.title(
        f"Outcome distribution for {'+ '.join([f'{n}d{f}' for (n, f) in clusters])}"
    )
    plt.show()


def plot_handful_p(clusters, cumulative=False):
    ni = clusters[:, 0]
    fi = clusters[:, 1]
    total = np.product([np.power(f, ni[i], dtype=float) for (i, f) in enumerate(fi)])
    data = np.trim_zeros(handful_p_set(clusters))
    if cumulative:
        data = np.cumsum(data)
    x = range(np.sum(ni), np.sum(ni * fi) + 1)
    plt.scatter(x, data)
    plt.ylabel("p(t)")
    plt.xlabel("t")
    plt.title(
        f"{'Cumulative probability' if cumulative else 'Probability'} distribution for {'+ '.join([f'{n}d{f}' for (n, f) in clusters])}"
    )
    plt.show()


if __name__ == "__main__":
    # test_dice = [(1, 4), (2, 6)]
    # print(expected_result(test_dice))
    # clusters = np.array([[10, 100], [50, 50], [100, 10]])
    # print(handful_N(clusters, 320))
    # clusters = [(1, 6), (1, 6)]
    # print(handful_N(clusters, 7))
    # print(np.polymul([1, 0], [1, 0]))
    clusters = np.array([[1, 4], [1, 6], [1, 8]])
    plot_handful_p(clusters, cumulative=True)
    plot_handful_p(clusters, cumulative=False)
    plot_handful_n(clusters)
