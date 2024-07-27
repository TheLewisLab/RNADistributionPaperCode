import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram, leaves_list
import os

experiment_dir = 'EU_data'
image_sets = ['eu']

if 'clustered_csvs' not in os.listdir(experiment_dir):
    os.makedirs(experiment_dir + '/clustered_csvs')

for channel in os.listdir(experiment_dir + '/peak_csvs/'):
    if channel not in os.listdir(experiment_dir + '/clustered_csvs/'):
        os.makedirs(experiment_dir + '/clustered_csvs/' + channel)
    group_dic = {}
    for file in os.listdir(experiment_dir + '/peak_csvs/' + channel + '/'):
        for image_set in image_sets:
            if image_set in file:
                if image_set in group_dic.keys():
                    group_dic[image_set].append(file)
                else:
                    group_dic[image_set] = [file]
                break
    for group, files in group_dic.items():
        c1_df = pd.DataFrame()
        c2_df = pd.DataFrame()
        c3_df = pd.DataFrame()
        for file in files:
            temp_df = pd.read_csv(experiment_dir + '/peak_csvs/' + channel + '/' + file)
            temp_df = temp_df.drop(columns=['Unnamed: 0'])
            c1_df = pd.concat([c1_df, temp_df[[col for col in temp_df.columns if 'Channel 1' in col]]], axis=1)
            c2_df = pd.concat([c2_df, temp_df[[col for col in temp_df.columns if 'Channel 2' in col]]], axis=1)
            c3_df = pd.concat([c3_df, temp_df[[col for col in temp_df.columns if 'Channel 3' in col]]], axis=1)
        Z = linkage(c1_df.T, method='average')
        column_order = leaves_list(Z)
        temp_c1_df = c1_df.iloc[:, column_order]
        temp_c2_df = c2_df.iloc[:, column_order]
        temp_c3_df = c3_df.iloc[:, column_order]
        temp_c1_df.to_csv(experiment_dir + '/clustered_csvs/' + channel + '/' + group + '_c1_clustered_c1.csv')
        temp_c2_df.to_csv(experiment_dir + '/clustered_csvs/' + channel + '/' + group + '_c1_clustered_c2.csv')
        temp_c3_df.to_csv(experiment_dir + '/clustered_csvs/' + channel + '/' + group + '_c1_clustered_c3.csv')
        Z = linkage(c2_df.T, method='average')
        column_order = leaves_list(Z)
        temp_c1_df = c1_df.iloc[:, column_order]
        temp_c2_df = c2_df.iloc[:, column_order]
        temp_c3_df = c3_df.iloc[:, column_order]
        temp_c1_df.to_csv(experiment_dir + '/clustered_csvs/' + channel + '/' + group + '_c2_clustered_c1.csv')
        temp_c2_df.to_csv(experiment_dir + '/clustered_csvs/' + channel + '/' + group + '_c2_clustered_c2.csv')
        temp_c3_df.to_csv(experiment_dir + '/clustered_csvs/' + channel + '/' + group + '_c2_clustered_c3.csv')
        Z = linkage(c3_df.T, method='average')
        column_order = leaves_list(Z)
        temp_c1_df = c1_df.iloc[:, column_order]
        temp_c2_df = c2_df.iloc[:, column_order]
        temp_c3_df = c3_df.iloc[:, column_order]
        temp_c1_df.to_csv(experiment_dir + '/clustered_csvs/' + channel + '/' + group + '_c3_clustered_c1.csv')
        temp_c2_df.to_csv(experiment_dir + '/clustered_csvs/' + channel + '/' + group + '_c3_clustered_c2.csv')
        temp_c3_df.to_csv(experiment_dir + '/clustered_csvs/' + channel + '/' + group + '_c3_clustered_c3.csv')
