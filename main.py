from subprocess import run
import os
import datetime
import numpy as np
from matplotlib import pyplot as plt
import setuptools
import mplcyberpunk
from tkinter import filedialog
import re

def main():
    # time zone for correcting the axis, because extracted is UTC time
    time_zone = np.timedelta64(3, 'h')
    # file open dialog window
    file_path = filedialog.askopenfilename(
        title="Выберите файл",
        initialdir=r'C:\YandexDisk\Astronomy\2do\\',  # \\ to protect '
        filetypes=[(['cr2', 'fit', 'xisf'], ['*.cr2', '*.fit', '*.xisf'])],  # to see which files are already processed
        multiple=True)

    # prepare empty numpy array for SQM values
    sqm = np.array([], dtype=float)
    # prepare empty numpy array for date and time
    creation_time = np.array([], dtype='datetime64')

    # main loop for file list
    for current_file_path in file_path:
        # convert file path to string
        current_file_replaced = str(current_file_path)
        # replace / by \ in file path
        current_file_replaced = current_file_replaced.replace('/', '\\')
        # check if file already solved (is there a *.wcs file)
        if not os.path.exists(current_file_path[:-3] + 'wcs'):
            # Define the command and arguments for ASTAP
            command = "\"C:\\Program Files\\astap\\astap.exe\" -f \"" + current_file_replaced + "\" -sqm 2046"
            #print(command)
            # Run the command
            result = run(command, shell=True, capture_output=True, text=True)

        # read sqm from file.
        # open file as txt
        if os.path.exists(current_file_path[:-3] + 'wcs'):
            with open(current_file_replaced[:-3] + 'wcs', 'r') as file:
                config_string = file.read()
            # find the strtings SQM     =  XX.XX               / Sky background [magn/arcsec^2]
            sqm_string = re.findall(r'SQM.*Sky background \[magn/arcsec\^2]\n', config_string)
            # parse the number
            sqm_value = re.findall(r'\d+\.\d+', sqm_string[0])
            # print the SQM value
            print(sqm_value)
            # add the value to the end of the array
            sqm = np.append(sqm, float(sqm_value[0]))
            # look for the date and time: DATE-OBS= '2024-10-05T00:26:00.000' / [UTC] The start time of the exposure
            time_string = re.findall(r'DATE-OBS.*\n', config_string)
            # parse for date and time
            time_value = re.findall(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', time_string[0])
            print(time_value)
            # add the date and time to the array
            creation_time = np.append(creation_time, np.datetime64(time_value[0]) + time_zone)

    # Print the output
    # print("stdout:", result.stdout)
    #print("stderr:", result.stderr)
    #print("returncode:", result.returncode)

    # transpose the arrays before merging
    sqm = np.transpose(sqm)
    creation_time = np.transpose(creation_time)
    # convert to string???
    creation_time_str = creation_time.astype(str)
    # sort by date-time
    sqm = sqm[np.argsort(creation_time)]
    creation_time_str = creation_time_str[np.argsort(creation_time)]
    creation_time = creation_time[np.argsort(creation_time)]
    # save to file
    np.savetxt(current_file_replaced[:-3] + "spc",
               np.column_stack((creation_time_str, sqm)), fmt='%s %s', delimiter=' ')
    # apply cyberpunk style
    plt.style.use("cyberpunk")  # add cyberpunk outlook
    plt.clf()
    plt.plot(creation_time, sqm, linewidth=2.0, label='SQM')
    plt.xlabel('Date and Time')
    plt.ylabel('SQM')
    plt.legend()
    plt.title("SQM")
    plt.xticks(rotation=45) # Rotate x-axis labels for better readability (optional)
    # mplcyberpunk.add_glow_effects(gradient_fill=True)  # add glow effect
    mplcyberpunk.add_gradient_fill(gradient_start='max')
    plt.show(block=True)

if __name__ == '__main__':
    main()

