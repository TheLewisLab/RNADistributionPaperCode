import pandas as pd
import os

csv_dir = 'csv_files'

out_df = pd.DataFrame(columns=['image set', 'total mito area', 'total HPG intensity in mito', 'avg HPG intensity in mito',
                               'avg cell body HPG intensity', 'normalized avg HPG intensity'])

for file in os.listdir(csv_dir):
    df = pd.read_excel(csv_dir + '/' + file)
    mito_df = df[df['Tags'].str.contains('Mito Clean')].reset_index(drop=True)
    cell_df = df[df['Tags'].str.contains('Cell Bodies Clean')].reset_index(drop=True)

    mito_area_sum = mito_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum()
    hpg_int_sum = mito_df['Sum, Intensities #1'].sum()
    hpg_cell_int = float(cell_df['Sum, Intensities #1'].sum() / cell_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum())

    out_df.loc[len(out_df)] = [str(file), mito_area_sum, hpg_int_sum, float(hpg_int_sum / mito_area_sum),
                               hpg_cell_int, (float(hpg_int_sum / mito_area_sum) - hpg_cell_int)]
    out_df.reset_index(drop=True, inplace=True)

out_df.to_csv('CAP_Control_values.csv')