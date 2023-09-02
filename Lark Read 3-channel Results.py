# Read 3-channel values.

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
Read the 3 channel values from a Honeybee result file
-
Provided by Lark 3.0.0

    Inputs:
        resFile: Path to a res file containing the 3 channel values
    Output:
        tree: The 3 channel values
"""

__author__ = "cpierson"
__version__ = "2022.05.06"

ghenv.Component.Name = "Lark Read 3-channel Results v3"
ghenv.Component.NickName = "Read RGB"
ghenv.Component.Message = '3.0.0'
ghenv.Component.Category = "Lark"
ghenv.Component.SubCategory = "Point-in-time"

from Grasshopper import DataTree
from Grasshopper.Kernel.Data import GH_Path
import rhinoscriptsyntax as rs



#check all inputs
error_list = []
inputs = [resFile]
inputs_name = ["resFile"]

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



#read values and add to tree
if check != "error":
    
    x = resFile
    
    f = open(x,"r")
    l = f.readlines()
    
    tree = DataTree[str]()
    pathCount = 0 
    new_path = GH_Path(pathCount)
    
    for i in range(len(l)):
        a = l[i].split("\t")
        for j in range(len(a)):
            new_path = GH_Path(pathCount,j)
            tree.Add(a[j],new_path)
        pathCount += 1
    
    tree.TrimExcess()
    
    f.close()
