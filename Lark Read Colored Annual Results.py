# Read content of .ill file.

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
Read the .ill file that results from an annual Lark simulation into a datatree
-
Provided by Lark 3.0.0

    Inputs:
        file: Path to ill file that results from an annual Lark simulation
    Output:
        tree: Results in datatree structure
"""

__author__ = "mgkaintatzimasouti" 
__version__ = "2021.11.15"

ghenv.Component.Name = "Lark Read Colored Annual Results v3"
ghenv.Component.NickName = "Read Annual"
ghenv.Component.Message = '3.0.0'
ghenv.Component.Category = "Lark"
ghenv.Component.SubCategory = "Timeseries"

from Grasshopper import DataTree
from Grasshopper.Kernel.Data import GH_Path



#read data and add to tree
if file:
    
    #read the .ill file
    f = open(file, "r")
    lines = f.readlines()
    f.close()
    
    #take the useful data from the file
    NROWS = lines[4]
    pts = int(NROWS.split("=")[1][0])
    NCOLS = lines[5]
    timesteps = int(NCOLS.split("=")[1][0])
    NCOMP = lines[6]
    channels = int(NCOMP.split("=")[1][0]) # this is always 3
    data = lines[9:len(lines)]
    
    #put the values in a data tree structure to use them in GH
    tree = DataTree[str]()
    pathCount = 0 
    for d in range(len(data)):
        timestep_data = data[d].split("\t")
        new_path = GH_Path(pathCount)
        for i in timestep_data:
            tree.Add(i, new_path)
        pathCount += 1
