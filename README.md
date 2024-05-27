This is a script on Python to plot the SQM (sky brightess in mag/arcsec^2) on time using star photos and ASTAP program.

1. First you should install ASTAP from https://www.hnsky.org/astap
2. Than run it and configure for plate solving. Press Stack menu button (with Sigma sign), go to Alignment tab and fill in 'Field of view', 'Radius search area' and 'Star database used'. Refer to ASTASP documentation.
3. Try running plate solving. If it is Ok, try SQM measurement from the main program menu. Fill in coordinates of the shot place.
4. Find the mean value of your Dark frames. You can press Stack menu button (with Sigma sign), go to Darks tab and load your darks. Than replace it with master dark. You will find the mean value in this window.
5. Substitute this mean value into the command in line ?? of the main.py file.
6. Also change the default folder in line ??
7. If you have original files with correct creation time, choose "C" (means creation time) in line ??. Otherwise choose "N" (means Name). Than on X axis will be file names.
8. Run the script, choose files and wait until they are processed. Enjoy the SQM plot and data saved in *.spc text file.
