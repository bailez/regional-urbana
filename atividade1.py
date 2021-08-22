import pandas as pd
import numpy as np

df = pd.read_excel('dados1.xlsx', sheet_name = 'Brasil 2002')

df.index = df[['COD MUN', 'Municípios/ 26 Categorias']]
df = df.iloc[:,3:]
# %%                 Quociente Locacional

'''

R_i = produção do setor i em uma região
R = produção total em uma região
N_i = produção do setor i no país
N = produção total no país


Quociente Locacional do steor i na região:
    
    R_i / N_i             R_i / R
  _____________ ;  ou ____________
      R / N              N_i / N
      
'''

N = df.iloc[-1,:]

R = df.iloc[:,-1]


regional_share = df.divide(N, axis=1)

regions_total = regional_share.iloc[:,-1]

quo_loc_reg = regional_share.divide(regions_total, axis=0)



sectoral_share = df.divide(R, axis=0)

sectors_total = sectoral_share.iloc[-1,:]

quo_loc_sec = sectoral_share.divide(sectors_total, axis=1)

# %%                  Coeficiente de Associação Geográfica

cl_reg = pd.DataFrame()

for i in regional_share.columns:
    cl_reg[i] = np.abs(regional_share[i] - regions_total)
    
cl_reg = cl_reg.sum(axis=0)/2

cl_sec = pd.DataFrame()

for i in sectoral_share.columns:
    cl_sec[i] = np.abs(sectoral_share[i] - sectors_total)
    
cl_sec = cl_sec.sum(axis=0)/2

# %%                   Curvas de Localização
ordered_shares = pd.DataFrame()
for i in regional_share.columns:
    ordered_shares[i] = regional_share[i].sort_values(ascending=False).values

ordered_shares = ordered_shares.iloc[1:,:]

accumulated_shares = dered_shares.cumsum()
