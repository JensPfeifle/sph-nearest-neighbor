import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
import random
import config as CONF


def make_cluster(center: tuple,
                 delta_x: float,
                 delta_y: float,
                 delta_z: float,
                 particle_spacing: float):
    n_x = int(delta_x / particle_spacing)
    n_y = int(delta_y / particle_spacing)
    n_z = int(delta_z / particle_spacing)
    x = np.linspace(center[0] - delta_x/2, center[0] + delta_x/2,
                    num=n_x)
    y = np.linspace(center[1] - delta_y/2, center[1] + delta_y/2,
                    num=n_y)
    z = np.linspace(center[2] - delta_z/2, center[2] + delta_z/2,
                    num=n_z)

    clusterpoints_x = np.ndarray(n_x * n_y * n_z)
    clusterpoints_y = np.ndarray(n_x * n_y * n_z)
    clusterpoints_z = np.ndarray(n_x * n_y * n_z)

    n = 0
    for i in range(n_x):
        for j in range(n_y):
            for k in range(n_z):
                clusterpoints_x[n] = x[i]
                clusterpoints_y[n] = y[j]
                clusterpoints_z[n] = z[k]
                n = n + 1

    return (clusterpoints_x, clusterpoints_y, clusterpoints_z)


def write_file(x: [], y: [], z: [], filename='output.txt'):
    TAB = "\t"
    assert (len(x) == len(y) == len(z))
    with open(filename, 'w') as f:
        for n in range(len(x)):
            f.write("{:.12f}{}{:.12f}{}{:.12f}\n".format(x[n], TAB, y[n],TAB, z[n]))


def write_datafile(data_x, data_y, data_z):
    write_file(data_x, data_y, data_z, "data.pts")


def write_queryfile(query_x, query_y, data_z):
    write_file(query_x, query_y, data_z, "query.pts")


if __name__ == "__main__":

    center = (3.5e-3, 7e-3,3e-3)
    delta_x = 1e-3
    delta_y = 1.3e-3
    delta_z = 1.3e-3
    x, y, z = make_cluster(center=center,
                           delta_x=delta_x,
                           delta_y=delta_y, 
                           delta_z=delta_z,
                           particle_spacing=CONF.dx)
    data_x = x
    data_y = y
    data_z = z

    center = (1.5e-3, 4e-3, 2e-3)
    delta_x = 1.6e-3
    delta_y = 0.8e-3
    delta_z = 1.3e-3
    x, y, z = make_cluster(center=center,
                           delta_x=delta_x,
                           delta_y=delta_y, 
                           delta_z=delta_z,
                           particle_spacing=CONF.dx)
    data_x = np.append(data_x, x)
    data_y = np.append(data_y, y)
    data_z = np.append(data_z, z)

    center = (3.5e-3, 1e-3, 1.3e-3)
    delta_x = 1.4e-3
    delta_y = 0.8e-3
    delta_z = 1.3e-3
    x, y, z = make_cluster(center=center,
                           delta_x=delta_x,
                           delta_y=delta_y, 
                           delta_z=delta_z,
                           particle_spacing=CONF.dx)
    data_x = np.append(data_x, x)
    data_y = np.append(data_y, y)
    data_z = np.append(data_z, z)


    write_datafile(data_x, data_y, data_z)
    print("Wrote {} data points.".format(len(data_x)))

    ###
    # select a random query point
    n = random.randint(0, len(data_x)-1)
    query_x = [data_x[n]]
    query_y = [data_y[n]]
    query_z = [data_z[n]]
    write_queryfile(query_x, query_y, query_z)
    print("Wrote {} query points.".format(len(query_x)))
