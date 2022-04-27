# evaluate circadian and photopic metrics from 9-channel simulations 
# Lark Spectral Lighting is a collaboration of University of Washington and ZGF Architects LLP
# Authors Dr. Mehlika Inanici, Marty Brennan & Ed Clark
# Copyright 2015-2022 Mehlika Inanici, Ph.D. (University of Washington) and ZGF Architects LLP
# Licensed under The 3-Clause BSD License (the "License");
# You may obtain a copy of the License at
# https://opensource.org/licenses/BSD-3-Clause

"""
Use this component to evaluate 9-channel circadian response.  
-
Provided by lark v1.0
2022-04-14 Updated license, removed Rea metrics, Lucas curve now reports Equivalent Melanopic Lux (EML), luminous efficacy coefficient is scaled at 179.  

    Args:
        picture1: filepath to 3-channel image (blue wavelength bin)
        picture2: filepath to 3-channel image (green wavelength bin)
        picture3: filepath to 3-channel image (red wavelength bin)
        RunPcomb: Set Boolean to True to run lark
        Directory: subfolder name (default folder is C:\lark)
    Returns:
        current_dir: current working folder 
        Photopic_lux: illuminance
        cir_Lucas_pic: filepath to circadian luminance picture [melanopic lux]
        cir_Lucas_lux: circadian illuminance [melanopic lux]
        Photopic_colorpic:filepath to color image
        Photopic_greyscalepic: filepath to greyscale picture
"""

ghenv.Component.Name = "Lark 9-channel circadian luminance"
ghenv.Component.NickName = '9-channel luminance'
ghenv.Component.Message = 'v1.0'
ghenv.Component.Category = "Extra"
ghenv.Component.SubCategory = "lark"


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



#check all inputs
error_list = []
inputs = [picture1,picture2,picture3,irradiance1,irradiance2,irradiance3,RunPcomb]
inputs_name = ["picture1","picture2","picture3","irradiance1","irradiance2","irradiane3","RunPcomb"]

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


if check != "error":

    #Convert 9 channels to photopic 3 channel image with color and luminance outputs   
    v0 =  "pcomb  -e" """ "ro=((ri(3)*0.2521)+ (gi(3)*0.0162) + (bi(3)*0.0002))/0.2685; go=((ri(2)*0.1288)+ (gi(2)*0.2231) + (bi(2)*0.3174))/0.6693; bo=((ri(1)*0.0004)+ (gi(1)*0.0095) + (bi(1)*0.0522))/0.0621" """ + picture1 + " " + picture2 + " " + picture3 + " > " + "Photopic9to3.hdr"

    #(Sum 9-channel radiometric values multiplied by vlambda action curve) 
    # process blue1, blue2, blue3
    v1 = "pcomb  -e " """ "ro=ri(1) * 0.0004 ;go=gi(1) * 0.0095;bo=bi(1) * 0.0522" """ + picture1 + " > " + "vtemp1.hdr"
    # process green1, green2, green3
    v2 = "pcomb  -e " """ "ro=ri(1) * 0.1288 ;go=gi(1) * 0.2231;bo=bi(1) * 0.3174" """ + picture2 + " > " + "vtemp2.hdr"
    #process red1, red2, red3
    v3 = "pcomb  -e" """  "ro=ri(1) * 0.2521 ;go=gi(1) * 0.0162;bo=bi(1) * 0.0002" """ + picture3 + " > " +  "vtemp3.hdr"
    # Add all channels for total luminance. Repeat for each channel to view greyscale luminance image
    vtotal = "pcomb  -e" """ "ro=ri(1)+ gi(1) + bi(1) + ri(2) + gi(2) + bi(2) + ri(3) + gi(3) + bi(3);go=ri(1) + gi(1) + bi(1) + ri(2) + gi(2) + bi(2) + ri(3) + gi(3) + bi(3);bo=ri(1) + gi(1) + bi(1) + ri(2) + gi(2) + bi(2) + ri(3) + gi(3) + bi(3)" """ + "vtemp1.hdr vtemp2.hdr vtemp3.hdr" + " > " + "Photopic9Lum.hdr"


    #(Sum of 9-channel radiometric values multiplied by Lucas circadian action curve) multiplied by luminous efficacy coefficient 179
    c1_1 = "pcomb  -e " """  "ro=ri(1) * 0.0166 ;go=gi(1) * 0.1819;bo=bi(1) * 0.3973"  """ + picture1 + " > " + "ctemp1_1.hdr" 
    c2_1 = "pcomb  -e " """  "ro=ri(1) * 0.2668 ;go=gi(1) * 0.1204;bo=bi(1) * 0.0351" """ + picture2 + " > " + "ctemp1_2.hdr"
    c3_1 = "pcomb  -e " """   "ro=ri(1) * 0.0018 ;go=gi(1) * 0;bo=bi(1) * 0" """ + picture3 + " > " + "ctemp1_3.hdr"
    ctotal_1 = "pcomb  -e " """  "ro=ri(1)+ gi(1) + bi(1) + ri(2) + gi(2) + bi(2) + ri(3) + gi(3) + bi(3);go=ri(1) + gi(1) + bi(1) + ri(2) + gi(2) + bi(2) + ri(3) + gi(3) + bi(3);bo=ri(1) + gi(1) + bi(1) + ri(2) + gi(2) + bi(2) + ri(3) + gi(3) + bi(3)" """ + "ctemp1_1.hdr ctemp1_2.hdr ctemp1_3.hdr" + " > " + "ctempcir1.hdr"
    ccoef_1 = "pcomb " +  "ctempcir1.hdr" + " > " + "Lucas9Cir.hdr"

    tempdel = "del *temp* "

    batch = open("batchfile.bat", "w")
    batch.write(v0 + '\n' * 3 + v1 + '\n' + v2 + '\n' + v3 + '\n' + vtotal + '\n' * 3 + c1_1 + '\n' + c2_1 + '\n' + c3_1 + '\n' + ctotal_1 + '\n' + ccoef_1 + '\n' * 3 + tempdel)
    batch.close()


if RunPcomb != True:
    pass
else:
    runbatch = Popen("batchfile.bat", cwd=path)
    stdout, stderr = runbatch.communicate()

#print filepaths for output pictures (all pictures are greyscale luminance to be viewed in falsecolor)
Photopic_colorpic = os.getcwd() + "\\" + "Photopic9to3.hdr"
Photopic_greyscalepic = os.getcwd() + "\\" + "Photopic9Lum.hdr"
cir_Lucas_pic = os.getcwd() + "\\" + "Lucas9Cir.hdr"


#Calculate circadian and photopic lux based on 9-channel irradiance 
#Outputs work for different Radiance extensions (.dat,.res)
#file = os.path.split(irradiance)[1]


if check != "error":

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
    #a = z[0][1]

    voutput = []
    lucasoutput = []

    i = 0
    while i < length:   #run photopic and circadian calculations on each row of list
        voutput.append(179 * (0.0004 * float(z[i][0]) + 0.0095 * float(z[i][1]) + 0.0522 * float(z[i][2]) + 0.1288 * float(z[i][3]) + 0.2231 * float(z[i][4]) + 0.3174 * float(z[i][5]) + 0.2521 * float(z[i][6]) + 0.0162 * float(z[i][7]) + 0.0002 * float(z[i][8]) ))
        lucasoutput.append(179 * (0.0166 * float(z[i][0]) + 0.1819 * float(z[i][1]) + 0.3973 * float(z[i][2]) + 0.2468 * float(z[i][3]) + 0.1204 * float(z[i][4]) + 0.0351 * float(z[i][5]) + 0.0018 * float(z[i][6]) + 0 * float(z[i][7]) + 0 * float(z[i][8]) ))
        i += 1


    Photopic_lux = voutput
    cir_Lucas_lux = lucasoutput

    #write illuminance metrics out to text files
    v = open('Photopic_lux.txt', 'w') 
    c2 = open('cir_Lucas_lux.txt', 'w')
    v.write(str(voutput))
    c2.write(str(lucasoutput))


    f1.close()
    f2.close()
    f3.close()
    v.close()
    c2.close()
