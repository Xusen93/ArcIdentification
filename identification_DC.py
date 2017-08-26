# -*- coding: utf-8 -*-
# @Author: Xusen
# @Email:  xusenthu@qq.com
# @Date:   2017-08-03 16:50:39
# @Last Modified by:   Xusen
# @Last Modified time: 2017-08-26 15:50:15
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


def getArcs(crt, zloc, MAW=100, MPH=1):
    '''getArcs

    identify arcs

    Arguments:
            zloc {[type]} -- index in current array of zero points

    Keyword Arguments:
            MAW {number} -- minimum arc width (default: {100})
            MPH {number} -- minimum peak height (default: {1})

    Returns:
            tuple of arrays -- index in current array of arc starts, arc ends, arc peak_locations
    '''
    logging.info('Getting arcs ...')
    fwdiff = np.hstack((0, zloc[1:]-zloc[0:-1]))
    bwdiff = np.hstack((zloc[1:]-zloc[0:-1], 0))
    s = zloc[np.nonzero(bwdiff > MAW)[0]]
    e = zloc[np.nonzero(fwdiff > MAW)[0]]
    def arcfilter(crt, s, e, MPH):
        crt_abs = np.abs(crt)
        ploc = crt_abs.tolist().index(np.max(crt_abs))
        if crt_abs[ploc] > MPH:
            return s, e, s+ploc
    filtered = [arcfilter(crt[s:e], s, e, MPH) for s, e in zip(s, e)]
    s_e_p = np.array([[p[0], p[1], p[2]] for p in filtered if p is not None])
    return s_e_p[:, 0], s_e_p[:, 1], s_e_p[:, 2]


def arcParameters(crt, vol, arcS, arcE, R=33):
    '''arcParameters

    calculate the defined arc parameters

    Arguments:
            crt {array} -- current
            vol {array} -- voltage
            arcS {array} -- index in current array of arc starts
            arcE {array} -- index in current array of arc ends

    Keyword Arguments:
            R {number} -- resistance(kΩ) of the test cycle (default: {33})

    Returns:
            array -- arc parameters, that is, Ta, To, Im, Ie, E, P
    '''
    logging.info('Calculating arc parameters ...')
    def cal_im(crt, s, e):
        return np.max(np.abs(crt[s:e]))
    def cal_ie(crt, s, e):
        return np.sqrt(np.mean(crt[s:e]**2))
    def cal_e(crt, vol, s, e, R):
        return np.sum((vol[s:e]-R*crt[s:e]*1e-3)*crt[s:e])/5000
    # ignore the last arc, because its 'To' could not be defined
    Ta = (arcE[:-1]-arcS[:-1])/5000
    To = (arcS[1:]-arcE[:-1])/5000
    Im = [cal_im(crt, s, e) for s, e in zip(arcS[:-1], arcE[:-1])]
    Ie = [cal_ie(crt, s, e) for s, e in zip(arcS[:-1], arcE[:-1])]
    E = [cal_e(crt, vol, s, e, R) for s, e in zip(arcS[:-1], arcE[:-1])]
    P = E/(Ta+To)
    return np.vstack((Ta, To, Im, Ie, E, P)).T
