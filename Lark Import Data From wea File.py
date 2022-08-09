# Import data from wea file.

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
Import data from a wea file.
-
Provided by Lark 2.0.0

    Inputs:
        wea: The path to a wea file
        RunIt: A boolean toggle to run this component
    Output:
        months: Months
        days: Days
        hours: Hours
        DNI: Direct normal irradiance
        DHI: Diffuse horizontal irradiance
"""

__author__ = "mgkaintatzimasouti" 
__version__ = "2021.11.15"

ghenv.Component.Name = "Lark Import Data From wea File"
ghenv.Component.NickName = "Import wea"
ghenv.Component.Message = '2.0.0'
ghenv.Component.Category = "Lark"
ghenv.Component.SubCategory = "Timeseries"



#read data from wea file
if RunIt == True:
    
    f = open(wea,"r")
    lines = f.readlines()[6:]
    
    months = []
    days = []
    hours = []
    DNI = []
    DHI = []
    for line in lines:
        months.append(line.split()[0])
        days.append(line.split()[1])
        hours.append(line.split()[2])
        DNI.append(line.split()[3])
        DHI.append(line.split()[4])
    
    f.close()
