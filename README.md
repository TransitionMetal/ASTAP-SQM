This is a script on Python to plot the SQM (sky brightess in mag/arcsec^2) on time using star photos and ASTAP program.

1. First you should install ASTAP from https://www.hnsky.org/astap
2. Than run it and configure for plate solving. Press 'Show Stack Menu' button (with Sigma sign) or Ctrl+A, go to Alignment tab and fill in 'Field of view' (according to your images), 'Radius search area' (180*) and 'Star database used' (Auto). Refer to ASTASP documentation.
3. Open your image (Ctrl+O or 'File-Load FITS or other format' menu or 'Browse & Preview FITS files' button) and try to run plate solving ('Solve' button). If it is Ok, try SQM measurement ('Tools-SQM report based on an image' menu). Fill in coordinates - Latitude and Longitude - of the shot place.
4. Find the mean value of your Dark frames. You can press 'Show Stack Menu' button (with Sigma sign), go to 'Darks' tab and load your darks ('Browse' button). Than replace it with master dark by pressing 'Replace check-marked by one or more master dark'. You will find the mean value in this window. Use 'Analyse' button if needed.
5. Substitute this mean value into the command in line ?? of the main.py file.
6. Also change the default folder in line ??
7. If you have original files with correct creation time, choose "C" (means creation time) in line ??. Otherwise choose "N" (means Name). Than on X axis will be file names.
8. Run the script, choose files and wait until they are processed. Enjoy the SQM plot and data saved in *.spc text file.
