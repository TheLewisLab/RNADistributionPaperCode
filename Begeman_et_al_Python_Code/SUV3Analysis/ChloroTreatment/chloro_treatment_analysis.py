import pandas as pd
import os

dic = {}

for file in os.listdir('output_csvs/bio_rep_2'):
    group = file.split('_')[0]
    if group in dic.keys():
        dic[group].append(pd.read_excel('output_csvs/bio_rep_2/' + file))
    else:
        dic[group] = [pd.read_excel('output_csvs/bio_rep_2/' + file)]

out_df = pd.DataFrame(columns=['image set', 'total mito area', 'total rnr2 area', 'percent of mito area covered', 'avg size of rnr2', 'avg rnr2 intensity'])
for group, data in dic.items():
    for df in data:
        mito_df = df[df['Tags'].str.contains(', Mito Clean')].reset_index(drop=True)
        rna_df = df[df['Tags'].str.contains(', RNR2 Thresholded in Mito Clean')].reset_index(drop=True)
        out_df.loc[len(out_df)] = [str(group), mito_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum(), rna_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum(),
                                   float(rna_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum() / mito_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum()),
                                   rna_df['Area (Mesh), Projection (XY/Z) (µm²)'].mean(),
                                   float(mito_df['Sum, Intensities #1'].sum() / mito_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum())]
        out_df.reset_index(drop=True, inplace=True)

out_df.to_csv('bio_rep_2_analysis.csv')