# Convert SPD to 3 or 9 channel Radiance materials

# Lark Spectral Lighting (v0.0.1, v0.0.2 and v1.0) is a collaboration of University of Washington and ZGF Architects LLP
# Authors Dr. Mehlika Inanici, Marty Brennan & Ed Clark
# Lark v2.0 is a collaboration of EPFL, Oregon State University, and Eindhoven University of Technology
# Authors Dr. Clotilde Pierson & Myrta Gkaintatzi-Masouti
# Copyright 2015-2022 Mehlika Inanici, Ph.D. (University of Washington) and ZGF Architects LLP
# Copyright 2022 Clotilde Pierson, Ph.D. (EPFL, Oregon State University) and Myrta Gkaintatzi-Masouti, M.Sc. (Eindhoven University of Technology)
# Licensed under The Modified 3-Clause BSD License (the "License");
# You may obtain a copy of the License at
# https://opensource.org/licenses/BSD-3-Clause

# Component updated by Dr. Clotilde Pierson for Lark v2.0 (2022-05-10):
# Added a fourth material type ([3 = electriclight]) and defined the main path accordingly

"""
Use this component to convert spectral data to Radiance materials
-
Provided by Lark 2.0.0

    Args:
        spd_input: filepath to spectral power distribution txt file. column 1 = wavelength/ column 2 = transmittance or reflectance
        source_interval: wavelengh increment from spd_input
        excel_daylight_series_cal: Boolean toggle True if data is derived from the Rochester Institute of Technology Excel Daylight Series Calculator
        material_name: Name of Radiance material (*no white space)
        roughness: float  0-1
        specularity: float 0-1
        material_type: [0 = glass] [1 = plastic] [2 = sky] [3 = electriclight]
        channel_type:  [0 = 3 channel]  [1 = 9 channel]  3 channel is RGB/ 9 channel is b1,b2,b3,g1,g2,g3,r1,r2,r3
    Returns:
        current_dir: current working folder 
        channel_output: average reflectance or transmissivity per channel [0-1] 
        mat_3: filepath to 3 channel Radiance material definition [r,g,b]
        mat_9a: filepath to 9 channel Radiance material definition [b1,b2,b3]
        mat_9b: filepath to 9 channel Radiance material definition [g1,g2,g3]
        mat_9c: filepath to 9 channel Radiance material definition [r1,r2,r3]
"""

ghenv.Component.Name = "Lark Convert SPD - Write Spectral Radiance Materials v2"
ghenv.Component.NickName = 'Spectral Materials'
ghenv.Component.Message = '2.0.0'
ghenv.Component.Category = "Lark"
ghenv.Component.SubCategory = "Basic Lark"

import re
import os
from subprocess import Popen
import math
from collections import OrderedDict
from decimal import Decimal



#check for missing inputs
error_list = []
inputs = [spd_input,source_interval,material_name,material_type,channel_type]
inputs_name = ["spd_input","source_interval","material_name","material_type","channel_type"]

for idx, val in enumerate (inputs):
    if val == None or val == []:
        error_list.append(inputs_name[idx])

if len(error_list) != 0 and material_type !=2:
    check = "error"
elif error_list == 'material_name' and material_type == 2:
        check  = 1
else:
    check = 1

if check == "error" :
    print "Warning! Connect the following inputs:" 
    print error_list



#create and assign working directory
if material_type == 3 : #main folder for electric light
    _path = 'C:\lark\luminaires\ies'
else: #main folder in other cases
    _path = 'C:\lark\materials'
#make lark directory if none exists
if os.path.isdir(_path) != True: 
    os.makedirs(_path)
else:
    pass
os.chdir(_path)
#print out current directory
current_dir = _path



#read lines of spectral data exported from Optics6; the header will be skipped
#read lines of spectral data from 2 column text file - first column must be wavelength; the second is for values
#Note, values should be between 0 to 1. excel_daylight_series_cal data will be converted automatically
if  check != "error":
    print spd_input
    fopen = open(spd_input, 'r')
    b = fopen.readlines()
    data = [] #create list
    for line in b:
        if not line.startswith('{'): #cull the Optics header
                data.append(line.split())

    data2 = filter(None, data)  #filter blank lines in data list

    spd = OrderedDict() #create a dictionary in order of wavelength
    for line in data2:
        (wave, val) =  line[0], line[1] #assign first 2 columns of data
        spd[float(wave)] = float(val)  #assign values to dictionary keys

    for keyA in spd.keys():
        if keyA < 10:  #true for Optics6 export which measures wavelenth in microns 
            spd[keyA*1000] = spd.pop(keyA)  #replace old dict key with new key
        else:
            pass

    #If excel_daylight_series_cal data is used, values need to be normalized 0 to 1
    maxkey = max(spd, key=lambda i: spd[i])
    maxvalue = spd[maxkey]
    factor = 1/maxvalue

    if excel_daylight_series_cal == 1:
        source_interval = 10
        for keyB in spd:
            spd[keyB] = spd[keyB]*factor
        else:
            pass



#interpolate function
def interpolate(value1,value2,key1,key2,increment): 
    slope = (value2-value1)/(key2-key1)
    value = value1 + (slope*increment)
    return float(value)



#run interpolate function on spectral power distribution
def run_interpolate (dict, bin, interval):   # nanometer bins from source file, interval to interpolate
    for x in dict.keys():  # x = keys
        if x >= 380 and x <=780 and x % source_interval == 0:  #filter dictionary for interpolation
            dict[float(x + interval)] = interpolate (dict[x],dict[x+bin],x,x+bin,interval) #define key and value from interpolate function

if  check != "error" :
    for iteration in xrange (1,source_interval): # iterate run_interpolate function at 1 nm intervals over source_interval
        run_interpolate (spd,source_interval,iteration)



#bin and channel are interchangeable terms: bins between 380 - 780nm for 9 and 3 channels 
bin9 = [380,422],[422,460],[460,498],[498,524],[524,550],[550,586],[586,650],[650,714],[714,780] #9 channels: b1,b2,b3,g1,g2,g3,r1,r2,r3 
bin3 = [586,780],[498,586],[380,498]  #3 channels: r,g,b 

if channel_type == 0:
    binType = bin3
if channel_type == 1:
    binType = bin9



#avg_count iterates within wavelength bin to return average
def avg_count(dict, channel):  #9 channels to choose from
    sum = 0
    count = 0
    for key in dict:
       if key >= binType[channel][0] and key  <= binType[channel][1]: #cull array by channel lowest and highest key 
           sum += dict[key] #sum values in channel
           count += 1
    avg = sum/count
    return round (avg,3) #round 3 places



#use avg_count function on each bin to generate a list of averages
avg_channel = []   #output average color per channel
def avg_list(dict):
    for binX in xrange (len(binType)): #iterates to 3 or 9
        avg_channel.append(avg_count(dict,binX)) #iterate avg_count over all channels

if check != "error":
    #run avg_list function on each wavelength dictionary
    avg_list(spd)

    if avg_channel[0] > 1:
        print "warning: channel data should be betwen 0 & 1. Set excel_daylight_series_cal data to true"



#convert transmittance to transmissivity for Radiance material definition
def glazing_transmissivity(Tn):
    transmissivity = (math.sqrt(0.8402528435+(0.0072522239*(Tn * Tn)))-0.9166530661)/(0.003626119*Tn)
    return round (transmissivity,3)



#convert list of average transmittance to transmissivity
if material_type == 0:   #glass type
    for index, item in enumerate (avg_channel):
        avg_channel[index] = glazing_transmissivity (item)



#print channel_output
channel_output = avg_channel



#assign main material properties
if material_type == 0:
    type = "glass"
if material_type == 1:
    type = "plastic"

modifier = "void" #overwrite for custom Radiance modifiers



#write Radiance material definition
if  check != "error" and material_type == 0:  #glazing material

    if channel_type == 0:  #3-channel
        r,g,b = avg_channel
        mat3 = "%s %s %s \n" %(modifier,type,material_name)+ ("0" + "\n")*2 + "3 %s %s %s" %(r,g,b)

    if channel_type == 1: #9-channel
        b1,b2,b3,g1,g2,g3,r1,r2,r3 = avg_channel
        mat_a = "%s %s %s_a \n" %(modifier,type,material_name)+ ("0" + "\n")*2 + "3 %s %s %s" %(b1,b2,b3) 
        mat_b = "%s %s %s_b \n" %(modifier,type,material_name)+ ("0" + "\n")*2 + "3 %s %s %s" %(g1,g2,g3) 
        mat_c = "%s %s %s_c \n" %(modifier,type,material_name)+ ("0" + "\n")*2 + "3 %s %s %s" %(r1,r2,r3)

if  check != "error" and material_type == 1:  #plastic material

    if roughness == None:
        roughness = 0
    if roughness > 1:
        print "roughness should be between 0 -1 "

    if specularity == None:
        specularity = 0
    if specularity > 1:
        print "speculariy should be between 0 -1 "

    if channel_type == 0: #3 channel
        r,g,b = avg_channel
        mat3 = "%s %s %s \n" %(modifier,type,material_name)+ ("0" + "\n")*2 + "5 %s %s %s %s %s" %(r,g,b,specularity,roughness)

    if channel_type == 1: #9 channel
        b1,b2,b3,g1,g2,g3,r1,r2,r3 = avg_channel
        mat_a = "%s %s %s_a \n" %(modifier,type,material_name)+ ("0" + "\n")*2 + "5 %s %s %s %s %s" %(b1,b2,b3,specularity,roughness) 
        mat_b = "%s %s %s_b \n" %(modifier,type,material_name)+ ("0" + "\n")*2 + "5 %s %s %s %s %s" %(g1,g2,g3,specularity,roughness) 
        mat_c = "%s %s %s_c \n" %(modifier,type,material_name)+ ("0" + "\n")*2 + "5 %s %s %s %s %s" %(r1,r2,r3,specularity,roughness)



#write radiance material files
if  check != "error" and channel_type == 0 and material_type != 2 and material_type != 3:
    material = open(material_name + ".rad", "w")
    material.write(mat3)
    material.close()

if  check != "error" and channel_type == 1 and material_type != 2 and material_type != 3:
    materiala = open(material_name + "_a.rad", "w")
    materiala.write(mat_a)
    materiala.close()    

    materialb = open(material_name + "_b.rad", "w")
    materialb.write(mat_b)
    materialb.close() 

    materialc = open(material_name + "_c.rad", "w")
    materialc.write(mat_c)
    materialc.close()



#print filepaths for rad materials
if  check != "error" and channel_type == 0 and material_type != 2 and material_type != 3:
    mat_3 = os.getcwd() + "\\" + material_name+".rad"
    
if  check != "error" and channel_type == 1 and material_type != 2 and material_type != 3:
    mat_9a = os.getcwd() + "\\" + material_name + "_a.rad"
    mat_9b = os.getcwd() + "\\" + material_name + "_b.rad"
    mat_9c = os.getcwd() + "\\" + material_name + "_c.rad"
else:
    pass



#write channel_output file
if  check != "error":
    #output avg_channel
    g = open('spd_avg.txt', 'w')
    for item in avg_channel:
        g.write(str(item) + '\n')
    g.close()
