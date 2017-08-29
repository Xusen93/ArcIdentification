# -*- coding: utf-8 -*-
# @Author: Xusen
# @Email:  xusenthu@qq.com
# @Date:   2017-08-03 16:50:39
# @Last Modified by:   Xusen
# @Last Modified time: 2017-08-29 19:14:17
import logging
import numpy as np
logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)


def findpeaks(crt, MPH, MPD):
    '''findpeaks

    find maximum in every sinusoidal cycle

    Arguments:
            crt {array} -- current
            MPH {number} -- minimum peak height, for filtering peaks in arc extinguishing
            MPD {number} -- minimum peak distance, for grouping adjacent extremes

    Returns:
            array -- indexes of maximums
    '''
    # the equation of finding extremes
    ex_con = np.hstack((0, (crt[2:]-crt[1:-1])*(crt[1:-1]-crt[0:-2]), 0))
    # positions of all extremes(amplitude > MPH)
    ex_pos = np.array([p for p in np.nonzero(ex_con <= 0)[0] if crt[p] > MPH])
    # distance between adjacent extremes
    pd = np.hstack((0, ex_pos[1:]-ex_pos[0:-1]))
    # grouping extremes according to pd
    gp_s = [0]+[d for d in np.nonzero(pd > MPD)[0]]
    gp_e = [d for d in np.nonzero(pd > MPD)[0]]+[len(pd)]

    def findmax(crt, ex_pos, gp_s, gp_e):
        '''findmax

        finding the maximum in a group of extremes

        Arguments:
                crt {array} -- current
                ex_pos {array} -- indexes in current array of extremes
                gp_s {list} -- group start
                gp_e {list} -- group end, a group of extremes is ex_pos[gp_s:gp_e]

        Returns:
                number -- index in current array of the maximum
        '''
        gp = ex_pos[gp_s:gp_e]
        return gp[crt[gp].tolist().index(np.max(crt[gp]))]
    ploc = [findmax(crt, ex_pos, gp_s[i], gp_e[i])
            for i in range(0, len(gp_s))]
    return np.array(ploc)


def getAllPeaks(crt, MPH=1, MPD=50):
    '''getAllPeaks

    use findpeaks to get all peaks(the maximum and minimum in every sinusoidal cycle)

    Arguments:
            crt {array} -- current

    Keyword Arguments:
            MPH {number} -- minimum peak height (default: {1})
            MPD {number} -- minimum peak distance (default: {50})

    Returns:
            array -- index in current array of peaks
    '''
    logging.info('Getting all peaks ...')
    peaks = findpeaks(crt, MPH, MPD)
    valleys = findpeaks(-crt, MPH, MPD)
    ploc = np.hstack((peaks, valleys))
    return np.sort(ploc)


def getZeros(crt, ploc, TH=0.1):
    '''getZeros

    find zero points by the side of peaks

    Arguments:
            crt {array} -- current
            ploc {array} -- index in current array of peaks

    Keyword Arguments:
            TH {number} -- zero threshold (default: {0.1})

    Returns:
            array -- index of zero points in current array
    '''
    logging.info('Getting zero points ...')
    len_crt = crt.size
    abs_crt = np.abs(crt)
    def findlz(abs_crt, p, TH):
        # find left zero point
        while abs_crt[p] > TH:
            p -= 1
            if p < 0:
                break
        return max(0, p)
    def findrz(abs_crt, p, TH):
        # find right zero point
        while abs_crt[p] > TH:
            p += 1
            if p > len_crt-1:
                break
        return min(p, len_crt-1)
    zeroloc = [findlz(abs_crt, p, TH) for p in ploc] + \
        [findrz(abs_crt, p, TH) for p in ploc]
    return np.array(sorted(zeroloc))


def getArcs(ploc, zloc, MAD=300, MPC=5):
    '''getArcs

    identify arcs

    Arguments:
            ploc {array} -- index in current array of peaks
            zloc {array} -- index in current array of zero points

    Keyword Arguments:
            MAD {number} -- minimum arc distance (default: {300})
            MPC {number} -- minimum peak count (default: {5})

    Returns:
            tuple of arrays -- index in current array of arc starts and arc ends
    '''
    logging.info('Getting arcs ...')
    dloc = np.hstack((0, ploc[1:]-ploc[0:-1]))
    # get index, if dloc > MAD
    idx = [d[0] for d in enumerate(dloc) if d[1] > MAD]
    idx = [0]+idx+[len(ploc)]
    arcStart = []
    arcEnd = []
    for m in range(0, len(idx[0:-1])):
        if idx[m+1]-idx[m]+1 > MPC:
            arcStart.append(zloc[2*idx[m]])
            arcEnd.append(zloc[2*idx[m+1]-1])
    return np.array(arcStart), np.array(arcEnd)
