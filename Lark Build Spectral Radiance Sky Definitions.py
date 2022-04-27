# Define 3 or 9 channel Radiance skies 
# Lark Spectral Lighting is a collaboration of University of Washington and ZGF Architects LLP
# Authors Dr. Mehlika Inanici, Marty Brennan & Ed Clark
# Copyright 2015-2022 Mehlika Inanici, Ph.D. (University of Washington) and ZGF Architects LLP
# Licensed under The 3-Clause BSD License (the "License");
# You may obtain a copy of the License at
# https://opensource.org/licenses/BSD-3-Clause

"""
Use this component to build Radiance sky definitions for rendering.  
-
Provided by lark v1.0

    Args:
        channel_output: use Lark SPD component to write 3 or 9 spectral channels 
        channel_type: Choose [0 = 3 channel]  [1 = 9 channel]
        latitude: north of the equator is positive  
        longitude: west of the Prime Meridian is positive
        UTC:Coordinated Universal Time 
        sky_type:[0 = clear sunny] [2 = intermediate] [4 = overcast]
        month: integer 1-12
        day: integer 1-31
        hour:float 1-24
        horizontal_direct: float radiation from measurement
        horizontal_diffuse: float radiation from measurement
        global_illuminance: calculated illuminance from unobstructed point looking up for CIE sky condition
        run_reindl: boolean to start gen_reindl program - place gen_reindl.exe in c:\lark\materials
        name: optional name for sky spectrum (example: 10k_CCT)
    Returns:
        current_dir: current working folder 
        sky_name_out: Radiance sky definition name
        reindl_output: gen_reindl txt output [month,day,hour,direct irradiance,diffuse irradiance]
        diffuse_horizontal: diffuse component of gen_reindl
        direct_normal: direct normal component of gen_reindl
        sky_mat_3: filepath for 3 channel sky definition
        sky_mat_9a: filepath for 9a channel sky definition
        sky_mat_9b: filepath for 9b channel sky definition
        sky_mat_9c: filepath for 9c channel sky definition
"""

ghenv.Component.Name = "Lark Build Spectral Radiance Sky Definitions"
ghenv.Component.NickName = 'Spectral Sky'
ghenv.Component.Message = 'v1.0'
ghenv.Component.Category = "Extra"
ghenv.Component.SubCategory = "lark"


import re
import os
from subprocess import Popen
import math
from collections import OrderedDict
from decimal import Decimal



#make lark directory if none exists
_path = 'C:\lark\materials'
if os.path.isdir(_path) != True: 
    os.makedirs(_path)
else:
    pass

os.chdir(_path)
#print out current directory
current_dir = _path


#check all inputs
error_list = []
inputs = [channel_output,channel_type,latitude,longitude,UTC,sky_type,month,day,hour,global_illuminance,run_reindl]
inputs_name = ["channel_output","channel_type","latitude","longitude","UTC","sky_type","month","day","hour","global_illuminance","run_reindl"]

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
    print check
#    print len(error_list)


if name == None:        
    name = ""

if  check != "error":
    if sky_type == 0:
        sky_type = "+s"  #sunny
        condition_name = "_s"
    if sky_type == 2:
        sky_type = "+i"  #intermediate
        condition_name = "_i"
    if sky_type == 4:
        sky_type = "-c"  #overcast
        condition_name = "_oc"
    space = "_"
    sky_name = "%s%s%s%s%s%s%s" %(month,space,day,space,hour,condition_name,name)
    sky_name_out = sky_name
    #convert global_illuminance to global_irradiance
    irrad = global_illuminance/179


    #write out a gen_reindl tab delimited file
    reindl_out = str(month) + "\t" + str(day)+ "\t" + str(hour)+ "\t" + str(irrad)   

    irradiance_out = open("reindl_out.txt", "w")
    irradiance_out.write(reindl_out) 
    irradiance_out.close()

    #convert to minutes
    UTC = int(UTC * -15) #positive west of primer meridian

    longitude = longitude * -1  #positive west of prime meridian

    batchfile = "%s %s %s %s %s %s %s" %("gen_reindl -m",UTC,"-l",longitude,"-a",latitude,"-i reindl_out.txt -o reindl.wea")


    batch = open("gen_reindl.bat", "w")
    batch.write(batchfile)
    batch.close()


if run_reindl != True or check == "error":
    pass
else:
    runbatch = Popen("gen_reindl.bat", cwd=_path)
    stdout, stderr = runbatch.communicate()

#read direct and diffuse outputs from gen_reindl output

    reindl_list = [] 
    reindl_reader = open("reindl.wea", "r") 
    for line in reindl_reader:
        direct,diffuse = line.split()[3:5]
        reindl_list.append(line)
    reindl_reader.close()

    reindl_output = reindl_list
    diffuse_horizontal = diffuse
    direct_normal  = direct

#photopic coefficients for each channel
v_b1 = .0004
v_b2 = .0095
v_b3 = .0522
v_g1 = .1288
v_g2 = .2231
v_g3 = .3174
v_r1 = .2521
v_r2 = .0162
v_r3 = .0002

v_r =  .2686  #.275
v_g =  .6693  #.670
v_b =  .0621  #.065  



if  check != "error" and run_reindl != False:
    
    if horizontal_direct == None:
        direct = round(float(irrad) - float(diffuse),2)
    else:
        direct = horizontal_direct

    if channel_type == 0:
        if len(channel_output) == 3:
            r,g,b = channel_output #assign channels
            sum3 = r*v_r + g*v_g + b*v_b  #multiply each channel by photopic coefficient (sum is less than 1.0)
            if horizontal_diffuse == None:
                diffuse = round(float(diffuse)/ sum3,2)
            else:
                diffuse = round(horizontal_diffuse/ sum3,2)
        else:
            print "channel_output should equal 3 values"

    if channel_type == 1:
        if len(channel_output) == 9:
            b1,b2,b3,g1,g2,g3,r1,r2,r3 = channel_output  #assign channels
            sum9 = b1*v_b1 + b2*v_b2 + b3*v_b3 + g1*v_g1 + g2*v_g2 + g3*v_g3 + r1*v_r1 + r2*v_r2 + r3*v_r3  #multiply each channel by photopic coefficient (sum is less than 1.0)
            if horizontal_diffuse == None:
                diffuse = round(float(diffuse)/ sum9,2)
            else:
                diffuse = round(horizontal_diffuse/ sum9,2)
        else:
            print "channel_output should equal 9 values"



    gensky =  "%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s \n" %("!gensky",month,day,hour,sky_type,"-B",diffuse,"-R",direct,"-a",latitude,"-o",longitude,"-m",UTC)+ "\n" 
    sky = "%s %s %s \n" %("sky_mat","source","sky") + ("0" + "\n")*2 + ("4" + "\n") + "%s %s %s %s" %(0,0,1,180) + "\n"*2
    ground_glow = "%s %s %s \n" %("skyfunc","glow","ground_glow") + ("0" + "\n")*2 + ("4" + "\n")+ "%s %s %s %s" %(1,0.8,0.5,0)+ "\n"*2 
    ground = "%s %s %s \n" %("ground_glow","source","ground") + ("0" + "\n")*2 +("4" + "\n") +"%s %s %s %s" %(0,0,-1,180)
    sky_def = sky + ground_glow + ground + "\n" * 2


    if channel_type == 0:
        sky_mat =  "%s %s %s \n" %("skyfunc","glow","sky_mat") + ("0" + "\n")*2 +("4" + "\n") + "%s %s %s %s" %(r,g,b,0) + "\n" * 2
        material = open(sky_name+".rad", "w")
        material.write(gensky + sky_mat + sky_def)
        material.close()

        
    if channel_type == 1:
        sky_mat_a =  "%s %s %s \n" %("skyfunc","glow","sky_mat") + ("0" + "\n")*2 + ("4" + "\n") + "%s %s %s %s" %(b1,b2,b3,0) + "\n" * 2
        sky_mat_b =  "%s %s %s \n" %("skyfunc","glow","sky_mat") + ("0" + "\n")*2 + ("4" + "\n") + "%s %s %s %s" %(g1,g2,g3,0) + "\n" * 2
        sky_mat_c =  "%s %s %s \n" %("skyfunc","glow","sky_mat") + ("0" + "\n")*2 + ("4" + "\n") + "%s %s %s %s" %(r1,r2,r3,0) + "\n" * 2

        materiala = open(sky_name + "_a" +".rad", "w")
        materiala.write(gensky + sky_mat_a + sky_def)
        materiala.close()    

        materialb = open(sky_name + "_b" +".rad", "w")
        materialb.write(gensky + sky_mat_b + sky_def)
        materialb.close() 

        materialc = open(sky_name + "_c" +".rad", "w")
        materialc.write(gensky + sky_mat_c + sky_def)
        materialc.close() 




    #print filepaths for output pictures (all pictures are greyscale luminance to be viewed in falsecolor)
    sky_mat_3 = os.getcwd() + "\\" + sky_name+".rad"
    sky_mat_9a = os.getcwd() + "\\" + sky_name + "_a" +".rad"
    sky_mat_9b = os.getcwd() + "\\" + sky_name + "_b" +".rad"
    sky_mat_9c = os.getcwd() + "\\" + sky_name + "_c" +".rad"