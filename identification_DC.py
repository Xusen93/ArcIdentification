# -*- coding: utf-8 -*-
# @Author: Xusen
# @Email:  xusenthu@qq.com
# @Date:   2017-08-03 16:50:39
# @Last Modified by:   Xusen
# @Last Modified time: 2017-08-29 19:14:39
import logging
import numpy as np
logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)


def getZeros(crt, TH=0.5):
    '''getZeros

    find zero points

    Arguments:
        crt {array} -- current

    Keyword Arguments:
        TH {number} -- [description] (default: {0.5})

    Returns:
        array -- index of zero points in current array
    '''
    logging.info('Getting zero points ...')
    crt_mod = np.abs(np.hstack((0, crt[1:-1], 0)))
    return np.nonzero(crt_mod < TH)[0]


def getArcs(crt, zloc, MAW=10, MAD=1000, MPH=1):
    '''getArcs

    identify arcs

    Arguments:
            crt {array} -- current
            zloc {[type]} -- index in current array of zero points

    Keyword Arguments:
            MAW {number} -- minimum arc width (default: {2})
            MAD {number} -- minimum arc distance (default: {300})
            MPH {number} -- minimum peak height (default: {1})

    Returns:
            tuple of arrays -- index in current array of arc starts, arc ends, arc peak_locations
    '''
    logging.info('Getting arcs ...')
    fwdiff = np.hstack((0, zloc[1:]-zloc[0:-1]))
    bwdiff = np.hstack((zloc[1:]-zloc[0:-1], 0))
    s_MAW = zloc[np.nonzero(bwdiff > MAW)[0]].tolist()
    e_MAW = zloc[np.nonzero(fwdiff > MAW)[0]].tolist()
    for i in range(1, len(s_MAW)):
        if s_MAW[i]-e_MAW[i-1] < MAD:
            s_MAW[i] = None
            e_MAW[i-1] = None
    s_MAD = [i for i in s_MAW if i is not None]
    e_MAD = [i for i in e_MAW if i is not None]
    ploc = []
    for i in range(0, len(s_MAD)):
        crt_abs = np.abs(crt[s_MAD[i]:e_MAD[i]])
        temp = crt_abs.tolist().index(np.max(crt_abs))
        if crt_abs[temp] < MPH:
            s_MAD[i] = None
            e_MAD[i] = None
            ploc.append(None)
        else:
            ploc.append(s_MAD[i]+temp)
    arcS = [i for i in s_MAD if i is not None]
    arcE = [i for i in e_MAD if i is not None]
    ploc = [i for i in ploc if i is not None]
    return np.array(arcS), np.array(arcE), np.array(ploc)
