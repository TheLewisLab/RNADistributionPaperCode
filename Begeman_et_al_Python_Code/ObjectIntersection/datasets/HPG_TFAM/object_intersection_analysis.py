import pandas as pd
import os
import sys
sys.path.insert(1, 'C:\\Users\\adamb\\PycharmProjects\\LewisLab\\RNADistributionPaper\\ObjectIntersection\\run_object_simulation')
import object_intersection_sim

file_path = 'csv_files'
dataset_name = os.getcwd().split('\\')[-1]

obj_out_df = pd.DataFrame(columns=['image name', 'sum of mito area', 'number of HPG', 'sum of HPG area', 'avg HPG area',
                                   'number of TFAM', 'sum of TFAM area', 'avg of TFAM area', 'number of TFAM in HPG', 'percent of TFAM in HPG',
                                   'avg percent of simulated TFAM in HPG', 'std percent of simulated TFAM in HPG'])
int_corr_df = pd.DataFrame(columns=['image name', 'object name', 'avg int channel 1', 'avg int channel 2'])

for file in os.listdir(file_path):
    df = pd.read_excel(file_path + '/' + file)
    image_name = file

    mito_df = df[df['Tags'].str.contains(', Mito Clean,')].reset_index(drop=True)
    obj1_df = df[df['Tags'].str.contains(', HPG thresholded,')].reset_index(drop=True)
    obj2_df = df[df['Tags'].str.contains(', TFAM,')].reset_index(drop=True)

    mito_area_sum = mito_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum()
    obj1_number = len(obj1_df)
    obj1_area_sum = obj1_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum()
    obj1_area_avg = obj1_df['Area (Mesh), Projection (XY/Z) (µm²)'].mean()
    obj2_number = len(obj2_df)
    obj2_area_sum = obj2_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum()
    obj2_area_avg = obj2_df['Area (Mesh), Projection (XY/Z) (µm²)'].mean()
    obj2_in_obj1 = len(obj2_df[obj2_df['Tags'].str.contains(', TFAM in Mito Clean in HPG thresholded in Mito Clean')].reset_index(drop=True))
    percent_obj2_in_obj1 = 100.0 * (obj2_in_obj1 / obj2_number)

    sim_results = object_intersection_sim.simulation(obj1_number, obj1_area_avg, obj2_number, obj2_area_avg,mito_area_sum, 80.0, 100)

    obj_out_df.loc[len(obj_out_df)] = [image_name, mito_area_sum, obj1_number, obj1_area_sum, obj1_area_avg, obj2_number,
                                       obj2_area_sum, obj2_area_avg, obj2_in_obj1, percent_obj2_in_obj1, sim_results[0], sim_results[1]]
    obj_out_df.reset_index(drop=True, inplace=True)

    for i in range(len(obj2_df)):
        int_corr_df.loc[len(int_corr_df)] = [image_name, obj2_df.at[i, 'Name'], obj2_df.at[i, 'Mean, Intensities #1'], obj2_df.at[i, 'Mean, Intensities #2']]
        int_corr_df.reset_index(drop=True, inplace=True)

obj_out_df.to_csv(dataset_name + '_Object_intersection_data.csv')
int_corr_df.to_csv(dataset_name + '_Object_intensity_correlation_data.csv')
