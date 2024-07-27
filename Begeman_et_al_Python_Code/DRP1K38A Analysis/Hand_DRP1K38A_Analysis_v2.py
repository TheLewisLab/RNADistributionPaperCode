import os
import pandas as pd

csv_dir = 'hand_csvs_v2'

# 803 pixels per square micron

out_df = pd.DataFrame(columns=['image name', 'DRP1K38A total mito area',
                               'DRP1K38A total mito intensity c1', 'DRP1K38A avg mito intensity c1',
                               'DRP1K38A total mito intensity c2', 'DRP1K38A avg mito intensity c2',
                               'DRP1K38A total mito intensity c3', 'DRP1K38A avg mito intensity c3',
                               'DRP1K38A RNR2 objects', 'DRP1K38A total RNR2 area', 'DRP1K38A avg RNR2 area',
                               'DRP1K38A RNR2 object avg intensity c1', 'DRP1K38A RNR2 object avg intensity c3',
                               'DRP1K38A HPG objects', 'DRP1K38A total HPG area', 'DRP1K38A avg HPG area',
                               'DRP1K38A HPG object avg intensity c1', 'DRP1K38A HPG object avg intensity c3',
                               'DRP1K38A RNA and HPG overlap', 'DRP1K38A percent of RNR2 overlap', 'DRP1K38A percent of HPG overlap',
                               'control total mito area',
                               'Control total mito intensity c1', 'Control avg mito intensity c1',
                               'Control total mito intensity c2', 'Control avg mito intensity c2',
                               'Control total mito intensity c3', 'Control avg mito intensity c3',
                               'Control RNR2 objects', 'Control total RNR2 area', 'Control avg RNR2 area',
                               'Control RNR2 object avg intensity c1', 'Control RNR2 object avg intensity c3',
                               'Control HPG objects', 'Control total HPG area', 'Control avg HPG area',
                               'Control HPG object avg intensity c1', 'Control HPG object avg intensity c3',
                               'Control RNA and HPG overlap', 'Control percent of RNR2 overlap', 'Control percent of HPG overlap'])

for file in os.listdir(csv_dir):
    df = pd.read_excel(csv_dir + '/' + file)
    drp1_df = df[df['Tags'].str.contains('DRP1K38A Cells, ')].reset_index(drop=True)
    ctr_df = df[df['Tags'].str.contains('Control Cells, ')].reset_index(drop=True)

    drp1_mito_df = drp1_df[drp1_df['Tags'].str.contains(', DRP1K38A Mitos')].reset_index(drop=True)
    ctr_mito_df = ctr_df[ctr_df['Tags'].str.contains(', Control Mitos')].reset_index(drop=True)

    drp1_rna_df = drp1_df[drp1_df['Tags'].str.contains(', RNR2 Objects,')].reset_index(drop=True)
    ctr_rna_df = ctr_df[ctr_df['Tags'].str.contains(', RNR2 Objects,')].reset_index(drop=True)

    drp1_hpg_df = drp1_df[drp1_df['Tags'].str.contains(', HPG Objects,')].reset_index(drop=True)
    ctr_hpg_df = ctr_df[ctr_df['Tags'].str.contains(', HPG Objects,')].reset_index(drop=True)

    out_df.loc[len(out_df)] = [str(file.split('.')[0]), drp1_mito_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum(),
                               drp1_mito_df['Sum, Intensities #1'].sum(), (drp1_mito_df['Sum, Intensities #1'].sum() / (drp1_mito_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum() if len(drp1_mito_df) != 0 else 1)),
                               drp1_mito_df['Sum, Intensities #2'].sum(), (drp1_mito_df['Sum, Intensities #2'].sum() / (drp1_mito_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum() if len(drp1_mito_df) != 0 else 1)),
                               drp1_mito_df['Sum, Intensities #3'].sum(), (drp1_mito_df['Sum, Intensities #3'].sum() / (drp1_mito_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum() if len(drp1_mito_df) != 0 else 1)),
                               len(drp1_rna_df), drp1_rna_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum(), drp1_rna_df['Area (Mesh), Projection (XY/Z) (µm²)'].mean(),
                               drp1_rna_df['Mean, Intensities #1'].mean(), drp1_rna_df['Mean, Intensities #3'].mean(),
                               len(drp1_hpg_df), drp1_hpg_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum(), drp1_hpg_df['Area (Mesh), Projection (XY/Z) (µm²)'].mean(),
                               drp1_hpg_df['Mean, Intensities #1'].mean(), drp1_hpg_df['Mean, Intensities #3'].mean(),
                               len(drp1_rna_df[drp1_rna_df['Tags'].str.contains(', RNR2 Objects with HPG Objects')]),
                               len(drp1_rna_df[drp1_rna_df['Tags'].str.contains(', RNR2 Objects with HPG Objects')]) / (len(drp1_rna_df) if len(drp1_rna_df) != 0 else 1),
                               len(drp1_rna_df[drp1_rna_df['Tags'].str.contains(', RNR2 Objects with HPG Objects')]) / (len(drp1_hpg_df) if len(drp1_hpg_df) != 0 else 1),
                               ctr_mito_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum(),
                               ctr_mito_df['Sum, Intensities #1'].sum(), (ctr_mito_df['Sum, Intensities #1'].sum() / (ctr_mito_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum() if len(ctr_mito_df) != 0 else 1)),
                               ctr_mito_df['Sum, Intensities #2'].sum(), (ctr_mito_df['Sum, Intensities #2'].sum() / (ctr_mito_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum() if len(ctr_mito_df) != 0 else 1)),
                               ctr_mito_df['Sum, Intensities #3'].sum(), (ctr_mito_df['Sum, Intensities #3'].sum() / (ctr_mito_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum() if len(ctr_mito_df) != 0 else 1)),
                               len(ctr_rna_df), ctr_rna_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum(),
                               ctr_rna_df['Area (Mesh), Projection (XY/Z) (µm²)'].mean(),
                               ctr_rna_df['Mean, Intensities #1'].mean(), ctr_rna_df['Mean, Intensities #3'].mean(),
                               len(ctr_hpg_df), ctr_hpg_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum(),
                               ctr_hpg_df['Area (Mesh), Projection (XY/Z) (µm²)'].mean(),
                               ctr_hpg_df['Mean, Intensities #1'].mean(), ctr_hpg_df['Mean, Intensities #3'].mean(),
                               len(ctr_rna_df[ctr_rna_df['Tags'].str.contains(', RNR2 Objects with HPG Objects')]),
                               len(ctr_rna_df[ctr_rna_df['Tags'].str.contains(', RNR2 Objects with HPG Objects')]) / (len(ctr_rna_df) if len(ctr_rna_df) != 0 else 1),
                               len(ctr_rna_df[ctr_rna_df['Tags'].str.contains(', RNR2 Objects with HPG Objects')]) / (len(ctr_hpg_df) if len(ctr_hpg_df) != 0 else 1)
                               ]

    out_df.reset_index(drop=True, inplace=True)

out_df.to_csv('hand_agg_analysis_v2.csv')

