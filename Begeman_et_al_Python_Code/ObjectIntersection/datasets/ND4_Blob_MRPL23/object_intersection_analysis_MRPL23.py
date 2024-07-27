import pandas as pd
import os
import sys
sys.path.insert(1, 'C:\\Users\\adamb\\PycharmProjects\\LewisLab\\RNADistributionPaper\\ObjectIntersection\\run_object_simulation')
import object_intersection_sim

#20% overlap

file_path = 'csv_files'
dataset_name = os.getcwd().split('\\')[-1]

obj_out_df = pd.DataFrame(columns=['image name', 'sum of mito area', 'number of MRPL23', 'sum of MRPL23 area', 'avg MRPL23 area',
                                   'number of ND4', 'sum of ND4 area', 'avg of ND4 area',
                                   'number of MRPL23 with ND4', 'percent of MRPL23 with ND4',
                                   'avg percent of simulated MRPL23 with ND4', 'std percent of simulated MRPL23 with ND4'
                                   ])
int_corr_obj1_df = pd.DataFrame(columns=['image name', 'object name', 'avg int channel 1', 'avg int channel 2', 'avg int channel 3'])
int_corr_obj2_df = pd.DataFrame(columns=['image name', 'object name', 'avg int channel 1', 'avg int channel 2', 'avg int channel 3'])

files_done = 0
for file in os.listdir(file_path):
    files_done += 1.0
    print(files_done / len(os.listdir(file_path)))
    df = pd.read_excel(file_path + '/' + file)
    image_name = file

    mito_df = df[df['Tags'].str.contains(', Mito Clean')].reset_index(drop=True)
    obj1_df = df[df['Tags'].str.contains(', MRPL23,')].reset_index(drop=True)
    obj2_df = df[df['Tags'].str.contains(', ND4 Blob Finder,')].reset_index(drop=True)

    mito_area_sum = mito_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum()
    obj1_number = len(obj1_df)
    obj1_area_sum = obj1_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum()
    obj1_area_avg = obj1_df['Area (Mesh), Projection (XY/Z) (µm²)'].mean()
    obj2_number = len(obj2_df)
    obj2_area_sum = obj2_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum()
    obj2_area_avg = obj2_df['Area (Mesh), Projection (XY/Z) (µm²)'].mean()
    obj1_in_obj2 = len(obj1_df[obj1_df['Tags'].str.contains(', MRPL23 in Mito Clean in ND4 Blob Finder in Mito Clean')].reset_index(drop=True))
    percent_obj1_in_obj2 = 100.0 * (obj1_in_obj2 / obj1_number)

    sim_results_1 = object_intersection_sim.simulation(obj1_number, obj1_area_avg, obj2_number, obj2_area_avg, mito_area_sum, 20.0, 100)

    obj_out_df.loc[len(obj_out_df)] = [image_name, mito_area_sum, obj1_number, obj1_area_sum, obj1_area_avg,
                                       obj2_number, obj2_area_sum, obj2_area_avg,
                                       obj1_in_obj2, percent_obj1_in_obj2, sim_results_1[0], sim_results_1[1]
                                       ]
    obj_out_df.reset_index(drop=True, inplace=True)

    for i in range(len(obj1_df)):
        int_corr_obj1_df.loc[len(int_corr_obj1_df)] = [image_name, obj1_df.at[i, 'Name'],
                                                       obj1_df.at[i, 'Mean, Intensities #1'],
                                                       obj1_df.at[i, 'Mean, Intensities #2'],
                                                       obj1_df.at[i, 'Mean, Intensities #3']]
        int_corr_obj1_df.reset_index(drop=True, inplace=True)
    for i in range(len(obj2_df)):
        int_corr_obj2_df.loc[len(int_corr_obj2_df)] = [image_name, obj2_df.at[i, 'Name'],
                                                       obj2_df.at[i, 'Mean, Intensities #1'],
                                                       obj2_df.at[i, 'Mean, Intensities #2'],
                                                       obj2_df.at[i, 'Mean, Intensities #3']]
        int_corr_obj2_df.reset_index(drop=True, inplace=True)

    obj_out_df.to_csv(dataset_name + 'MRPL23_Object_intersection_data.csv')
    int_corr_obj1_df.to_csv(dataset_name + 'MRPL23_Object1_intensity_correlation_data.csv')
    int_corr_obj2_df.to_csv(dataset_name + 'MRPL23_Object2_intensity_correlation_data.csv')
