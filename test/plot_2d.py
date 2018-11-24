import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
import config as CONF
import re


def read_datapts(file="data.pts"):
    with open(file, 'r') as f:
        lines = f.readlines()
        n = len(lines)
        x = np.ndarray(n)
        y = np.ndarray(n)
        for n, line in enumerate(lines):
            x[n], y[n] = line.strip().split("\t")
    return (x, y)


def read_results(file="result.dat"):

    re_float = r"[0-9]*\.[0-9]*"

    with open(file, 'r') as f:
        lines = f.readlines()
        n = len(lines)
        x = np.ndarray(n, dtype=np.float64)
        y = np.ndarray(n, dtype=np.float64)
        neighbor_idxs = []
        for n, line in enumerate(lines):
            if n == 0:
                radius = float(re.findall(re_float, line)[0])
            elif n == 2:
                p1, p2 = re.findall(re_float, line)
                query_point = (float(p1), float(p2))
            elif n >= 5:
                neighbor_idxs.append(int(line.strip().split()[1]))

    return radius, query_point, neighbor_idxs


if __name__ == "__main__":
    data_x, data_y = read_datapts("data.pts")
    r, qp, nn_idx = read_results("result.dat")

    neighbors_x = [data_x[i] for i in nn_idx]
    neighbors_y = [data_y[i] for i in nn_idx]

    fig, ax = plt.subplots(figsize=(6, 8))
    ax.scatter(data_x, data_y, s=10, label="datapoints")
    ax.scatter(neighbors_x, neighbors_y,
               label='{} neighbors'.format(len(nn_idx)))
    ax.scatter(qp[0], qp[1], s=10, label='query point')
    ax.set_aspect('equal')
    ax.set_xlim((0, CONF.Lx))
    ax.set_ylim((0, CONF.Ly))
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.legend()
    plt.title("Test Domain")
    plt.show()
