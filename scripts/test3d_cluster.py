#!/usr/bin/python3
import datetime
import sys
from pathlib import Path
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np

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
            f.write("{:.12f}{}{:.12f}{}{:.12f}\n".format(
                x[n], TAB, y[n], TAB, z[n]))


def write_datafile(data_x, data_y, data_z, filename = "data.pts"):
    write_file(data_x, data_y, data_z, str(filename))


def write_queryfile(query_x, query_y, data_z):
    write_file(query_x, query_y, data_z, "query.pts")


def make_fill(fillfactor: float, N: int) -> ([float], [float], [float]):
    """
    Returns x,y,z arrays for a clustered fill 
    of approximately fillfactor using N clusters
    """

    assert N % 2 == 1, "N must be odd"
    fillfactor = fillfactor**(1/3)

    hx = CONF.Lx*fillfactor/N
    hy = CONF.Ly*fillfactor/N
    hz = CONF.Lz*fillfactor/N

    tx = CONF.Lx/(N)
    ty = CONF.Ly/(N)
    tz = CONF.Lz/(N)

    tx0 = (CONF.Lx)/2
    ty0 = (CONF.Ly)/2
    tz0 = (CONF.Lz)/2

    data_x = []
    data_y = []
    data_z = []
    for i in range(-(N-1)//2, N//2+1):
        for j in range(-(N-1)//2, N//2+1):
            for k in range(-(N-1)//2, N//2+1):
                x = tx0 + tx*i
                y = ty0 + ty*j
                z = tz0 + tz*k

                px, py, pz = make_cluster(center=(x, y, z),
                                          delta_x=hx,
                                          delta_y=hy,
                                          delta_z=hz,
                                          particle_spacing=CONF.dx)
                data_x = np.append(data_x, px)
                data_y = np.append(data_y, py)
                data_z = np.append(data_z, pz)

    return (data_x, data_y, data_z)


if __name__ == "__main__":

    try:
        fillfactor = float(sys.argv[1])
        N = int(sys.argv[2])
    except:
        print("Test3d: arguments required:")
        print("   fill factor as float, e.g. 0.3")
        print("   number of clusters as int, e.g. 5")
        sys.exit(1)

    x, y, z = make_fill(fillfactor, N)

    write_datafile(x, y, z)
    ndatapts = len(x)

    print("Test3d: wrote {} data points".format(ndatapts))
    N_full = CONF.Lx * CONF.Ly * CONF.Lz / CONF.dx**3

    actualfill = ndatapts/N_full
    print("Test3d: fill = {}".format(actualfill))

    filltype = "cluster"
    fill = str(actualfill)
    # write statistics

    statsfilepath = Path("./stats.csv")
    if not statsfilepath.is_file():
        print("Test3d: creating stats file")
        with open(statsfilepath, 'w') as f:
            f.write('time,sizex,sizey,sizez,filltype,fill,ndatapts,'
                    + 'ttotal,tksearch,tfrsearch,tprocessing\n')
    with open(statsfilepath, 'a') as f:
        time = datetime.datetime.now().isoformat()
        data = [time, CONF.Lx, CONF.Ly, CONF.Lz, filltype, fill, ndatapts]
        datastr = ",".join([str(d) for d in data])
        f.write(datastr)
