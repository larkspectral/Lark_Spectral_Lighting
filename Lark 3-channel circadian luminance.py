# Evaluate circadian and photopic metrics from 3-channel simulations 

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

# Component updated by Dr. Mehlika Inanici, Marty Brennan & Ed Clark for Lark v1.0 (2020-11-15):
# Updated Lucas coefficients 

# Component updated by Dr. Mehlika Inanici, Marty Brennan & Ed Clark for Lark v1.0 (2022-04-14):
# Updated license, removed Rea metrics, Lucas curve now reports Equivalent Melanopic Lux (EML), luminous efficacy coefficient is scaled at 179.  

# Component updated by Dr. Clotilde Pierson (2022-05-10) but not used in Lark 2.0 templates:
# Corrected photopic coefficients in image-based and point-based simulation post-process
# Corrected Lucas circadian coefficients in point-based simulation post-process

# Component updated by Bo Jung for Lark v3.0 (2023-07-05):
# Updated coefficients for rgb.
# Modified output name (cir_Lucas_pic and cir_Lucas_lux changed to melanopic_pic and melanopic_lux respectively).

"""
Use this component to evaluate 3-channel circadian response.  
-
Provided by Lark 3.0.0

    Args:
        picture: filepath to 3-channel image [rgb]
        irradiance: filepath to 3-channel irradiance output (example .dat, .res)
        RunPcomb: Set Boolean to True to run lark
        directory: optional subfolder name (default folder is C:\lark)
    Returns:
        out: warnings and errors
        current_dir: current working folder 
        photopic_pic: filepath to photopic luminance picture
        photopic_lux: list of photopic illuminance
        melanopic_pic:filepath to circadian luminance picture [Lucas curve]
        melanopic_lux: list of circadian illuminance [Equivalent Melanopic Lux - EML]
"""

ghenv.Component.Name = "Lark 3-channel Circadian Luminance v3"
ghenv.Component.NickName = '3-channel Luminance'
ghenv.Component.Message = '3.0.0'
ghenv.Component.Category = "Lark"
ghenv.Component.SubCategory = "Basic Lark"

import os
from subprocess import Popen
import Grasshopper.Kernel as gh
e = gh.GH_RuntimeMessageLevel.Error
w = gh.GH_RuntimeMessageLevel.Warning

def is_input_valid(dic, name):
    if name not in dic:
        return False
    if dic[name] == None:
        return False
    if dic[name] == []:
        return False
    return True

#check all inputs
error_list = []
inputs = [picture, irradiance, RunPcomb]
inputs_name = ["picture", "irradiance", "RunPcomb"]
inputs_dict = {name:value for (value, name) in zip(inputs, inputs_name)}

if RunPcomb != True:
    ghenv.Component.AddRuntimeMessage(w, "Warning! Set Boolean True for RunPcomb to postprocess results.")

# raise error if input missing
for name, value in inputs_dict.items():
    if irradiance != None:  # PtBased
        if 'picture' in name:
            continue
        if not is_input_valid(inputs_dict, name):
            error_occurred = True
            error_list.append(name)
            
    if picture != None:  # ImgBased
        if 'irradiance' in name:
            continue
        if not is_input_valid(inputs_dict, name):
            error_occurred = True
            error_list.append(name)

if len(error_list) > 0:
    ghenv.Component.AddRuntimeMessage(w, "Warning! Connect the following inputs: " + ", ".join(error_list))

error_occurred = False

if len(error_list) != 0:
    check = "error"
else:
    check = 1




#make lark directory if none exists
basedir = 'C:\lark'
if os.path.isdir(basedir) != True: 
    os.makedirs(basedir)
else:
    pass

#create path to directory if provided
if directory == None:
    path = basedir
else:
    path = os.path.join (basedir, directory)

#create folder if directory is provided
if os.path.isdir(path) != True: 
    os.makedirs(path)
else:
    pass
os.chdir(path)

#print out current directory
current_dir = path



#process image
if RunPcomb:
    if picture != None:
        #Sum (radiometric values * Lucas circadian action curve)
        m = "pcomb  -e " """  "ro=ri(1) * 0.0021 ;go=gi(1) * 0.3911 ;bo=bi(1) * 0.6068"  """ + picture + " > " + "mtemp.hdr" 
        m_total = "pcomb  -e " """  "ro=ri(1)+ gi(1) + bi(1) ;go=ri(1) + gi(1) + bi(1) ;bo=ri(1) + gi(1) + bi(1)" """ + "-o mtemp.hdr > 3c_m.hdr"
        
        tempdel = "del *temp*"
        
        batch = open("batchfile3.bat", "w")
        batch.write(m + '\n' + m_total + '\n' + tempdel)
        batch.close()
        
        if RunPcomb != True:
            print "Set RunPcomb to true"
            pass
        else:
            runbatch = Popen("batchfile3.bat", cwd=path)
            stdout, stderr = runbatch.communicate()
        
        #print filepaths for output pictures
        photopic_pic = picture
        melanopic_pic = os.getcwd() + "\\" + "3C_m.hdr"
    
    
    
    #process irradiance
    if irradiance != None:
        
        #calculate circadian and photopic lux based on 3-channel irradiance
        #outputs work for different Radiance extensions (.dat,.res)
        f = open(irradiance, 'r')
        
        #create output tables
        result_p_l = []
        result_m_l = []
        
        p_l = open('photopic_lux.txt', 'w')
        m_l = open('melanopic_lux.txt', 'w')
        
        #loop on each row for photopic and circadian calculations
        for line in f:
            R,G,B = line.split()[0:3]
            
            p_loutput = 179 * (0.265 * float(R) + 0.67 * float(G) + 0.065 * float(B))   #photopic output
            m_loutput = 179 * ( 0.0021 * float (R) + 0.3911 * float (G) + 0.6068 * float (B))  #circadian output
            
            p_l.write(str(p_loutput) + '\n')
            m_l.write(str(m_loutput) + '\n')
            
            result_p_l.append(p_loutput)
            result_m_l.append(m_loutput)
        
        #assign output tables
        photopic_lux = result_p_l
        melanopic_lux = result_m_l
        
        f.close()
        p_l.close()
        m_l.close()
