# run .rad files in a folder

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
Use this component to run radiance files in a folder for image based and/or point based simulation.  
-
Provided by Lark 3.0.0
        
    Args:
        ImgBased_filepath: filepath for image based simulation to run. Filepath should include all radiance files.
        PtBased_filepath: filepath for point based simulation to run. Filepath should include all radiance files.
        ImgBased_Run: Boolean (True or False) to start running simulation.
        PtBased_Run: Boolean (True or False) to start running simulation.
    Returns:
        Results: filepath to irradiance (.dat, .res) or image(.hdr) results.
"""

__author__ = "bojung"
__version__ = "2023"

ghenv.Component.Name = "Lark Run Rad Files v3"
ghenv.Component.NickName = 'run rad files'
ghenv.Component.Message = '3.0.0'
ghenv.Component.Category = "Lark"
ghenv.Component.SubCategory = "Point-in-time"

import re
import os
from subprocess import check_output, Popen
import subprocess

#define a regex function to write a new electric light source file
def run_radfiles(filepath):
    all_files = os.listdir(filepath)
    print(type(filepath))
    batch_files = [file for file in all_files if file.endswith('.bat')]
    
    if ImgBased_Run == True:
        init_file = [file for file in batch_files if 'Init' in file]
        # assert len(init_file) == 1 # Error checking, just to double check we only have one ''
        init_file = init_file[0]
        # print (filepath + '\\' + init_file)
        # subprocess.call([filepath + '\\' + init_file])
        img_file = [file for file in batch_files if 'IMG' in file]
        img_file = img_file[0]
        
        pcomp_file = [file for file in batch_files if 'PCOMP' in file]
        pcomp_file = pcomp_file[0]

        runinit = Popen(init_file, cwd=filepath, shell=True)
        stdout, stderr = runinit.communicate()
        
        runimg = Popen(img_file, cwd=filepath, shell=True)
        stdout, stderr = runimg.communicate()
        
        runpcomp = Popen(pcomp_file, cwd=filepath, shell=True)
        stdout, stderr = runpcomp.communicate()
        
        new_files = os.listdir(filepath)
        hdr_file = [file for file in new_files if '.HDR' in file]
        hdr_file = [file for file in hdr_file if '_temp' not in file]
        hdr_file = hdr_file[0]
        print(hdr_file)
        
        return(filepath + '\\' + hdr_file)
        
    if PtBased_Run == True:
        print(batch_files)
        init_file = [file for file in batch_files if 'Init' in file]
        print(init_file)
        init_file = init_file[0]
        print(init_file)
        
        rad_file = [file for file in batch_files if 'RAD' in file]
        print(rad_file)
        rad_file = rad_file[0]
        print(rad_file)

        runinit = Popen(init_file, cwd=filepath, shell=True)
        stdout, stderr = runinit.communicate()
        
        runrad = Popen(rad_file, cwd=filepath, shell=True)
        stdout, stderr = runrad.communicate()
        
        new_files = os.listdir(filepath)
        res_file = [file for file in new_files if '.res' in file]
        res_file = res_file[0]
        
        return(filepath + '\\' + res_file)
        
if ImgBased_Run == True:
    ImgBased_Results = run_radfiles(ImgBased_filepath)
    
if PtBased_Run == True:
    PtBased_Results = run_radfiles(PtBased_filepath)
