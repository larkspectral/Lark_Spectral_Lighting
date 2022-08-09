# Decompose an analysis period to lists of months, days, hours, HOYs, round HOYs and lines of wea.

# Lark Spectral Lighting (v0.0.1, v0.0.2 and v1.0) is a collaboration of University of Washington and ZGF Architects LLP
# Authors Dr. Mehlika Inanici, Marty Brennan & Ed Clark
# Lark v2.0 is a collaboration of EPFL, Oregon State University, and Eindhoven University of Technology
# Authors Dr. Clotilde Pierson & Myrta Gkaintatzi-Masouti
# Copyright 2015-2022 Mehlika Inanici, Ph.D. (University of Washington) and ZGF Architects LLP
# Copyright 2022 Clotilde Pierson, Ph.D. (EPFL, Oregon State University) and Myrta Gkaintatzi-Masouti, M.Sc. (Eindhoven University of Technology)
# Licensed under The Modified 3-Clause BSD License (the "License");
# You may obtain a copy of the License at
# https://opensource.org/licenses/BSD-3-Clause

"""
Use this to find months, days and hours from an analysis period.
-
Provided by Lark 2.0.0

    Inputs:
        analysisPeriod: Analysis period
        timestep: Timestep within the hour in minutes. This should be an integer betweeen 1 and 60 (60 = hourly timestep, 1 = timestep every minute).
    Output:
        months: List of month numbers
        days: List of day numbers
        hours: List of hour numbers
        HOY: List of hours of the year. If the timestep is less than 60 (subhourly) the hours will have decimals
        HOYround: List of hours of the year rounded (the above output rounded)
        weaLines: The number of the lines from a wea (weather file) that correspond to the analysis period (hourly data of diffuse hor. irradiance and direct normal irradiance start at line 7 of the wea).
"""

__author__ = "mgkaintatzi-masouti"
__version__ = "2021.10.15"

ghenv.Component.Name = "Lark Analysis Period Decomposition"
ghenv.Component.NickName = 'Decompose Period'
ghenv.Component.Message = '2.0.0'
ghenv.Component.Category = "Lark"
ghenv.Component.SubCategory = "Timeseries"

import datetime



#define a range function
def range1(start, end):
    return range(start, end+1)
    # range function including the end in the range



# check all inputs
error_list = []
inputs = [analysisPeriod, timestep]
inputs_name = ["analysisPeriod", "timestep"]

for idx, val in enumerate (inputs):
    if val == None or val == []:
        error_list.append(inputs_name[idx])

if len(error_list) != 0:
    check = "error"
else:
    check = 1

if check == "error":
    print "Warning! Connect the following inputs:" 
    print error_list



# get months, days, hours, HOYs, round HOYs and lines of wea as lists
if check != "error":
    
    x = analysisPeriod
    step = timestep
    
    months = []
    days = []
    hours = []
    minutes = []
    
    n = int(round(60/step)) # minutes
    
    dt0 = datetime.datetime(2010, 1, 1, 00, 00, 00) # dt0 is the start of the year (it doesn't matter which year we use)
    HOY = []
    HOYround = []
    for i in range1(x[0][0], x[1][0]): # for all months
        for j in range1(x[0][1], x[1][1]): # for all days
            for k in range1(x[0][2], x[1][2]): # for all hours
                for l in range(n): # for all minutes
                    if not(i == 2 and (j == 29 or j == 30 or j == 31)):  # there is no February 29,30,31
                        if not((i == 4 or i == 6 or i==9 or i == 11) and (j ==31)): # there is no April,June,September,November 31
                            months.append(i)
                            days.append(j)
                            minute = (l*step)/60 # minutes as a fraction of the hour
                            minutes.append(minute) 
                            hour = k + minute # hour including fractions
                            hours.append(hour)
                            dt = datetime.datetime(2010, i, j, k, int(l*step), 00)
                            dt_round = datetime.datetime(2010, i, j, k, 00, 00) # without the minutes
                            HOY.append((dt-dt0).days*24 + (dt-dt0).seconds/3600) # hour of the year (calculated from the difference between the time and the first hour of the year)
                            HOYround.append((dt_round-dt0).days*24 + (dt_round-dt0).seconds/3600)
    
    weaLines = []
    for i in HOY:
        weaLines.append(i*(60/step) + 7) # the first 6 lines in the wea are text
