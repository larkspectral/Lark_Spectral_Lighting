# Define the analysis period to be simulated.

# Lark Spectral Lighting (v0.0.1, v0.0.2 and v1.0) is a collaboration of University of Washington and ZGF Architects LLP
# Authors Dr. Mehlika Inanici, Marty Brennan & Ed Clark
# Lark v2.0 is a collaboration of EPFL, Oregon State University, and Eindhoven University of Technology
# Authors Dr. Clotilde Pierson & Myrta Gkaintatzi-Masouti
# Lark Spectral Lighting v3.0 is a collaboration of University of Washington and ZGF Architects LLP
# Authors Bo Jung, Dr. Mehlika Inanici, Marty Brennan, and Zining Cheng 
# Copyright 2015-2022 University of Washington (Mehlika Inanici, Ph.D.) and ZGF Architects LLP
# Copyright 2022 EPFL, Oregon State University (Clotilde Pierson, Ph.D.), and Eindhoven University of Technology (Myrta Gkaintatzi-Masouti, M.Sc.)
# Copyright 2023 University of Washington (Bo Jung, M.Sc., Mehlika Inanici, Ph.D., Zining Cheng, M.Sc.) and ZGF Architects LLP
# Licensed under The Modified 3-Clause BSD License (the "License");
# You may obtain a copy of the License at
# https://opensource.org/licenses/BSD-3-Clause

"""
Create an analysis period.
-
Provided by Lark 3.0.0

    Inputs:
        fromMonth: Start month
        fromDay: Start day
        fromHour: Start hour
        toMonth: End month
        toDay: End day
        toHour: End hour
    Output:
        analysisPeriod: Analysis period
"""

__author__ = "mgkaintatzi-masouti"
__version__ = "2021.10.15"

ghenv.Component.Name = "Lark Analysis Period Definition v3"
ghenv.Component.NickName = 'Define Period'
ghenv.Component.Message = '3.0.0'
ghenv.Component.Category = "Lark"
ghenv.Component.SubCategory = "Timeseries"

from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML



# check for missing inputs
error_list = []
inputs = [fromMonth, fromDay, fromHour, toMonth, toDay, toHour]
inputs_name = ["fromMonth", "fromDay", "fromHour", "toMonth", "toDay", "toHour"]

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



#create analysis period
if check != "error":
    
    # check if months, days, hours are correct
    if fromMonth <1 or fromMonth>12 or toMonth<1 or toMonth>12:
        ghenv.Component.AddRuntimeMessage(RML.Error, "Month should be between 1 and 12")
    if fromDay <1 or fromDay>31 or toDay<1 or toDay>31:
        ghenv.Component.AddRuntimeMessage(RML.Error, "Day should be between 1 and 31")
    if fromHour<0 or fromHour>23 or toHour<0 or toHour>23:
        ghenv.Component.AddRuntimeMessage(RML.Error, "Hour should be between 0 and 23")
    
    # create analysis period
    analysisPeriod = ((int(fromMonth), int(fromDay), int(fromHour)), ((int(toMonth), int(toDay), int(toHour))))
