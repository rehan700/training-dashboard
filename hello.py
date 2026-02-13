import pandas as pd
df=pd.read_csv('health.csv')
#print(df.head())
#print(df.describe())
#df.dropna(inplace=True)
df['Date'] = pd.to_datetime(df['Date'],format='mixed')
#print(df.to_string())
print(df.loc[[0,1]])