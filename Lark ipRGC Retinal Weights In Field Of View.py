# Apply ipRGC retinal coefficients to different parts of the field of view 

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
Use this component to apply ipRGC retinal coefficients to different parts of the field of view.  
-
Before using this component place the 4 .hdr mask files (1_upper_inner.hdr, 2_lower_inner.hdr, 3_upper_outer.hdr, 4_lower_outer.hdr) in the lark folder (C:\lark).
-
More information about the retinal weighting can be found in this PhD thesis:
Khademagha, P. 2021, “Light directionality in design of healthy offices”, https://research.tue.nl/en/publications/light-directionality-in-design-of-healthy-offices-exploration-of-
-
Provided by Lark 2.0.0

    Args:
        picture: filepath to 3-channel HDR image
        resolution: pixel resolution of the 3-channel HDR image
        RunPcomb: Set Boolean to True to apply weighting
        filename: optional name for the output HDR image
    Returns:
        out: warnings and errors
        current_dir: current working folder 
        weighted_pic: filepath to ipRGC retinal weighted HDR image
"""

__author__ = "cpierson"
__version__ = "2022.07.25"

ghenv.Component.Name = "Lark ipRGC Retinal Weights In Field Of View"
ghenv.Component.NickName = 'ipRGC FOV Weighting'
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
path_masks = 'C:\lark'
os.chdir(path)
#print out current directory
current_dir = path



#check all inputs
error_list = []
inputs = [picture,resolution,RunPcomb]
inputs_name = ["picture","resolution","RunPcomb"]

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



#if no error in inputs, apply the ipRGC retinal weighting coefficients through masks
if check != "error":
    extension = "weighted.hdr"
    picname = "%s%s" %(filename,extension)

    #resize HDR masks based on size of the HDR image that they have to be applied to
    if resolution != 512:
        v0 = "pfilt -1 -x " + str(int(resolution)) + " -y " + str(int(resolution)) + " " + path_masks + "\\" + "1_upper_inner.hdr > " + path_masks + "\\" + "1_upper_inner_Temp.hdr"
        v1 = "pfilt -1 -x " + str(int(resolution)) + " -y " + str(int(resolution)) + " " + path_masks + "\\" + "2_lower_inner.hdr > " + path_masks + "\\" + "2_lower_inner_Temp.hdr"
        v2 = "pfilt -1 -x " + str(int(resolution)) + " -y " + str(int(resolution)) + " " + path_masks + "\\" + "3_upper_outer.hdr > " + path_masks + "\\" + "3_upper_outer_Temp.hdr"
        v3 = "pfilt -1 -x " + str(int(resolution)) + " -y " + str(int(resolution)) + " " + path_masks + "\\" + "4_lower_outer.hdr > " + path_masks + "\\" + "4_lower_outer_Temp.hdr"
        mask1 = "1_upper_inner_Temp.hdr"
        mask2 = "2_lower_inner_Temp.hdr"
        mask3 = "3_upper_outer_Temp.hdr"
        mask4 = "4_lower_outer_Temp.hdr"
    else:
        v0 = ''
        v1 = ''
        v2 = ''
        v3 = ''
        mask1 = "1_upper_inner.hdr"
        mask2 = "2_lower_inner.hdr"
        mask3 = "3_upper_outer.hdr"
        mask4 = "4_lower_outer.hdr"

    #apply ipRGC retinal weighting coefficient by masked area
    v4 =  "pcomb -h -e " """ "thresh=if((ri(2)+bi(2)+gi(2)-0.01),2.06,0)" -e "ro=thresh*ri(1);go=thresh*gi(1);bo=thresh*bi(1)" """ + "-o " + picture + " " + path_masks + "\\" + mask1 + " > " + "Temp_upper_inner_masked.hdr"
    v5 =  "pcomb -h -e " """ "thresh=if((ri(2)+bi(2)+gi(2)-0.01),1.37,0)" -e "ro=thresh*ri(1);go=thresh*gi(1);bo=thresh*bi(1)" """ + "-o " + picture + " " + path_masks + "\\" + mask3 + " > " + "Temp_upper_outer_masked.hdr"
    v6 =  "pcomb -h -e " """ "thresh=if((ri(2)+bi(2)+gi(2)-0.01),0.34,0)" -e "ro=thresh*ri(1);go=thresh*gi(1);bo=thresh*bi(1)" """ + "-o " + picture + " " + path_masks + "\\" + mask2 + " > " + "Temp_lower_inner_masked.hdr"
    v7 =  "pcomb -h -e " """ "thresh=if((ri(2)+bi(2)+gi(2)-0.01),0.23,0)" -e "ro=thresh*ri(1);go=thresh*gi(1);bo=thresh*bi(1)" """ + "-o " + picture + " " + path_masks + "\\" + mask4 + " > " + "Temp_lower_outer_masked.hdr"

    #sum 4 parts of the field of view into one ipRGC retinal weighted HDR image 
    vtotal = "pcomb -h -e " """ "ro=ri(1)+ri(2)+ri(3)+ri(4);go=gi(1)+gi(2)+gi(3)+gi(4);bo=bi(1)+bi(2)+bi(3)+bi(4)" """ + "-o " + "Temp_upper_inner_masked.hdr Temp_upper_outer_masked.hdr Temp_lower_inner_masked.hdr Temp_lower_outer_masked.hdr" + " > " + picname

    #delete temporary images
    tempdel1 = "del *Temp* "

    #create batch file
    batch = open("batchfile.bat", "w")
    batch.write(v0 + '\n' * 3 + v1 + '\n' * 3 + v2 + '\n' * 3 + v3 + '\n' * 3 + v4 + '\n' * 3 + v5 + '\n' * 3 + v6 + '\n' * 3 + v7 + '\n' * 3 + vtotal + '\n' * 3 + tempdel1)
    batch.close()

    #run batch file
    if RunPcomb != True:
        pass
    else:
        runbatch = Popen("batchfile.bat", cwd=path)
        stdout, stderr = runbatch.communicate()
        
        #print filepath to output picture
        weighted_pic = os.getcwd() + "\\" + picname
