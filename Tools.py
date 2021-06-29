#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 15:02:43 2020

@author: ToniPanzera
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import astropy.table as table
import seaborn as sns

sns.set()
sns.set_style("white")
sns.set_context("paper")
sns.set_style("ticks")

'''A set of functions to plot various line and continuum behaviours of Wolf-Rayet Binary Stars'''

#Function to convert q to percentage
def get_percent_q(q):
    q_percent = q*100
    return q_percent

def get_percent_u(u):
    u_percent = u*100
    return u_percent

#Function to calculate the position angle given q and u values. Returns a degree value
def get_pa(q,u, name='PA'):
    pa = np.rad2deg(0.5*np.arctan2(u,q))
    i = 0
    for angle in pa:
        if angle < 0:
            pa[i] = angle + 180
            i += 1
    return pa

#Function to calculate position angle error
def calc_pa_err(q, u, qerr, uerr, name='PAerr'):
    p = np.sqrt(q**2 + u **2)
    return table.column((1 / p**2) * np.sqrt((q * qerr)**2 + (u * uerr)**2), name=name)

#Function to calculate total polarisation (p) given q and u
def get_p(q,u, name='P'):
    p = np.sqrt(q**2+u**2)
    return p

#Wraps the phase so that it runs from -0.2-1.2 instead of 0-1
def phase_wrap(a):
    return np.concatenate((a-1,a,a+1))

#Wraps data to that it is in line with the phase wrapping
def wrap(c):
    return np.concatenate((c,c,c))

#Function to calculate the BME fit
def BME_func_full(phase, q0, q3, q4):
    return q0 + q3*np.cos(4*np.pi*phase) + q4*np.sin(4*np.pi*phase)

#Function to plot the BME fit
def BME_fit_plot(BME_func_full, phase, fit_data, fit_data_error):
    fit, cov = curve_fit(BME_func_full, phase, fit_data, 
                sigma = np.ones(len(fit_data))*fit_data_error, absolute_sigma = True)
    phase_range = np.linspace(-0.2, 1.2)
    fit_result = BME_func_full(phase_range, *fit)
    return plt.plot(phase_range, fit_result, color='gray', label = 'BME FIT')

#Function to rotate q by the desired position angle
def q_rot(q,u,pa):
    return q*np.cos(np.deg2rad(2*int(pa)))+u*np.sin(np.deg2rad(2*int(pa)))

#Function to rotate u by the desired position angle
def u_rot(q,u,pa):
    return -q*np.sin(np.deg2rad(2*int(pa)))+u*np.cos(np.deg2rad(2*int(pa)))

#Function to calculate angle from a regression line
def get_reg_angle(slope):
    a = np.rad2deg(0.5*(np.pi+np.tan(slope)))
    return a

#Function to calculate x, based on parameters from the BME fit
def calc_x(q0, q3, q4, u0, u3, u4):
    x = ((u3+q4)**2+(u4-q3)**2)/((u4+q3)**2+(u3-q4)**2)
    return x

#Function to calculate the inclination angle
def calc_i(x):
    i = np.rad2deg(np.arccos((x**0.25 - 1)/(-(x**0.25) - 1)))
    return i

def calc_omega(q3,q4,u3,u4,i):
    
    T = (u3+q4)/(1+np.cos(i)**2-2*np.cos(i))
    B = (u4-q3)/(1+np.cos(i)**2-2*np.cos(i))
    C = (u4+q3)/(1+np.cos(1)**2+2*np.cos(i))
    D = (q4-u3)/(1+np.cos(1)**2+2*np.cos(i))
    
    omega = np.arctan((B+C)/(D+T))
    
    return omega

def calc_lambda_2(q3,q4, i, omega):
    
    L = (1+np.cos(i)**2)*np.cos(omega)
    M = 2*np.cos(i)*np.sin(omega)
    
    lambda_2 = 0.5*np.arctan((q3*M+q4*L)/(q4*M-q3*L))
    
    return lambda_2

#Convert wavelength to velocity
def get_rv(lamda, lamda0):
    lamda0 = lamda0*np.ones(len(lamda))
    c = 299792.458*np.ones(len(lamda))
    v = (lamda-lamda0)*c/lamda0
    return v

#Calculates a moving slope for a group pf points
#Num = how many points you want in each slope calculation, so 10 means doing the slope from 0-9, then 1-10, etc.
#Data are the y-values. You can modify the function to use x-values to calculate change in x; I'm just using
    #the indices here because of the data I designed this for
#Start_idx is where in your data you want to start; you can make these 0 to the end if you want to do the whole thing
#End_idx is where you want to end
#Jump is how far you want to jump ahead each time, so if num=10 and jump = 5, it'll calculate the slope from
    #0-10, then 5-15, and so on.
def moving_slope(data, num, jump, start_idx, end_idx):
    slope_array = []
    for i in range(start_idx, end_idx-num):
        start = i
        end = i+num
        slope = (data[end]-data[start])/(end-start)
        slope_array.append(slope)
        i+=jump
    return slope_array
    
    
        
    