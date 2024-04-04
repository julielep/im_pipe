#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 11:34:21 2024

@author: julie
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 12:35:25 2024

@author: philippe.gris@clermont.in2p3.fr
"""
import pandas as pd
from optparse import OptionParser
import numpy as np
from num import GetRunNumber, DoFit
from ptc import process, plot_ampli

def process_ptc_multi(toproc, params, j=0, output_q=None):
    """
    Function to process ptc using multiprocessing

    Parameters
    ----------
    toproc : list(int)
        List of indexes (row num) to process.
    params : dict
        parameters.
    j : int, optional
        internal tag for multiproc. The default is 0.
    output_q : multiprocessing queue, optional
        Where to dump the data. The default is None.

    Returns
    -------
    pandas dataframe
        Output Data.

    """

    imin = np.min(toproc)
    imax = np.max(toproc)+1
    data = params['data'][imin:imax]
    res = process_ptc(data)

    if output_q is not None:
        return output_q.put({j: res})
    else:
        return res


def process_ptc(data) -> pd.DataFrame:
    """
    Function to process the ptc

    Parameters
    ----------
    data : pandas df
        Data to process.

    Returns
    -------
    resa : pandas df
        Processed data.

    """

    resa = pd.DataFrame()
    for i, row in data.iterrows():
        flat0 = row['full_path_flat0']
        flat1 = row['full_path_flat1']
        res = process(flat0, flat1)
        resa = pd.concat([res, resa]).reset_index(drop=True)

    return resa


parser = OptionParser(description='Script to estimate the gain from the PTC on FP images')




parser.add_option('--dataPtcDir', type=str,
                  default='../ptc_resu/',
                  help='Path to data [%default]')

opts, args = parser.parse_args()
dataPtcDir = opts.dataPtcDir
runs = GetRunNumber(dataPtcDir)


parser.add_option('--run_num', type=str,
                  default=runs['run'].unique(),
                  help='list of runs to process [%default]')

parser.add_option('--outDir', type=str,
                  default="../fit_resu",
                  help='output dir for the processed data[%default]')

parser.add_option('--outName', type=str,
                  default="fit_resu_",
                  help='output file name[%default]')


parser.add_option('--prefix', type=str,
                  default=runs['filter'].unique(),
                  help='prefix for Flat files [%default]')

opts, args = parser.parse_args()
run_num = opts.run_num
outDir = opts.outDir
outName = opts.outName
prefix = opts.prefix
 

for run in run_num : 
    print(run) 
    dd = list(runs['FileName'][runs['run']==run])
    resu_fit = DoFit(dd, dataPtcDir, run)
        
    # save data
    outPath = '{}/{}{}.hdf5'.format(outDir, outName, run)
    resu_fit.to_hdf(outPath, key='ptc')
  


    

