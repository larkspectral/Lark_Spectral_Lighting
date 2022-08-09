"LICENSE"


Modified 3-Clause BSD License (https://opensource.org/licenses/BSD-3-Clause)

Copyright 2015-2022 Mehlika Inanici, Ph.D. (University of Washington) and ZGF Architects LLP ; and
Copyright 2022 Clotilde Pierson, Ph.D. (EPFL, Oregon State University) and Myrta Gkaintatzi-Masouti, M.Sc. (Eindhoven University of Technology) < Lark Spectral Lighting v2.0** > 


**Further information on copyright and contributions for specific Lark versions detailed below.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

	(a). The name "Lark Spectral Lighting" and/or “Lark” and its logo must not be used to endorse or promote products derived from this software without prior written permission.
 
	(b). Products derived from this software may not be called "Lark Spectral Lighting" and/or "Lark", nor may "Lark Spectral Lighting" and/or "Lark" appear in their name, without prior written permission. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

=========================================================

Lark Spectral Lighting v2.0
  
This version is based upon Lark Spectral Lighting v1.0. Modifications and new features in Lark Spectral Lighting v2.0 were developed by Clotilde Pierson, Ph.D. (EPFL, Oregon State University) and Myrta Gkaintatzi-Masouti, M.Sc. (Eindhoven University of Technology) with contributions from ZGF Architects LLP for the electric lighting simulation workflow and contributions from Priji Balakrishnan, Ph.D. and Alstan J. Jakubiec, Ph.D. for the implementation of the Perez sky model.

Specific modifications to existing components include:
- in the "Lark Convert SPD - Write Spectral Radiance Materials" component, addition of a fourth material type ([3 = electriclight]) and definition of the main path accordingly.
- in the "Lark Build Spectral Radiance Sky Definitions" component, modification of the sky definition command line using gendaylit to include dew point temperature (version of 2021 in Radiance 5.4); removal of gen_reindl program; modification of inputs (removal of sky_type as information not needed for Perez sky model; modification of horizontal_direct to normal_direct; removal of global_illuminance/global_irradiation and run_reindl since gen_reindl program not used anymore; addition of dew point temperature for gendaylit); modification of RGB components of ground_glow (set to a grey color (1,1,1) instead of a red color (1,0.8,0.5)); modification of outputs (removal of reindl_output, diffuse_horizontal, and direct_normal since gen_reindl program not used anymore); modification of RGB coefficients (R coefficient updated to 0.2685 (instead of 0.2686) for sum of 3 coefficients to equal 1).
- in the "Lark 3-channel Circadian Luminance" component, modification of photopic coefficients in image-based and point-based simulation post-process and modification of circadian coefficients in point-based simulation post-process (for their sum to be equal to 1 and to match the CIE-published action spectra).
- in the "Lark 9-channel Circadian Luminance" component, addition of inputs to indicate whether an image-based or a grid-based (or both) simulation is ran (inputs and outputs will vary accordingly); modification of outputted HDR image name based on HDR image treatment (application of ipRGC FOV weighting or not); modification of pcomb function command line to include -h option (to reduce header size for readability) and -o option (to account for exposure value in post treatments); modification of Lucas circadian coefficients in image-based simulation post-process to match the CIE-published melanopic action spectrum and pre-defined wavelength bins.

New components include:
- the "Lark CIE Toolbox Alpha-opic Quantities" component, to calculate the quantities of the CIE S 026 toolbox.
- the "Lark Write To csv Or txt File" component, to export the data to a csv or txt file.
- the "Lark Colored Electric Luminaire File" component, to add the RGB color to an existing rad file for a luminaire and perform an electric lighting simulation with Lark.
- the "Lark ipRGC Retinal Weights In Field Of View" component, to apply ipRGC retinal coefficients to different parts of the field of view.
- the "Lark Calculation of RGB Irradiance From HDR Image" component, to calculate RGB irradiance values from an HDR luminance image.
- the "Lark Read 3-channel Results" component, to read the 3 channel values from a Honeybee result file.
- the "Lark Analysis Period Definition" component, to create an analysis period.
- the "Lark Analysis Period Decomposition" component, to extract the months, days and hours from an analysis period.
- the "Lark Generate Sub-Hourly wea File" component, to create a wea weather file with subhourly data in order to apply the non-visual direct response (nvRD) model with a timestep of 6 minutes.
- the "Lark Analyze wea File" component, to generate a new wea file with selected lines for a Radiance simulation.
- the "Lark Colored Sky For Annual Irradiance" component, to perform an annual Radiance simulation with a colored sky.
- the "Lark Read Colored Annual Results" component, to read the .ill file that results from an annual Lark simulation into a datatree.
- the "Lark Concatenate 9-channel Data" component, to concatenate the channel data from the 3 simulations.
- the "Lark Read 9-channel For CIE Toolbox" component, to organize the 9 channel data to be used with the "CIE toolbox" component.
- the "Lark Import Data From wea File" component, to import data from a wea file.
- the "Lark Non-Visual Direct Response Model" component, to compute the relative and cumulative alerting response using the non-visual direct response (nvRD) model.

This version uses the Lark Spectral Lighting name and logo with permission from Mehlika Inanici, Ph.D. (University of Washington) and ZGF Architects LLP.

=========================================================

Lark Spectral Lighting v1.0

Lark Spectral Lighting v1.0 is a joint collaboration of the University of Washington and ZGF Architects LLP. The software project is based off a paper titled Spectral Daylighting Simulations: Computing Circadian Light. 

=========================================================

The name "Lark Spectral Lighting" and its logo are the property of Mehlika Inanici, Ph.D. (University of Washington) and ZGF Architects LLP, and cannot be used without permission.  

=========================================================

This product uses the Rhinoceros RhinoCommon and Grasshopper libraries (http://www.en.na.mcneel.com).

Copyright (c) 2022 Robert McNeel & Associates. All Rights Reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software.

THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT EXPRESS OR IMPLIED WARRANTY. ALL IMPLIED WARRANTIES OF FITNESS FOR ANY PARTICULAR PURPOSE AND OF MERCHANTABILITY ARE HEREBY DISCLAIMED.

Rhinoceros is a registered trademark of Robert McNeel & Associates.

=========================================================

This product includes Radiance software (http://radsite.lbl.gov/) developed by the Lawrence Berkeley National Laboratory (http://www.lbl.gov/).

The Radiance Software License, Version 1.0

Copyright (c) 1990 - 2002 The Regents of the University of California, through Lawrence Berkeley National Laboratory. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. The end-user documentation included with the redistribution, if any, must include the following acknowledgment:
   "This product includes Radiance software (http://radsite.lbl.gov/) developed by the Lawrence Berkeley National Laboratory (http://www.lbl.gov/)."
   Alternately, this acknowledgment may appear in the software itself, if and wherever such third-party acknowledgments normally appear.

4. The names "Radiance," "Lawrence Berkeley National Laboratory" and "The Regents of the University of California" must not be used to endorse or promote products derived from this software without prior written permission. For written permission, please contact radiance@radsite.lbl.gov.

5. Products derived from this software may not be called "Radiance", nor may "Radiance" appear in their name, without prior written permission of Lawrence Berkeley National Laboratory.

THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL Lawrence Berkeley National Laboratory OR ITS CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
  
=========================================================

This product includes the executable files gen_reindl and ds_shortterm derived from: DAYSIM (http://daysim.ning.com/page/credits).

DAYSIM LICENSE INFORMATION  

SOFTWARE END‐USER LICENSE AGREEMENT 

Copyright (c) 2012 National Research Council Canada, Ottawa, Canada 

Copyright (c) 2012 Fraunhofer Institute for Solar Energy Systems, Freiburg, Germany 

Copyright (c) 2013 The Pennsylvania State University, University Park, PA, USA 

IMPORTANT READ CAREFULLY:  

This end user license agreement is a legal agreement between you, in your capacity as an individual and/or as an agent for your company, institution or other entity (called herein the "User") and the NATIONAL RESEARCH COUNCIL OF CANADA, the FRAUNHOFER INSTITUTE FOR SOLAR ENERGY SYSTEMS, and THE PENNSYLVANIA STATE UNIVERSITY (collectively called herein "NRC/ISE/PSU")  

The User desires to use the computer software, in source code form, developed by NRC/ISE/PSU and identified as DAYSIM (called herein the "Software", a term which includes both original and modified versions of computer programs and computer data, and also includes printed matter intended to explain or assist the use of parts of the Software). Downloading, installing, using or copying the software by the User or a third party indicates that the User agrees to be bound by the terms and conditions that follow: 

1. TITLE AND GRANT 
NRC/ISE/PSU grant to the User, and the User accepts, a non‐transferable, non‐exclusive license to install and use the version of the computer software program noted above, without any license fee, only in the manner described under the heading "USAGE". All proprietary interest, right, title, and copyright in the Software which are not explicitly granted to you herein remain with NRC/ISE/PSU. 

2. USAGE 

2.1 The User may install and use the Software. 

2.2 The User may copy the Software for backup or archival purposes provided that the user reproduces all copyright notices and other proprietary notices on any copies of the Software. 

2.3 The User may create computer programs which incorporate or modify the Software. These programs may be made available to other persons under the following conditions: 

(a) the new software shall include a statement giving appropriate credit to NRC/ISE/PSU for the development of DAYSIM 

(b) NRC/ISE/PSU will all receive one free copy of the new software that will allow NRC/ISE/PSU to verify that requirement (a) has been fully satisfied. Failure to provide NRC/ISE/PSU with a new software later than 10 working days before its original release will terminate this User License Agreement. 

2.4 Materials generated through the use of the Software and/or data collected from using the Software (e.g. publications, web pages, presentation) shall include a statement giving appropriate credit to NRC/ISE/PSU.  

3. NO MAINTENANCE SUPPORT 

NRC/ISE/PSU shall be under no obligation whatsoever to provide maintenance or support for the Software; or to notify the User of bug fixes, patches, or upgrades to the Software (if any). If, in its sole discretion, NRC/ISE/PSU makes a Software bug fix, patch or upgrade available to the User and NRC/ISE/PSU does not separately enter into a written license agreement with the User relating to such bug fix, patch or upgrade, then it shall be deemed incorporated into the Software and subject to this Agreement.  

4. SOURCE CODE 

Source code for the DAYSIMps user interface is available upon request from Richard Mistrick,  Penn State University, Dept. of Architectural Engineering, 104 Engineering A, University Park, PA 16802.   

WARRANTY DISCLAIMER 

THE SOFTWARE IS SUPPLIED "AS IS". NRC/ISE/PSU DISCLAIM ANY WARRANTIES, EXPRESSED, IMPLIED, OR STATUTORY, OF ANY KIND OR NATURE WITH RESPECT TO THE SOFTWARE, INCLUDING WITHOUT LIMITATION ANY WARRANTY OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE. NRC/ISE/PSU SHALL NOT BE LIABLE IN ANY EVENT FOR ANY DAMAGES, WHETHER DIRECT OR INDIRECT, SPECIAL OR GENERAL, CONSEQUENTIAL OR INCIDENTAL, ARISING FROM THE USE OF THE SOFTWARE. 

NRC/ISE/PSU DO: 

(1) NOT ASSUME ANY LEGAL LIABILITY OR RESPONSIBILITY FOR THE ACCURACY, COMPLETENESS, OR USEFULNESS OF THE SOFTWARE,  

(2) NOT WARRANT THAT THE SOFTWARE WILL FUNCTION UNINTERRUPTED, THAT IT IS ERROR‐FREE OR THAT ANY ERRORS WILL BE CORRECTED.  

If you have any questions concerning this license, contact Dr. Guy Newsham, National Research Council, Montreal Road, Ottawa, Ontario, K1A 0R6, Canada. 

BY DOWNLOADING, INSTALLING, OR USING THE SOFTWARE YOU ARE INDICATING YOUR ACCEPTANCE OF THE TERMS AND CONDITIONS HEREIN. 
  
=========================================================

ACKNOWLEDGEMENTS:

Dr. Mehlika Inanici, Marty Brennan and Ed Clark

Special thanks to Todd Stine, Deborah Gumm, Leslie Morison, Jordan Grant at ZGF

Thanks from Clotilde Pierson and Myrta Gkaintatzi-Masouti to Maria Amundadottir and Parisa Khademagha for providing the code of their dissertations and to Jan Wienold and Stephen Wasilewski for their help with Radiance.
  
=========================================================

REFERENCES:

Lark v0.0.1
Inanici M., Brennan M., and Clark E. “Spectral Daylighting Simulations: Computing Circadian Light”. International Building Performance Simulation Association (IBPSA) Conference, Hyderabad, India, 2015.

Lark v2.0
Gkaintatzi-Masouti M., Pierson C., Van Duijnhoven J., Andersen M., Aarts M. "A simulation tool for indoor lighting design considering ipRGC-induced responses". BuildSim Nordic Conference, Copenhagen, Denmark, Aug. 22-23, 2022


Others
Khademagha, P. “Light directionality in design of healthy offices”. Ph. D. thesis, Eindhoven University of Technology. Eindhoven, Netherlands. 2021.

Balakrishnan, P., Jakubiec, A. “Spectral Rendering with Daylight: A Comparison of Two Spectral Daylight Simulation Platforms.” In Proceedings of Building Simulation 2019: 16th Conference of IBPSA, Volume 16, Rome, Italy, pp. 1191–1198. 2019.

International Commission on Illumination. 2018. System for Metrology of Optical Radiation for ipRGC-Influenced Responses to Light (CIE S 026/E:2018).

Amundadottir, M. L. “Light-driven model for identifying indicators of non-visual health potential in the built environment”. Ph. D. thesis, Ecole Polytechnique Federale de Lausanne. Lausanne, Switzerland. 2016.

Lucas R., Peirson S., Berson D., Brown T., Cooper H., Czeisler C., Figueri M., Gamlin, P., Lockley, S., O’hagan J., Price, L., Provencio I., Skene D., Brainard G. “Measuring and Using Light in the Melanopsin Age”, Trends in Neurosciences, 37(1), 1-9. 2014 .

Munsell Color Science Laboratory. 2002. Excel Daylight Series Calculator. http://www.ritmcsl.org/UsefulData/DaylightSeries.xls [20 March, 2015]. https://www.rit.edu/cos/colorscience/rc_useful_data.php

Reindl, D.T., Beckman W.A., 1990. Diffuse Fractions Correlations”, Solar Energy. 45(1), 1-7.

