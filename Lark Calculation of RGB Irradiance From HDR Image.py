# Get RGB irradiance values from an HDR luminance image 

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
Use this component to calculate RGB irradiance values from an HDR luminance image
-
Provided by Lark 2.0.0

    Args:
        picture: filepath to 3-channel HDR image
        filename: optional name for the txt file containing RGB values
    Returns:
        out: warnings and errors
        RGB_values: RGB values calculated from HDR image
"""

__author__ = "cpierson"
__version__ = "2022.05.06"

ghenv.Component.Name = "Lark Calculation of RGB Irradiance From HDR Image"
ghenv.Component.NickName = 'RGB From HDR'
ghenv.Component.Message = '2.0.0'
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
os.chdir(path)



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
    extension = "RGBvalues.txt"
    name = "%s%s" %(filename,extension)

    #Check view of masked HDR image
    v1 =  "vwright -vf " + picture + " V > " +  "vwr.cal"

    #Calculate the RGB values of the masked HDR image
    v2 =  "pcomb -h -f "  +  "vwr.cal" + " -e " """ "dot=Dx(1)*Vdx+Dy(1)*Vdy+Dz(1)*Vdz" -e "ro=if(dot,S(1)*dot*ri(1),0);go=if(dot,S(1)*dot*gi(1),0);bo=if(dot,S(1)*dot*bi(1),0)" """ + "-o " + picture + " | pvalue -h -H -df | total -if3 > " + name

    #Delete temporary file
    tempdel1 = "del *vwr* "

    #Create batch file
    batch = open("batchfile.bat", "w")
    batch.write(v1 + '\n' * 3 + v2 + '\n' * 3 + tempdel1)
    batch.close()

    #Run batch file
    runbatch = Popen("batchfile.bat", cwd=path)
    stdout, stderr = runbatch.communicate()
    #Print filepath to RGB values file
    RGB_values = os.getcwd() + "\\" + name
