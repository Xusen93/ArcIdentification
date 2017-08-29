# -*- coding: utf-8 -*-
# @Author: Xusen
# @Date:   2017-08-29 19:13:38
# @Last Modified by:   Xusen
# @Last Modified time: 2017-08-29 19:17:29
import logging
import numpy as np
logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)


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