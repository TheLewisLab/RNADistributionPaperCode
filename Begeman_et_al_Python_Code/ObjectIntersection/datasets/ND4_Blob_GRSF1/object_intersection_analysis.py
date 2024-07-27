import pandas as pd
import os
import sys
sys.path.insert(1, 'C:\\Users\\adamb\\PycharmProjects\\LewisLab\\RNADistributionPaper\\ObjectIntersection\\run_object_simulation')
import object_intersection_sim

#20% overlap

file_path = 'csv_files'
dataset_name = os.getcwd().split('\\')[-1]

obj_out_df = pd.DataFrame(columns=['image name', 'sum of mito area', 'number of ND4', 'sum of ND4 area', 'avg ND4 area',
                                   'number of GRSF1', 'sum of GRSF1 area', 'avg of GRSF1 area',
                                   'number of DNA', 'sum of DNA area', 'avg DNA area',
                                   'number of ND4 in GRSF1', 'percent of ND4 in GRSF1',
                                   'avg percent of simulated ND4 in GRSF1', 'std percent of simulated ND4 in GRSF1',
                                   'number of ND4 in DNA', 'percent of ND4 in DNA',
                                   'avg percent of simulated ND4 in DNA', 'std percent of simulated ND4 in DNA',
                                   'number of DNA in GRSF1', 'percent of DNA in GRSF1',
                                   'avg percent of simulated DNA in GRSF1', 'std percent of simulated DNA in GRSF1'
                                   ])
int_corr_obj1_df = pd.DataFrame(columns=['image name', 'object name', 'avg int channel 1', 'avg int channel 2', 'avg int channel 3'])
int_corr_obj2_df = pd.DataFrame(columns=['image name', 'object name', 'avg int channel 1', 'avg int channel 2', 'avg int channel 3'])
int_corr_obj3_df = pd.DataFrame(columns=['image name', 'object name', 'avg int channel 1', 'avg int channel 2', 'avg int channel 3'])

files_done = 0
for file in os.listdir(file_path):
    files_done += 1.0
    print(files_done / len(file_path))
    df = pd.read_excel(file_path + '/' + file)
    image_name = file

    mito_df = df[df['Tags'].str.contains(', Mito Clean')].reset_index(drop=True)
    obj1_df = df[df['Tags'].str.contains(', ND4 Blob Finder,')].reset_index(drop=True)
    obj2_df = df[df['Tags'].str.contains(', GRSF1,')].reset_index(drop=True)
    obj3_df = df[df['Tags'].str.contains(', DNA,')].reset_index(drop=True)

    mito_area_sum = mito_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum()
    obj1_number = len(obj1_df)
    obj1_area_sum = obj1_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum()
    obj1_area_avg = obj1_df['Area (Mesh), Projection (XY/Z) (µm²)'].mean()
    obj2_number = len(obj2_df)
    obj2_area_sum = obj2_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum()
    obj2_area_avg = obj2_df['Area (Mesh), Projection (XY/Z) (µm²)'].mean()
    obj3_number = len(obj3_df)
    obj3_area_sum = obj3_df['Area (Mesh), Projection (XY/Z) (µm²)'].sum()
    obj3_area_avg = obj3_df['Area (Mesh), Projection (XY/Z) (µm²)'].mean()
    obj1_in_obj2 = len(obj1_df[obj1_df['Tags'].str.contains(', ND4 Blob Finder in Mito Clean in GRSF1 in Mito Clean')].reset_index(drop=True))
    percent_obj1_in_obj2 = 100.0 * (obj1_in_obj2 / obj1_number)
    obj1_in_obj3 = len(obj1_df[obj1_df['Tags'].str.contains(', ND4 Blob Finder in Mito Clean in DNA in Mito Clean')].reset_index(drop=True))
    percent_obj1_in_obj3 = 100.0 * (obj1_in_obj3 / obj1_number)
    obj3_in_obj2 = len(obj3_df[obj3_df['Tags'].str.contains(', DNA in Mito Clean in GRSF1 in Mito Clean')].reset_index(drop=True))
    percent_obj3_in_obj2 = 100.0 * (obj3_in_obj2 / obj3_number)

    sim_results_1 = object_intersection_sim.simulation(obj1_number, obj1_area_avg, obj2_number, obj2_area_avg, mito_area_sum, 20.0, 100)
    sim_results_2 = object_intersection_sim.simulation(obj1_number, obj1_area_avg, obj3_number, obj3_area_avg, mito_area_sum, 20.0, 100)
    sim_results_3 = object_intersection_sim.simulation(obj2_number, obj2_area_avg, obj3_number, obj3_area_avg, mito_area_sum, 20.0, 100)

    obj_out_df.loc[len(obj_out_df)] = [image_name, mito_area_sum, obj1_number, obj1_area_sum, obj1_area_avg, obj2_number,
                                       obj2_area_sum, obj2_area_avg, obj3_number, obj3_area_sum, obj3_area_avg,
                                       obj1_in_obj2, percent_obj1_in_obj2, sim_results_1[0], sim_results_1[1],
                                       obj1_in_obj3, percent_obj1_in_obj3, sim_results_2[0], sim_results_2[1],
                                       obj3_in_obj2, percent_obj3_in_obj2, sim_results_3[0], sim_results_3[1]]
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
    for i in range(len(obj3_df)):
        int_corr_obj3_df.loc[len(int_corr_obj3_df)] = [image_name, obj3_df.at[i, 'Name'],
                                                       obj3_df.at[i, 'Mean, Intensities #1'],
                                                       obj3_df.at[i, 'Mean, Intensities #2'],
                                                       obj3_df.at[i, 'Mean, Intensities #3']]
        int_corr_obj3_df.reset_index(drop=True, inplace=True)

    obj_out_df.to_csv(dataset_name + '_Object_intersection_data.csv')
    int_corr_obj1_df.to_csv(dataset_name + '_Object1_intensity_correlation_data.csv')
    int_corr_obj2_df.to_csv(dataset_name + '_Object2_intensity_correlation_data.csv')
    int_corr_obj3_df.to_csv(dataset_name + '_Object3_intensity_correlation_data.csv')