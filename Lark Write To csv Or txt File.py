# Write results to file.

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
Write data to csv or txt file
-
Provided by Lark 2.0.0

    Inputs:
        folder: folder path
        filename: name of the file to write
        extension: [1 = .csv] [2 = .txt]
        data: data to write
        headings: optional column headings for the data
        write: boolean toggle to run this component
    Output:
        file: file path
"""

__author__ = "mgkaintatzi-masouti"
__version__ = "2021.09.15"

ghenv.Component.Name = "Lark Write To csv Or txt File"
ghenv.Component.NickName = "File Writer"
ghenv.Component.Message = '2.0.0'
ghenv.Component.Category = "Lark"
ghenv.Component.SubCategory = "Utilities"

import os
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML



#check all inputs
error_list = []
inputs = [folder, filename, extension, data, write]
inputs_name = ["folder", "filename", "extension", "data", "write"]

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



#write to file
if check != "error":
    
    #make directory if none exists
    if os.path.isdir(folder) != True: 
        os.makedirs(folder)
    else:
        pass
    
    if write == True:
        if folder and filename and data: 
            folder.replace("\\", "/")
            if extension == 1:
                file = folder + "\\" + filename + '.csv'
            elif extension == 2:
                file = folder + "\\" + filename + '.txt'
            
            f = open(file,"w")
            if headings:
                f.write(headings +'\n')
            for d in data:
                f.write(d + '\n')
            f.close()
