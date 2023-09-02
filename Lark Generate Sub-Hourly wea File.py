# Run ds_shortterm to get sub-hourly irradiance.

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
Use this to create a wea weather file with subhourly data. 
This is necessary to run the nvRD component for which the input data should be with a timestep of 6 minutes (reccommended resolution).
-
This component uses the ds_shortterm program of daysim which uses a stochastic model to compute irradiance data with 1-min resolution from hourly data. 
-
More information about how it works in this paper: Walkenhorst et al., 2002, "Dynamic annual daylight simulations based on one-hour and one-minute means of irradiance data".
https://www.sciencedirect.com/science/article/pii/S0038092X02000191?via%3Dihub
-
Provided by Lark 3.0.0

    Inputs:
        epw: Path to an epw weather file
        folder: Folder to save the wea file which comes as an output
        timestep: Timestep within the hour in minutes. This should be an integer betweeen 1 and 60 (60 = hourly timestep, 1 = timestep every minute).
        RunIt: A boolean toggle to run this component
    Output:
        shortWea: The path to the generated wea file with subhourly data
"""

__author__ = "mgkaintatzi-masouti"
__version__ = "2021.10.15"

ghenv.Component.Name = "Lark Generate Sub-Hourly wea File v3"
ghenv.Component.NickName = 'wea Short-Term'
ghenv.Component.Message = '3.0.0'
ghenv.Component.Category = "Lark"
ghenv.Component.SubCategory = "Timeseries"

from subprocess import Popen
import os
import time



# check all inputs
error_list = []
inputs = [epw, folder, timestep]
inputs_name = ["epw", "folder", "timestep"]

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



#create wea file with timesteps smaller than hour
if check != "error":
    
    if RunIt == True:
        
        #convert epw to wea using the epw2wea Radiance command
        epw_folder = (os.path.split(epw))[0]
        epw_name = (os.path.split(epw))[1]
        wea = epw_name.replace(".epw", ".wea")
        wea = folder + "\\" + wea
        f = open(folder + "\\"  + "convert2wea.bat","w")
        f.write("epw2wea " + "\"" + epw + "\"" + " \"" + wea + "\"")
        f.close()
        runbatch = Popen(folder + "\\" + "convert2wea.bat")
        
        #get info from wea
        time.sleep(0.5) # small delay, because the wea takes some ms to be created and the next line is searching for it
        wea_data = open(wea,"r")
        lines = wea_data.readlines()
        place = lines[0]
        lat = lines[1]
        long = lines[2]
        timezone = lines[3]
        elevation = lines[4]
        units = lines[5]
        wea_data.close()
        
        #write header file
        # Daysim ds_shortterm program needs a header in a specific format. Thanks to Jan Wienold for the example header he shared with us.
        header_file = folder + "\\" + "daysim_header.hea"
        project_dir = folder + "\\"
        bin_dir = "C:\DAYSIM\bin" # the daysim dir path
        wea_name = (os.path.split(wea))[1]
        shortWea = wea_name.replace(".wea","_" + str(timestep) + "_short.wea")
        h = open(header_file, "w")
        # the header:
        string = """#====================
        # DAYSIM 2.1.P2header file
        # 
        #====================
        
        # 
        # 
        # 
        # 
        
        
        project_directory	{}
        bin_directory		{}
        
        
        
        ##################
        # site information
        ##################
        {}
        {}
        {}
        {}
        {}
        {}
        # input data name
        wea_data_file {}
        
        first_weekday 1
        # every n minutes
        time_step {} 
        # output data name
        wea_data_short_file {}
        # 1 keeps the solar radiation, 2 converts it to photopic 
        wea_data_short_file_units 1
        
        """.format(project_dir,bin_dir,place,lat,long,timezone,elevation,units,wea_name,timestep,shortWea)
        h.write(string)
        h.close()
        
        #run ds_shortterm to create file with timesteps smaller than hour
        f = open(folder + "\\" + "run_ds_shortterm.bat","w")
        f.write("cd " + folder + "\n")
        f.write("ECHO Wait until this window closes \n")
        f.write("ds_shortterm daysim_header.hea")
        f.close()
        
        #create file
        runbatch = Popen(folder + "\\" + "run_ds_shortterm.bat")
        shortWea = folder + "\\" + shortWea
