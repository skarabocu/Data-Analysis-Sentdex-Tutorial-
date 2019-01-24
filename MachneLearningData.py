import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
from statistics import mean
from sklearn import svm,preprocessing,model_selection

style.use('fivethirtyeight')
pd.set_option('display.max_columns', None)

def create_labels(cur_hpi, fut_hpi):
    if fut_hpi > cur_hpi:
        return 1
    else:
        return 0

def moving_average(values):
    return mean(values)

HPI_data = pd.read_pickle('pickles/Final_HPI.pickle')
HPI_data = HPI_data.pct_change()


HPI_data['USA_HPI_Future'] = HPI_data['USA'].shift(-1)#shifting data 1 down

HPI_data['LABEL']= list(map(create_labels,HPI_data['USA'],HPI_data['USA_HPI_Future']))#map function
HPI_data['ma_apply_example'] = HPI_data['M30'].rolling(10).apply(moving_average)#rolling function
HPI_data.replace([np.inf,-np.inf],np.nan,inplace=True)
HPI_data.dropna(inplace=True)
#!!!!!!!!!!!!!!!!!!!!!!
#MACHINE LEARNING STUFF
x = np.array(HPI_data.drop(['LABEL','USA_HPI_Future'],axis=1))#features .aka input
x = preprocessing.scale(x)#converts to data in a scale from -1 to 1
y = np.array(HPI_data['LABEL'])#labels or classifications .aka output

x_train, x_test, y_train, y_test = model_selection.train_test_split(x,y,test_size=0.2)# trains %80 of the data and compares it with %20
clf = svm.SVC(kernel='linear')
clf.fit(x_train,y_train)#training the data

print(clf.score(x_test,y_test))