# Define 3 channel radiance sky using Perez -C (colored) option

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
                                                                                        
                                                                
"""
Use this component to build Radiance sky (gendaylit luminance based spectral sky) definitions.  
-
Provided by Lark 3.0.0
        
    Args:
        channel_type: Choose [0 = 3 channel]  [1 = 9 channel]
        latitude: north of the equator is positive  
        longitude: west of the Prime Meridian is positive
        UTC:Coordinated Universal Time
        month: integer 1-12
        day: integer 1-31
        hour:float 1-24 (hour should not account for daylight saving time)
        normal_dir_irrad: normal direct irradiance
        horizontal_diff_irrad: horizontal diffuse irradiance
        dir_diff_OR_global: Choose [0 = direct & diffuse irradiance (-W option in gendaylit)] [1 = global irradiance (-E option in gendaylit)] 
        global_hor_irrad: global horizontal irradiance
    Returns:
        sky_def_3: 3 channel sky definition
"""

__author__ = "bojung"
__version__ = "2023"

ghenv.Component.Name = "Lark Perez Sky - Colored with Luminance v3"
ghenv.Component.NickName = 'Spectral Sky'
ghenv.Component.Message = '3.0.0'
ghenv.Component.Category = "Lark"
ghenv.Component.SubCategory = "Basic Lark"

import re
import os
from subprocess import check_output
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
inputs = [latitude, longitude, UTC, month, day, hour, normal_dir_irrad, horizontal_diff_irrad, dir_diff_OR_global, global_hor_irrad]
inputs_name = ["latitude", "longitude", "UTC", "month", "day", "hour", "normal_dir_irrad", "horizontal_diff_irrad", "dir_diff_OR_global", "global_hor_irrad"]
inputs_dict = {name:value for (value, name) in zip(inputs, inputs_name)}

# Raise Error if input is missing
for name, value in inputs_dict.items():
    if 'irrad' in name or 'dir_diff' in name:
        continue
    if not is_input_valid(inputs_dict, name):
        error_occurred = True
        error_list.append(name)
#        print("Warning! Connect the following inputs:", name)

# Raise Error if global / dir / diff irrad is not provided 
valid_global = is_input_valid(inputs_dict, 'global_hor_irrad')
valid_normal = is_input_valid(inputs_dict, 'normal_dir_irrad')
valid_horizontal = is_input_valid(inputs_dict, 'horizontal_diff_irrad')

global_mode = (inputs_dict['dir_diff_OR_global'] == 1) and valid_global
dir_diff_mode = (inputs_dict['dir_diff_OR_global'] == 0) and valid_normal and valid_horizontal

error_occurred = False

if not (global_mode or dir_diff_mode):
    ghenv.Component.AddRuntimeMessage(w, "Warning! if dir_diff_OR_global = 0, connect 'global_hor_irrad' AND 'normal_dir_irrad', or if dir_diff_OR_global = 1, connect 'horizontal_diff_irrad'")
    error_occurred = True
    
if len(error_list) > 0:
    ghenv.Component.AddRuntimeMessage(w, "Warning! Connect the following inputs: " + ", ".join(error_list))

if not error_occurred:
    # define CCT based colored perez sky
    # 1. convert variables
    # 1.1 UTC - convert to minutes
    print(-8 * -15)
    UTC = int(UTC * -15)  # positive west of primer meridian
    
    longitude = longitude * -1  # positive west of prime meridian
        
    # 1.2. sky definition
    direct = normal_dir_irrad
    diffuse = horizontal_diff_irrad
    globl = global_hor_irrad
    
    # 1. Write gendaylit
    if dir_diff_OR_global == 0:
        gendaylit =  "%s %s %s %s %s %s %s %s %s %s %s %s %s %s" %("gendaylit",month,day,hour, "-C", "-W",direct,diffuse,"-a",latitude,"-o",longitude,"-m",UTC)
    if dir_diff_OR_global == 1:
        gendaylit =  "%s %s %s %s %s %s %s %s %s %s %s %s %s" %("gendaylit",month,day,hour, "-C", "-E",globl,"-a",latitude,"-o",longitude,"-m",UTC)
    
    sky_mat = "%s %s %s \n" %("skyfunc","glow","sky_mat") + ("0" + "\n")*2 + ("4" + "\n") + "%s %s %s %s" %(1,1,1,0) + "\n"*2
    sky = "%s %s %s \n" %("sky_mat","source","sky") + ("0" + "\n")*2 + ("4" + "\n") + "%s %s %s %s" %(0,0,1,180) + "\n"*2
    ground_glow = "%s %s %s \n" %("skyfunc","glow","ground_glow") + ("0" + "\n")*2 + ("4" + "\n")+ "%s %s %s %s" %(1,0.8,0.5,0)+ "\n"*2
    ground = "%s %s %s \n" %("ground_glow","source","ground") + ("0" + "\n")*2 +("4" + "\n") +"%s %s %s %s" %(0,0,-1,180)
    sky_def = sky_mat + sky + ground_glow + ground
    
    sky_def_3 = "!" + gendaylit + "\n" + sky_def
    print(sky_def_3)