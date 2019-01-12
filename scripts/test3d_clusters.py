#!/usr/bin/python3
import datetime
import sys
from pathlib import Path
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np

import config as CONF


def write_file(x: [], y: [], z: [], filename='output.txt'):
    TAB = "\t"
    assert (len(x) == len(y) == len(z))
    with open(filename, 'w') as f:
        for n in range(len(x)):
            f.write("{:.12f}{}{:.12f}{}{:.12f}\n".format(
                x[n], TAB, y[n], TAB, z[n]))


def write_datafile(data_x, data_y, data_z, filename="data.pts"):
    write_file(data_x, data_y, data_z, str(filename))


def write_stats(ndatapts: int, actuallfill: float,
                statsfilepath: Path = Path("./stats.csv")):
    if not statsfilepath.is_file():
        print("Test3d: creating stats file")
        with open(statsfilepath, 'w') as f:
            f.write('time,sizex,sizey,sizez,filltype,fill,ndatapts,'
                    + 'ttotal,tksearch,tfrsearch,tprocessing,listmethod,memory\n')
    with open(statsfilepath, 'a') as f:
        time = datetime.datetime.now().isoformat()
        data = [time, CONF.Lx, CONF.Ly, CONF.Lz, filltype, fill, ndatapts]
        datastr = ",".join([str(d) for d in data])
        f.write(datastr)


def make_fill(fill: float = 0.3, N: int = 4):

    #assert N%2 == 0, "N must be even"

    F = fill**(1/3)

    l = np.array([CONF.Lx, CONF.Ly, CONF.Lz])
    n = (l/CONF.dx).astype('int')

    t = n/N
    h = ((n*F)/N).astype(int)
    field = np.zeros(3*n)

    for i in range(N+1):
        x = n[0] + int(i*t[0])
        for j in range(N+1):
            y = n[1] + int(j*t[1])
            for k in range(N+1):
                z = n[2] + int(k*t[2])
                x0 = x - int(h[0]/2)
                x1 = x + int(h[0]/2)
                y0 = y - int(h[1]/2)
                y1 = y + int(h[1]/2)
                z0 = z - int(h[2]/2)
                z1 = z + int(h[2]/2)
                field[x0:x1, y0:y1, z0:z1] = 1
                #field[x0:x1, y0:y1, :] = 1

    field = field[50:100, 100:200, 50:100]

    npoints = int(field.sum())
    points_x = np.ndarray(npoints)
    points_y = np.ndarray(npoints)
    points_z = np.ndarray(npoints)

    p = 0
    for i in range(n[0]):
        for j in range(n[1]):
            for k in range(n[2]):
                if field[i, j, k] == 1:
                    # print(i,j,k)
                    points_x[p] = i*CONF.dx
                    points_y[p] = j*CONF.dx
                    points_z[p] = k*CONF.dx
                    p = p + 1

    return (points_x, points_y, points_z)


if __name__ == "__main__":

    try:
        fillfactor = float(sys.argv[1])
        N = int(sys.argv[2])
    except:
        print("Test3d: arguments required:")
        print("   fill factor as float, e.g. 0.3")
        print("   number of clusters as int, e.g. 5")
        sys.exit(1)

    filltype = "clusters{}".format(N)
    x, y, z = make_fill(fillfactor, N)
    ndatapts = len(x)

    write_datafile(x, y, z)
    print("Test3d: wrote {} data points".format(ndatapts))

    actualfill = ndatapts/(CONF.Lx * CONF.Ly * CONF.Lz / CONF.dx**3)
    fill = str(actualfill)
    print("Test3d: fill = " + fill)
    write_stats(ndatapts, fill)
