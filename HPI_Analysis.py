import quandl
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from matplotlib import style

style.use('fivethirtyeight')
pd.set_option('display.max_columns', None)

def state_list():
    fiddy_states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
    return fiddy_states[0][1][1:]

def grab_initial_state_data():
    states = state_list()
    main_df = pd.DataFrame()

    for abbv in states:

        df = quandl.get('FMAC/HPI_'+str(abbv),start_date='1994-01-31',authtoken="RK_AGhxhN3gXSut69X5A")
        df.columns=[str(abbv)]
        df[abbv] = (df[abbv]-df[abbv][0])/df[abbv][0] * 100.0#gets the percent change

        if main_df.empty:
            main_df = df

        else:
            main_df = main_df.join(df,on='Date',how='left')

    print(main_df.head())
    pickle_out = open('fiddy_states_pcn_change.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()

def HPI_Benchmark():
    df = quandl.get('FMAC/HPI_USA',authtoken="RK_AGhxhN3gXSut69X5A")
    df.columns = ['USA']
    df['USA'] = (df['USA']-df['USA'][0])/df['USA'][0]*100.0
    return df

def sp500_data():
    df = quandl.get('MULTPL/SP500_PE_RATIO_MONTH',start_date='1994-01-01',authtoken="RK_AGhxhN3gXSut69X5A")
    df['Value'] = (df['Value']-df['Value'][0])/df['Value'][0]*100.0
    df = df.resample('M').sum()
    df.columns=['sp500']
    return df

def mortgage_30year():
    mortage_df = quandl.get('FMAC/MORTG',start_date='1994-01-01',authtoken="RK_AGhxhN3gXSut69X5A")
    mortage_df['Value'] = (mortage_df['Value']-mortage_df['Value'][0])/mortage_df['Value'][0]*100.0
    mortage_df = mortage_df.resample('M').sum()
    mortage_df.columns=['M30']
    return mortage_df

def GDP_data():
    df = quandl.get('BCB/4385', start_date='1994-01-31',authtoken="RK_AGhxhN3gXSut69X5A")
    df.rename(columns={'Value':'GDP'}, inplace=True)
    df['GDP'] = (df['GDP'] - df['GDP'][0]) / df['GDP'][0] * 100.0
    df = df['GDP']

    return df

def unemployment_data():
    df = quandl.get('BCB/3787', authtoken="RK_AGhxhN3gXSut69X5A")
    df.rename(columns={'Value': 'Unemployment Rate'}, inplace=True)
    df['Unemployment Rate'] = (df['Unemployment Rate'] - df['Unemployment Rate'][0]) / df['Unemployment Rate'][0] * 100.0

    return df

#grab_initial_state_data()
mortages = mortgage_30year()
sp500 = sp500_data()
GDP = GDP_data()
unemployment = unemployment_data()
us_data = HPI_Benchmark()

pickle_in = open('pickles/fiddy_states_pcn_change.pickle','rb')
HPI_data = pickle.load(pickle_in)#GETTİNG THE HOUSING PRICE INDEX
state_HPI_M30 = HPI_data.join(mortages, on='Date')
Final_HPI = state_HPI_M30.join([us_data,GDP, unemployment,sp500])

print(Final_HPI.corr())
pickle_out = open('pickles/Final_HPI.pickle','wb')
pickle.dump(Final_HPI, pickle_out)#save it to pickle



#ARRANGE MATPLOTLIB FOR SHOWING THE DATA
fig = plt.figure()
ax1 = plt.subplot2grid((3,1),(0,0))#first paranthesis is the grid of the window and the second paranthesis is to where to place the graph
ax2 = plt.subplot2grid((3,1),(1,0),sharex=ax1)

#'''''''''''''''''''''''''''''''''''''
#RESAMPLING AND HANDLING NaN VALUES
#HPI_data['TX1yr'] = HPI_data['TX'].resample('A').mean()
#HPI_data.dropna(inplace=True)  drops the NaN values
#HPI_data.fillna(method='ffill',inplace=True)# ffill fills with previous data and bfill fills with future data for method parameter
                                                                                                                # OR use value = -9999
#''''''''''''''''''''''''''''''''''
#''''''''''''''
# #SHOWING CORROLATION

# HPI_data['12MA'] = HPI_data['TX'].rolling(12).mean()
# HPI_data['12STD'] = HPI_data['TX'].rolling(12).std()
#HPI_data['12CORR'] = HPI_data['CA'].rolling(12).corr(other=HPI_data['AK'])


# HPI_data['12CORR'] = HPI_data['CA'].corr(other=HPI_data['AK'])
# HPI_data[['CA','AK']].plot(ax = ax1)
# HPI_data['12CORR'].plot(ax=ax2)
# plt.show()
#HPI_State_Correlation = HPI_data.corr()
#print(HPI_State_Correlation.describe())#describes all data
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
