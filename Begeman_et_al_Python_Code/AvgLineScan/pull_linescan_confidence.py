import pandas as pd
import os

data_dic = {'hpg_with_protein': ['GRSF1', 'MRPL23', 'PTPMT1', 'TFAM'],
            'mtRNA_GRSF1_dsDNA' : ['ND4', 'RNR2', 'tRNAs'],
            'mtRNA_HPG' : ['ND4', 'RNR2', 'tRNAs'],
            'mtRNA_MRPL23' : ['ND4', 'RNR2', 'tRNAs'],
            'mtRNA_TOM20' : ['ND4', 'RNR2', 'tRNAs'],
            'pulse_chase' : ['15minPulse', '30minPulse', '1hrPulse', '15minChase', '30minChase', '1hrChase']}

data_dic = {'example_linescans' : ['TFAM_DNA']}
#data_dic = {'EU_Data' : ['EU_GRSF1']}
#data_dic = {'mtRNA_GRSF1_dsDNA' : ['tRNAs']}
data_dic = {'example_linescans' : ['New_GRSF1_DNA']}
data_dic = {'hpg_with_protein' : ['DRP1']}

csv_dir = 'peak_csvs'

john_file_override = False

for experiment_dir, image_sets in data_dic.items():
    if experiment_dir not in os.listdir('confidence_data'):
        os.makedirs('confidence_data/' + experiment_dir)
    for channel in os.listdir(experiment_dir + '/' + csv_dir):
        if channel not in os.listdir('confidence_data/' + experiment_dir + '/'):
            os.makedirs('confidence_data/' + experiment_dir + '/' + channel)
        group_dic = {}
        for file in os.listdir(experiment_dir + '/' + csv_dir + '/' + channel):
            for image_set in image_sets:
                if image_set.upper() in file.upper() or john_file_override:
                    if image_set in group_dic.keys():
                        group_dic[image_set].append(file)
                    else:
                        group_dic[image_set] = [file]
                    break

        for group, files in group_dic.items():
            if group not in os.listdir('confidence_data/' + experiment_dir + '/' + channel + '/'):
                os.makedirs('confidence_data/' + experiment_dir + '/' + channel + '/' + group)
            image_n = 0
            c1_df = pd.DataFrame()
            c2_df = pd.DataFrame()
            c3_df = pd.DataFrame()
            for file in files:
                image_n += 1
                df = pd.read_csv(experiment_dir + '/' + csv_dir + '/' + channel + '/' + file)
                df = df.drop(columns=['Unnamed: 0'])
                c1_df = pd.concat([c1_df, df[[col for col in df.columns if 'Channel 1' in col]]], axis=1)
                c2_df = pd.concat([c2_df, df[[col for col in df.columns if 'Channel 2' in col]]], axis=1)
                c3_df = pd.concat([c3_df, df[[col for col in df.columns if 'Channel 3' in col]]], axis=1)
            c1_df.to_csv('confidence_data/' + experiment_dir + '/' + channel + '/' + group + '/Channel_1_all_data.csv')
            c2_df.to_csv('confidence_data/' + experiment_dir + '/' + channel + '/' + group + '/Channel_2_all_data.csv')
            c3_df.to_csv('confidence_data/' + experiment_dir + '/' + channel + '/' + group + '/Channel_3_all_data.csv')
            out_df = pd.DataFrame(columns=['Distance', 'Channel 1 Avg', 'Channel 1 Std', 'Channel 2 Avg', 'Channel 2 Std', 'Channel 3 Avg', 'Channel 3 Std'])
            def row_avg(row):
                return row.mean()
            def row_std(row):
                return row.std()
            out_df['Distance'] = df['Distance']
            out_df['Channel 1 Avg'] = c1_df.apply(row_avg, axis=1)
            out_df['Channel 1 Std'] = c1_df.apply(row_std, axis=1)
            out_df['Channel 2 Avg'] = c2_df.apply(row_avg, axis=1)
            out_df['Channel 2 Std'] = c2_df.apply(row_std, axis=1)
            out_df['Channel 3 Avg'] = c3_df.apply(row_avg, axis=1)
            out_df['Channel 3 Std'] = c3_df.apply(row_std, axis=1)
            out_df.to_csv('confidence_data/' + experiment_dir + '/' + channel + '/' + group + '/summary_data.csv')




