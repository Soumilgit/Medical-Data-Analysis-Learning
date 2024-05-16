import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

datf = pd.read_csv('medical_examination.csv')

datf['overweight'] = (datf['weight'] / (df['height'] / 100) ** 2 > 25).astype(int)


datf['cholesterol'] = (datf['cholesterol'] >= 1).astype(int)
datf['gluc'] = (datf['gluc'] >= 1).astype(int)


def drw_cat_plt():
    
    datf_cat = pd.melt(datf, id_vars=['cardio'],
                     value_vars=['cholesterol', 'smoke', 'alcohol', 'obese'])

    
    datf_cat = datf_cat.groupby(['cardio', 'variable',]).size().reset_index()
    datf_cat = datf_cat.rename(columns={0: 'total'})

    
    graph = sns.catplot(data=datf_cat, kind="bar", x="variable", y="total", hue="value", col="cardio")
    fig = graph.fig

    
    fig.savefig('catplot.png')
    return fig



def drw_ht_mp():
   
    datf_heat = datf[(datf['ap_lo'] <= df['ap_hi']) &
                 (datf['height'] >= df['height'].quantile(0.029)) &
                 (datf['height'] <= df['height'].quantile(0.963)) &
                 (datf['weight'] >= df['weight'].quantile(0.029)) &
                 (datf['weight'] <= df['weight'].quantile(0.963))
                 ]

    
    corr = datf_heat.corr()

    
    mask = np.triu(np.ones_like(corr, dtype=bool))

    
    fig, ax = plt.subplots(figsize=(25,18))

    
    sns.heatmap(corr, mask=mask, square=True, linewidths=1.3, annot=True)

    
    fig.savefig('heatmap.png')
    return fig
