import pandas as pd
import os

dic = {}

for file in os.listdir('output_csvs/network_level'):
    group = file.split('_')[0]
    if group in dic.keys():
        dic[group].append(pd.read_excel('output_csvs/network_level/' + file))
    else:
        dic[group] = [pd.read_excel('output_csvs/network_level/' + file)]

out_df = pd.DataFrame(columns=['image set', 'total mito area', 'total rnr2 area', 'percent of mito area covered',
                               'number of rnr2 obj', 'avg size of rnr2 obj', 'avg rnr2 intensity in mito'])
for group, data in dic.items():
    for df in data:
        network_df = df[df['Tags'].str.contains(', Mito Network')].reset_index(drop=True)
        mito_df = df[df['Tags'].str.contains(', Network Mitos in Mito Network')].reset_index(drop=True)
        rna_df = df[df['Tags'].str.contains(', RNR2 Thresholded in Network Mitos in Mito Network')].reset_index(drop=True)
        for i in range(len(network_df)):
            network_id = network_df.at[i, 'Id']
            net_mito_df = mito_df[mito_df['Parent Ids'] == network_id].reset_index(drop=True)
            net_rna_df = pd.DataFrame(columns=rna_df.columns)
            for j in range(len(net_mito_df)):
                if not pd.isna(net_mito_df.at[j, 'Children Ids']):
                    for c_id in net_mito_df.at[j, 'Children Ids'].split(', '):
                        net_rna_df = net_rna_df.append(rna_df.loc[rna_df.index[rna_df['Id'] == int(c_id)].tolist()[0]], ignore_index=True)
                        net_rna_df.reset_index(drop=True, inplace=True)

            out_df.loc[len(out_df)] = [str(group), net_mito_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum(),
                                       net_rna_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum(),
                                       float(net_rna_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum() / net_mito_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum()),
                                       len(net_rna_df), net_rna_df['Area (Mesh), Projection (XY/Z) (µm²)'].mean(),
                                       float(net_mito_df['Sum, Intensities #1'].sum() / net_mito_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum())]
            out_df.reset_index(drop=True, inplace=True)

grouping = out_df.groupby(out_df.columns[0])
final_df = pd.DataFrame()

for group, group_df in grouping:
    new_columns = {col: f"{group}_{col}" for col in group_df.columns if col != out_df.columns[0]}
    group_df_renamed = group_df.rename(columns=new_columns).drop(columns=[out_df.columns[0]])
    group_df_renamed = group_df_renamed.reset_index(drop=True)
    final_df = pd.concat([final_df, group_df_renamed], axis=1)

final_df.to_csv('network_level_bio2_analysis.csv')

