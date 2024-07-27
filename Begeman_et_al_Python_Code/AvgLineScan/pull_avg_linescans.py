import pandas as pd
from scipy.signal import find_peaks
import os
import matplotlib.pyplot as plt
from warnings import simplefilter
import numpy as np

simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

pxiel_distance = 0.035
region_to_pull = 14
saving_data = True
show_plot = False

experiment_dir = 'hpg_with_protein'
csv_dir = 'csv_files'
channels_in_image = 3
#image_sets = ['GRSF1', 'MRPL23', 'PTPMT1', 'TFAM']
#image_sets = ['john_tfam', 'john_polg']
#image_sets = ['john_lsrna_edu', 'john_lsrna_polg']
#image_sets = ['15minPulse', '30minPulse', '1hrPulse', '15minChase', '30minChase', '1hrChase']
#image_sets = ['ND4_GRSF1', 'RNR2_GRSF1', 'tRNAs_GRSF1']
#image_sets = ['ND4_HPG', 'RNR2_HPG', 'tRNAs_HPG']
#image_sets = ['ND4_MRPL23', 'RNR2_MRPL23', 'tRNAs_MRPL23']
#image_sets = ['ND4_TOM20', 'RNR2_TOM20', 'tRNAs_TOM20']
#image_sets = ['COX1_ND4_HPG', 'ND2_ND4_HPG', 'RNR2_ND4_HPG', 'tRNAs_ND4_HPG']
image_sets = ['DRP1']
#image_sets = ['SUV3_HPG', 'SUV3_RNR2']
#image_sets = ['TFAM_DNA', 'New_GRSF1_DNA']
#image_sets = ['EU_GRSF1']
channel_sets = ['Channel_1', 'Channel_3']
#Pull this from Cyto Value Calculated, add on avg Blue to Red bleed (better would adaptive value based on Blue bleed or correcting line scan for blue bleed
# params are lists of [min width, min height, min prominence], distance of 6 conservative based on limit of resolution
#NOTE: Play around with larger GRSF1 heights (20000) and TFAM Heights (10000)
channel_1_peak_params = {'15minPulse' : [4, 1297, 200],'30minPulse' : [4, 1443, 200], '1hrPulse' : [4, 1588, 200],
                         '15minChase' : [4, 784, 200], '30minChase' : [4, 685, 200], '1hrChase' : [4, 583, 200],
                         'GRSF1' : [4, 1297, 200], 'MRPL23' : [4, 1297, 200], 'PTPMT1': [4, 1297, 200], 'TFAM' : [4, 1297, 200],
                         'ND4_GRSF1' : [4, 800, 500], 'RNR2_GRSF1' : [4, 4000, 1000], 'tRNAs_GRSF1' : [4, 1000, 300],
                         'ND4_HPG' : [4, 300, 200], 'RNR2_HPG' : [4, 4000, 2000], 'tRNAs_HPG' : [4, 1500, 700],
                         'ND4_MRPL23' : [4, 200, 100], 'RNR2_MRPL23' : [4, 2000, 1000], 'tRNAs_MRPL23' : [4, 700, 200],
                         'ND4_TOM20' : [4, 800, 500], 'RNR2_TOM20' : [4, 4000, 1000], 'tRNAs_TOM20' : [4, 1000, 300],
                         'john_lsrna_edu' : [2, 100, 50], 'john_lsrna_polg' : [2, 100, 50],
                         'COX1_ND4_HPG' : [4, 600, 400], 'ND2_ND4_HPG' : [4, 500, 300],
                         'RNR2_ND4_HPG' : [4, 3000, 1000], 'tRNAs_ND4_HPG' : [4, 1000, 300],
                         'DRP1' : [4, 1297, 200],
                         'SUV3_GRSF1' : [], 'SUV3_HPG' : [4, 1297, 200], 'SUV3_RNR2' : [4, 2000, 1000],
                         'TFAM_DNA' : [], 'GRSF1_DNA' : [],
                         'EU_GRSF1' : [4, 800, 400], 'New_DNA_GRSF1' : []
                         }
channel_2_peak_params = {'15minPulse' : np.NaN,'30minPulse' : np.NaN, '1hrPulse' : np.NaN,
                         '15minChase' : np.NaN, '30minChase' : np.NaN, '1hrChase' : np.NaN,
                         'GRSF1' : [3, 6000, 4000], 'MRPL23' : [3, 1000, 800], 'PTPMT1': [3, 800, 800], 'TFAM' : [4, 5000, 5000],
                         'ND4_GRSF1' : [3, 6000, 4000], 'RNR2_GRSF1' : [3, 6000, 4000], 'tRNAs_GRSF1' : [3, 6000, 4000],
                         'ND4_HPG' : [4, 1000, 200], 'RNR2_HPG' : [4, 1000, 200], 'tRNAs_HPG' : [4, 1000, 200],
                         'ND4_MRPL23': [3, 1000, 800], 'RNR2_MRPL23': [3, 1000, 800], 'tRNAs_MRPL23': [3, 1000, 800],
                         'ND4_TOM20': [], 'RNR2_TOM20': [], 'tRNAs_TOM20': [],
                         'john_tfam' : [2, 655, 100], 'john_polg' : [2, 655, 100],
                         'john_lsrna_edu' : [4, 400, 200], 'john_lsrna_polg' : [2, 655, 100],
                         'COX1_ND4_HPG' : [4, 600, 400], 'ND2_ND4_HPG' : [4, 600, 400],
                         'RNR2_ND4_HPG': [4, 300, 200], 'tRNAs_ND4_HPG': [4, 300, 200],
                         'DRP1' : [],
                         'SUV3_GRSF1' : [3, 6000, 4000], 'SUV3_HPG' : [4, 8000, 4000], 'SUV3_RNR2' : [4, 8000, 4000],
                         'TFAM_DNA' : [4, 5000, 1500], 'GRSF1_DNA' : [4, 15000, 10000],
                         'EU_GRSF1' : [4, 6000, 4000], 'New_GRSF1_DNA' : [3, 6000, 4000]
                         }
channel_3_peak_params = {'15minPulse' : [3, 5000, 5000],'30minPulse' : [3, 5000, 5000], '1hrPulse' : [3, 5000, 5000],
                         '15minChase' : [3, 5000, 5000], '30minChase' : [3, 5000, 5000], '1hrChase' : [3, 5000, 5000],
                         'GRSF1' : np.NaN, 'MRPL23' : np.NaN, 'PTPMT1': np.NaN, 'TFAM' : np.NaN,
                         'ND4_GRSF1' : [3, 5000, 5000], 'RNR2_GRSF1' : [3, 5000, 5000], 'tRNAs_GRSF1' : [3, 5000, 5000],
                         'ND4_HPG' : [], 'RNR2_HPG' : [], 'tRNAs_HPG' : [],
                         'ND4_MRPL23': [], 'RNR2_MRPL23': [], 'tRNAs_MRPL23': [],
                         'ND4_TOM20': [3, 5000, 5000], 'RNR2_TOM20': [3, 5000, 5000], 'tRNAs_TOM20': [3, 5000, 5000],
                         'john_tfam' : [2, 4000, 2000], 'john_polg' : [2, 4000, 2000],
                         'COX1_ND4_HPG' : [4, 1000, 200], 'ND2_ND4_HPG' : [4, 1000, 200],
                         'RNR2_ND4_HPG': [4, 800, 300], 'tRNAs_ND4_HPG': [4, 800, 300],
                         'DRP1' : [4, 2000, 1000],
                         'SUV3_GRSF1' : [4, 3000, 2000], 'SUV3_HPG' : [], 'SUV3_RNR2' : [],
                         'TFAM_DNA' : [2, 4000, 2000], 'GRSF1_DNA' : [2, 4000, 2000],
                         'EU_GRSF1' : [], 'New_GRSF1_DNA' : [3, 5000, 5000]
                         }

if saving_data:
    log_file = open(experiment_dir + '/drp1_metadata.txt', 'a')

for image_set in image_sets:
    print(image_set)
    c1_max = 0
    c2_max = 0
    c3_max = 0
    c1_peak_df = pd.DataFrame()
    c2_peak_df = pd.DataFrame()
    c3_peak_df = pd.DataFrame()

    total_line_scans = 0

    for peak_channel in channel_sets:
        print(peak_channel)

        channel_peak_max = 0

        if peak_channel == 'Channel_1':
            peak_params = channel_1_peak_params[image_set]
        elif peak_channel == 'Channel_2':
            peak_params = channel_2_peak_params[image_set]
        else:
            peak_params = channel_3_peak_params[image_set]

        avg_height = 0
        avg_width = 0
        avg_prominence = 0
        total_peaks = 0

        image_avg_df = pd.DataFrame({'Distance': [i * pxiel_distance for i in range(((2*region_to_pull) + 1))],
                                   'Channel 1': [0] * ((2*region_to_pull) + 1),
                                   'Channel 2': [0] * ((2*region_to_pull) + 1),
                                   'Channel 3': [0] * ((2*region_to_pull) + 1)})
        image_n = 0

        for file in os.listdir(experiment_dir + '/' + csv_dir + '/' + image_set):
            df = pd.read_csv(experiment_dir + '/' + csv_dir+'/'+image_set+'/'+file)
            name = file.split('.')[0]
            image_n += 1
            n = 1
            running_avg_height = 0
            running_avg_width = 0
            running_avg_prominence = 0
            running_peaks = 0
            out_df = pd.DataFrame([i * pxiel_distance for i in range(((2*region_to_pull) + 1))], columns=['Distance'])
            avg_df = pd.DataFrame({'Distance': [i * pxiel_distance for i in range(((2*region_to_pull) + 1))],
                                   'Channel 1': [0] * ((2*region_to_pull) + 1),
                                   'Channel 2': [0] * ((2*region_to_pull) + 1),
                                   'Channel 3': [0] * ((2*region_to_pull) + 1)})

            for i in range(int(len(df.columns) / (channels_in_image + 1))):
                roi_line = pd.DataFrame()
                roi_line['Distance'] = df['ROI_' + str(i) + ' distance (micron)']
                drop_value = len(roi_line)
                for j in range(1,len(roi_line)):
                    if roi_line['Distance'][j] == 0:
                        drop_value = j
                        break
                roi_line['Channel_1'] = df['ROI_' + str(i) + ' Channel_1']
                roi_line['Channel_2'] = df['ROI_' + str(i) + ' Channel_2']
                roi_line['Channel_3'] = df['ROI_' + str(i) + ' Channel_3']
                roi_line = roi_line.drop([k for k in range(drop_value,len(roi_line))], axis=0)
                peak_values = find_peaks(roi_line[peak_channel], prominence=peak_params[2], width=peak_params[0], distance=6, height=peak_params[1])
                total_line_scans += 1
                for j in range(len(peak_values[0])):
                    peak_position = peak_values[0][j]
                    if peak_position > region_to_pull and peak_position < (len(roi_line) - region_to_pull):
                        out_df['Peak_' + str(n) + ' Channel 1'] = roi_line['Channel_1'][peak_position-region_to_pull:peak_position+ (region_to_pull+1)].reset_index(drop=True)
                        out_df['Peak_' + str(n) + ' Channel 2'] = roi_line['Channel_2'][peak_position - region_to_pull:peak_position + (region_to_pull+1)].reset_index(drop=True)
                        out_df['Peak_' + str(n) + ' Channel 3'] = roi_line['Channel_3'][peak_position - region_to_pull:peak_position + (region_to_pull+1)].reset_index(drop=True)
                        avg_df['Channel 1'] = avg_df['Channel 1'] + out_df['Peak_' + str(n) + ' Channel 1']
                        avg_df['Channel 2'] = avg_df['Channel 2'] + out_df['Peak_' + str(n) + ' Channel 2']
                        avg_df['Channel 3'] = avg_df['Channel 3'] + out_df['Peak_' + str(n) + ' Channel 3']
                        temp_peak_height = peak_values[1]['peak_heights'][j]
                        running_avg_height += temp_peak_height
                        running_avg_width += peak_values[1]['widths'][j]
                        running_avg_prominence += peak_values[1]['prominences'][j]
                        n += 1
                        if temp_peak_height > channel_peak_max:
                            channel_peak_max = temp_peak_height
            sum_df = avg_df.copy()
            avg_df = avg_df.div(n)
            avg_df['Distance'] = [i_1 * pxiel_distance for i_1 in range(((2*region_to_pull) + 1))]
            sum_df['Distance'] = [i_1 * pxiel_distance for i_1 in range(((2 * region_to_pull) + 1))]
            if saving_data:
                out_df.to_csv(experiment_dir + '/peak_csvs/' + peak_channel + '/' + name + '_each_peak.csv')
                avg_df.to_csv(experiment_dir + '/avg_peak_csvs/' + peak_channel + '/' + name + '_avg_peaks.csv')
                sum_df.to_csv(experiment_dir + '/sum_peak_csvs/' + peak_channel + '/' + name + '_sum_peaks.csv')
            image_avg_df['Channel 1'] = image_avg_df['Channel 1'] + sum_df['Channel 1']
            image_avg_df['Channel 2'] = image_avg_df['Channel 2'] + sum_df['Channel 2']
            image_avg_df['Channel 3'] = image_avg_df['Channel 3'] + sum_df['Channel 3']
            avg_height += running_avg_height
            avg_width += running_avg_width
            avg_prominence += running_avg_prominence
            running_peaks = n
            total_peaks += running_peaks

        total_peaks = total_peaks - image_n
        image_avg_df = image_avg_df.div(total_peaks)
        image_avg_df['Distance'] = [i_1 * pxiel_distance for i_1 in range(((2 * region_to_pull) + 1))]
        if peak_channel == 'Channel_1':
            c1_max = channel_peak_max
            c1_peak_df = image_avg_df.copy()
        elif peak_channel == 'Channel_2':
            c2_max = channel_peak_max
            c2_peak_df = image_avg_df.copy()
        else:
            c3_max = channel_peak_max
            c3_peak_df = image_avg_df.copy()

        if saving_data:
            image_avg_df.to_csv(experiment_dir + '/' + image_set + '_' + peak_channel + '_avg_peaks.csv')
            log_file.write('name: ' + image_set + '\n')
            log_file.write('Channel: ' + peak_channel + '\n')
            log_file.write('Peak Width Minimum: ' + str(peak_params[0]) + '\n')
            log_file.write('Peak Height Minimum: ' + str(peak_params[1]) + '\n')
            log_file.write('Peak Prominence Minimum: ' + str(peak_params[2]) + '\n')
            log_file.write('avg height: ' + str(avg_height / total_peaks) + '\n')
            log_file.write('avg_width: ' + str(avg_width / total_peaks) + '\n')
            log_file.write('avg_prominence: ' + str(avg_prominence / total_peaks) + '\n')
            log_file.write('total_peaks: ' + str(total_peaks) + '\n')
            log_file.write('avg peaks per image: ' + str(total_peaks / image_n) + '\n')

        print('avg height: ' + str(avg_height / total_peaks))
        print('avg_width: ' + str(avg_width / total_peaks))
        print('avg_prominence: ' + str(avg_prominence / total_peaks))
        print('total_peaks: ' + str(total_peaks))
        print('avg peaks per image: ' + str(total_peaks / image_n))

    max_values = [1, c1_max, c2_max, c3_max]
    #HERE calculate Normalized Peaks with known max peak data
    figure, axis = plt.subplots(1,len(channel_sets))
    z = 0
    for channel in channel_sets:
        if channel == 'Channel_1':
            image_avg_df = c1_peak_df.copy()
        elif channel == 'Channel_2':
            image_avg_df = c2_peak_df.copy()
        else:
            image_avg_df = c3_peak_df.copy()
        image_norm_avg_df = image_avg_df.div(max_values)
        if saving_data:
            image_norm_avg_df.to_csv(experiment_dir + '/' + image_set + '_' + channel + 'norm_avg_peaks.csv')
        axis[z].plot(image_norm_avg_df['Channel 1'], color='r')
        axis[z].plot(image_norm_avg_df['Channel 2'], color='g')
        axis[z].plot(image_norm_avg_df['Channel 3'], color='b')
        axis[z].axvline(region_to_pull, color='black', linestyle='--')
        axis[z].set_xlim([0, ((region_to_pull*2) + 1)])
        axis[z].set_ylim([0,1])
        axis[z].set_title(str(image_set + ' ' + channel))
        z += 1
    if show_plot:
        plt.show()
    print(total_line_scans)
    if saving_data:
        log_file.write('c1_max: ' + str(c1_max) + '\n')
        log_file.write('c2_max: ' + str(c2_max) + '\n')
        log_file.write('c3_max: ' + str(c3_max) + '\n')
        log_file.write('total line scans: ' + str(total_line_scans) + '\n')
