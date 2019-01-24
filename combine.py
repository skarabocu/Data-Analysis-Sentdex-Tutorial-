import pandas as pd


df1 = pd.DataFrame({'HPI':[80,85,88,85],
                    'Int_rate':[2, 3, 2, 2],
                    'US_GDP_Thousands':[50, 55, 65, 55]},
                   index = [2001, 2002, 2003, 2004])

df2 = pd.DataFrame({'HPI':[80,85,88,85],
                    'Int_rate':[2, 3, 2, 2],
                    'US_GDP_Thousands':[50, 55, 65, 55]},
                   index = [2005, 2006, 2007, 2008])

df3 = pd.DataFrame({'HPI':[80,85,88,85],
                    'Unemployment':[7, 8, 9, 6],
                    'Low_tier_HPI':[50, 52, 50, 53]},
                   index = [2001, 2002, 2003, 2004])

#concatination is adding to the bottom and not that effective
concat = pd.concat([df1,df3], sort=True)

s = pd.Series([80,2,50],index=['HPI','Int_rate','US_GDP_Thousands'])
#append
df4 = df1.append(s, ignore_index=True)

#merging !index doesn't matter
print(pd.merge(df1,df2,on=['HPI','Int_rate'],how='left'))

df1.set_index('HPI',inplace=True)
df3.set_index('HPI',inplace=True)

#joining !index matters
joined = df1.join(df3)#don't work that much since the indexes are repating itself
print(joined)