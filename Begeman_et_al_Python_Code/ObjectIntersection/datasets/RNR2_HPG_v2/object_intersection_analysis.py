import pandas as pd
import os
import sys
sys.path.insert(1, 'C:\\Users\\adamb\\PycharmProjects\\LewisLab\\RNADistributionPaper\\ObjectIntersection\\run_object_simulation')
import object_intersection_sim

file_path = 'csv_files'
dataset_name = os.getcwd().split('\\')[-1]

obj_out_df = pd.DataFrame(columns=['image name', 'sum of mito area', 'number of HPG', 'sum of HPG area', 'avg HPG area',
                                   'number of RNR2', 'sum of RNR2 area', 'avg of RNR2 area',
                                   'number of HPG in RNR2', 'percent of HPG in RNR2',
                                   'avg percent of simulated HPG in RNR2', 'std percent of simulated HPG in RNR2'])
int_corr_obj2_df = pd.DataFrame(columns=['image name', 'object name', 'avg int channel 1', 'avg int channel 2'])

files_done = 0
for file in os.listdir(file_path):
    files_done += 1.0
    print(files_done / len(os.listdir(file_path)))
    df = pd.read_excel(file_path + '/' + file)
    image_name = file

    mito_df = df[df['Tags'].str.contains(', Mito Clean')].reset_index(drop=True)
    obj1_df = df[df['Tags'].str.contains(', RNR2 Thresholded,')].reset_index(drop=True)
    obj2_df = df[df['Tags'].str.contains(', HPG Thresholded,')].reset_index(drop=True)

    mito_area_sum = mito_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum()
    obj1_number = len(obj1_df)
    obj1_area_sum = obj1_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum()
    obj1_area_avg = obj1_df['Area (Mesh), Projection (XY/Z) (µm²)'].mean()
    obj2_number = len(obj2_df)
    obj2_area_sum = obj2_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum()
    obj2_area_avg = obj2_df['Area (Mesh), Projection (XY/Z) (µm²)'].mean()

    obj2_in_obj1 = len(obj2_df[obj2_df['Tags'].str.contains(', HPG Thresholded in Mito Clean in RNR2 Thresholded in Mito Clean')].reset_index(drop=True))
    percent_obj2_in_obj1 = 100.0 * (obj2_in_obj1 / obj2_number)
    
    sim_results_1 = object_intersection_sim.simulation(obj1_number, obj1_area_avg, obj2_number, obj2_area_avg, mito_area_sum, 20.0, 100)

    obj_out_df.loc[len(obj_out_df)] = [image_name, mito_area_sum, obj1_number, obj1_area_sum, obj1_area_avg, obj2_number,
                                       obj2_area_sum, obj2_area_avg, obj2_in_obj1, percent_obj2_in_obj1, sim_results_1[0], sim_results_1[1]]
    obj_out_df.reset_index(drop=True, inplace=True)

    for i in range(len(obj2_df)):
        int_corr_obj2_df.loc[len(int_corr_obj2_df)] = [image_name, obj2_df.at[i, 'Name'],
                                                       obj2_df.at[i, 'Mean, Intensities #1'],
                                                       obj2_df.at[i, 'Mean, Intensities #2']]
        int_corr_obj2_df.reset_index(drop=True, inplace=True)

    obj_out_df.to_csv(dataset_name + '_Object_intersection_data.csv')
    int_corr_obj2_df.to_csv(dataset_name + '_Object2_intensity_correlation_data.csv')
