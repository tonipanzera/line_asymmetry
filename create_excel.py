#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 11 16:40:53 2021

@author: ToniPanzera
"""


import numpy as np
import pandas as pd
import xlsxwriter as excelwriter
import math
import astropy.io.ascii as ascii
import get_info
import get_phases

#--------------------------------------------------------------------------------------------------------------
# A script to read in .csv files of flux and p-flux output by PySplot.
# Instructions for use:
#    1. Make sure you call your pysplot files something easy, and whatever you want your excel sheets to be
#    called. I recommend 'pysplot_flux_4640' or something like that.
#    2. Change the number of columns in the worksheet below to match the number of bisect heights.
#    3. Make sure all your pysplot files are housed in the same place as this script.
#    4. Change the names of your pysplot files in the code below; 
#    be sure to keep the order the same as the example.
#    5. This script relies on you bisecting the same number of times across all lines (8 times actually); 
#       however, you are free to change the start height as necessary. You can also manually adjust the code 
#       for a different number of bisect heights.
#    6. For the phases, make sure you change the path to the folder that has all your dates in it.
#---------------------------------------------------------------------------------------------------------------
'''
#Creating variables
period = ''
e0 = ''
lines = []
form = ''
pysplot_excels = []
no_of_dates = ''
no_bisects = int
start_height_array = []
bisect_separation_array = []
end_height_array = []
bisect_heights_array = []
worksheet_array = []
big_array = []
start_indices = []

def get_initial_info():
    
    global star
    global period
    global e0
    global lines
    global form
    global pysplot_excels
    global no_of_dates
    global no_bisects
    
    #Get initial inputs: what the star is, and how many lines have been done, and how the data is binned, etc.
    star = input('What is the name of the star? ')

    period = input('What is the period of the star? ')

    e0 = input('What is the E0 of the star? ')

    lines = input('What lines have you bisected? Please list in ascending order with no spaces between. ')

    lines = list(map(''.join, zip(*[iter(lines)]*4)))

    form = input('How has the data been binned/modified? Eg. Bin2A, GaussianSmoothed, etc. ')

    #print(lines)

    #Define each of the pysplot docs. Change these to whatever your files are called. No need to add .csv 

    pysplot_excels = ['pysplot_flux_4640', 
                      'pysplot_p_flux_4640',
                      'pysplot_flux_4686', 
                      'pysplot_p_flux_4686', 
                      'pysplot_flux_4859', 
                      'pysplot_p_flux_4859', 
                      'pysplot_flux_5412', 
                      'pysplot_p_flux_5412',
                      #'pysplot_flux_5805',
                      #'pysplot_p_flux_5805',
                      'pysplot_flux_6560', 
                      'pysplot_p_flux_6560',
                      'pysplot_flux_7125', 
                      'pysplot_p_flux_7125']

    #Now see how many observations are in the sample, and how many bisects since these shouldn't
    #change from line to line.

    no_of_dates = int(input('How many dates do you have? '))

    no_bisects = 8
'''

global star
global period
global e0
global lines
global form
global pysplot_excels
global no_of_dates
global no_bisects
global datapath

def get_bisects():
    
    global star
    global period
    global e0
    global lines
    global form
    global pysplot_excels
    global no_of_dates
    global no_bisects
    global datapath
    global phases
    
    star = get_info.star
    period = get_info.period
    e0 = get_info.e0
    pysplot_excels = get_info.pysplot_excels
    no_of_dates = get_info.no_of_dates
    no_bisects = get_info.no_bisects
    datapath = get_info.datapath
    form = get_info.form
    lines = get_info.lines
    
    #star, period, e0, lines, form, pysplot_excels, no_of_dates, no_bisects, datapath = get_info.get_initial_info()

    phase_file = ascii.read(str(star)+'_Phases.txt')
    phases = phase_file['Phase']

    global start_height_array
    start_height_array = []
    global bisect_separation_array
    bisect_separation_array = []
    global end_height_array
    end_height_array = []
    global bisect_heights_array
    bisect_heights_array = []
       
    #Now ask for input

    for i in range(0, len(lines)):
    
        start_height = float(input('What height did you start bisecting line '+str(lines[i])+ ' at? '))
        start_height_array.append(start_height)
        start_height_array.append(start_height) #need two of each value for the flux and p-flux

        bisect_separation = float(input('What was the distance between each bisect for line '+str(lines[i])+'? '))
        bisect_separation_array.append(bisect_separation)
        bisect_separation_array.append(bisect_separation)

        end_height = np.round(((no_bisects-1)*bisect_separation)+start_height, 2)
        end_height_array.append(end_height)
        end_height_array.append(end_height)
    
        bisect_heights = np.linspace(start_height, end_height, num=no_bisects)
        bisect_heights = np.round(bisect_heights, 2)
        bisect_heights_array.append(bisect_heights)
        bisect_heights_array.append(bisect_heights)
    
    print(bisect_heights_array)


def make_excel():
    
    global worksheet_array
    worksheet_array = []
    #global big_array
    #global start_indices

    #Create the big workbook: each pysplot excel will get its own sheet
    workbook = excelwriter.Workbook(str(star)+'_Asymmetry_Efficiency_Test_'+str(form)+'.xlsx', 
                                {'strings_to_numbers': True})


    #Now comes a BIG loop to loop over each pysplot excel file

    for t in range(0, len(pysplot_excels)):

        worksheet = workbook.add_worksheet(str(pysplot_excels[t][8:]))
        worksheet_array.append(str(pysplot_excels[t][8:]))
        
        #Change this to fit how ever many heights you've got.
        worksheet.write(0,0, 'Date')
        worksheet.write(0,1, 'Phase')
        worksheet.write(0,2, 'Height1')
        worksheet.write(0,3, 'Height2')
        worksheet.write(0,4, 'Height3')
        worksheet.write(0,5, 'Height4')
        worksheet.write(0,6, 'Height5')
        worksheet.write(0,7, 'Height6')
        worksheet.write(0,8, 'Height7')
        worksheet.write(0,9, 'Height8')
    
        big_array = []
        start_indices = []
    
        excel = pd.read_csv(pysplot_excels[t]+'.csv', skiprows=2, header=None)

        #Extract each height's information
        for i in range(0, no_bisects):
            array = excel[(excel[11]==bisect_heights_array[t][i])]
            start_idx = np.where(excel[11]==bisect_heights_array[t][i])
            start_idx = start_idx[0][0]
            #print(array)
            big_array.append(array)
            start_indices.append(start_idx)

        print(start_indices)
            #print(big_array[0])

        for k in range(0, no_of_dates):
                
            #Change this to fit how ever many heights you've got.
            newrow = np.hstack((excel[0][start_indices[0]+k][-17:-9], 
                        phases[k], 
                        big_array[0][8][start_indices[0]+k], 
                        big_array[1][8][start_indices[1]+k], 
                        big_array[2][8][start_indices[2]+k], 
                        big_array[3][8][start_indices[3]+k],
                        big_array[4][8][start_indices[4]+k],
                        big_array[5][8][start_indices[5]+k],
                        big_array[6][8][start_indices[6]+k],
                        big_array[7][8][start_indices[7]+k]))
            print(newrow)
            worksheet.write_row(k+1, 0, newrow)
    
    workbook.close()

def get_plotting_info():
    
    workbook_name = str(star)+'_Asymmetry_Efficiency_Test_'+str(form)+'.xlsx'    
    return worksheet_array, bisect_heights_array, phases, workbook_name