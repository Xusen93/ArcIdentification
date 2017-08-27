# -*- coding: utf-8 -*-
# @Author: Xusen
# @Date:   2017-08-20 21:03:30
# @Last Modified by:   Xusen
# @Last Modified time: 2017-08-27 14:06:53
from identification_DC import *
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import csv


def csvread(addr='demo/DC/demo_data.csv'):
    '''csvread

    load leakage current data from .csv files

    Keyword Arguments:
            addr {str} -- address of .csvfiles (default: {'demo/DC/demo_data.csv'})

    Returns:
            array -- including 3 columns, that is, time, voltage and current
    '''
    with open(addr, 'r') as f:
        logging.info("Loading data from %s" % addr)
        reader = csv.reader(f)
        return np.array([line for line in reader], dtype=float)


def csvwrite(data, filename):
    with open(filename, 'w', newline='') as f:
        logging.info("Saving arc parameters to %s" % filename)
        writer = csv.writer(f)
        writer.writerows(np.around(data, 3))


def imgplot(time, crt, **kw):
    fig = plt.figure(dpi=150)
    ax = fig.add_subplot(111)
    ax.plot(time, crt, c='gray', linewidth='0.5')
    ax.set_xlabel('Time(s)')
    ax.set_ylabel('Current(mA)')
    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    if 'ploc' in kw:
        ax.scatter(time[kw['ploc']], crt[kw['ploc']], label='Peak')
    if 'zloc' in kw:
        ax.scatter(time[kw['zloc']], crt[kw['zloc']], marker='.', label='Zero')
    if 'arcS' in kw:
        ax.scatter(time[kw['arcS']], crt[kw['arcS']],
                   marker='^', label='Start')
    if 'arcE' in kw:
        ax.scatter(time[kw['arcE']], crt[kw['arcE']], marker='x', label='End')
    if 'xlim' in kw:
        ax.set_xlim(kw['xlim'])
    if 'ylim' in kw:
        ax.set_ylim(kw['ylim'])
    ax.legend(loc='lower left')
    if 'fname' in kw:
        plt.savefig(kw['fname'])
    else:
        plt.show()


if __name__ == '__main__':
    data = csvread()
    time = data[:, 0]
    vol = data[:, 1]
    crt = data[:, 2]
    zloc = getZeros(crt)
    arcS, arcE, ploc = getArcs(crt, zloc)
    imgplot(time, crt, ploc=ploc, zloc=zloc, arcS=arcS,
            arcE=arcE, xlim=[0, 31], fname='demo/DC/demo.png')
    csvwrite(arcParameters(crt, vol, arcS, arcE, R=33), 'demo/DC/demo_arc.csv')
