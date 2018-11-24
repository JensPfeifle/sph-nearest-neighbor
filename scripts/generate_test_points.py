import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
import random
import config as CONF


def make_cluster(dims: int, center: tuple,  delta_x: float,  delta_y: float, particle_spacing: float):
    if not dims == 2:
        raise NotImplementedError
    n_x = int(delta_x / particle_spacing)
    n_y = int(delta_y / particle_spacing)
    x = np.linspace(center[0] - delta_x/2, center[0] + delta_x/2,
                    num=n_x)
    y = np.linspace(center[1] - delta_y/2, center[1] + delta_y/2,
                    num=n_y)

    clusterpoints_x = np.ndarray(n_x * n_y)
    clusterpoints_y = np.ndarray(n_x * n_y)
    n = 0
    for i in range(len(x)):
        for j in range(len(y)):
            clusterpoints_x[n] = x[i]
            clusterpoints_y[n] = y[j]
            n = n + 1

    return (clusterpoints_x, clusterpoints_y)


def write_file(x: [], y: [], filename='output.txt'):
    TAB = "\t"
    assert (len(x) == len(y))
    with open(filename, 'w') as f:
        for n in range(len(x)):
            f.write("{:.6f}{}{:.6f}\n".format(x[n], TAB, y[n]))


def write_datafile(data_x, data_y):
    write_file(data_x, data_y, "data.pts")


def write_queryfile(query_x, query_y):
    write_file(query_x, query_y, "query.pts")


if __name__ == "__main__":

    center = (3.5e-3, 7e-3)
    delta_x = 1e-3
    delta_y = 1.3e-3
    x, y = make_cluster(dims=2, center=center,  delta_x=delta_x,
                        delta_y=delta_y, particle_spacing=CONF.dx)
    data_x = x
    data_y = y

    center = (1.5e-3, 4e-3)
    delta_x = 1.6e-3
    delta_y = 0.8e-3
    x, y = make_cluster(dims=2, center=center,  delta_x=delta_x,
                        delta_y=delta_y, particle_spacing=CONF.dx)
    data_x = np.append(data_x, x)
    data_y = np.append(data_y, y)

    center = (3.5e-3, 1e-3)
    delta_x = 1.4e-3
    delta_y = 0.8e-3
    x, y = make_cluster(dims=2, center=center,  delta_x=delta_x,
                        delta_y=delta_y, particle_spacing=CONF.dx)
    data_x = np.append(data_x, x)
    data_y = np.append(data_y, y)

    write_datafile(data_x, data_y)
    print("Wrote {} data points.".format(len(data_x)))

    ###
    # select a random query point
    n = random.randint(0,len(data_x)-1)
    query_x = [data_x[n]]
    query_y = [data_y[n]]
    write_queryfile(query_x, query_y)
    print("Wrote {} query points.".format(len(query_x)))
