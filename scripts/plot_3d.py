import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from typing import List, Tuple
import config as CONF
import re


def read_datapts(file="data.pts"):
    with open(file, 'r') as f:
        lines = f.readlines()
        n = len(lines)
        x = np.ndarray(n)
        y = np.ndarray(n)
        z = np.ndarray(n)
        for n, line in enumerate(lines):
            x[n], y[n], z[n] = line.strip().split("\t")
    return (x, y, z)


def read_results(file="result.dat"):

    re_float = r"[0-9]*\.[0-9]*"

    with open(file, 'r') as f:
        lines = f.readlines()
        n = len(lines)
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
    data_x, data_y, data_z = read_datapts("data.pts")
    # r, qp, nn_idx = read_results("result.dat")

    #neighbors_x = [data_x[i] for i in nn_idx]
    #neighbors_y = [data_y[i] for i in nn_idx]
    #neighbors_z = [data_z[i] for i in nn_idx]

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter3D(data_x, data_y, data_z, s=10, label="datapoints")
    # ax.scatter3d(neighbors_x, neighbors_y,
    #           label='{} neighbors'.format(len(nn_idx)))
    #ax.scatter3d(qp[0], qp[1],qp[2], s=10, label='query point')

    # plot corners of test domain
    domain_x = [0,  CONF.Lx, CONF.Lx,        0, 0]
    domain_y = [0,        0, CONF.Ly,  CONF.Ly, 0]
    domain_z = [0,        0,       0,        0, 0]
    ax.plot3D(domain_x, domain_y, domain_z, c='red')
    domain_x = [      0, CONF.Lx, CONF.Lx,       0,       0]
    domain_y = [      0,       0, CONF.Ly, CONF.Ly,       0]
    domain_z = [CONF.Lz, CONF.Lz, CONF.Lz, CONF.Lz, CONF.Lz]
    ax.plot3D(domain_x, domain_y, domain_z, c='red', label="domain bounds")
    maxdim = max(CONF.Lx, CONF.Ly, CONF.Lz)
    ax.set_xlim((0, maxdim))
    ax.set_ylim((0, maxdim))
    ax.set_zlim((0, maxdim))
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.legend()
    plt.title("Test Domain")
    plt.show()
