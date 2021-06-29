# line_asymmetry
Code to take csv files output by PySplot, reorganise, and perform line asymmetry calculations 

To run, download all files to the place where the PySplot csv files are housed. This code is still limited in its functionality, so there are additional steps that must be followed. In updated versions, these will no longer be necessary.

1. Download the six scripts.
2. Rename your PySplot excels as "pysplot_flux_4640.csv" or "pysplot_p_flux_4640.csv" where 4640 is the rest wavelength of the line in question.
3. Open the ```get_info``` script. This is one of the biggest limitations. You need to list te names of your PySplot files in the array called ```pysplot_excels```. Save the script and close it.
4. Lastly, open ```Main``` and run it. You will be prompted for the following information, so make sure you have it handy:
    * Name of star
    * Period (for phase calculations)
    * E0 (for phase calculations)
    * Path to dated folders (for phase calculations)
    * Lines you bisected, as well as start heights and step intervals
    * Form (is this binned? Smoothed? Modified in any other way?)
    * Number of dates you have
5. One final limitation is that you must bisect 8 times. This will be refined in later versions.
