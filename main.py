from subprocess import run
import os
import datetime
import numpy as np
from matplotlib import pyplot as plt
import mplcyberpunk
from tkinter import filedialog
import configparser

def main():
    # define date acquisition method
    # C - file creation, N - file name
    date_type = 'C'
    file_path = filedialog.askopenfilename(
        title="Выберите файл",
        initialdir=r'C:\YandexDisk\Astronomy\2do\\',  # \\ to protect '
        filetypes=[(['cr2', 'fit', 'xisf'], ['*.cr2', '*.fit', '*.xisf'])],  # to see which files are already processed
        multiple = True)

    sqm = np.array([], dtype=float)
    match date_type:
        case 'C': creation_time = np.array([], dtype='datetime64')
        case 'N': creation_time = np.array([])

    for current_file_path in file_path:

        # replace / by \ in file path
        current_file_replaced = str(current_file_path)
        current_file_replaced = current_file_replaced.replace('/', '\\')

        # Define the command and arguments for ASTAP
        command = "\"C:\\Program Files\\astap\\astap.exe\" -f \"" + current_file_replaced + "\" -sqm 2046"
        print(command)
        # Run the command
        #result = run(command, shell=True, capture_output=True, text=True)

        # read sqm from file.
        # open file as .ini and add dummy section
        with open(current_file_replaced[:-3] + 'ini', 'r') as ini_file:
            config_string = '[dummy_section]\n' + ini_file.read()
        config = configparser.ConfigParser()
        config.read_string(config_string)
        #print(config_string)
        section = 'dummy_section'
        #for key in config[section]:
          #   print(f"  Key: {key} - {config[section][key]}")
        key = 'sqm'
        if section in config and key in config[section]:
            value = config[section][key]
            print(value)
            sqm = np.append(sqm, float(value))
            #print(sqm)

            # get the creation date and time
            match date_type:
                case 'C':
                    # Convert to a readable format
                    creation_time = np.append(creation_time, np.datetime64(
                        datetime.datetime.fromtimestamp(os.path.getctime(current_file_path))))
                    #print(creation_time)
                case 'N':
                    current_file_name = current_file_replaced[current_file_replaced.rfind('\\')+1:-4]
                    if len(current_file_name) > 14:
                        creation_time = np.append(creation_time, current_file_name[:19])
                    else:
                        creation_time = np.append(creation_time, current_file_name[:8])


    # Print the output
    # print("stdout:", result.stdout)
    #print("stderr:", result.stderr)
    #print("returncode:", result.returncode)
    sqm = np.transpose(sqm)
    creation_time = np.transpose(creation_time)
    creation_time_str = creation_time.astype(str)
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

