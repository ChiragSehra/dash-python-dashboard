l = ["0","24"]
import pandas as pd
import numpy as np  
df = pd.read_excel("main.xlsx",sheet_name="main")
print(df.shape)
print(np.arange(min(df['Average Speed']), max(df['Average Speed']), 0.1))

df = df[df['Average Speed'].isin(range(int(l[0]),int(l[1])))]

print(set(df['Average Speed']))