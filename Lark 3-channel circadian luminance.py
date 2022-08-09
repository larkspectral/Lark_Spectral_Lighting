# Evaluate circadian and photopic metrics from 3-channel simulations 

# Lark Spectral Lighting (v0.0.1, v0.0.2 and v1.0) is a collaboration of University of Washington and ZGF Architects LLP
# Authors Dr. Mehlika Inanici, Marty Brennan & Ed Clark
# Lark v2.0 is a collaboration of EPFL, Oregon State University, and Eindhoven University of Technology
# Authors Dr. Clotilde Pierson & Myrta Gkaintatzi-Masouti
# Copyright 2015-2022 Mehlika Inanici, Ph.D. (University of Washington) and ZGF Architects LLP
# Copyright 2022 Clotilde Pierson, Ph.D. (EPFL, Oregon State University) and Myrta Gkaintatzi-Masouti, M.Sc. (Eindhoven University of Technology)
# Licensed under The Modified 3-Clause BSD License (the "License");
# You may obtain a copy of the License at
# https://opensource.org/licenses/BSD-3-Clause

# Component updated by Dr. Mehlika Inanici, Marty Brennan & Ed Clark for Lark v1.0 (2020-11-15):
# Updated Lucas coefficients 

# Component updated by Dr. Mehlika Inanici, Marty Brennan & Ed Clark for Lark v1.0 (2022-04-14):
# Updated license, removed Rea metrics, Lucas curve now reports Equivalent Melanopic Lux (EML), luminous efficacy coefficient is scaled at 179.  

# Component updated by Dr. Clotilde Pierson (2022-05-10) but not used in Lark 2.0 templates:
# Corrected photopic coefficients in image-based and point-based simulation post-process
# Corrected Lucas circadian coefficients in point-based simulation post-process

"""
Use this component to evaluate 3-channel circadian response.  
-
Provided by Lark 2.0.0

    Args:
        picture: filepath to 3-channel image [rgb]
        irradiance: filepath to 3-channel irradiance output (example .dat, .res)
        RunPcomb: Set Boolean to True to run lark
        Directory: optional subfolder name (default folder is C:\lark)
    Returns:
        out: warnings and errors
        current_dir: current working folder 
        cir_Lucas_pic:filepath to circadian luminance picture [Lucas curve]
        cir_Lucas_lux: list of circadian illuminance [Equivalent Melanopic Lux - EML]
        photopic_pic: filepath to photopic luminance picture
        photopic_lux: list of photopic illuminance
"""

ghenv.Component.Name = "Lark 3-channel Circadian Luminance v2"
ghenv.Component.NickName = '3-channel Luminance'
ghenv.Component.Message = '2.0.0'
ghenv.Component.Category = "Lark"
ghenv.Component.SubCategory = "Basic Lark"

import os
from subprocess import Popen



#check all inputs
error_list = []
inputs = [picture,irradiance,RunPcomb]
inputs_name = ["picture","irradiance","RunPcomb"]

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



#make lark directory if none exists
basedir = 'C:\lark'
if os.path.isdir(basedir) != True: 
    os.makedirs(basedir)
else:
    pass

#create path to Directory if provided
if Directory == None:
    path = basedir
else:
    path = os.path.join (basedir, Directory)

#create folder if Directory is provided
if os.path.isdir(path) != True: 
    os.makedirs(path)
else:
    pass
os.chdir(path)

#print out current directory
current_dir = path



#process image
if picture != None:
    
    #Sum (radiometric values *  photopic v lambda action curve)
    v1 = "pcomb -h -e " """ "ro=ri(1) * 0.2685 ;go=gi(1) * 0.6694 ;bo=bi(1) * 0.0621" """ + "-o " + picture + " > vtemp.hdr"
    vtotal = "pcomb -h -e" """ "ro=ri(1)+ gi(1) + bi(1);go=ri(1) + gi(1) + bi(1);bo=ri(1) + gi(1) + bi(1)" """ + "-o vtemp.hdr > Calc3Lum.hdr"
    
    #Sum (radiometric values * Lucas circadian action curve)
    c_l = "pcomb  -e " """  "ro=ri(1) * 0.0022 ;go=gi(1) * 0.4021 ;bo=bi(1) * 0.5957"  """ + picture + " > " + "c_l_temp.hdr" 
    c_l_total = "pcomb  -e " """  "ro=ri(1)+ gi(1) + bi(1) ;go=ri(1) + gi(1) + bi(1) ;bo=ri(1) + gi(1) + bi(1)" """ + "-o c_l_temp.hdr > Calc3Cir.hdr"
    
    tempdel = "del *temp*"
    
    batch = open("batchfile3.bat", "w")
    batch.write(v1 + '\n' + vtotal + '\n' + c_l + '\n' + c_l_total + '\n' + tempdel)
    batch.close()
    
    if RunPcomb != True:
        print "Set RunPcomb to true"
        pass
    else:
        runbatch = Popen("batchfile3.bat", cwd=path)
        stdout, stderr = runbatch.communicate()
    
    #print filepaths for output pictures
    photopic_pic = os.getcwd() + "\\" + "Calc3Lum.hdr"
    cir_Lucas_pic = os.getcwd() + "\\" + "Calc3Cir.hdr"



#process irradiance
if irradiance != None:
    
    #calculate circadian and photopic lux based on 3-channel irradiance
    #outputs work for different Radiance extensions (.dat,.res)
    f = open(irradiance, 'r')
    
    #create output tables
    result_pho = []
    result_cir_l = []
    
    v = open('photopic_lux.txt', 'w')
    c_l = open('cir_Lucas_lux.txt', 'w')
    
    #loop on each row for photopic and circadian calculations
    for line in f:
        R,G,B = line.split()[0:3]
        
        voutput = 179 * (0.2685 * float(R) + 0.6694 * float(G) + 0.0621 * float(B))   #photopic output
        c_loutput = 179 * ( 0.0022 * float (R) + 0.4021 * float (G) + 0.5957 * float (B))  #circadian output
        
        v.write(str(voutput) + '\n')
        c_l.write(str(c_loutput) + '\n')
        
        result_pho.append(voutput)
        result_cir_l.append(c_loutput)
    
    #assign output tables
    photopic_lux = result_pho
    cir_Lucas_lux = result_cir_l
    
    f.close()
    v.close()
    c_l.close()
