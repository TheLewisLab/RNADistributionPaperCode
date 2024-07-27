import pandas as pd
import os
import random

data_dic = {'hpg_with_protein': ['GRSF1', 'MRPL23', 'PTPMT1', 'TFAM'],
            'mtRNA_GRSF1_dsDNA' : ['ND4_GRSF1', 'RNR2_GRSF1', 'tRNAs_GRSF1'],
            'mtRNA_HPG' : ['ND4_HPG', 'RNR2_HPG', 'tRNAs_HPG'],
            'mtRNA_MRPL23' : ['ND4_MRPL23', 'RNR2_MRPL23', 'tRNAs_MRPL23'],
            'mtRNA_TOM20' : ['ND4_TOM20', 'RNR2_TOM20', 'tRNAs_TOM20'],
            'pulse_chase' : ['15minPulse', '30minPulse', '1hrPulse', '15minChase', '30minChase', '1hrChase']}

data_dic = {'example_linescans' : ['TFAM_DNA'],
            'EU_Data' : ['EU_GRSF1']}

data_dic = {'hpg_with_protein' : ['DRP1']}
csv_dir = 'csv_files'

for experiment_dir, image_sets in data_dic.items():
    for image_set in image_sets:
        out_df = pd.DataFrame(columns=['Channel_1', 'Channel_2', 'Channel_3'])
        for file in os.listdir(experiment_dir + '/' + csv_dir + '/' + image_set):
            df = pd.read_csv(experiment_dir + '/' + csv_dir+'/'+image_set+'/'+file)
            for i in range(int(len(df.columns) / 4)):
                roi_line = pd.DataFrame()
                roi_line['Distance'] = df['ROI_' + str(i) + ' distance (micron)']
                drop_value = len(roi_line)
                for j in range(1, len(roi_line)):
                    if roi_line['Distance'][j] == 0:
                        drop_value = j
                        break
                roi_line['Channel_1'] = df['ROI_' + str(i) + ' Channel_1']
                roi_line['Channel_2'] = df['ROI_' + str(i) + ' Channel_2']
                roi_line['Channel_3'] = df['ROI_' + str(i) + ' Channel_3']
                roi_line = roi_line.drop(columns=['Distance'])
                roi_line = roi_line.drop([k for k in range(drop_value, len(roi_line))], axis=0)
                out_df = out_df.append(roi_line, ignore_index=True)
        avg_peak = pd.DataFrame({'Channel_1': [0]*29,
                                 'Channel_2' : [0]*29,
                                 'Channel_3' : [0]*29})
        peak_n = 0
        while peak_n < 2000:
            location = random.randrange(15, len(out_df) - 15)
            avg_peak['Channel_1'] = avg_peak['Channel_1'] + out_df['Channel_1'][location - 14:location + 15].reset_index(drop=True)
            avg_peak['Channel_2'] = avg_peak['Channel_2'] + out_df['Channel_2'][location - 14:location + 15].reset_index(drop=True)
            avg_peak['Channel_3'] = avg_peak['Channel_3'] + out_df['Channel_3'][location - 14:location + 15].reset_index(drop=True)
            peak_n += 1
        avg_peak = avg_peak.div(peak_n)
        avg_peak.to_csv('random_data_lines/' + str(image_set) + '_random_avg_linescan.csv')
        out_file = open('random_data_lines/' + str(image_set) + '_avg_channel_value.txt', 'w')
        out_file.write('image set mean\n')
        out_file.write(str(out_df.mean()))
        out_file.write('\nimage set std\n')
        out_file.write(str(out_df.std()))
        out_file.close()