import pandas as pd
import numpy as np
from scipy.stats import pearsonr

data = pd.read_csv('xxxx.csv')    #### input .csv file
data = data.rename(columns={'GPP.gross': 'GPP', 'ET.gross': 'ET', 'SWC_1_1_1': 'SWC'})
df = data[['GPP', 'ET', 'VPD', 'SWC']]

#### data control
df = df.replace(0, pd.NA)
df = df.dropna()

#### Grouping data based on the percentage of SWC
swc_percentiles = np.percentile(df['SWC'], np.linspace(0, 100, 11))
df['SWC_percentile'] = pd.cut(df['SWC'], bins=swc_percentiles, labels=False, include_lowest=True)

#### calulate coefficients between dryland fluxes and VPD/SM at each SM percentile
pearsonr_swctype = {}
for percent in range(10):
    subset = df[df['SWC_percentile'] == percent]
    pearsonr_swctype[percent] = {
        'SWC percentile': (percent+1)*10,
        'GPP_SWC': pearsonr(subset['GPP'], subset['SWC'])[0],
        'ET_SWC': pearsonr(subset['ET'], subset['SWC'])[0],
        'GPP_VPD': pearsonr(subset['GPP'], subset['VPD'])[0],
        'ET_VPD': pearsonr(subset['ET'], subset['VPD'])[0]
    }
pearsonr_results_swctype = pd.DataFrame(pearsonr_swctype)

print(pearsonr_results_swctype)