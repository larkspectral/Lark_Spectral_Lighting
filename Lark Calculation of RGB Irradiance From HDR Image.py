# Get RGB irradiance values from an HDR luminance image 

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

# Component updated by Bo Jung for Lark v3.0 (2023-08-15):
# Updated option to add where the text file for RGB values are saved (default is 'C:\lark\\temp').

"""
Use this component to calculate RGB irradiance values from an HDR luminance image
-
Provided by Lark 3.0.0

    Args:
        picture: filepath to 3-channel HDR image
        filename: optional name for the txt file containing RGB values
        filepath: optional directory for the txt file containing RGB values
    Returns:
        out: warnings and errors
        RGB_values: RGB values calculated from HDR image
"""

__author__ = "Bo Jung"
__version__ = "2023.08.15"

ghenv.Component.Name = "Lark Calculation of RGB Irradiance From HDR Image v3"
ghenv.Component.NickName = 'RGB From HDR'
ghenv.Component.Message = '3.0.0'
ghenv.Component.Category = "Lark"
ghenv.Component.SubCategory = "Point-in-time"

import rhinoscriptsyntax as rs
import os
import re
from subprocess import Popen



#make lark directory if none exists
path = 'C:\lark\\temp'
if os.path.isdir(path) != True: 
    os.makedirs(path)
else:
    pass
path_masks = 'C:\lark'
os.chdir(path)

if filepath == None or []:        
    filepath = path
    

#print out current directory
current_dir = filepath


#check all inputs
error_list = []
inputs = [picture]
inputs_name = ["picture"]

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

if filename == None:        
    filename = ""



#extract RGB irradiance values from HDR image
if check != "error":
    extension = "_RGBvalues.txt"
    name = "%s%s" %(filename,extension)

    #Check view of masked HDR image
    v1 =  "vwright -vf " + picture + " V > " +  "vwr.cal"
    print(v1)

    #Calculate the RGB values of the masked HDR image
    v2 =  "pcomb -h -f "  +  filepath + "vwr.cal" + " -e " """ "dot=Dx(1)*Vdx+Dy(1)*Vdy+Dz(1)*Vdz" -e "ro=if(dot,S(1)*dot*ri(1),0);go=if(dot,S(1)*dot*gi(1),0);bo=if(dot,S(1)*dot*bi(1),0)" """ + "-o " + picture + " | pvalue -h -H -df | total -if3 > " + name

    #Delete temporary file
    tempdel1 = "del *vwr* "

    #Create batch file
    batch_loc = filepath + "\\batchfile.bat"
    batch = open(batch_loc, "w")
    batch.write(v1 + '\n' * 3 + v2 + '\n' * 3 + tempdel1)
    batch.close()

    #Run batch file
    runbatch = Popen("batchfile.bat", cwd=filepath)
    stdout, stderr = runbatch.communicate()
    #Print filepath to RGB values file
    RGB_values = filepath + "\\" + name
