# # Evaluate circadian and photopic metrics from 3-channel simulations 
# Lark Spectral Lighting is a collaboration of University of Washington and ZGF Architects LLP
# Authors Dr. Mehlika Inanici, Marty Brennan & Ed Clark
# Copyright 2015-2022 Mehlika Inanici, Ph.D. (University of Washington) and ZGF Architects LLP
# Licensed under The 3-Clause BSD License (the "License");
# You may obtain a copy of the License at
# https://opensource.org/licenses/BSD-3-Clause

"""
Use this component to evaluate 3-channel circadian response.  
-
Provided by lark v1.0
2020-11-15 Updated Lucas coefficients 
2022-04-14 Updated license, removed Rea metrics, Lucas curve now reports Equivalent Melanopic Lux (EML), luminous efficacy coefficient is scaled at 179.  

    Args:
        picture: filepath to 3-channel image [rgb]
        irradiance: filepath to 3-channel irradiance output (example .dat, .res)
        RunPcomb: Set Boolean to True to run lark
        Directory: subfolder name (default folder is C:\lark)
    Returns:
        out: warnings and errors
        current_dir: current working folder 
        cir_Lucas_pic:filepath to circadian luminance picture [Lucas curve]
        cir_Lucas_lux: list of circadian illuminance [Lucas curve]
        photopic_pic: filepath to photopic luminance picture
        photopic_lux: list of photopic illuminance
"""

ghenv.Component.Name = "Lark 3-channel circadian luminance"
ghenv.Component.NickName = '3-channel luminance'
ghenv.Component.Message = 'v1.0'
ghenv.Component.Category = "Extra"
ghenv.Component.SubCategory = "lark"



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
#    print len(error_list)




import os
from subprocess import Popen

#make lark directory if none exists
basedir = 'C:\lark'
if os.path.isdir(basedir) != True: 
    os.makedirs(basedir)
else:
    pass


#Create path to Directory if provided
if Directory == None:
    path = basedir
else:
    path = os.path.join (basedir, Directory)

#Create folder if Directory is provided
if os.path.isdir(path) != True: 
    os.makedirs(path)
else:
    pass

os.chdir(path)
#print out current directory
current_dir = path




if picture != None:

    #calculate circadian luminance 
    #Sum (radiometric values *  photopic v lambda action curve)
    v1 = "pcomb  -e " """ "ro=ri(1) * 0.2537 ;go=gi(1) * 0.6635 ;bo=bi(1) * 0.0622" """ + picture + " > " + "vtemp.hdr"
    vtotal = "pcomb  -e" """ "ro=ri(1)+ gi(1) + bi(1);go=ri(1) + gi(1) + bi(1) ;bo=ri(1) + gi(1) + bi(1)" """ + "vtemp.hdr" + " > " + "Calc3Lum.hdr"


    #Sum (radiometric values * Lucas circadian action curve) * luminous efficacy coefficient 179
    c_l = "pcomb  -e " """  "ro=ri(1) * 0.0018 ;go=gi(1) * 0.4024;bo=bi(1) * 0.5958"  """ + picture + " > " + "c_l_temp.hdr" 
    c_l_total = "pcomb  -e " """  "ro=ri(1)+ gi(1) + bi(1) ;go=ri(1) + gi(1) + bi(1) ;bo=ri(1) + gi(1) + bi(1)" """ + "c_l_temp.hdr"  + " > " + "c_l_tempcir3.hdr"
    c_l_coef = "pcomb " +  "c_l_tempcir3.hdr" + " > " + "Calc3_Lucas.hdr"


    tempdel = "del *temp*"

    batch = open("batchfile3.bat", "w")
    batch.write(v1 + '\n' + vtotal + '\n' + c_l + '\n' + c_l_total + '\n' + c_l_coef + '\n' + tempdel)
    batch.close()


    if RunPcomb != True:
        print "Set RunPcomb to true"
        pass
    else:
        runbatch = Popen("batchfile3.bat", cwd=path)
        stdout, stderr = runbatch.communicate()

        #print filepaths for output pictures
        cir_Lucas_pic = os.getcwd() + "\\" + "Calc3_Lucas.hdr"
        photopic_pic = os.getcwd() + "\\" + "Calc3Lum.hdr"


#Calculate circadian lux based on 3-channel irradiance 
#Outputs work for different Radiance extensions (.dat,.res)
#file = os.path.split(irradiance)[1]


if irradiance != None:

    f = open(irradiance, 'r')
    v = open('photopic_lux.txt', 'w')
    c_l = open('cir_Lucas_lux.txt', 'w')

    result_pho = []
    result_cir_l = []

    for line in f:
        R,G,B = line.split()[0:3]
        voutput = 179 * (0.2537 * float(R) + 0.6635* float(G) + 0.0622* float(B))   #photopic output
        l_coutput = 179 * ( 0.0018* float (R) + 0.4024* float (G) + 0.5958 * float (B))  #circadian output 
        v.write(str(voutput) + '\n')
        c_l.write(str(l_coutput) + '\n')
        result_pho.append(voutput)
        result_cir_l.append(l_coutput) 

    photopic_lux = result_pho
    cir_Lucas_lux = result_cir_l

    f.close()
    v.close()
    c_l.close()
