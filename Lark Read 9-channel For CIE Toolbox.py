# Prepare 9 channel data for the CIE toolbox component.

# Lark Spectral Lighting (v0.0.1, v0.0.2 and v1.0) is a collaboration of University of Washington and ZGF Architects LLP
# Authors Dr. Mehlika Inanici, Marty Brennan & Ed Clark
# Lark v2.0 is a collaboration of EPFL, Oregon State University, and Eindhoven University of Technology
# Authors Dr. Clotilde Pierson & Myrta Gkaintatzi-Masouti
# Copyright 2015-2022 Mehlika Inanici, Ph.D. (University of Washington) and ZGF Architects LLP
# Copyright 2022 Clotilde Pierson, Ph.D. (EPFL, Oregon State University) and Myrta Gkaintatzi-Masouti, M.Sc. (Eindhoven University of Technology)
# Licensed under The Modified 3-Clause BSD License (the "License");
# You may obtain a copy of the License at
# https://opensource.org/licenses/BSD-3-Clause

"""
Organize the 9 channel data to be used with the "CIE toolbox" component.
-
Provided by Lark 2.0.0

    Inputs:
        BRG: 9 channel data (output of "9channels" component) - should be flattened
    Output:
        tree: 9 channel data to be used with the "CIE toolbox" component
"""

__author__ = "mgkaintatzimasouti" 
__version__ = "2021.11.15"

ghenv.Component.Name = "Lark Read 9-channel For CIE Toolbox"
ghenv.Component.NickName = "9-ch For CIE"
ghenv.Component.Message = '2.0.0'
ghenv.Component.Category = "Lark"
ghenv.Component.SubCategory = "Timeseries"

from Grasshopper import DataTree
from Grasshopper.Kernel.Data import GH_Path



#organize the channel data so that they can run with the CIE toolbox component
tree = DataTree[float]()
pathCount = 0 
for i in range(len(BRG)):
    list = BRG[i].split(" ")
    new_path = GH_Path(pathCount)
    for j in list:
        tree.Add(float(j), new_path)
    pathCount += 1
