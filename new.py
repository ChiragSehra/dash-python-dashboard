l = ["0","24"]
import pandas as pd
import numpy as np  
df = pd.read_excel("main.xlsx",sheet_name="main")
print(df.shape)

windScale = df[df['Wind Scale'].isin([1,2,3,4,5])]
print(windScale.shape)
# print(windScale.tail())

seaScale = windScale[windScale['Sea'].isin([1,2,3,4,5,6,7,8,9,0])]
print(seaScale.shape)
print(seaScale.tail())

min_speed_value=0
max_speed_value=100
# print(np.around(np.arange(min_speed_value, max_speed_value, 0.1), decimals=1))
speedScale = seaScale[seaScale['Speedvalue'].isin(np.around(np.arange(min_speed_value, max_speed_value, 0.1), decimals=1))]
print(speedScale.shape)
print(speedScale.tail())