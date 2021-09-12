import pandas as pd
import numpy as np

df = pd.read_excel('dados1.xlsx', sheet_name = 'Brasil 2002')

df.index = df[['COD MUN', 'Municípios/ 26 Categorias']]
df = df.iloc[:,3:]
regions = [ 'IND MECANICA - Indústria mecânica',
           'ALIM E BEB - Indústria de produtos alimentícios, bebidas e álcool etílico',
            'ADM PUBLICA - Administraçao pública direta e autárquica']

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

# %%                  Coeficiente de Localização

cl = pd.DataFrame()

for i in regional_share.columns:
    cl[i] = np.abs(regional_share[i] - regions_total)
    
cl = cl.sum(axis=0)/2

# %%                  Coeficiente de Associação Geográfica

cga = pd.DataFrame()

for i in regional_share.columns:
    for j in regional_share.columns:
        cga[i + '//' + j] = np.abs(regional_share[i] - regional_share[j])

cga = cga.sum(axis=0)/2
cga = cga.reset_index()
first = list(map(lambda x: x.split('//')[0], cga['index']))
second = list(map(lambda x: x.split('//')[1], cga['index']))

cga['first'] = first
cga['second'] = second
# %%                   Curvas de Localização
ordered_shares = pd.DataFrame()
for i in regional_share.columns:
    ordered_shares[i] = regional_share[i].sort_values(ascending=False).values

ordered_shares = ordered_shares.iloc[1:,:]

accumulated_shares = ordered_shares.cumsum()
# %%
'''
            Respostas das atividades

'''

# %%  

'''

        Quociente Locacional para as três regiões onde o setor é relatviamente
        mais concentrado
 

'''

for i in regions:
    print(quo_loc_reg[i].sort_values(ascending=False).head())
# %% 
'''
        Coeficiente de Localização (valores)

'''
print(cl[regions])
 
# %% 
'''
        Coeficiente Associação Geográfica (valores)

'''
coef_ass = cga[cga['first'].isin(regions)]
for i in regions:
    ranked_coef = coef_ass[coef_ass['first'] == i].sort_values(0, ascending=False)
    print('\n')
    print(i)
    
    print(ranked_coef.head()[[0, 'second']])
    

# %%
'''
        Curvas de Localização (identificar posição relativa dos setores)

'''
sorted_curves = pd.DataFrame(accumulated_shares.mean().\
                             sort_values(ascending=False).dropna()).reset_index()
    
sorted_curves.index = sorted_curves.index +1
    
curves_ranks = sorted_curves[sorted_curves['index'].isin(regions)]



