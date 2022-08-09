# Define 3 or 9 channel Radiance skies 

# Lark Spectral Lighting (v0.0.1, v0.0.2 and v1.0) is a collaboration of University of Washington and ZGF Architects LLP
# Authors Dr. Mehlika Inanici, Marty Brennan & Ed Clark
# Lark v2.0 is a collaboration of EPFL, Oregon State University, and Eindhoven University of Technology
# Authors Dr. Clotilde Pierson & Myrta Gkaintatzi-Masouti
# Copyright 2015-2022 Mehlika Inanici, Ph.D. (University of Washington) and ZGF Architects LLP
# Copyright 2022 Clotilde Pierson, Ph.D. (EPFL, Oregon State University) and Myrta Gkaintatzi-Masouti, M.Sc. (Eindhoven University of Technology)
# Licensed under The Modified 3-Clause BSD License (the "License");
# You may obtain a copy of the License at
# https://opensource.org/licenses/BSD-3-Clause

# Component updated by Dr. Priji Balakrishnan & Dr. Alstan J. Jakubiec (2020-05-17): 
# Updated Radiance sky definition with gendaylit replacing gensky

# Component updated by Dr. Clotilde Pierson for Lark v2.0 (2022-05-10):
# Removed gen_reindl program since models (Reindl, Erbs…) using only global horizontal sky irradiance for splitting up into direct and diffuse horizontal sky irradiance can show high deviations.
# Updated Radiance sky definition: gendaylit (version of 2021 in Radiance 5.4) including dew point temperature, RGB components of ground_glow have been set to a grey color (1,1,1) instead of a red color (1,0.8,0.5)
# Updated inputs (removed sky_type as information not needed for Perez sky model; modified horizontal_direct to normal_direct since gendaylit -W requires normal direct; removed global_illuminance/global_irradiation since gen_reindl program not used anymore; removed run_reindl since gen_reindl program not used anymore; added dew point temperature for more accurate sky definition)
# Updated outputs (removed reindl_output, diffuse_horizontal and direct_normal since gen_reindl program not used anymore)
# Updated RGB coefficients: R coefficient updated to 0.2685 (instead of 0.2686) for sum of 3 coefficients to equal 1

"""
Use this component to build Radiance sky definitions for rendering.  
-
Provided by Lark 2.0.0

    Args:
        channel_output: use Lark SPD component to write 3 or 9 spectral channels 
        channel_type: Choose [0 = 3 channel]  [1 = 9 channel]
        latitude: north of the equator is positive  
        longitude: west of the Prime Meridian is positive
        UTC:Coordinated Universal Time
        month: integer 1-12
        day: integer 1-31
        hour:float 1-24 (hour should not account for daylight saving time)
        normal_direct: normal direct irradiance
        horizontal_diffuse: float radiation from measurement
        temperature: dew point temperature
        name: optional name for sky spectrum (example: 10k_CCT)
    Returns:
        current_dir: current working folder 
        sky_name_out: Radiance sky definition name
        sky_mat_3: filepath for 3 channel sky definition
        sky_mat_9a: filepath for 9a channel sky definition
        sky_mat_9b: filepath for 9b channel sky definition
        sky_mat_9c: filepath for 9c channel sky definition
"""

ghenv.Component.Name = "Lark Build Spectral Radiance Sky Definitions v2"
ghenv.Component.NickName = 'Spectral Sky'
ghenv.Component.Message = '2.0.0'
ghenv.Component.Category = "Lark"
ghenv.Component.SubCategory = "Basic Lark"

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
inputs = [channel_output,channel_type,latitude,longitude,UTC,month,day,hour,normal_direct,horizontal_diffuse,temperature]
inputs_name = ["channel_output","channel_type","latitude","longitude","UTC","month","day","hour","normal_direct","horizontal_diffuse","temperature"]

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



#assign sky name and process inputs
if name == None:        
    name = ""

if  check != "error":
    space = "_"
    sky_name = "%s%s%s%s%s%s" %(month,space,day,space,hour,name)
    sky_name_out = sky_name

    #convert to minutes
    UTC = int(UTC * -15) #positive west of primer meridian
    longitude = longitude * -1  #positive west of prime meridian



#photopic coefficients for each channel
v_b1 = .0004
v_b2 = .0095
v_b3 = .0522
v_g1 = .1288
v_g2 = .2231
v_g3 = .3175
v_r1 = .2521
v_r2 = .0162
v_r3 = .0002

v_r =  .2685
v_g =  .6694
v_b =  .0621



#prepare variables for sky definition
if  check != "error":
    direct = normal_direct

    if channel_type == 0:
        if len(channel_output) == 3:
            r,g,b = channel_output #assign channels
            sum3 = r*v_r + g*v_g + b*v_b  #multiply each channel by photopic coefficient (sum is less than 1.0)
            #the weighting of the sky model to account for the spectral calculation is done on the RGB components of the sky below so that it does not impact the result of the luminous efficacy model in gendaylit if done on the irradiance
            diffuse = horizontal_diffuse
        else:
            print "channel_output should equal 3 values"

    if channel_type == 1:
        if len(channel_output) == 9:
            b1,b2,b3,g1,g2,g3,r1,r2,r3 = channel_output  #assign channels
            sum9 = b1*v_b1 + b2*v_b2 + b3*v_b3 + g1*v_g1 + g2*v_g2 + g3*v_g3 + r1*v_r1 + r2*v_r2 + r3*v_r3 #multiply each channel by photopic coefficient (sum is less than 1.0)
            #the weighting of the sky model to account for the spectral calculation is done on the RGB components of the sky below so that it does not impact the result of the luminous efficacy model in gendaylit if done on the irradiance
            diffuse = horizontal_diffuse
        else:
            print "channel_output should equal 9 values"



#write Radiance sky definition
    gendaylit =  "%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s \n" %("!gendaylit",month,day,hour,"-W",direct,diffuse,"-d",temperature,"-a",latitude,"-o",longitude,"-m",UTC)+ "\n"
    sky = "%s %s %s \n" %("sky_mat","source","sky") + ("0" + "\n")*2 + ("4" + "\n") + "%s %s %s %s" %(0,0,1,180) + "\n"*2
    ground_glow = "%s %s %s \n" %("skyfunc","glow","ground_glow") + ("0" + "\n")*2 + ("4" + "\n")+ "%s %s %s %s" %(1,1,1,0)+ "\n"*2
    ground = "%s %s %s \n" %("ground_glow","source","ground") + ("0" + "\n")*2 +("4" + "\n") +"%s %s %s %s" %(0,0,-1,180)
    sky_def = sky + ground_glow + ground + "\n" * 2



#write Radiance sky file
    if channel_type == 0:
        #the weighting of the sky model to account for the spectral calculation is done here on the RGB components of the sky so that it does not impact the result of the luminous efficacy model in gendaylit if done on the irradiance
        sky_mat =  "%s %s %s \n" %("skyfunc","glow","sky_mat") + ("0" + "\n")*2 +("4" + "\n") + "%s %s %s %s" %(round(r/sum3,2),round(g/sum3,2),round(b/sum3,2),0) + "\n" * 2
        material = open(sky_name+".rad", "w")
        material.write(gendaylit + sky_mat + sky_def)
        material.close()

    if channel_type == 1:
        #the weighting of the sky model to account for the spectral calculation is done here on the RGB components of the sky so that it does not impact the result of the luminous efficacy model in gendaylit if done on the irradiance
        sky_mat_a =  "%s %s %s \n" %("skyfunc","glow","sky_mat") + ("0" + "\n")*2 + ("4" + "\n") + "%s %s %s %s" %(round(b1/sum9,2),round(b2/sum9,2),round(b3/sum9,2),0) + "\n" * 2
        sky_mat_b =  "%s %s %s \n" %("skyfunc","glow","sky_mat") + ("0" + "\n")*2 + ("4" + "\n") + "%s %s %s %s" %(round(g1/sum9,2),round(g2/sum9,2),round(g3/sum9,2),0) + "\n" * 2
        sky_mat_c =  "%s %s %s \n" %("skyfunc","glow","sky_mat") + ("0" + "\n")*2 + ("4" + "\n") + "%s %s %s %s" %(round(r1/sum9,2),round(r2/sum9,2),round(r3/sum9,2),0) + "\n" * 2

        materiala = open(sky_name + "_a" +".rad", "w")
        materiala.write(gendaylit + sky_mat_a + sky_def)
        materiala.close()    

        materialb = open(sky_name + "_b" +".rad", "w")
        materialb.write(gendaylit + sky_mat_b + sky_def)
        materialb.close() 

        materialc = open(sky_name + "_c" +".rad", "w")
        materialc.write(gendaylit + sky_mat_c + sky_def)
        materialc.close() 



#print filepaths for rad sky
    sky_mat_3 = os.getcwd() + "\\" + sky_name+".rad"
    sky_mat_9a = os.getcwd() + "\\" + sky_name + "_a" +".rad"
    sky_mat_9b = os.getcwd() + "\\" + sky_name + "_b" +".rad"
    sky_mat_9c = os.getcwd() + "\\" + sky_name + "_c" +".rad"
