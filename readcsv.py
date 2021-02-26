
import numpy as np
import pandas as pd

file_name = 'Data/USICSAM.csv'
#file_name = 'Data/USDEUR.csv'

df = pd.read_csv(file_name, sep=',', header=2, index_col=0, parse_dates=['Date'])

s = df['Close']     
print(s)     ## Pandas "Series" (array) indexed by date
print(s.resample('D').pad())    ## pad missing values with previous value
print(s.resample('D').interpolate()) ## pad missing values with linear interpolation
print(s['1970-01-01':])  ## return all values after certain date
print(s.to_numpy())   ## convert to numpy array



