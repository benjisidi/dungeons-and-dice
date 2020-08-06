import math
from typing import List, Tuple
import matplotlib.pyplot as plt
import numpy as np
import random
import timeit

#   Nomenclature:
#     A _set_ of dice is a collection of n dice all with the same number of faces, f,
#       denoted ndf - eg, three six-sided die would be the set 3d6. These are represented
#       as a tuple [n, f]
#       (since set is a python keyword, they are referred to as set_ in the code)
#     A _cluster_ of dice is a collection of N sets, represented as a 2xN matrix:
#     [
#       [ n1, f1 ],
#       [ n2, f2 ],
#       ...,
#       [ nN, fN ]
#     ]


def roll_set(n, f):
    return [random.randint(1, f) for i in range(n)]


def roll_cluster(cluster, n=1):
    return [[roll_set(n, f) for (n, f) in cluster] for i in range(n)]


def expected_result(cluster):
    return [n * (f + 1) / 2 for (n, f) in cluster]


def powerset(n, f):
    return np.polynomial.polynomial.polypow([0, *[1 for i in range(f)]], n)


def cluster_powerset(sets):
    overall_powerset = [1]
    for set_ in sets:
        overall_powerset = np.polynomial.polynomial.polymul(
            overall_powerset, powerset(*set_)
        )
    return overall_powerset


def ways_to_roll(target, n, f):
    if target > n * f or target < n:
        return 0
    if target == n * f or target == n:
        return 1
    return powerset[target]


def ways_to_roll_cluster(target, cluster):
    return cluster_powerset(cluster)[target]


def p_of_rolling(target, n, f):
    return ways_to_roll(target, n, f) / (f ** n)


def cluster_p_distribution(cluster):
    ni = cluster[:, 0]
    fi = cluster[:, 1]
    total = np.product([np.power(f, ni[i], dtype=float) for (i, f) in enumerate(fi)])
    return cluster_powerset(cluster) / total


def p_of_rolling_cluster(target, cluster):
    return cluster_p_distribution(cluster)[target]


def plot_powerset(n, f):
    data = [ways_to_roll(i, n, f) for i in range(n, n * f + 1)]
    x = range(n, n * f + 1)
    plt.scatter(x, data)
    plt.ylabel(f"N({n},d,{f})")
    plt.xlabel("t")
    plt.title(f"Outcome distribution for {n}d{f}")
    plt.show()


def plot_p_distribution(n, f, cumulative=False):
    data = [p_of_rolling(i, n, f) for i in range(n, n * f + 1)]
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


def plot_cluster_powerset(cluster):
    ni = cluster[:, 0]
    fi = cluster[:, 1]
    data = np.trim_zeros(cluster_powerset(cluster))
    x = range(np.sum(ni), np.sum(ni * fi) + 1)
    plt.scatter(x, data)
    plt.ylabel("# of ways of rolling t")
    plt.xlabel("t")
    plt.title(
        f"Outcome distribution for {'+ '.join([f'{n}d{f}' for (n, f) in cluster])}"
    )
    plt.show()


def plot_cluster_p_distribution(clusters, cumulative=False):
    ni = clusters[:, 0]
    fi = clusters[:, 1]
    total = np.product([np.power(f, ni[i], dtype=float) for (i, f) in enumerate(fi)])
    data = np.trim_zeros(cluster_p_distribution(clusters))
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
    test_dice = np.array([[1, 4], [2, 6]])
    plot_cluster_p_distribution(test_dice)
