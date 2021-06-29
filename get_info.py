#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 22 11:59:14 2021

@author: ToniPanzera
"""

def get_initial_info():
    
    global star
    global period
    global e0
    global lines
    global form
    global pysplot_excels
    global no_of_dates
    global no_bisects
    global datapath
    
    #Get initial inputs: what the star is, and how many lines have been done, and how the data is binned, etc.
    star = input('What is the name of the star? ')

    period = input('What is the period of the star? ')

    e0 = input('What is the E0 of the star? ')
    
    datapath = input('What is the datapath that points to the folder containing your date folders of the format YYYMMDD? ')

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
    
    return star, period, e0, lines, form, pysplot_excels, no_of_dates, no_bisects, datapath


