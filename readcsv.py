import numpy as np
import pandas as pd

def get_data(start='2001-01-01', end='2020-12-31', method='ffill',
    normalize=True, init='bfill', txt='file_names.txt', verbose=False):   

    """ 
    Get all daily data, padding NaNs with appropriate values.

    - start: start day of timeseries.  
    - end: end day of timeseries.  
    - method: how to fill missing data points (see pd.reindex documentation).
    - normalize: if True, normalize so Close timeseries has mean 0 variance 1.
      USD-EUR exchange rates are never normalized.
    - init: how to fill leading NaNs (data history too short).
        'bfill': fill with first valid data point.
        x: custom replacement value.
    - txt: text file containing file names to include.
    - verbose: print file names and columns as we go.
    """

    file_names = get_file_names(txt)
    series = []
    ix = pd.date_range(start=start, end=end, freq='D')

    for name in file_names:

        df = pd.read_csv(name, sep=',', header=2, index_col=0, parse_dates=['Date'])

        mean = None
        std = None

        for col in ['Close', 'Open', 'High', 'Low']:

            s = df[col]

            ## if column NaN, don't use
            if pd.isna(s[0]):
                continue

            if verbose:
                print(name, col)

            ## resample to have daily data points
            s = s.reindex(ix, method=method)

            ## normalize to Close
            ticker = df['Ticker'][0]
            if normalize and ticker != 'USDEUR':
                if col == 'Close':
                    mean = s.mean()
                    std = s.std(ddof=0)
                s = (s - mean)/std

            ## handle leading NaNs
            if init == 'bfill':
                s.bfill(inplace=True)
            else:
                s.fillna(init, inplace=True)

            series.append(s)

    return pd.concat(series, axis=1).to_numpy()



def get_file_names(txt):
   with open(txt) as f:
       file_names = ['Data/'+s.strip('\n') for s in f.readlines()]
   return file_names 



