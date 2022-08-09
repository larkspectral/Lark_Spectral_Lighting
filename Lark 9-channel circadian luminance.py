# Evaluate circadian and photopic metrics from 9-channel simulations 

# Lark Spectral Lighting (v0.0.1, v.0.0.2 and v1.0) is a collaboration of University of Washington and ZGF Architects LLP
# Authors Dr. Mehlika Inanici, Marty Brennan & Ed Clark
# Lark v2.0 is a collaboration of EPFL, Oregon State University, and Eindhoven University of Technology
# Authors Dr. Clotilde Pierson & Myrta Gkaintatzi-Masouti
# Copyright 2015-2022 Mehlika Inanici, Ph.D. (University of Washington) and ZGF Architects LLP
# Copyright 2022 Clotilde Pierson, Ph.D. (EPFL, Oregon State University) and Myrta Gkaintatzi-Masouti, M.Sc. (Eindhoven University of Technology)
# Licensed under The Modified 3-Clause BSD License (the "License");
# You may obtain a copy of the License at
# https://opensource.org/licenses/BSD-3-Clause

# Component updated by Dr. Mehlika Inanici, Marty Brennan & Ed Clark for Lark v1.0 (2022-04-14):
# Updated license, removed Rea metrics, Lucas curve now reports Equivalent Melanopic Lux (EML), luminous efficacy coefficient is scaled at 179.  

# Component updated by Dr. Clotilde Pierson for Lark v2.0 (2022-05-10):
# Added inputs to define whether an image-based simulation or a grid-based (or both) simulation is ran (inputs and outputs will vary accordingly)
# Added output image name based on previous image treatment (ipRGC FOV weighting)
# Modified pcomb function calls to include -h option (reduce header size for readability) and -o option (account for exposure value in post treatments)
# Updated Lucas circadian coefficients in image-based simulation post-process to match melanopic curve published in CIE toolbox and pre-defined wavelength bins

"""
Use this component to evaluate 9-channel circadian response.  
-
Provided by Lark 2.0.0

    Args:
        picture1: filepath to 3-channel image (blue wavelength bin)
        picture2: filepath to 3-channel image (green wavelength bin)
        picture3: filepath to 3-channel image (red wavelength bin)
        irradiance1: simulated RGB values (blue wavelength bin)
        irradiance2: simulated RGB values (green wavelength bin)
        irradiance3: simulated RGB values (red wavelength bin)
        ImageBasedSimulation: set Boolean to True if Grasshopper template includes imageBasedSimulation recipe and the outputs will be HDR images
        PointBasedSimulation: set Boolean to True if Grasshopper template includes gridBasedSimulation recipe and the outputs will be RGB values
        RunPcomb: set Boolean to True to run lark
        Directory: optional subfolder name (default folder is C:\lark)
    Returns:
        current_dir: current working folder 
        Photopic_lux: illuminance
        cir_Lucas_pic: filepath to circadian luminance picture [Lucas curve]
        cir_Lucas_lux: circadian illuminance [Equivalent Melanopic Lux - EML]
        Photopic_colorpic:filepath to color image
        Photopic_greyscalepic: filepath to greyscale picture
"""

ghenv.Component.Name = "Lark 9-channel Circadian Luminance v2"
ghenv.Component.NickName = '9-channel Luminance'
ghenv.Component.Message = '2.0.0'
ghenv.Component.Category = "Lark"
ghenv.Component.SubCategory = "Basic Lark"

import os
import re
from subprocess import Popen



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



#check inputs for simulation type
error_list = []
inputs = [ImageBasedSimulation,PointBasedSimulation]
inputs_name = ["ImageBasedSimulation","PointBasedSimulation"]

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



#check inputs and process images for image-based simulations
if ImageBasedSimulation == True:
    
    #check inputs
    error_list = []
    inputs = [picture1,picture2,picture3,RunPcomb]
    inputs_name = ["picture1","picture2","picture3","RunPcomb"]
    
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
    
    
    
    #process images
    if check != "error":
        
        #adapt name of output images based on treatment (ipRGC weighting or not)
        weightcheck = bool(re.search("weighted", picture1))
        if weightcheck:
            extension = "_weighted.hdr"
        else:
            extension = ".hdr"
         
        #convert 9 channels to photopic 3 channel image with color and luminance outputs   
        v0 =  "pcomb -h -e" """ "ro=((ri(3)*0.2521)+ (gi(3)*0.0162) + (bi(3)*0.0002))/0.2685; go=((ri(2)*0.1288)+ (gi(2)*0.2231) + (bi(2)*0.3175))/0.6694; bo=((ri(1)*0.0004)+ (gi(1)*0.0095) + (bi(1)*0.0522))/0.0621" """ + "-o " + picture1 + " -o " + picture2 + " -o " + picture3 + " > Photopic9to3" + extension
        
        #(Sum 9-channel radiometric values multiplied by vlambda action curve)
        #process blue1, blue2, blue3
        v1 = "pcomb -h -e " """ "ro=ri(1) * 0.0004;go=gi(1) * 0.0095;bo=bi(1) * 0.0522" """ + "-o " + picture1 + " > vtemp1.hdr"
        #process green1, green2, green3
        v2 = "pcomb -h -e " """ "ro=ri(1) * 0.1288;go=gi(1) * 0.2231;bo=bi(1) * 0.3175" """ + "-o " + picture2 + " > vtemp2.hdr"
        #process red1, red2, red3
        v3 = "pcomb -h -e" """  "ro=ri(1) * 0.2521;go=gi(1) * 0.0162;bo=bi(1) * 0.0002" """ + "-o " + picture3 + " > vtemp3.hdr"
        #add all channels for total photopic luminance. Repeat for each channel to view greyscale photopic luminance image
        vtotal = "pcomb -h -e" """ "ro=ri(1)+ gi(1) + bi(1) + ri(2) + gi(2) + bi(2) + ri(3) + gi(3) + bi(3);go=ri(1) + gi(1) + bi(1) + ri(2) + gi(2) + bi(2) + ri(3) + gi(3) + bi(3);bo=ri(1) + gi(1) + bi(1) + ri(2) + gi(2) + bi(2) + ri(3) + gi(3) + bi(3)" """ + "-o vtemp1.hdr -o vtemp2.hdr -o vtemp3.hdr > Photopic9Lum" + extension
        
        #(Sum of 9-channel radiometric values multiplied by Lucas circadian action curve)
        #process blue1, blue2, blue3
        c1 = "pcomb -h -e " """  "ro=ri(1) * 0.0168;go=gi(1) * 0.1815;bo=bi(1) * 0.3974"  """ + "-o " + picture1 + " > ctemp1.hdr" 
        #process green1, green2, green3
        c2 = "pcomb -h -e " """  "ro=ri(1) * 0.2468;go=gi(1) * 0.1207;bo=bi(1) * 0.0346" """ + "-o " + picture2 + " > ctemp2.hdr"
        #process red1, red2, red3
        c3 = "pcomb -h -e " """   "ro=ri(1) * 0.0022;go=gi(1) * 0;bo=bi(1) * 0" """ + "-o " + picture3 + " > ctemp3.hdr"
        #add all channels for total melanopic equivalent luminance. Repeat for each channel to view greyscale melanopic equivalent luminance image
        ctotal = "pcomb -h -e " """  "ro=ri(1)+ gi(1) + bi(1) + ri(2) + gi(2) + bi(2) + ri(3) + gi(3) + bi(3);go=ri(1) + gi(1) + bi(1) + ri(2) + gi(2) + bi(2) + ri(3) + gi(3) + bi(3);bo=ri(1) + gi(1) + bi(1) + ri(2) + gi(2) + bi(2) + ri(3) + gi(3) + bi(3)" """ + "-o ctemp1.hdr -o ctemp2.hdr -o ctemp3.hdr > Lucas9Cir" + extension
        
        tempdel = "del *temp* "
        
        batch = open("temp\\batchfile.bat", "w")
        batch.write(v0 + '\n' * 3 + v1 + '\n' + v2 + '\n' + v3 + '\n' + vtotal + '\n' * 3 + c1 + '\n' + c2 + '\n' + c3 + '\n' + ctotal + '\n' * 3 + tempdel)
        batch.close()
    
    if RunPcomb != True:
        pass
    else:
        runbatch = Popen("temp\\batchfile.bat", cwd=path)
        stdout, stderr = runbatch.communicate()
    
    
    
    #print filepaths for output pictures
    Photopic_colorpic = os.getcwd() + "\\" + "Photopic9to3" + extension
    Photopic_greyscalepic = os.getcwd() + "\\" + "Photopic9Lum" + extension
    cir_Lucas_pic = os.getcwd() + "\\" + "Lucas9Cir" + extension



#check inputs and process irradiances for point-based simulations
if PointBasedSimulation == True:
    
    #check inputs
    error_list = []
    inputs = [irradiance1,irradiance2,irradiance3]
    inputs_name = ["irradiance1","irradiance2","irradiance3"]
    
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
    
    
    
    #calculate circadian and photopic lux based on 9-channel irradiance
    if check != "error":
        
        #outputs work for different Radiance extensions (.dat,.res)
        f1 = open(irradiance1, 'r')
        f2 = open(irradiance2, 'r')
        f3 = open(irradiance3, 'r')
        
        list1 = []
        for line in f1:
            list1.append(line.split())
        
        list2 = []
        for line in f2:
            list2.append(line.split())
        
        list3 = []
        for line in f3:
            list3.append(line.split())
        
        #combine B1,B2,B3,G1,G2,G3,R1,R2,R3 in list of lists
        length = len(list1)  #number of grid points evaluated
        z = []  # z = list of lists
        count = 0
        while count < length:  
            z.append(list1[count] + list2[count] + list3[count])
            count += 1
        
        #create output tables
        voutput = []
        lucasoutput = []
        
        #loop on each row of list for photopic and circadian calculations
        i = 0
        while i < length:
            voutput.append(179 * (0.0004 * float(z[i][0]) + 0.0095 * float(z[i][1]) + 0.0522 * float(z[i][2]) + 0.1288 * float(z[i][3]) + 0.2231 * float(z[i][4]) + 0.3175 * float(z[i][5]) + 0.2521 * float(z[i][6]) + 0.0162 * float(z[i][7]) + 0.0002 * float(z[i][8]) ))
            lucasoutput.append(179 * (0.0168 * float(z[i][0]) + 0.1815 * float(z[i][1]) + 0.3974 * float(z[i][2]) + 0.2468 * float(z[i][3]) + 0.1207 * float(z[i][4]) + 0.0346 * float(z[i][5]) + 0.0022 * float(z[i][6]) + 0 * float(z[i][7]) + 0 * float(z[i][8]) ))
            i += 1
        
        #assign output tables
        Photopic_lux = voutput
        cir_Lucas_lux = lucasoutput

        #write illuminance metrics out to text files
        v = open('SpectralSimu_Results_PhotopicLux.txt', 'w')
        c = open('SpectralSimu_Results_LucasMelanopicLux.txt', 'w')
        v.write(str(voutput))
        c.write(str(lucasoutput))

        f1.close()
        f2.close()
        f3.close()
        v.close()
        c.close()
