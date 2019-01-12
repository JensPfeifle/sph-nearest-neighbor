#!/usr/bin/python3
import datetime
from pathlib import Path
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


def make_fill():

    l = np.array([CONF.Lx, CONF.Ly, CONF.Lz])
    n = (l/CONF.dx).astype('int')

    npoints = n[0]*n[1]*n[2]
    points_x = np.ndarray(npoints)
    points_y = np.ndarray(npoints)
    points_z = np.ndarray(npoints)

    p = 0
    for i in range(n[0]):
        for j in range(n[1]):
            for k in range(n[2]):
                points_x[p] = i*CONF.dx
                points_y[p] = j*CONF.dx
                points_z[p] = k*CONF.dx
                p = p + 1

    return (points_x, points_y, points_z)


if __name__ == "__main__":

    filltype = "full"
    x, y, z = make_fill()
    ndatapts = len(x)

    write_datafile(x, y, z)
    print("Test3d: wrote {} data points".format(ndatapts))

    actualfill = ndatapts/(CONF.Lx * CONF.Ly * CONF.Lz / CONF.dx**3)
    fill = str(actualfill)
    print("Test3d: fill = " + fill)
    write_stats(ndatapts, fill)
