import pandas as pd
import os

csv_dir = 'csv_files/new_csv_files'

for file in os.listdir(csv_dir):
    df = pd.read_csv(csv_dir + '/' + file)
    offset_value = round(len(df.columns) / 1000)
    if offset_value <= 1:
        df.to_csv(file + '_sampled.csv')
    new_df = df.iloc[:, ::offset_value]
    new_df.to_csv(file + '_sampled.csv')