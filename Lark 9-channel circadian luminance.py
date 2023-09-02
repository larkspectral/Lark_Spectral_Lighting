# Evaluate circadian and photopic metrics from 9-channel simulations 

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

# Component updated by Dr. Mehlika Inanici, Marty Brennan & Ed Clark for Lark v1.0 (2022-04-14):
# Updated license, removed Rea metrics, Lucas curve now reports Equivalent Melanopic Lux (EML), luminous efficacy coefficient is scaled at 179.  

# Component updated by Dr. Clotilde Pierson for Lark v2.0 (2022-05-10):
# Added inputs to define whether an image-based simulation or a grid-based (or both) simulation is ran (inputs and outputs will vary accordingly)
# Added output image name based on previous image treatment (ipRGC FOV weighting)
# Modified pcomb function calls to include -h option (reduce header size for readability) and -o option (account for exposure value in post treatments)
# Updated Lucas circadian coefficients in image-based simulation post-process to match melanopic curve published in CIE toolbox and pre-defined wavelength bins

# Component updated by Bo Jung for Lark v3.0 (2023-07-05):
# Updated coefficients for 9 channel rgb.
# Modified output name (cir_Lucas_pic and cir_Lucas_lux changed to melanopic_pic and melanopic_lux respectively).
# Added neuropic output.

"""
Use this component to evaluate 9-channel circadian response.  
-
Provided by Lark 3.0.0

    Args:
        picture1: filepath to 3-channel image (blue wavelength bin)
        picture2: filepath to 3-channel image (green wavelength bin)
        picture3: filepath to 3-channel image (red wavelength bin)
        irradiance1: simulated RGB values (blue wavelength bin)
        irradiance2: simulated RGB values (green wavelength bin)
        irradiance3: simulated RGB values (red wavelength bin)
        ImageBasedSimulation: set Boolean to True if Grasshopper template includes imageBasedSimulation recipe and the outputs will be HDR images
        PointBasedSimulation: set Boolean to True if Grasshopper template includes gridBasedSimulation recipe and the outputs will be RGB values
        RunPcomb: Set Boolean to True to run lark
        Directory: subfolder name (default folder is C:\lark)
    Returns:
        current_dir: current working folder 
        photopic_lux: photopic illuminance [OPN1]
        photopic_colorpic:filepath to color image
        photopic_greyscalepic: filepath to greyscale picture
        melanopic_lux: equivalent melanopic lux [OPN4]
        melanopic_pic: filepath to equivalent melanopic lux picture
        neuropic_lux: neuropic lux [OPN5]
        neuropic_pic: filepath to neuropic lux picture
"""

ghenv.Component.Name = "Lark 9-channel Circadian Luminance v3"
ghenv.Component.NickName = '9-channel luminance'
ghenv.Component.Message = '3.0.0'
ghenv.Component.Category = "Lark"
ghenv.Component.SubCategory = "Basic Lark"

import os
import re
from subprocess import Popen
import Grasshopper.Kernel as gh
e = gh.GH_RuntimeMessageLevel.Error
w = gh.GH_RuntimeMessageLevel.Warning



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


# raise error if input missing
error_list = []
inputs = [picture1,picture2,picture3,irradiance1, irradiance2, irradiance3, ImageBasedSimulation, PointBasedSimulation, RunPcomb]
inputs_name = ["picture1","picture2","picture3","irradiance1","irradiance2","irradiance3","ImageBasedSimulation", "PointBasedSimulation", "RunPcomb"]
inputs_dict = {name:value for (value, name) in zip(inputs, inputs_name)}

def is_input_valid(dic, name):
    if name not in dic:
        return False
    if dic[name] == None:
        return False
    if dic[name] == []:
        return False
    return True
    
if RunPcomb != True:
    ghenv.Component.AddRuntimeMessage(w, "Warning! Set Boolean True for RunPcomb to postprocess results.")

for name, value in inputs_dict.items():
    if PointBasedSimulation:  # PtBased
        if 'picture' or 'Image' in name:
            continue
        if not is_input_valid(inputs_dict, name):
            error_occurred = True
            error_list.append(name)
            
    elif ImageBasedSimulation:  # ImgBased
        if 'irradiance' or 'Point' in name:
            continue
        if not is_input_valid(inputs_dict, name):
            error_occurred = True
            error_list.append(name)
      
      
    elif (ImageBasedSimulation == None or []) and (PointBasedSimulation == None or []):
        ghenv.Component.AddRuntimeMessage(w, "Warning! Set Boolean True ImageBasedSimulation and/or PointBasedSimulation!")

if len(error_list) > 0:
    ghenv.Component.AddRuntimeMessage(w, "Warning! Connect the following inputs: " + ", ".join(error_list))

error_occurred = False

if len(error_list) != 0:
    check = "error"
else:
    check = 1


#check inputs and process images for image-based simulations
if RunPcomb == True:
    if ImageBasedSimulation:
        
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
            ghenv.Component.AddRuntimeMessage(w, "Warning! Connect the following inputs: " + ", ".join(error_list))
        
        
        
        #process images
        if check != "error":
            #adapt name of output images based on treatment (ipRGC weighting or not)
            weightcheck = bool(re.search("weighted", picture1))
            if weightcheck:
                extension = "_weighted.hdr"
            else:
                extension = ".hdr"
            
            #Convert 9 channels to photopic 3 channel image with color and luminance outputs   
            p0 =  "pcomb  -e" """ "ro=((ri(3)*0.130177072)+ (gi(3)*0.081085718) + (bi(3)*0.049591265))/0.265; go=((ri(2)*0.164071102)+ (gi(2)*0.250355905) + (bi(2)*0.259754249))/0.67; bo=((ri(1)*0.0003)+ (gi(1)*0.009098397) + (bi(1)*0.055590209))/0.065" """ + picture1 + " " + picture2 + " " + picture3 + " > " + "photopic9.hdr"
            
            #(Sum 9-channel radiometric values multiplied by vlambda action curve) 
            # process blue1, blue2, blue3
            p1 = "pcomb  -e " """ "ro=ri(1) * 0.0003 ;go=gi(1) * 0.009098397;bo=bi(1) * 0.055590209" """ + picture1 + " > " + "ptemp1.hdr"
            # process green1, green2, green3
            p2 = "pcomb  -e " """ "ro=ri(1) * 0.164071102 ;go=gi(1) * 0.250355905;bo=bi(1) * 0.259754249" """ + picture2 + " > " + "ptemp2.hdr"
            #process red1, red2, red3
            p3 = "pcomb  -e" """  "ro=ri(1) * 0.130177072 ;go=gi(1) * 0.081085718;bo=bi(1) * 0.049591265" """ + picture3 + " > " +  "ptemp3.hdr"
            # Add all channels for total luminance. Repeat for each channel to view greyscale luminance image. GRESCALE IMAGE
            ptotal = "pcomb  -e" """ "ro=ri(1)+ gi(1) + bi(1) + ri(2) + gi(2) + bi(2) + ri(3) + gi(3) + bi(3);go=ri(1) + gi(1) + bi(1) + ri(2) + gi(2) + bi(2) + ri(3) + gi(3) + bi(3);bo=ri(1) + gi(1) + bi(1) + ri(2) + gi(2) + bi(2) + ri(3) + gi(3) + bi(3)" """ + "ptemp1.hdr ptemp2.hdr ptemp3.hdr" + " > " + "photopic9_grey.hdr"
            
            #(Sum of 9-channel radiometric values multiplied by melanopic action curve) 
            m1 = "pcomb  -e " """  "ro=ri(1) * 0.0119 ;go=gi(1) * 0.1784;bo=bi(1) * 0.4165"  """ + picture1 + " > " + "mtemp1.hdr" 
            m2 = "pcomb  -e " """  "ro=ri(1) * 0.268843 ;go=gi(1) * 0.1033;bo=bi(1) * 0.019" """ + picture2 + " > " + "mtemp2.hdr"
            m3 = "pcomb  -e " """   "ro=ri(1) * 0.0017 ;go=gi(1) * 0.000296;bo=bi(1) * 0.000061" """ + picture3 + " > " + "mtemp3.hdr"
            mtotal = "pcomb  -e " """  "ro=ri(1)+ gi(1) + bi(1) + ri(2) + gi(2) + bi(2) + ri(3) + gi(3) + bi(3);go=ri(1) + gi(1) + bi(1) + ri(2) + gi(2) + bi(2) + ri(3) + gi(3) + bi(3);bo=ri(1) + gi(1) + bi(1) + ri(2) + gi(2) + bi(2) + ri(3) + gi(3) + bi(3)" """ + "mtemp1.hdr mtemp2.hdr mtemp3.hdr" + " > " + "melanopic9.hdr"
            #mcoef = "pcomb " +  "melanopic9temp.hdr" + " > " + "mel9.hdr"
            
            #(Sum of 9-channel radiometric values multiplied by neuropic action curve)
            n1 = "pcomb  -h -e " """  "ro=((ri(3)*0)+ (gi(3)*0) + (bi(3)*0)); go=((ri(2)*0)+ (gi(2)*0) + (bi(2)*0)); bo=((ri(1)*0.905130569) + (gi(1)*0.0948) + (bi(1)*0.00007))"  """ + " -o " + picture1 + " -o " + picture2 + " -o " + picture3 + " > " + "ntemp.hdr"
            n2 = "pcomb  -e " """  "ro=ri(1)+ gi(1) + bi(1);go=ri(1) + gi(1) + bi(1);bo=ri(1) + gi(1) + bi(1)" """ + "ntemp.hdr" + " > " + "neuropic9.hdr"
           
            tempdel = "del *temp* "
            
            batch = open(current_dir + "\\batchfile.bat", "w")
            batch.write(p0 + '\n' * 3 + p1 + '\n' + p2 + '\n' + p3 + '\n' + ptotal + '\n' * 3 + m1 + '\n' + m2 + '\n' + m3 + '\n' + mtotal +'\n' * 3 + n1 + '\n' + n2 + '\n' * 3 + tempdel)
            batch.close()
        
        if RunPcomb != True:
            pass
        else:
            runbatch = Popen(current_dir + "\\batchfile.bat", cwd=path)
            stdout, stderr = runbatch.communicate()
        
        # CHECK WHY PHOTOPIC HAS 2 OUTPUT
        #print filepaths for output pictures (all pictures are greyscale luminance to be viewed in falsecolor)
        photopic_colorpic = os.getcwd() + "\\" + "photopic9" + extension
        photopic_greyscalepic = os.getcwd() + "\\" + "photopic9_grey" + extension
        melanopic_pic = os.getcwd() + "\\" + "melanopic9" + extension
        neuropic_pic = os.getcwd() + "\\" + "neuropic9" + extension
    
    
    #check inputs and process irradiances for point-based simulations
    if PointBasedSimulation:
        
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
            ghenv.Component.AddRuntimeMessage(w, "Warning! Connect the following inputs: " + ", ".join(error_list))
        
        
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
            poutput = []
            moutput = []
            noutput = []
            
            #loop on each row of list for photopic, melanopic, and neuropic calculations
            i = 0
            while i < length:   #run photopic and circadian calculations on each row of list
                poutput.append(179 * (0.0003 * float(z[i][0]) + 0.009098397 * float(z[i][1]) + 0.055590209 * float(z[i][2]) + 0.164071102 * float(z[i][3]) + 0.250355905 * float(z[i][4]) + 0.259754249 * float(z[i][5]) + 0.130177072 * float(z[i][6]) + 0.081085718 * float(z[i][7]) + 0.049591265 * float(z[i][8]) ))
                moutput.append(179 * (0.0119 * float(z[i][0]) + 0.1784 * float(z[i][1]) + 0.4165 * float(z[i][2]) + 0.268843 * float(z[i][3]) + 0.1033 * float(z[i][4]) + 0.019 * float(z[i][5]) + 0.0017 * float(z[i][6]) + 0.000296 * float(z[i][7]) + 0.000061 * float(z[i][8]) ))
                noutput.append(179 * (0.905130569 * float(z[i][0]) + 0.0948 * float(z[i][1]) + 0.000069431 * float(z[i][2]) + 0 * float(z[i][3]) + 0 * float(z[i][4]) + 0 * float(z[i][5]) + 0 * float(z[i][6]) + 0 * float(z[i][7]) + 0 * float(z[i][8]) ))
                i += 1
            
            #assign output tables
            photopic_lux = poutput
            melanopic_lux = moutput
            neuropic_lux = noutput
    
            #write illuminance metrics out to text files
            v = open('photopic_lux.txt', 'w') 
            m = open('melanopic_lux.txt', 'w')
            n = open('neuropic_lux.txt', 'w')
            v.write(str(poutput))
            m.write(str(moutput))
            n.write(str(noutput))
    
            f1.close()
            f2.close()
            f3.close()
            v.close()
            m.close()
            n.close()