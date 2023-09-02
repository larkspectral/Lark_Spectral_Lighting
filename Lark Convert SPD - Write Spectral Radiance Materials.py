# Convert SPD to 3 or 9 channel Radiance materials
        
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
        
# Component updated by Dr. Clotilde Pierson for Lark v2.0 (2022-05-10):
# Added a fourth material type ([3 = electriclight]) and defined the main path accordingly

# Component updated by Bo Jung for Lark v3.0 (2023-07-03):
# Modified bins for 3 and 9 channel. Removed 'source_interval' and 'excel_daylight_series_cal' input. Script updated to auto-read input spectra interval and ignore any text in the input.
# If the range of SPD input is not between 380-780nm, the last digits will be repeated to make up the range. i.e. if the data started from 385nm (0.8W/m2)  and reached to 780nm, 0.8W/m2 will be copied in the beginning so that 380nm to 384n is also 0.8W/m2.      
        
"""
Use this component to convert spectral data to Radiance materials
-
Provided by Lark 3.0.0
        
    Args:
        spd_input: filepath to spectral power distribution txt file. column 1 = wavelength/ column 2 = transmittance or reflectance
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
        
ghenv.Component.Name = "Lark Convert SPD - Write Spectral Radiance Materials v3"
ghenv.Component.NickName = 'Spectral Materials'
ghenv.Component.Message = '3.0.0'
ghenv.Component.Category = "Lark"
ghenv.Component.SubCategory = "Basic Lark"
        
import re
import os
from subprocess import Popen
import math
from collections import OrderedDict
from decimal import Decimal
        
import Grasshopper.Kernel as gh
e = gh.GH_RuntimeMessageLevel.Error
w = gh.GH_RuntimeMessageLevel.Warning
        
#check for missing inputs
        
def is_input_valid(dic, name):
    if name not in dic:
        return False
    if dic[name] == None:
        return False
    if dic[name] == []:
        return False
    return True
            
            
error_list = []
inputs = [spd_input, material_name, roughness, specularity, material_type, channel_type]
inputs_name = ["spd_input", "material_name", "roughness", "specularity", "material_type", "channel_type"]
inputs_dict = {name:value for (value, name) in zip(inputs, inputs_name)}
        
# Raise Error if input is missing
for name, value in inputs_dict.items():
    if material_type == 2 or material_type == 3:  # for light sources, ignore roughness and specularity
        if 'roughness' in name or 'specularity' in name:
            continue
    if material_type == 2: # for sky, it's okay to leave out material name
        if 'material_name' in name:
            continue
    if not is_input_valid(inputs_dict, name):
        error_occurred = True
        error_list.append(name)
        
if len(error_list) > 0:
    ghenv.Component.AddRuntimeMessage(w, "Warning! Connect the following inputs: " + ", ".join(error_list))
            
else:
    error_occurred = False
        
        
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
        
def split_on_space_or_comma(line):
    line = line.strip()
    if ',' in line:
        return line.split(',')
    elif ' ' in line:
        return line.split()
    elif '\t' in line:
        return line.split('\t')
    else:
        ghenv.Component.AddRuntimeMessage(w, "Input should be separated by ',' or space or tab!")
        
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
        
#read lines of spectral data from 2 column text file - first column must be wavelength; the second is for values
#Note, values should be between 0 to 1. excel_daylight_series_cal data will be converted automatically
if not error_occurred:
    MIN_A, MAX_A = 380, 780
            
    lines = open(spd_input).readlines()
            
    lines = [split_on_space_or_comma(line) for line in lines if line.strip() != ""]
    lines = [line for line in lines if isfloat(line[0])]
    lines = [[float(word) for word in line] for line in lines]
    lines = [line for line in lines if line[0] >= MIN_A and line[0] <= MAX_A]
    lines = [line for line in lines if line[0] % 1 == 0]
            
    # copy previous data to make range 380 to 780nm  
    # (i.e. 390:1.0 to 770:0.8 will be 380:1.0 to 780:0.8)
    if lines[0][0] > MIN_A:
    	old_a, old_b = lines[0]
    	new_a, new_b = lines[1] 
    	a_diff = new_a - old_a
    	b_diff = new_b - old_b
    	grad = b_diff / a_diff
    	lines.insert(0, [MIN_A, old_b - grad * (old_a - MIN_A)])
            
    if lines[-1][0] < MAX_A:
    	old_a, old_b = lines[-2]
    	new_a, new_b = lines[-1]
    	a_diff = new_a - old_a
    	b_diff = new_b - old_b
    	grad = b_diff / a_diff
    	lines.insert(len(lines), [MAX_A, new_b + grad * (MAX_A - new_a)])
            
    newlines = [[float(word) for word in lines[0]]]
            
    for idx in range(len(lines)-1):
    	old_a, old_b = lines[idx]
    	new_a, new_b = lines[idx+1]
    	interp_num = int(new_a - old_a)
    	assert interp_num > 0
    	new_a_list = [old_a + (new_a - old_a) / interp_num * (idx + 1) for idx in range(interp_num)]
    	new_b_list = [old_b + (new_b - old_b) / interp_num * (idx + 1) for idx in range(interp_num)]
    	newlines.extend(zip(new_a_list, new_b_list))
            
    spd_dict = {}
    for line in newlines:
    	spd_dict[line[0]] = line[1]
        
# bin and channel are interchangeable terms: bins between 380 - 780nm for 9 and 3 channels 
bin9 = [380,419],[419,459],[459,499],[499,529],[529,558],[558,587],[587,608],[608,630],[630,780] #9 channels: b1,b2,b3,g1,g2,g3,r1,r2,r3 
bin3 = [587,780],[499,587],[380,499]  #3 channels: r,g,b 
        
if channel_type == 0:
    binType = bin3
if channel_type == 1:
    binType = bin9
        
# avg_count iterates within wavelength bin to return average
def avg_count(dict, channel):  #9 channels to choose from
    sum = 0
    count = 0
    for key in dict:
       if key >= binType[channel][0] and key  <= binType[channel][1]: # cull array by channel lowest and highest key 
           sum += dict[key] # sum values in channel
           count += 1
    avg = sum/count
    return round (avg,3) # round 3 places
        
        
        
# use avg_count function on each bin to generate a list of averages
avg_channel = []   # output average color per channel
def avg_list(dict):
    for binX in xrange (len(binType)): # iterates to 3 or 9
        avg_channel.append(avg_count(dict,binX)) # iterate avg_count over all channels
        
if not error_occurred:
    #run avg_list function on each wavelength dictionary
    avg_list(spd_dict)
 
        
# convert transmittance to transmissivity for Radiance material definition
def glazing_transmissivity(Tn):
    transmissivity = (math.sqrt(0.8402528435+(0.0072522239*(Tn * Tn)))-0.9166530661)/(0.003626119*Tn)
    return round (transmissivity,3)
        
        
        
# convert list of average transmittance to transmissivity
if material_type == 0:   #glass type
    for index, item in enumerate (avg_channel):
        avg_channel[index] = glazing_transmissivity (item)
        
        
        
# print channel_output
channel_output = avg_channel
        
        
        
# assign main material properties
if material_type == 0:
    type = "glass"
if material_type == 1:
    type = "plastic"
        
modifier = "void" # overwrite for custom Radiance modifiers
        
        
        
# write Radiance material definition
if  not error_occurred and material_type == 0:  # glazing material
        
    if channel_type == 0:  # 3-channel
        r,g,b = avg_channel
        mat3 = "%s %s %s \n" %(modifier,type,material_name)+ ("0" + "\n")*2 + "3 %s %s %s" %(r,g,b)
        
    if channel_type == 1: # 9-channel
        b1,b2,b3,g1,g2,g3,r1,r2,r3 = avg_channel
        mat_a = "%s %s %s_a \n" %(modifier,type,material_name)+ ("0" + "\n")*2 + "3 %s %s %s" %(b1,b2,b3) 
        mat_b = "%s %s %s_b \n" %(modifier,type,material_name)+ ("0" + "\n")*2 + "3 %s %s %s" %(g1,g2,g3) 
        mat_c = "%s %s %s_c \n" %(modifier,type,material_name)+ ("0" + "\n")*2 + "3 %s %s %s" %(r1,r2,r3)
        
if  not error_occurred and material_type == 1:  # plastic material
        
    if roughness == None:
        roughness = 0
    if roughness > 1:
        ghenv.Component.AddRuntimeMessage(w, "roughness should be between 0 -1 ")
        
    if specularity == None:
        specularity = 0
    if specularity > 1:
        ghenv.Component.AddRuntimeMessage(w, "speculariy should be between 0 -1 ")
        
    if channel_type == 0: # 3 channel
        r,g,b = avg_channel
        mat3 = "%s %s %s \n" %(modifier,type,material_name)+ ("0" + "\n")*2 + "5 %s %s %s %s %s" %(r,g,b,specularity,roughness)
        
    if channel_type == 1: # 9 channel
        b1,b2,b3,g1,g2,g3,r1,r2,r3 = avg_channel
        mat_a = "%s %s %s_a \n" %(modifier,type,material_name)+ ("0" + "\n")*2 + "5 %s %s %s %s %s" %(b1,b2,b3,specularity,roughness) 
        mat_b = "%s %s %s_b \n" %(modifier,type,material_name)+ ("0" + "\n")*2 + "5 %s %s %s %s %s" %(g1,g2,g3,specularity,roughness) 
        mat_c = "%s %s %s_c \n" %(modifier,type,material_name)+ ("0" + "\n")*2 + "5 %s %s %s %s %s" %(r1,r2,r3,specularity,roughness)
        
        
        
# write radiance material files
if  not error_occurred and channel_type == 0 and material_type != 2 and material_type != 3:
    material = open(material_name + ".rad", "w")
    material.write(mat3)
    material.close()
        
if  not error_occurred and channel_type == 1 and material_type != 2 and material_type != 3:
    materiala = open(material_name + "_a.rad", "w")
    materiala.write(mat_a)
    materiala.close()    
        
    materialb = open(material_name + "_b.rad", "w")
    materialb.write(mat_b)
    materialb.close() 
        
    materialc = open(material_name + "_c.rad", "w")
    materialc.write(mat_c)
    materialc.close()
        
        
        
# print filepaths for rad materials
if  not error_occurred and channel_type == 0 and material_type != 2 and material_type != 3:
    mat_3 = os.getcwd() + "\\" + material_name+".rad"
            
if  not error_occurred and channel_type == 1 and material_type != 2 and material_type != 3:
    mat_9a = os.getcwd() + "\\" + material_name + "_a.rad"
    mat_9b = os.getcwd() + "\\" + material_name + "_b.rad"
    mat_9c = os.getcwd() + "\\" + material_name + "_c.rad"
else:
    pass
        
        
        
# write channel_output file
if not error_occurred:
    #output avg_channel
    g = open('spd_avg.txt', 'w')
    for item in avg_channel:
        g.write(str(item) + '\n')
    g.close()
        
