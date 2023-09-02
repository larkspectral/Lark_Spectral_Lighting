# re-write the sky file to have colored sun and sky
   
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
Use this component to re-write radiance sky file to include spectral information.
-
Provided by Lark 3.0.0
                
    Args:
        filepath: filepath to substitute
        subsitutue_txt: txt to substitute with
"""
        
__author__ = "bojung"
__version__ = "2023"
        
ghenv.Component.Name = "Lark Re-Write Radiance Sky File v3"
ghenv.Component.NickName = 're-write sky'
ghenv.Component.Message = '3.0.0'
ghenv.Component.Category = "Lark"
ghenv.Component.SubCategory = "Point-in-time"
        
        
import re
import os
from subprocess import check_output
import Grasshopper.Kernel as gh
e = gh.GH_RuntimeMessageLevel.Error
w = gh.GH_RuntimeMessageLevel.Warning
        

# Raise Error if input is missing
error_list = []
inputs = [filepath, substitute_txt]
inputs_name = ["filepath", "substitute_txt"]
inputs_dict = {name:value for (value, name) in zip(inputs, inputs_name)}

def is_input_valid(dic, name):
    if name not in dic:
        return False
    if dic[name] == None:
        return False
    if dic[name] == []:
        return False
    return True
    
for name, value in inputs_dict.items():
    if not is_input_valid(inputs_dict, name):
        error_occurred = True
        error_list.append(name)
    else:
        error_occurred = False

if len(error_list) > 0:
    ghenv.Component.AddRuntimeMessage(w, "Warning! Connect the following inputs: " + ", ".join(error_list))
    
    
# function to overwrite sky file
def replace(filepath, substitute):
    with open(filepath, 'w') as file:
        file.write(substitute)

if not error_occurred:
    replace (filepath, substitute_txt)
        
