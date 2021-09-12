import geopandas as gpd
import pandas as pd

df = gpd.read_file('UFs_QLs.shp')
df.plot(column = 'S36', cmap='coolwarm')



dff = pd.read_excel('data.xlsx')
dff = dff.set_index('UF')
dff = dff.applymap(lambda x: float(str(x).replace(',','.')))
df_2 = pd.concat([df,dff], axis=1)

df_2.plot(column = 'PR', cmap='coolwarm', legend='a')
