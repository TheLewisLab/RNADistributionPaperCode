import pandas as pd
import os

csv_dir = 'csv_files/NTRKO_Chloro'

image_out_df = pd.DataFrame(columns=['image name',
                                     'Ctr total mito area', 'Ctr total mito c1 int', 'Ctr avg mito c1 int', 'Ctr total mito c2 int', 'Ctr avg mito c2 int'])
ctr_mito_out_df = pd.DataFrame(columns=['image name', 'segment name', 'segment area', 'segment side ratio', 'segment roundness',
                                        'total c1 int', 'avg c1 int', 'max c1 int',
                                        'total c2 int', 'avg c2 int', 'max c2 int'])

for file in os.listdir(csv_dir):
    ctr_df = pd.read_excel(csv_dir + '/' + file)

    image_out_df.loc[len(image_out_df)] = [str(file),
                                           ctr_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum(),
                                           ctr_df['Sum, Intensities #1'].sum(),
                                           float(ctr_df['Sum, Intensities #1'].sum() / ctr_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum()),
                                           ctr_df['Sum, Intensities #2'].sum(),
                                           float(ctr_df['Sum, Intensities #2'].sum() / ctr_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum()),
                                           ]
    image_out_df.reset_index(drop=True, inplace=True)

    for i in range(len(ctr_df)):
        ctr_mito_out_df.loc[len(ctr_mito_out_df)] = [str(file), ctr_df.at[i, 'Name'], ctr_df.at[i, 'Area (Mesh), Projection (XY/Z) (µm²)'],
                                                   ctr_df.at[i, 'Side Ratio, 2D Oriented Bounds'], ctr_df.at[i, 'Roundness (Mesh), Projection (XY/Z)'],
                                                   ctr_df.at[i, 'Sum, Intensities #1'], ctr_df.at[i, 'Mean, Intensities #1'],
                                                   ctr_df.at[i, 'Max, Intensities #1'], ctr_df.at[i, 'Sum, Intensities #2'],
                                                   ctr_df.at[i, 'Mean, Intensities #2'], ctr_df.at[i, 'Max, Intensities #2']]
        ctr_mito_out_df.reset_index(drop=True, inplace=True)

image_out_df.to_csv('NTRKO_Chloro_image_hpg_quant.csv')
ctr_mito_out_df.to_csv('NTRKO_Chloro_ctr_mito_quant.csv')
