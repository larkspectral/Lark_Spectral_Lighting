# Generate a wea file for a sub-annual simulation period.

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
Use this to generate a new wea file with selected lines for a Radiance simulation.
-
Provided by Lark 3.0.0

    Inputs:
        wea: The path to a wea file
        weaLines: The numbers of the lines in the input wea file to write to the new wea file
        RunIt: A boolean toggle to run this component
    Output:
        weaAnalysis: The output wea file containing only the selected lines
"""

__author__ = "mgkaintatzi-masouti"
__version__ = "2021.10.15"

ghenv.Component.Name = "Lark Analyze wea File v3"
ghenv.Component.NickName = 'wea Analysis'
ghenv.Component.Message = '3.0.0'
ghenv.Component.Category = "Lark"
ghenv.Component.SubCategory = "Timeseries"



# check all inputs
error_list = []
inputs = [wea, weaLines]
inputs_name = ["wea", "weaLines"]

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



#prepare a new wea file
if check != "error":
    
    if RunIt == True:
        
        # read all lines of the wea file
        f = open(wea,"r")
        lines = f.readlines()
        f.close()
        
        # write selected lines in new wea file
        weaAnalysis = wea.replace('.wea', '_analysis.wea')
        f = open(weaAnalysis,"w")
        for i in range(len(lines)):
            if (i+1) <= 6: # the first 6 lines are the place, lat,long ... information
                f.write(lines[i])
            elif (i+1) in weaLines:
                f.write(lines[i])
        f.close()
