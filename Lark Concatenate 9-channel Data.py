# Concatenate data from the blue, green and red simulations.

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
Concatenate the channel data from the 3 simulations.
-
Provided by Lark 2.0.0

    Inputs:
        blue: Data from blue simulation (output of "ReadAnnual" component)
        green: Data from green simulation (output of "ReadAnnual" component)
        red: Data from red simulation (output of "ReadAnnual" component)
    Output:
        BRG: 9 channel data in a datatree format
"""

__author__ = "mgkaintatzimasouti" 
__version__ = "2021.11.15"

ghenv.Component.Name = "Lark Concatenate 9-channel Data"
ghenv.Component.NickName = "9-ch Concat"
ghenv.Component.Message = '2.0.0'
ghenv.Component.Category = "Lark"
ghenv.Component.SubCategory = "Timeseries"



#concatenate BRG
BRG =[]
for i in range(len(blue)):
    BRG.append( blue[i].replace("\n", "") + " " + green[i].replace("\n", "") + " " +  red[i].replace("\n", ""))
