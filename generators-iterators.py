import pandas as pd
table = pd.DataFrame({'a':[1,2,3,4,5],'b':[6,7,8,9,10]})
print(table)
for i,row in table.iterrows():
    for k in row:
        print(i,k.index)