import pandas as pd
import os
import numpy as np

dic = {}

for file in os.listdir('output_csvs/bio_rep_2'):
    group = file.split('_')[0]
    if group in dic.keys():
        dic[group].append(pd.read_excel('output_csvs/bio_rep_2/' + file))
    else:
        dic[group] = [pd.read_excel('output_csvs/bio_rep_2/' + file)]

mito_out_df = pd.DataFrame(columns=['image set', 'total area', 'percent of mito area covered', 'avg rnr2 intensity'])
rna_out_df = pd.DataFrame(columns=['image set', 'total area', 'avg rnr2 intensity'])
for group, data in dic.items():
    for df in data:
        mito_df = df[df['Tags'].str.contains(', Mito Clean')].reset_index(drop=True)
        rna_df = df[df['Tags'].str.contains(', RNR2 Thresholded in Mito Clean')].reset_index(drop=True)

        for i in range(len(mito_df)):
            if not pd.isna(mito_df.at[i, 'Children Ids']):
                rna_size = 0
                for c_id in mito_df.at[i, 'Children Ids'].split(', '):
                    rna_size += rna_df.at[rna_df.index[rna_df['Id'] == int(c_id)].tolist()[0], 'Area (Mesh), Projection (XY/Z) (µm²)']
            else:
                rna_size = 0
            mito_out_df.loc[len(mito_out_df)] = [str(group), mito_df.at[i, 'Area (Mesh), Projection (XY/Z) (µm²)'],
                                                 float(rna_size / mito_df.at[i, 'Area (Mesh), Projection (XY/Z) (µm²)']),
                                                 mito_df.at[i, 'Mean, Intensities #1']]
            mito_out_df.reset_index(drop=True, inplace=True)

        for i in range(len(rna_df)):
            rna_out_df.loc[len(rna_out_df)] = [str(group), rna_df.at[i, 'Area (Mesh), Projection (XY/Z) (µm²)'],
                                               rna_df.at[i, 'Mean, Intensities #1']]
            rna_out_df.reset_index(drop=True, inplace=True)


mito_out_df.to_csv('bio_rep_2_mito_only_analysis.csv')
rna_out_df.to_csv('bio_rep_2_rna_only_analysis.csv')