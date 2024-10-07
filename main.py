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
    time_zone = np.timedelta64(3, 'h')
    file_path = filedialog.askopenfilename(
        title="Выберите файл",
        initialdir=r'C:\YandexDisk\Astronomy\2do\\',  # \\ to protect '
        filetypes=[(['cr2', 'fit', 'xisf'], ['*.cr2', '*.fit', '*.xisf'])],  # to see which files are already processed
        multiple=True)

    sqm = np.array([], dtype=float)
    creation_time = np.array([], dtype='datetime64')

    for current_file_path in file_path:
        # replace / by \ in file path
        current_file_replaced = str(current_file_path)
        current_file_replaced = current_file_replaced.replace('/', '\\')
        # check if file already solved
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
            sqm_string = re.findall(r'SQM.*Sky background \[magn/arcsec\^2]\n', config_string)
            sqm_value = re.findall(r'\d+\.\d+', sqm_string[0])
            print(sqm_value)
            sqm = np.append(sqm, float(sqm_value[0]))
            time_string = re.findall(r'DATE-OBS.*\n', config_string)
            time_value = re.findall(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', time_string[0])
            print(time_value)
            creation_time = np.append(creation_time, np.datetime64(time_value[0]) + time_zone)

    # Print the output
    # print("stdout:", result.stdout)
    #print("stderr:", result.stderr)
    #print("returncode:", result.returncode)
    sqm = np.transpose(sqm)
    creation_time = np.transpose(creation_time)
    creation_time_str = creation_time.astype(str)
    sqm = sqm[np.argsort(creation_time)]
    creation_time_str = creation_time_str[np.argsort(creation_time)]
    creation_time = creation_time[np.argsort(creation_time)]
    np.savetxt(current_file_replaced[:-3] + "spc",
               np.column_stack((creation_time_str, sqm)), fmt='%s %s', delimiter=' ')

    plt.style.use("cyberpunk")  # add cyberpunk outlook
    plt.clf()
    plt.plot(creation_time, sqm, linewidth=2.0, label='SQM')
    plt.xlabel('Date and Time')
    plt.ylabel('SQM')
    plt.legend()
    plt.title("SQM")
    plt.xticks(rotation=45) # Rotate x-axis labels for better readability (optional)
    #mplcyberpunk.add_glow_effects(gradient_fill=True)  # add glow effect
    mplcyberpunk.add_gradient_fill(gradient_start='max')
    plt.show(block=True)

if __name__ == '__main__':
    main()

