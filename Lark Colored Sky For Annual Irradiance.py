# Simulate analysis period with 2-phase method with accurate sun position. The workflow is based on the tutorial of S. Subramaniam "Daylighting Simulations with Radiance using Matrix-based Methods" (2-phase method DDS), but modifications to it were made (sun and sky components are calculated individually without using a room with black materials).

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
Use this component to perform an annual Radiance simulation with a colored sky.
The color of the sun is assumed to be neutral.
-
Provided by Lark 3.0.0

    Inputs:
        materials: The path to a Radiance materials file.
        geometry: The path to a Radiance geometry file.
        points: The path to a Radiance points file.  
        wea: The path to a wea weather file.
        skyColor: A list with 3 RGB color coordinates representing the color of the sky.
        radParameters: Radiance simulation parameters.
        folder: The folder path containing the materials, geometry and point files.
        radFileName: The name for the simulation files.
        RunIt: A boolean toggle to trigger the simulation.
    Output:
        resultSun: The 3 irradiance values from the Radiance simulation due to sun.
        resultSky: The 3 irradiance values from the Radiance simulation due to sky.
"""

__author__ = "mgkaintatzi-masouti"
__version__ = "2022.02.10"

ghenv.Component.Name = "Lark Colored Sky For Annual Irradiance v3"
ghenv.Component.NickName = 'Color Annual Irrad'
ghenv.Component.Message = '3.0.0'
ghenv.Component.Category = "Lark"
ghenv.Component.SubCategory = "Timeseries"

from subprocess import Popen, STDOUT, PIPE
import time



Done = False



#check all inputs
error_list = []
inputs = [materials,geometry, points, wea, skyColor, radParameters, folder, radFileName]
inputs_name = ["materials","geometry", "points", "wea", "skyColor", "radParameters", "folder", "radFileName"]

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



#write Radiance files and commands in a batch file and run it.
if check != "error":
    if RunIt:
        
        #write neutral color skyglow.rad file
        f = open(folder + "\\"  + "skyglow.rad","w")
        string = """#@rfluxmtx u=+Y h=u
        void glow groundglow
        0
        0
        4 1 1 1 0
        
        groundglow source ground
        0
        0
        4 0 0 -1 180
        
        #@rfluxmtx u=+Y h=r1
        void glow skyglow
        0
        0
        4 1 1 1 0
        
        skyglow source skydome
        0
        0
        4 0 0 1 180"""
        
        f.write(string)
        f.close()
        sky = folder + "\\"  + "skyglow.rad"
        
        # open a batch file and start writing the commands
        f = open(folder + "\\"  + "AnnualColor.bat","w")
        
        
        
        #step 1: Perform an annual daylight coefficient simulation
        f.write(":: STEP 1: Perform an annual daylight coefficient simulation. \n\n")
        
        #write octree from geometry and materials
        materials = '"' + materials + '"'
        geometry = '"' + geometry + '"'
        oct = '"' + folder + radFileName + "_oct.oct" + '"'
        SetCD = "cd " + folder + "\n\n" # set current directory
        f.write(SetCD)
        f.write(":: Write octree from geometry and materials. \n\n")
        CreateOct = "oconv {} {} > {} \n".format(materials,geometry,oct)
        f.write(CreateOct)
        
        #copy reinhartb.cal from the Radiance folder to the project folder (if it is not there rfluxmtx gives an error)
        CopyRein = "copy " + "C:\Radiance\lib\\reinhartb.cal "  + folder + "\n\n"
        f.write(CopyRein)
        
        #run rfluxmtx to prepare the Daylight Coefficient matrix
        f.write(":: Run rfluxmtx to prepare the Daylight Coefficient matrix. \n\n")
        illummtxSky = '"' + folder + radFileName + '_illum_sky.mtx' '"'
        sky = '"' + sky + '"'
        countPts = len(open(points).readlines( ))
        points = '"' + points + '"'
        RunRfluxmtxSky = "rfluxmtx -I+ -y {} {} - {} -i {} < {} > {} \n\n".format(countPts,radParameters,sky,oct,points,illummtxSky)
        f.write(RunRfluxmtxSky)
        
        #run gendaymtx to create the annual sky matrix
        # Here input the color information
        # The color information for the sky is given with the -c option
        # The -s option is to do a sky only simulation (no sun)
        # The -m 1 is to define a sky with 145 patches
        f.write(":: Run gendaymtx to create the annual sky matrix. \n\n")
        wea = '"' + wea + '"'
        skymtxSky = '"' + folder + radFileName + '_Sky.mtx' '"'
        RunGendaymtxSky = "gendaymtx -m 1 -s -c {} {} {} {} > {} \n\n".format(skyColor[0],skyColor[1],skyColor[2],wea,skymtxSky)
        f.write(RunGendaymtxSky)
        
        #run dctimestep to multiply the sky with the coefficient matrix and do the annual simulation
        f.write(":: Run dctimestep to multiply the sky with the coefficient matrix and do the annual simulation. \n\n")
        resultSky = '"' + folder + radFileName + '_annual_sky.ill' '"'
        RunDCSky = "dctimestep {} {} > {} \n\n".format(illummtxSky,skymtxSky,resultSky)
        f.write(RunDCSky + "\n")
        
        
        
        #step 2: Perform an annual direct-only daylight coefficients simulation with accurate sun position
        # This also includes reflections due to sun.
        f.write(":: STEP 2: Perform an annual direct-only daylight coefficients simulation with accurate sun position.\n\n")
        CopyReinsrc = "copy " + "C:\Radiance\lib\\reinsrc.cal "  + folder + "\n\n"
        f.write(CopyReinsrc)
        
        #create sun primitive definition and write it in a file called suns.rad 
        f.write(":: Create sun primitive definition and write it in a file called suns.rad. \n\n") 
        SunPrimit = "echo void light solar 0 0 3 1e6 1e6 1e6 > suns.rad \n"
        f.write(SunPrimit)
        
        #create solar discs and corresponding modifiers
        f.write(":: Create solar discs and corresponding modifiers. \n\n")
        SolarDisks = "cnt 5165 | rcalc -e MF:6 -f reinsrc.cal -e Rbin=recno -o \"solar source sun 0 0 4 ${Dx} ${Dy} ${Dz} 0.533\" >> suns.rad \n\n"
        f.write(SolarDisks)
        
        #create an octree with the previous materials and geometry and also a sun disk
        f.write(":: Create an octree with the previous materials and geometry and also a sun disk. \n\n")
        suns = '"' + folder + "suns.rad" + '"'
        octSun = '"' + folder + radFileName + "_oct_sun.oct" + '"'
        CreateOctSun = "oconv -f {} {} {}  > {} \n\n".format(materials,geometry,suns,octSun)
        f.write(CreateOctSun)
        
        #calculate illuminance sun coefficients for illuminance calculations
        f.write(":: Calculate illuminance sun coefficients for illuminance calculations. \n\n")
        illummtxSun = '"' + folder + radFileName + '_illum_sun.mtx' '"'
        CopyReinhart = "copy " + "C:\Radiance\lib\\reinhart.cal "  + folder + "\n\n"
        f.write(CopyReinhart)
        
        RunRcontribSun = "rcontrib -I+ -y {} {} -faf -e MF:6 -f reinhart.cal -b rbin -bn Nrbins -m solar {} < {} > {} \n\n".format(countPts,radParameters,octSun,points,illummtxSun)
        f.write(RunRcontribSun)
        
        #run gendaymtx to create sun matrix
        # The -5 refers to the 5-phase method (although we are not using the 5-phase method the sun definition is the same)
        # The 0.533 is the size of the solar disk in steradians
        # The -d option is to to sun calculation only without sky
        # The -m 6 defines the number of sun positions
        # The color of the sun is neutral (the -c option cannot be used here)
        f.write(":: Run gendaymtx to create sun matrix. \n\n") 
        skymtxSun = '"' + folder + radFileName + '_Sun.mtx' '"'
        RunGendaymtxSun = "gendaymtx -5 0.533 -d -m 6 {} > {} \n\n".format(wea,skymtxSun)
        f.write(RunGendaymtxSun)
        
        #run dctimestep to multiply the sun matrix with the coefficient matrix and do the annual simulation
        f.write(":: Run dctimestep to multiply the sun matrix with the coefficient matrix and do the annual simulation. \n") 
        resultSun = '"' + folder + radFileName + '_annual_sun.ill' '"'
        RunDCSun = "dctimestep {} {} > {} \n\n".format(illummtxSun,skymtxSun,resultSun)
        
        f.write(RunDCSun)
        f.close()
        
        #run the batch file with all the commands
        batch = folder + "\\"  + "AnnualColor.bat"
        runbatch = Popen(batch)
        runbatch.wait() # wait for the batch file to run before moving on
        
        
        
        #write results
        resultSun = folder + radFileName + '_annual_sun.ill'
        resultSky = folder + radFileName + '_annual_sky.ill'
        
        
        
        Done = True
