# Write sky file to have colored sun and sky

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
                                
# Component updated by Dr. Priji Balakrishnan & Dr. Alstan J. Jakubiec (2020-05-17): 
# Updated Radiance sky definition with gendaylit replacing gensky
                                
# Component updated by Dr. Clotilde Pierson for Lark v2.0 (2022-05-10):
# Removed gen_reindl program since models (Reindl, Erbs…) using only global horizontal sky irradiance for splitting up into direct and diffuse horizontal sky irradiance can show high deviations.
# Updated Radiance sky definition: gendaylit (version of 2021 in Radiance 5.4) including dew point temperature, RGB components of ground_glow have been set to a grey color (1,1,1) instead of a red color (1,0.8,0.5)
# Updated inputs (removed sky_type as information not needed for Perez sky model; modified horizontal_direct to normal_direct since gendaylit -W requires normal direct; removed global_illuminance/global_irradiation since gen_reindl program not used anymore; removed run_reindl since gen_reindl program not used anymore; added dew point temperature for more accurate sky definition)
# Updated outputs (removed reindl_output, diffuse_horizontal and direct_normal since gen_reindl program not used anymore)
# Updated RGB coefficients: R coefficient updated to 0.2685 (instead of 0.2686) for sum of 3 coefficients to equal 1
                                      
# Component updated by Bo Jung for Lark v3.0 (2023-01-28):
# Put in option to use direct and diffuse irradiance (-W) option or global irradiance (-E) option in gendaylit
# Updated inputs (removed temperature as information not needed for Perez sky model; Added option for global_hor_irrad (-E option in gendaylit); Added option to input spectral information for the sun (direct_channel).; removed current_dir as the outputs are not written in a file.)
# Updated outputs (sky_def directly output the sky definitions, no longer referencing sky file directory. The outputs are written into sky files later on in the gh script).
                                
                                
"""
Use this component to build Radiance sky (Perez spectra based sky and sun) definitions.  
-                    
Provided by Lark 3.0.0
                                        
    Args:
        diffuse_channel: color of the sky - use Lark SPD component to write 3 or 9 spectral channels 
        direct_channel: color of the sun - use lark SPD componenet to write 3 or 9 spectral channels
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
        sky_def_9a: 9a channel sky definition
        sky_def_9b: 9b channel sky definition
        sky_def_9c: 9c channel sky definition
"""
                                
__author__ = "bojung"
__version__ = "2023"
                                
ghenv.Component.Name = "Lark Perez Sky - Colored with Sky and Sun Spectra v3"
ghenv.Component.NickName = 'Spectral Sky and Sun'
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
inputs = [channel_type, diffuse_channel, direct_channel, latitude, longitude, UTC, month, day, hour, normal_dir_irrad, horizontal_diff_irrad, dir_diff_OR_global, global_hor_irrad]
inputs_name = ["channel_type", "diffuse_channel", "direct_channel", "latitude", "longitude", "UTC", "month", "day", "hour", "normal_dir_irrad", "horizontal_diff_irrad", "dir_diff_OR_global", "global_hor_irrad"]
inputs_dict = {name:value for (value, name) in zip(inputs, inputs_name)}
                                
# Raise Error if input is missing
for name, value in inputs_dict.items():
    if 'irrad' in name or 'dir_diff' in name:
        continue
    if not is_input_valid(inputs_dict, name):
        error_occurred = True
        error_list.append(name)
        # print("Warning! Connect the following inputs:", name)
                                
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
                                    
    # 2. Assign Sun and Sky color
    # 2.1. Assign RGB for 3C or 9C
    if channel_type == 0:  # 3C
        if len(diffuse_channel) == 3 and len(direct_channel) == 3:
            print("channel type is 3C")
            print("direct:", direct_channel)
            print("diffuse:", diffuse_channel)
            r_solar,g_solar,b_solar = direct_channel 
            r_diff,g_diff,b_diff = diffuse_channel 
        else:
            ghenv.Component.AddRuntimeMessage(w, "diffuse and direct channel should equal 3 values as channel_type is 0")
                                
    if channel_type == 1:  #9c
        if len (diffuse_channel) == 9 and len(direct_channel) == 9:
            print("channel type is 9C")
            print("direct:", direct_channel)
            print("diffuse:", diffuse_channel)
            b1_solar,b2_solar,b3_solar,g1_solar,g2_solar,g3_solar,r1_solar,r2_solar,r3_solar = direct_channel 
            b1_diff,b2_diff,b3_diff,g1_diff,g2_diff,g3_diff,r1_diff,r2_diff,r3_diff = diffuse_channel
        else:
            ghenv.Component.AddRuntimeMessage(w, "diffuse and direct channel should equal 9 values as channel_type is 1")
                                    
    # photopic coefficients for 3C and 9C 
    v3_r =  .265  
    v3_g =  .67  
    v3_b =  .065  
                                    
    v9_r1 = .130177072
    v9_r2 = .081085718
    v9_r3 = .049591265
    v9_g1 = .164071102
    v9_g2 = .250355905
    v9_g3 = .259754249
    v9_b1 = .0003  
    v9_b2 = .009098397
    v9_b3 = .055590209
                                    
    # 3. Modify sun color
    # 3.1. Write gendaylit
    if dir_diff_OR_global == 0:
        gendaylit =  "%s %s %s %s %s %s %s %s %s %s %s %s %s" %("gendaylit",month,day,hour,"-W",direct,diffuse,"-a",latitude,"-o",longitude,"-m",UTC)
    if dir_diff_OR_global == 1:
        gendaylit =  "%s %s %s %s %s %s %s %s %s %s %s %s" %("gendaylit",month,day,hour,"-E",globl,"-a",latitude,"-o",longitude,"-m",UTC)
                                        
                                    
    print(gendaylit)
    # 3.2. Run gendaylit to get solar rgb color
    gendaylit_out = check_output(gendaylit)
                                    
    # 3.3. Calculate modified solar rgb based on gendaylit_out
    for idx, line in enumerate(gendaylit_out.split('\n')):
        if len(line) == 0:
            continue
        if line[0] == "3":  # for line that has RGB color component for the sun
            line_num_to_sub = idx
            # split with space and save as a list called solar_rgb
            solar_rgb = [float(x) for x in line.strip().split(' ')]
            print(solar_rgb)
                                            
            # Calculate coefficient to multiply each rgb values to scale them
            if channel_type == 0:  # 3C
                sum3_solar = r_solar*v3_r + g_solar*v3_g + b_solar*v3_b
                coef_solar = ((solar_rgb[1] + solar_rgb[2] + solar_rgb[3]) / 3) / sum3_solar
                                                
                # Change RGB to scaled RGB
                solar_rgb[1] = round(r_solar*coef_solar,2)
                solar_rgb[2] = round(g_solar*coef_solar,2)
                solar_rgb[3] = round(b_solar*coef_solar,2)  # Change RGB to scaled RGB
                                                
                solar_rgb = [int(item) if index == 0 else item for index, item in enumerate(solar_rgb)]
                solar_rgb = ' '.join([str(i) for i in solar_rgb])
                                                
                # 3.4. Modify solar light source rgb in gendaylit result (gendaylit_out)
                # 3.4.1. Save results of gen_daylit as a list of strings (divided by new line)
                gendaylit_out_mod = gendaylit_out.split('\n') 
                                                
                # 3.4.2. Replace original gendaylit result with modified solar rgb
                gendaylit_out_mod[line_num_to_sub] = str(solar_rgb) 
                                                
                # 3.4.3. Concatenate list back to strings
                gendaylit_out_mod = '\n'.join([item.strip() for item in gendaylit_out_mod[:]])
                                    
                                                
            if channel_type == 1:
                sum9_solar = r1_solar*v9_r1 + r2_solar*v9_r2 + r3_solar*v9_r3 + \
                             g1_solar*v9_g1 + g2_solar*v9_g2 + g3_solar*v9_g3 + \
                             b1_solar*v9_b1 + b2_solar*v9_b2 + b3_solar*v9_b3

                coef_solar = solar_rgb[1] / sum9_solar
         
                # copy solar_rgb 3 times
                solar_mat_a = solar_rgb[:]
                solar_mat_b = solar_rgb[:]
                solar_mat_c = solar_rgb[:]
                                                
                # change 9c solar rgb to scaled color
                solar_mat_a[1] = round(b1_solar*coef_solar,2)
                solar_mat_a[2] = round(b2_solar*coef_solar,2)
                solar_mat_a[3] = round(b3_solar*coef_solar,2)
                solar_mat_b[1] = round(g1_solar*coef_solar,2)
                solar_mat_b[2] = round(g2_solar*coef_solar,2)
                solar_mat_b[3] = round(g3_solar*coef_solar,2)
                solar_mat_c[1] = round(r1_solar*coef_solar,2)
                solar_mat_c[2] = round(r2_solar*coef_solar,2)
                solar_mat_c[3] = round(r3_solar*coef_solar,2)
                                                
                solar_tot = [solar_mat_a, solar_mat_b, solar_mat_c]
                for idx in range(3):
                   solar_tot[idx] = [int(item) if index == 0 else item for index, item in enumerate(solar_tot[idx])]
                   solar_tot[idx] = ' '.join([str(j) for j in solar_tot[idx]])
                                                
                solar_mat_a, solar_mat_b, solar_mat_c = solar_tot
                          
                                    
                # 3.4. Modify solar light source rgb in gendaylit result (gendaylit_out)
                # 3.4.1. Save results of gen_daylit as a list of strings (divided by new line)
                gendaylit_out_mod_a = gendaylit_out.split('\n') 
                gendaylit_out_mod_b = gendaylit_out.split('\n') 
                gendaylit_out_mod_c = gendaylit_out.split('\n') 
                                                
                # 3.4.2. Replace original gendaylit result with modified solar rgb
                gendaylit_out_mod_a[line_num_to_sub] = str(solar_mat_a) 
                gendaylit_out_mod_b[line_num_to_sub] = str(solar_mat_b) 
                gendaylit_out_mod_c[line_num_to_sub] = str(solar_mat_c) 
                                                
                # 3.4.3. Concatenate list back to strings
                gendaylit_out_mod_a = '\n'.join([item.strip() for item in gendaylit_out_mod_a[:]])
                gendaylit_out_mod_b = '\n'.join([item.strip() for item in gendaylit_out_mod_b[:]])
                gendaylit_out_mod_c = '\n'.join([item.strip() for item in gendaylit_out_mod_c[:]])

                                            
    # 4. Modify sky color
    # 4.1. Write Radiance Sky Definition
    sky = "%s %s %s \n" %("sky_mat","source","sky") + ("0" + "\n")*2 + ("4" + "\n") + "%s %s %s %s" %(0,0,1,180) + "\n"*2
    ground_glow = "%s %s %s \n" %("skyfunc","glow","ground_glow") + ("0" + "\n")*2 + ("4" + "\n")+ "%s %s %s %s" %(1,1,1,0)+ "\n"*2
    ground = "%s %s %s \n" %("ground_glow","source","ground") + ("0" + "\n")*2 +("4" + "\n") +"%s %s %s %s" %(0,0,-1,180)
    sky_def = sky + ground_glow + ground + "\n" * 2
                                    
    # 4.2. Calculate diffuse irradiance ratio
    if channel_type == 0:
        sum3 = r_diff*v3_r + g_diff*v3_g + b_diff*v3_b  # multiply each channel by photopic coefficient (sum is less than 1.0)
        sky_mat = "%s %s %s \n" %("skyfunc","glow","sky_mat") + \
                    ("0" + "\n")*2 + \
                    ("4" + "\n") + \
                    "%s %s %s %s" %(round(r_diff/sum3,2),round(g_diff/sum3,2),round(b_diff/sum3,2),0) + \
                    "\n" * 2
        sky_def_3 = gendaylit_out_mod + "\n" + sky_mat + sky_def
                                        
                                    
    if channel_type == 1:
        # the weighting of the sky model to account for the spectral calculation is done here on the RGB components of the sky so that it does not impact the result of the luminous efficacy model in gendaylit if done on the irradiance
        sum9_diff = r1_diff*v9_r1 + r2_diff*v9_r2 + r3_diff*v9_r3 + \
                             g1_diff*v9_g1 + g2_diff*v9_g2 + g3_diff*v9_g3 + \
                             b1_diff*v9_b1 + b2_diff*v9_b2 + b3_diff*v9_b3
                                                             
        sky_mat_a =  "%s %s %s \n" %("skyfunc","glow","sky_mat") + ("0" + "\n")*2 + ("4" + "\n") + \
                     "%s %s %s %s" %(round(b1_diff/sum9_diff,2),round(b2_diff/sum9_diff,2),round(b3_diff/sum9_diff,2),0) + "\n" * 2
        sky_mat_b =  "%s %s %s \n" %("skyfunc","glow","sky_mat") + ("0" + "\n")*2 + ("4" + "\n") + \
                     "%s %s %s %s" %(round(g1_diff/sum9_diff,2),round(g2_diff/sum9_diff,2),round(g3_diff/sum9_diff,2),0) + "\n" * 2
        sky_mat_c =  "%s %s %s \n" %("skyfunc","glow","sky_mat") + ("0" + "\n")*2 + ("4" + "\n") + \
                     "%s %s %s %s" %(round(r1_diff/sum9_diff,2),round(r2_diff/sum9_diff,2),round(r3_diff/sum9_diff,2),0) + "\n" * 2
                                
        sky_def_9a = gendaylit_out_mod_a + "\n" + sky_mat_a + sky_def
        sky_def_9b = gendaylit_out_mod_b + "\n" + sky_mat_b + sky_def
        sky_def_9c = gendaylit_out_mod_c + "\n" + sky_mat_c + sky_def
                                        
                                
                        
                
        
