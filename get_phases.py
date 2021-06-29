#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 22 11:51:07 2021

@author: ToniPanzera
"""

import astropy.io.fits as fits
from astropy.table import Table
import glob
import math
import get_info

def get_phases():
    
    star = get_info.star
    period = get_info.period
    e0 = get_info.e0
    datapath = get_info.datapath
    #star, period, e0, lines, form, pysplot_excels, no_of_dates, no_bisects, datapath = get_info.get_initial_info()
    
    #Make sure to change this to the path that contains dates in the format YYYYMMDD.
    folderList = glob.glob(str(datapath)+'/20*')

    filePattern = '/*.fits'

    #Loads fits files
    def fileLoad(folder):
        '''Loads a fits file'''
        dataFile = glob.glob(folder+filePattern)
        
        #Open fits file
        with fits.open(dataFile[0]) as hdul:
            julienDate = hdul[0].header['JD']
            return julienDate
        
        #main
        #user inputs
        #datapath = input("Enter the name of the star: ")
        #period = input("Enter Stars period: ")
        #e0 = input("Enter Stars E0: ")
    
    #table setup
    final_result = Table(names=("Date", "Phase"), dtype=('S8', 'f8'))

    #Cycles through each folder
    for folder in folderList:
        date = folder[-8:]
        
        jDate = fileLoad(folder)
        result=[date]
        
        #Calculation
        phase = (jDate-float(e0))/float(period)
        #Disregarding the numbers before the decimal point.
        (phase, etc) = math.modf(phase) #If you want the whole number just comment this line out.
        result.append(phase)
        print(phase)
        final_result.add_row(result)
        final_result.sort('Date')
        
    print(final_result)

    final_result.write(star+"_Phases.txt", format='ascii', overwrite=True)