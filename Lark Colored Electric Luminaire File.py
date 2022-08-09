# Add the RGB color to the luminaire rad file

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
Use this component to perform an electric lighting simulation with Lark.
It modifies an existing rad file for a luminaire by adding the RGB color to it.
-
Provided by Lark 2.0.0

    Args:
        path: folder path of the existing luminaire rad file
        filename: filename of the existing luminaire rad file
        RGB_triplet: a list of 9 values that describe the spectral power distribution of the luminaire
        count: 0: blue part of the spectrum (first 3 of the 9 spectral values), 1: green part of the spectrum (second 3 of the 9 spectral values), 2: red part of the spectrum (last 3 of the 9 spectral values)
    Returns:
        file: modified filename (this is the same as the input file, the component modifies the existing and does not create a new)
"""

__author__ = "mbrennan+eclark"
__version__ = "2016"

ghenv.Component.Name = "Lark Colored Electric Luminaire File"
ghenv.Component.NickName = 'Colored Electric'
ghenv.Component.Message = '2.0.0'
ghenv.Component.Category = "Lark"
ghenv.Component.SubCategory = "Point-in-time"

import re
import os



#check all inputs
error_list = []
inputs = [path, filename, RGB_triplet, count]
inputs_name = ["path", "filename", "RGB_triplet", "count"]

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

if filename == None:        
    filename = ""



#replace RGB triplet in electric light source file
if check != "error":
    
    #provide a directory with .rad file in folder
    _path = path
    if os.path.isdir(_path) != True: 
        os.makedirs(_path)
    else:
        pass
    os.chdir(_path)
    
    #print out current directory
    current_dir = _path
    
    #detect the triplet by choosing first and last value of one slice
    slice = [0,3],[3,6],[6,9]
    start = slice[count][0]
    end = slice[count][1]
    triplet = RGB_triplet[start:end]
    
    #substitue the RGB values
    substitute = 3,triplet[0],triplet[1],triplet[2]
    substitute = ' '.join(map(str, substitute))
    
    #define a regex function to write a new electric light source file
    def replace( filepath, subs, flags=0 ):
        with open( filepath, "r+" ) as file:
            fileContents = file.read()
            textPattern = re.compile(ur'3 1 1 1') #regex for Radiance default light
            fileContents = textPattern.sub( subs, fileContents ) #replace regex with subs 
            file.seek( 0 )
            file.truncate()
            file.write( fileContents )
    
    #write a new electric light source file
    file = filename + '.rad'
    replace (file, substitute)
    radfile = current_dir + file
    
    #print out the electric light source file
    print radfile
