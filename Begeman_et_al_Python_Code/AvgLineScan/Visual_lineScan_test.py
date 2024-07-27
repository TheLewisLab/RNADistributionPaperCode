import pandas as pd
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

pxiel_distance = 0.035
# good paramaters, prominence may be under calling for Chases as signal is generally lower but might not matter

df = pd.read_csv('example_linescans/csv_files/New_GRSF1_DNA/mtdr-647_GRSF1-488_dsDNA-405-02-AiryscanProcessing-ExtendedDepthofFocus_mito_VoxelResult.ome.csv')

for i in range(int(len(df.columns)/4)):

    raw_line = df['ROI_'+str(i)+' Channel_2']
    plt.plot(raw_line, color='g')
    plt.plot(df['ROI_'+str(i)+' Channel_3'], color='b')

    raw_peak_values = find_peaks(raw_line, prominence=1, width=4, height=1, distance=6)
    print('Prominences: ' + str(raw_peak_values[1]['prominences']))
    print('Widths: ' + str(raw_peak_values[1]['widths']))
    print('Peak Heights: ' + str(raw_peak_values[1]['peak_heights']))
    print(i)
    for j in range(len(raw_peak_values[0])):
        plt.axvline(raw_peak_values[0][j], color='black', linestyle='--', label=str(raw_peak_values[0][j]))
        plt.axvspan(raw_peak_values[1]['left_ips'][j], raw_peak_values[1]['right_ips'][j], alpha=0.3, color='gray')

    plt.show()