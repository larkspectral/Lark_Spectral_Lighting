"LICENSE"

Lark Spectral Lighting Software License, Version 3.0

Modified 3-Clause BSD License (https://opensource.org/licenses/BSD-3-Clause)

Copyright 2015-2022 University of Washington (Mehlika Inanici, Ph.D.) and ZGF Architects LLP < Lark Spectral Lighting v1.0** >; and
Copyright 2022 EPFL, Oregon State University (Clotilde Pierson, Ph.D.) and Eindhoven University of Technology (Myrta Gkaintatzi-Masouti, M.Sc.) < Lark Spectral Lighting v2.0** > ; and
Copyright 2023 University of Washington (Bo Jung, M.Sc., Mehlika Inanici, Ph.D., Zining Cheng, M.Sc.) and ZGF Architects LLP < Lark Spectral Lighting v3.0** >


**Further information on copyright and contributions for specific Lark versions detailed below.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

	(a). The name "Lark Spectral Lighting" and/or “Lark” and its logo must not be used to endorse or promote products derived from this software without prior written permission.
 
	(b). Products derived from this software may not be called "Lark Spectral Lighting" and/or "Lark", nor may "Lark Spectral Lighting" and/or "Lark" appear in their name, without prior written permission. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

=========================================================
Lark Spectral Lighting v3.0
  
This version is based upon Lark Spectral Lighting v1.0 and 2.0. Modifications and new features in Lark Spectral Lighting v3.0 were developed by University of Washington (Bo Jung, M.Sc., Mehlika Inanici, Ph.D., Zining Cheng, M.Sc.) and ZGF Architects LLP. 
Specific modifications to existing components include:
- 9-channel division bins in all relevant components. The new bin divisions are in v.3.0 [380-419], [419-459], [459-499], [499-529],[529-558], [558-587], [587-608], [608-630], [630-780]. In v.0-2.0, the divisions were different (listed below in v.1.0). **Due to this change, the components from previous versions should not be used in v.3.0.**  
- in the "Lark Convert SPD - Write Spectral Radiance Materials" component, modification of spectral coefficients for 3 and 9 channel; removal of input  'source_interval' and 'excel_daylight_series_cal' input; modification to auto-read input spectral interval and ignore any text in the input; modification to auto fill missing spectral range within 380-780nm to match the previous number. i.e.) if the data started from 385nm (0.8W/m2)  and reached to 780nm, 0.8W/m2 will be copied in the beginning so that 380nm to 384nm is also 0.8W/m2.
- in the “Lark 3-channel Luminance” component, modification of output name (cir_Lucas_pic and cir_Lucas_lux changed to melanopic_pic and melanopic_lux respectively); modification of component error handling using dictionaries instead of lists and raising gh runtime messages.
- in the “Lark 9-channel Luminance” component, modification of spectral coefficients for 9 channel; modification of output name (cir_Lucas_pic and cir_Lucas_lux changed to melanopic_pic and melanopic_lux respectively); addition of neuropic output (neuropic_lux and neuropic_pic); modification of component error handling using dictionaries instead of lists and raising gh runtime messages. Neuropic curve is modeled after Kojima et al, 2011. Neuropsin is active between 303 and 460 nm, peaking at 380. The spectral range below 380 is omitted in Lark computations to exclude the harmful effects of UV light.
- in the “Lark Build Spectral Radiance Sky Definitions” component, modification of component name to “Lark Perez Sky - Colored with Sky and Sun Spectra”; addition of option to use either direct and diffuse irradiance (-W option in gendaylit) or global irradiance (-E option in gendaylit); addition of option to input spectral power distribution of direct (sun) irradiance; modification of input name channel_ouput to diffuse channel where spectral power distribution of diffuse (sky) irradiance is given; deletion of temperature input; modification of output to sky definition instead of sky file directory; deletion of output current_dir as output is not a sky file but sky definition; deletion of output sky_name_out as output is not a sky file but sky definition.
- in the "Lark CIE Toolbox Alpha-opic Quantities" component, modification of spectra intervals for 9 channels.
- in the “Lark ipRGC Retinal Weights In Field Of View” component, modification to include option for adding file save location (default is "C:/lark/temp"); removal of option to change file name. File name is now based on the picture name with "_weighted" added at the end. i.e. picture = blue.hdr, filename = blue_weighted.hdr.
- in the “Lark Calculation of RGB Irradiance From HDR Image” component, modification to include an option to add where the text file for RGB values are saved (default is 'C:\lark\\temp'). 



New components include:
-the “Lark Re-Write Radiance Sky File” component, to re-write standard colorless Perez sky files with a CCT-based or luminance based colored Perez sky definition.
- the “Lark Perez Sky - Colored with luminance” component, to define 3 channel radiance Perez sky, based on luminance. This component uses “-C” option from gendaylit radiance command.
- the "Run Rad Files” component, to run batchfiles created by Ladybug 0.0.69 and Honeybee 0.0.66 [Legacy Plugins] in a folder.

=========================================================
Lark Spectral Lighting v2.0
  
This version is based upon Lark Spectral Lighting v1.0. Modifications and new features in Lark Spectral Lighting v2.0 were developed by EPFL, Oregon State University (Clotilde Pierson, Ph.D.) and Eindhoven University of Technology (Myrta Gkaintatzi-Masouti, M.Sc.) with contributions from ZGF Architects LLP for the electric lighting simulation workflow and contributions from Priji Balakrishnan, Ph.D. and Alstan J. Jakubiec, Ph.D. for the implementation of the Perez sky model.

Specific modifications to existing components include:
- in the "Lark Convert SPD - Write Spectral Radiance Materials" component, addition of a fourth material type ([3 = electriclight]) and definition of the main path accordingly.
- in the "Lark Build Spectral Radiance Sky Definitions" component, modification of the sky definition command line using gendaylit to include dew point temperature (version of 2021 in Radiance 5.4); removal of gen_reindl program; modification of inputs (removal of sky_type as information not needed for Perez sky model; modification of horizontal_direct to normal_direct; removal of global_illuminance/global_irradiation and run_reindl since gen_reindl program not used anymore; addition of dew point temperature for gendaylit); modification of RGB components of ground_glow (set to a grey color (1,1,1) instead of a red color (1,0.8,0.5)); modification of outputs (removal of reindl_output, diffuse_horizontal, and direct_normal since gen_reindl program not used anymore); modification of RGB coefficients (R coefficient updated to 0.2685 (instead of 0.2686) for sum of 3 coefficients to equal 1).
- in the "Lark 3-channel Circadian Luminance" component, modification of photopic coefficients in image-based and point-based simulation post-process and modification of circadian coefficients in point-based simulation post-process (based onCIE-published action spectra).
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

Lark Spectral Lighting v1.0 is a joint collaboration of the University of Washington and ZGF Architects LLP. The software project is based of a paper titled Spectral Daylighting Simulations: Computing Circadian Light. The 3 channel divisions are [380-498], [498, 586], [586-780].  The bins in 9 channel divisions are [380-422], [422-460], [460-498], [498-524], [524-550], [550-586], [586-650], [650-714], [714-780]. 

=========================================================

The name "Lark Spectral Lighting" and its logo are the property of University of Washington (Mehlika Inanici, Ph.D.) and ZGF Architects LLP, and cannot be used without permission.  

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

We tested the current version of LARK (v3.0) with Ladybug 0.0.69 and Honeybee 0.0.66 [Legacy Plugins] and Ladybug Tools 1.5.0 installation.

=========================================================

ACKNOWLEDGEMENTS:

v.1.0. Dr. Mehlika Inanici, Marty Brennan and Ed Clark: Special thanks to Todd Stine, Deborah Gumm, Leslie Morison, Jordan Grant at ZGF

v.2.0. Thanks from Clotilde Pierson and Myrta Gkaintatzi-Masouti to Maria Amundadottir and Parisa Khademagha for providing the code of their dissertations and to Jan Wienold and Stephen Wasilewski for their help with Radiance.

Thanks from Marty Brennan to Ed Clark for spearheading the electric light simulation workflow.
 
v.3.0.  Mehlika Inanici, Marty Brennan, Bo Jung and Zining Cheng: We thank Dr. James Greenberg and Dr. Richard Lang from Cincinnati Children’s Hospital Medical Center for providing information on neuropsin, human development, and metabolism; Todd Stine and Victoria Nichols at ZGF Architects for support of applied research in circadian lighting, daylight measurement at Gould Hall, and the Lark Spectral Lighting project; Dean Renée Cheng and Teri Thomson Randall for Applied Research Consortium leadership and support of the daylight spectral measurement at Gould Hall; Sara Cao at the Lang Lab for sharing research and scripts for daylight measurement. 

Bo Jung and Zining Cheng  were supported by the Applied Research Consortium at the University of Washington College of Built Environments and ZGF Architects.

Special thanks from Marty Brennan:
Deborah Gumm, Julia Leitman,Kelly Chanopas and Lahmi Kim at ZGF. 
Zining Cheng for exploring and documenting neuropic lighting in your thesis.
Bo Jung for recording and analyzing spectral sky data on top of Gould Hall and leading the massive effort building Lark v3.0.
Dr. Mehlika Inanici for friendship, pioneering research, and two years partnership with ARC and ZGF.


=========================================================

REFERENCES:

Lark v0.0.1-1.0
Inanici M., Brennan M., and Clark E. “Spectral Daylighting Simulations: Computing Circadian Light”. International Building Performance Simulation Association (IBPSA) Conference, Hyderabad, India, 2015.

Lark v2.0
Gkaintatzi-Masouti M., Pierson C., Van Duijnhoven J., Andersen M., Aarts M. "A simulation tool for indoor lighting design considering ipRGC-induced responses". BuildSim Nordic Conference, Copenhagen, Denmark, Aug. 22-23, 2022

Lark v3.0
Jung B., Cheng Z., Brennan M., Inanici M. "Multispectral Lighting Simulation Approaches for Predicting Opsin-driven Metrics and their Application in a Neonatal Intensive Care Unit," IBPSA 2023 Conference, Shanghai, China, September 4-6, 2023.

Others
Khademagha, P. “Light directionality in design of healthy offices”. Ph. D. thesis, Eindhoven University of Technology. Eindhoven, Netherlands. 2021.

Balakrishnan, P., Jakubiec, A. “Spectral Rendering with Daylight: A Comparison of Two Spectral Daylight Simulation Platforms.” In Proceedings of Building Simulation 2019: 16th Conference of IBPSA, Volume 16, Rome, Italy, pp. 1191–1198. 2019.

International Commission on Illumination. 2018. System for Metrology of Optical Radiation for ipRGC-Influenced Responses to Light (CIE S 026/E:2018).

Amundadottir, M. L. “Light-driven model for identifying indicators of non-visual health potential in the built environment”. Ph. D. thesis, Ecole Polytechnique Federale de Lausanne. Lausanne, Switzerland. 2016.

Lucas R., Peirson S., Berson D., Brown T., Cooper H., Czeisler C., Figueri M., Gamlin, P., Lockley, S., O’hagan J., Price, L., Provencio I., Skene D., Brainard G. “Measuring and Using Light in the Melanopsin Age”, Trends in Neurosciences, 37(1), 1-9. 2014 .

Kojima, D., Mori, S., Torii, M., Wada, A., Morishita, R., & Fukada, Y. (2011). UV-sensitive photoreceptor protein OPN5 in humans and mice. PloS One, 6(10).




