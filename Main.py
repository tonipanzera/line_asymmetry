#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 19 17:01:15 2021

@author: ToniPanzera
"""

import get_info
import get_phases
import create_excel
import Asymmetry_Plots

def Main():

    get_info.get_initial_info()
    get_phases.get_phases()
    create_excel.get_bisects()
    create_excel.make_excel()
    create_excel.get_plotting_info()
    Asymmetry_Plots.plot_asymmetry()
    
Main()