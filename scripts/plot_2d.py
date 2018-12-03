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
        z = np.ndarray(n)
        for n, line in enumerate(lines):
            x[n], y[n], z[n] = line.strip().split("\t")
    return (x, y, z)

if __name__ == "__main__":
    data_x, data_y, data_z = read_datapts("data.pts")

    size = 5
    fig, axes = plt.subplots(1,3, figsize =(14,6))
    axes[0].scatter(data_x, data_y, s=size, label="datapoints")
    axes[0].set_aspect('equal')
    axes[0].set_xlim((0, CONF.Lx))
    axes[0].set_ylim((0, CONF.Ly))
    axes[0].set_xlabel('x')
    axes[0].set_ylabel('y')

    axes[1].scatter(data_y, data_z, s=size, label="datapoints")
    axes[1].set_aspect('equal')
    axes[1].set_xlim((0, CONF.Ly))
    axes[1].set_ylim((0, CONF.Lz))
    axes[1].set_xlabel('y')
    axes[1].set_ylabel('z')

    axes[2].scatter(data_x, data_z, s=size, label="datapoints")
    axes[2].set_aspect('equal')
    axes[2].set_xlim((0, CONF.Lx))
    axes[2].set_ylim((0, CONF.Lz))
    axes[2].set_xlabel('x')
    axes[2].set_ylabel('z')
    
    plt.title("Test Domain")
    plt.show()
