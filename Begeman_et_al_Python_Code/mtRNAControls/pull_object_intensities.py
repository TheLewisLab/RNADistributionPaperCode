import pandas as pd
import os

treatment = 'RNaseA'
image_set = 'tRNAs'

dir_path = 'csv_files/' + treatment + '/' + image_set + '/'

out_df = pd.DataFrame(columns=['image name', 'total mito area',
                               'total channel 1 int', 'total channel 2 int', 'total channel 3 int', 'total mtDNA',
                               'avg channel 1 int', 'avg channel 2 int', 'avg channel 3 int', 'norm mtDNA'])

for file in os.listdir(dir_path):
    image_name = file.split('.')[0]
    df = pd.read_excel(dir_path + file)
    mito_df = df[df['Tags'].str.contains(', Mito Clean')].reset_index(drop=True)

    total_mito_area = mito_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum()
    c1_int = mito_df['Sum, Intensities #1'].sum()
    c2_int = mito_df['Sum, Intensities #2'].sum()
    c3_int = mito_df['Sum, Intensities #3'].sum()
    mtDNA = mito_df['mtDNA in Mito Clean Count'].sum()

    out_df.loc[len(out_df)] = [image_name, total_mito_area, c1_int, c2_int, c3_int, mtDNA,
                               float(c1_int / total_mito_area), float(c2_int / total_mito_area), float(c2_int / total_mito_area),
                               float(mtDNA / total_mito_area)]
    out_df.reset_index(drop=True, inplace=True)

out_df.to_csv(treatment + '_' + image_set + '_MitoData.csv')