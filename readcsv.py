
import numpy as np
import pandas as pd

def get_file_names():
   f = open('file_names.txt')
   file_names = ['Data/'+s.strip('\n') for s in f.readlines()]
   f.close()
   return file_names 



def get_data(start='2001-01-01', end='2019-12-31', pad='pad', verbose=False):   
    """ 
    Get all daily data, padding NaNs with appropriate values.

    - start: start day of timeseries.  
    - end: end day of timeseries.  
    - pad: either 'pad' for repeat last value, or 'interpolate' for linear
      interpolation between data points. Missing values in the beginning are
      filled with the first value of the data set.
    - verbose: print file names and columns as we go
    """

    file_names = get_file_names()
    series = []
    ix = pd.date_range(start=start, end=end, freq='D')

    for name in file_names:

        df = pd.read_csv(name, sep=',', header=2, index_col=0, parse_dates=['Date'])

        ## get all columns for USDEUR. 
        if df['Ticker'][0] == 'USDEUR':
            cols = ['Close', 'Open', 'High', 'Low']
        else:
            cols = ['Close']

        for col in cols:
            s = df[col]

            ## if column NaN, don't use
            if pd.isna(s[0]):
                continue

            if verbose:
                print(name, col)

            s = s.reindex(ix)

            ## apply padding
            if pad == 'pad':
                s.ffill(inplace=True)
            elif pad == 'interpolate':
                s.interpolate(inplace=True)
            else:
                raise KeyError('pad keyword not valid')
            s.bfill(inplace=True)   ## replace leading NaN with first entry

            series.append(s)

    return pd.concat(series, axis=1).to_numpy()

