#!/usr/bin/python3

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


if __name__ == "__main__":
    data_x, data_y, data_z = read_datapts("data.pts")

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter3D(data_x, data_y, data_z, s=10, label="datapoints")

    # plot corners of test domain
    domain_x = [0,  CONF.Lx, CONF.Lx,        0, 0]
    domain_y = [0,        0, CONF.Ly,  CONF.Ly, 0]
    domain_z = [0,        0,       0,        0, 0]
    ax.plot3D(domain_x, domain_y, domain_z, c='red')
    domain_x = [      0, CONF.Lx, CONF.Lx,       0,       0]
    domain_y = [      0,       0, CONF.Ly, CONF.Ly,       0]
    domain_z = [CONF.Lz, CONF.Lz, CONF.Lz, CONF.Lz, CONF.Lz]
    ax.plot3D(domain_x, domain_y, domain_z, c='red', label="domain bounds")

    ax.set_xlim((-CONF.Lx/2, CONF.Lx*3/2))
    ax.set_ylim((-CONF.Ly/4, CONF.Ly*3/4))
    ax.set_zlim((0, CONF.Lz*2))
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.legend()
    plt.title("Test Domain")
    plt.show()
