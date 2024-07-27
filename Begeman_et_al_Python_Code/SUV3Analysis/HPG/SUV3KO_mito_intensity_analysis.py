import pandas as pd
import os

csv_dir = 'csv_files/SUV3KO_Chloro'

image_out_df = pd.DataFrame(columns=['image name',
                                     'KO total mito area', 'KO total mito c1 int', 'KO avg mito c1 int', 'KO total mito c2 int', 'KO avg mito c2 int',
                                     'Ctr total mito area', 'Ctr total mito c1 int', 'Ctr avg mito c1 int', 'Ctr total mito c2 int', 'Ctr avg mito c2 int'])
ko_mito_out_df = pd.DataFrame(columns=['image name', 'segment name', 'segment area', 'segment side ratio', 'segment roundness',
                                        'total c1 int', 'avg c1 int', 'max c1 int',
                                        'total c2 int', 'avg c2 int', 'max c2 int'])
ctr_mito_out_df = pd.DataFrame(columns=['image name', 'segment name', 'segment area', 'segment side ratio', 'segment roundness',
                                        'total c1 int', 'avg c1 int', 'max c1 int',
                                        'total c2 int', 'avg c2 int', 'max c2 int'])

for file in os.listdir(csv_dir):
    df = pd.read_excel(csv_dir + '/' + file)
    ko_df = df[df['Tags'].str.contains('KO Mitos')].reset_index(drop=True)
    ctr_df = df[df['Tags'].str.contains('Control Mitos')].reset_index(drop=True)

    image_out_df.loc[len(image_out_df)] = [str(file), ko_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum(), ko_df['Sum, Intensities #1'].sum(),
                                           float(ko_df['Sum, Intensities #1'].sum() / ko_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum()),
                                           ko_df['Sum, Intensities #2'].sum(),
                                           float(ko_df['Sum, Intensities #2'].sum() / ko_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum()),
                                           ctr_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum(),
                                           ctr_df['Sum, Intensities #1'].sum(),
                                           float(ctr_df['Sum, Intensities #1'].sum() / ctr_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum()),
                                           ctr_df['Sum, Intensities #2'].sum(),
                                           float(ctr_df['Sum, Intensities #2'].sum() / ctr_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum()),
                                           ]
    image_out_df.reset_index(drop=True, inplace=True)

    for i in range(len(ko_df)):
        ko_mito_out_df.loc[len(ko_mito_out_df)] = [str(file), ko_df.at[i, 'Name'], ko_df.at[i, 'Area (Mesh), Projection (XY/Z) (µm²)'],
                                                   ko_df.at[i, 'Side Ratio, 2D Oriented Bounds'], ko_df.at[i, 'Roundness (Mesh), Projection (XY/Z)'],
                                                   ko_df.at[i, 'Sum, Intensities #1'], ko_df.at[i, 'Mean, Intensities #1'],
                                                   ko_df.at[i, 'Max, Intensities #1'], ko_df.at[i, 'Sum, Intensities #2'],
                                                   ko_df.at[i, 'Mean, Intensities #2'], ko_df.at[i, 'Max, Intensities #2']]
        ko_mito_out_df.reset_index(drop=True, inplace=True)

    for i in range(len(ctr_df)):
        ctr_mito_out_df.loc[len(ctr_mito_out_df)] = [str(file), ctr_df.at[i, 'Name'], ctr_df.at[i, 'Area (Mesh), Projection (XY/Z) (µm²)'],
                                                   ctr_df.at[i, 'Side Ratio, 2D Oriented Bounds'], ctr_df.at[i, 'Roundness (Mesh), Projection (XY/Z)'],
                                                   ctr_df.at[i, 'Sum, Intensities #1'], ctr_df.at[i, 'Mean, Intensities #1'],
                                                   ctr_df.at[i, 'Max, Intensities #1'], ctr_df.at[i, 'Sum, Intensities #2'],
                                                   ctr_df.at[i, 'Mean, Intensities #2'], ctr_df.at[i, 'Max, Intensities #2']]
        ctr_mito_out_df.reset_index(drop=True, inplace=True)

image_out_df.to_csv('SUV3KO_Chloro_image_hpg_quant.csv')
ko_mito_out_df.to_csv('SUV3KO_Chloro_KO_mito_quant.csv')
ctr_mito_out_df.to_csv('SUV3KO_Chloro_ctr_mito_quant.csv')
