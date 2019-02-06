#!/usr/bin/python3
import datetime
import sys
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


def make_fill(fill: float):

    F = fill

    # define field for only half of each axis
    l = np.array([CONF.Lx/2, CONF.Ly/2, CONF.Lz/2])
    n = (l/CONF.dx).astype('int')

    field = np.zeros(n)

    b = max(n) * F
    # fill a fraction of the field
    #nx, ny, nz = [int(F*n) for n in field.shape]
    nx, ny, nz = field.shape
    print(nx, ny, nz)
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                if j + i < b:
                    if k + i < b:
                        if j + k < b:
                            field[i, j, k] = 1

    # field is 1/8th of the total volume
    # fill another eighth across the x axis
    zeros = np.zeros(field.shape)
    field = np.concatenate([field, field[::-1, :, :]], axis=0)
    # fill a quarter across the y axis
    #zeros = np.zeros(field.shape)
    field = np.concatenate([field, field[:, ::-1, :]], axis=1)
    # then mirror the half of the field we currently have over each axis
    # and set it to be the top half of the field
    field = np.concatenate([field, field[:, :, ::-1]], axis=2)

    npoints = int(field.sum())
    points_x = np.ndarray(npoints)
    points_y = np.ndarray(npoints)
    points_z = np.ndarray(npoints)

    p = 0
    for i in range(field.shape[0]):
        for j in range(field.shape[1]):
            for k in range(field.shape[2]):
                if field[i, j, k] == 1:
                    points_x[p] = i*CONF.dx
                    points_y[p] = j*CONF.dx
                    points_z[p] = k*CONF.dx
                    p = p + 1

    return (points_x, points_y, points_z)


if __name__ == "__main__":

    try:
        fillfactor = float(sys.argv[1])
    except:
        print("Test3d: arguments required:")
        print("   fill factor as float, e.g. 0.3")
        sys.exit(1)

    filltype = "diagonal"
    x, y, z = make_fill(fillfactor)
    ndatapts = len(x)

    write_datafile(x, y, z)
    print("Test3d: wrote {} data points".format(ndatapts))

    actualfill = ndatapts/(CONF.Lx * CONF.Ly * CONF.Lz / CONF.dx**3)
    fill = str(actualfill)
    print("Test3d: fill = " + fill)
    write_stats(ndatapts, fill)
