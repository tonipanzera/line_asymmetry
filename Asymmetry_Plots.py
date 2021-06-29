#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 14:16:17 2020

@author: ToniPanzera
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import Tools as tools
from astropy.table import Table
from scipy import stats
import create_excel
import line_species
import get_info

#---------------------------------------------------------------------------------------------------------------------
# A script to plot asymmetry values versus phase, using the workbook created by 'create_excel'
# Instructions for use:
#   1. There is no need to change the path variable, as long as your 'create_excel' code is in the same place as this.
#   2. If you wish, you can change the name of the figure that will be output.
#---------------------------------------------------------------------------------------------------------------------

def plot_asymmetry():
    
    worksheet_array, bisect_heights_array, phases, workbook_name = create_excel.get_plotting_info()
    #phases = phases[:-2]
    phases.sort()
    star = get_info.star
    lines = get_info.lines
    datapath = get_info.datapath
    no_of_dates = get_info.no_of_dates
    form = get_info.form

    if len(lines)%2==0:
        no_rows = len(lines)/2
    else:
        no_rows = (len(lines)+1)/2
        
    #Major and Minor Tick Marks
    sns.set()
    sns.set_style("white")
    sns.set_context("paper", font_scale=1.5)
    sns.set_style("ticks")

    #Reading the Excel File
    df = pd.ExcelFile(workbook_name)

    #Creating the sheet arrays
    p_sheets = worksheet_array[1::2]
    print(p_sheets)

    f_sheets = worksheet_array[::2]

    #headings = [r'N III $\lambda$4641', r'He II $\lambda$4686', r'He II $\lambda$4859', r'He II $\lambda$5411',
    #            r'He II $\lambda$6560', r'N IV $\lambda$7103-7129']
    
    headings = worksheet_array[::2][-4]

    heights = bisect_heights_array[::2]

    fig, axes = plt.subplots(no_rows, 2, figsize=(15,18), sharex=False)


    #Cycle through the sheets
    for i in range(0,len(p_sheets)):
    
        p_data = pd.read_excel(df, str(p_sheets[i]))
        p_data = p_data.sort_values('Phase')
        p_data = p_data.reset_index()
        del p_data['index']
    
        f_data = pd.read_excel(df, str(f_sheets[i]))
        f_data = pd.DataFrame(f_data)
        f_data = f_data.sort_values('Phase')
        f_data = f_data.reset_index()
        del f_data['index']
    
        #Create a frame for the regression
        p_reg_frame = Table(names=('Slope','Std_err'), dtype=('f8','f8'))
        f_reg_frame = Table(names=('Slope','Std_err'), dtype=('f8','f8'))
    
        these_heights = heights[i]
    
        for k in range(0,no_of_dates):
            #Get the wavelengths that we want to find the slope for
            p_wavelengths = list((p_data['Height1'][k], p_data['Height2'][k], p_data['Height3'][k], p_data['Height4'][k],
                        p_data['Height5'][k], p_data['Height6'][k], p_data['Height7'][k], p_data['Height8'][k]))
        
            #Calculate regression
            slope, intercept, rvalue, pvalue, stderr = stats.linregress(these_heights, p_wavelengths)
        
            newrow = np.array([slope, stderr])
            p_reg_frame.add_row(newrow)
        
            #Same thing for flux
            f_wavelengths = list((f_data['Height1'][k], f_data['Height2'][k], f_data['Height3'][k], f_data['Height4'][k],
                        f_data['Height5'][k], f_data['Height6'][k], f_data['Height7'][k], f_data['Height8'][k]))
    
            slope, intercept, rvalue, pvalue, stderr = stats.linregress(these_heights, f_wavelengths)
        
            newrow = np.array([slope, stderr])
            f_reg_frame.add_row(newrow)
    
        p_average = np.average(p_reg_frame['Slope'], weights=p_reg_frame['Std_err'])
        p_average_err = np.std(p_reg_frame['Slope'])
        f_average = np.average(f_reg_frame['Slope'], weights=f_reg_frame['Std_err'])
        f_average_err = np.std(f_reg_frame['Slope'])
    
        ax = plt.subplot(no_rows,2,i+1)
        ax.errorbar(tools.phase_wrap(phases), tools.wrap(p_reg_frame['Slope']), 
                yerr=tools.wrap(p_reg_frame['Std_err']), xerr=None, capsize=3, color='g', 
                label='P-Flux, Mean: '+str(np.round(p_average, 1))+' $\pm$ '+str(np.round(p_average_err, 1)))
        ax.errorbar(tools.phase_wrap(phases), tools.wrap(f_reg_frame['Slope']), 
                yerr=tools.wrap(f_reg_frame['Std_err']), xerr=None, capsize=3, color='b', 
                label='Flux, Mean: '+str(np.round(f_average, 1))+' $\pm$ '+str(np.round(f_average_err, 1)))
        ax.fill_between(tools.phase_wrap(phases), 
                    tools.wrap(p_reg_frame['Slope'])-tools.wrap(p_reg_frame['Std_err']),
                    tools.wrap(p_reg_frame['Slope'])+tools.wrap(p_reg_frame['Std_err']), alpha=0.3, color='g')
        ax.fill_between(tools.phase_wrap(phases), 
                    tools.wrap(f_reg_frame['Slope'])-tools.wrap(f_reg_frame['Std_err']),
                    tools.wrap(f_reg_frame['Slope'])+tools.wrap(f_reg_frame['Std_err']), alpha=0.3, color='b')
    
        #Plot Features
        ax.set_xlim(-0.2, 1.2)
        #ax.set_ylim(ystarts[i],yends[i])
        ax.axhline(0, linestyle='--', color='gray')
        ax.set_ylabel('Asymmetry', fontsize=14)
        ax.set_xlabel('Phase', fontsize=14)
        plt.legend(loc='upper right', fontsize=12)
        plt.title(headings[i])
        
        plt.minorticks_on()
        plt.tick_params(direction="in",which='both')
        plt.tick_params(axis="both",which='both',top=True,right=True,labelleft=True,labelbottom=True)

    if len(lines)%2==1:
        ax1 = plt.subplot(no_rows,2,len(lines)+1)
        ax1.axis('off')
            
    #Titles
    plt.suptitle(str(star)+' Flux and P-Flux Asymmetry'+'\n'+str(form),fontsize=20)
        
    plt.subplots_adjust(hspace=0.5)
        
    plt.savefig(str(star)+'_Flux_P_Flux_Line_Asymmetry_'+str(form)+'.png', dpi=300)
        
    plt.show()