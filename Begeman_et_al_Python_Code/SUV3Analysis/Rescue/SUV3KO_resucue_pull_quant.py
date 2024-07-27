import pandas as pd
import os

csv_dir = 'csv_files/first_pass/'

out_df = pd.DataFrame(columns=['network type', 'total mito area', 'total RNA area', 'percent of mito area covered',
                               'avg rna int in mito', 'avg ha int in mito', 'number of rna obj', 'avg size of rna obj'])
for file in os.listdir(csv_dir):
    name = file.split('_')[0]
    df = pd.read_excel(csv_dir + file)
    wt_df = df[df['Tags'].str.contains('WT')].reset_index(drop=True)
    exp_df =df[df['Tags'].str.contains('Expressing')].reset_index(drop=True)
    if len(wt_df) > 0:
        mito_df = wt_df[wt_df['Tags'].str.contains(' Mito Network')].reset_index(drop=True)
        rna_df = wt_df[wt_df['Tags'].str.contains(' RNR2 Thresholded')].reset_index(drop=True)
        out_df.loc[len(out_df)] = ['WT', mito_df['Area (Mesh), Projection (XY/Z, filled holes) (µm²)'].sum(),
                                   rna_df['Area (Mesh), Projection (XY/Z, filled holes) (µm²)'].sum(),
                                   float(rna_df['Area (Mesh), Projection (XY/Z, filled holes) (µm²)'].sum() / mito_df['Area (Mesh), Projection (XY/Z, filled holes) (µm²)'].sum()),
                                   float(mito_df['Sum, Intensities #1'].sum() / mito_df['Area (Mesh), Projection (XY/Z, filled holes) (µm²)'].sum()),
                                   float(mito_df['Sum, Intensities #2'].sum() / mito_df['Area (Mesh), Projection (XY/Z, filled holes) (µm²)'].sum()),
                                   len(rna_df), rna_df['Area (Mesh), Projection (XY/Z, filled holes) (µm²)'].mean()]
        out_df.reset_index(drop=True, inplace=True)
    if len(exp_df) > 0:
        mito_df = exp_df[exp_df['Tags'].str.contains(' Mito Network')].reset_index(drop=True)
        rna_df = exp_df[exp_df['Tags'].str.contains(' RNR2 Thresholded')].reset_index(drop=True)
        out_df.loc[len(out_df)] = [str(name), mito_df['Area (Mesh), Projection (XY/Z, filled holes) (µm²)'].sum(),
                                   rna_df['Area (Mesh), Projection (XY/Z, filled holes) (µm²)'].sum(),
                                   float(rna_df['Area (Mesh), Projection (XY/Z, filled holes) (µm²)'].sum() / mito_df[
                                       'Area (Mesh), Projection (XY/Z, filled holes) (µm²)'].sum()),
                                   float(mito_df['Sum, Intensities #1'].sum() / mito_df[
                                       'Area (Mesh), Projection (XY/Z, filled holes) (µm²)'].sum()),
                                   float(mito_df['Sum, Intensities #2'].sum() / mito_df[
                                       'Area (Mesh), Projection (XY/Z, filled holes) (µm²)'].sum()),
                                   len(rna_df), rna_df['Area (Mesh), Projection (XY/Z, filled holes) (µm²)'].mean()]
        out_df.reset_index(drop=True, inplace=True)

grouping = out_df.groupby(out_df.columns[0])
final_df = pd.DataFrame()

for group, group_df in grouping:
    new_columns = {col: f"{group}_{col}" for col in group_df.columns if col != out_df.columns[0]}
    group_df_renamed = group_df.rename(columns=new_columns).drop(columns=[out_df.columns[0]])
    group_df_renamed = group_df_renamed.reset_index(drop=True)
    final_df = pd.concat([final_df, group_df_renamed], axis=1)

final_df.to_csv('SUV3_rescue_analysis_rep1_wt_only.csv')