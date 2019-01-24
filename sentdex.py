import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import style
import quandl
style.use('ggplot')
#web_stats = {'Day':[1,2,3,4,5,6],
             #'Visitors':[43,53,34,45,64,34],
             #'Bounce_Rate':[65,72,62,64,54,66]}

#df = pd.DataFrame(web_stats)
#print(df.set_index('Day'))

#prices = pd.read_csv('ZILLOW-CO1749_ZHVISF.csv')
#prices.set_index('Date',inplace=True)
#prices.columns=['House Prices']
#print(prices.head())

#prices.to_html('example.html') converts to html


api_key =  'RK_AGhxhN3gXSut69X5A'

df = quandl.get("FMAC/HPI_MI", authtoken="RK_AGhxhN3gXSut69X5A")

print(df.head())