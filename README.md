# Lark v2.0


This is version 2.0 of Lark Spectral Lighting, based upon Lark Spectral Lighting v1.0 for Grasshopper/Rhino environment to investigate circadian, non-visual light. The objective of Lark Spectral Lighting is to make circadian lighting analysis more accessible to architects, lighting designers, researchers, and other interested parties. The simulation engine is Radiance; and Lark is provided as an open source and freely available tool. Lark allows for simulations in 9 channels and computes photopic (luminance and illuminance values) and circadian/non-visual metrics (e.g. alpha-opic values).


Lark is originally developed as a collaboration between Mehlika Inanici, Ph.D. (University of Washington) and ZGF Architects LLP. The beta version of Lark was released in 2015. After 7 years of testing by the developers and third parties, Lark 1.0 was released in 2022. Modifications and new features in Lark Spectral Lighting v2.0 were developed by Clotilde Pierson, Ph.D. (EPFL, Oregon State University) and Myrta Gkaintatzi-Masouti, M.Sc. (Eindhoven University of Technology), with contributions from ZGF Architects LLP for the electric lighting simulation workflow and contributions from Priji Balakrishnan, Ph.D. and Alstan J. Jakubiec, Ph.D. for the implementation of the Perez sky model.



### What is new in v2.0:


Lark v2.0 includes the following new features:
• Option to run daylight and/or electric light spectral simulations. For the daylight simulations, a more accurate sky model is used that takes as an input the diffuse horizontal irradiance (DHI), direct normal irradiance (DNI) and dew point temperature.
• Calculation of spectral irradiance and the α-opic metrics defined by CIE.
• Spatially weighted image-based analysis, which makes it possible to account for the direction at which light enters the human eye, since the literature indicates that the spatial sensitivity of the IIL responses is not uniform within the field of view (Khademagha, 2021).
• Calculation of time-series of light exposures using a Radiance matrix-based method (Subramaniam, 2017). The time series of light exposures can be used as input for the so-called non-visual direct response (nvRD) model, a light-driven prediction model for alertness (Amundadottir, 2016).



### Installation instructions:


1. On a Windows machine, install:
- Rhino3D v6 or later (https://www.rhino3d.com/)
- Radiance v5.3 or later (https://github.com/LBNL-ETA/Radiance/releases)
- Ladybug v0.0.69 or later and Honeybee v0.0.66 or later [Legacy Plugins] (https://www.food4rhino.com/en/app/ladybug-tools) 
	/!\ Follow the installation instructions for Ladybug/Honeybee (including the installation of Daysim v4.0)
	/!\ If you cannot find the FalseStartToggle after installing the Legacy Plugins, also install Ladybug Tools 1.5.0 or later (https://www.food4rhino.com/en/app/ladybug-tools)

2. In Windows, search for “Edit the system environment variables”, and make sure that for the “PATH” and "RAYPATH" variables, the Radiance installation directory paths (C:\Radiance\bin and C:\Radiance\lib) are at the top of the list, above any other path of software using Radiance such as Daysim. Once you saved the environment variables, open the terminal and type e.g. “where gendaylit”. The first path displayed should be the one of your original Radiance directory (C:\Radiance\bin\gendaylit.exe).

3. Go to https://www.food4rhino.com/en/app/lark-spectral-lighting and download Lark Spectral Lighting v2.0. Unzip the file.

4. Open Rhino and type "Grasshopper" into the command line (without quotations). Wait for grasshopper to load.

5. Select and drag all the userObject files (.ghuser) from the Lark_Spectral_Lighting_v2 folder that you downloaded onto your grasshopper canvas. You should see a Lark tab appear on the Grasshopper tool bar.

6. Create the lark folder (C:\lark) if none exists. From the Lark_Spectral_Lighting_v2 folder, copy the 4 HDR masking files (1_upper_inner.hdr, 2_lower_inner.hdr, 3_upper_outer.hdr, 4_lower_outer.hdr) and paste them in the lark folder.

7. Restart Rhino and grasshopper. You now have a fully-functioning Lark 2.0. You can open and use the provided example 3D model (.3dm), example simulation inputs, and one of the three Lark 2.0 templates (.gh) as the starting point for your simulations.




## Lark v1.0


This is version 1.0 release of Lark Spectral Lighting for Grasshopper/Rhino environment to investigate circadian, non-visual light.
The objective is to make circadian lighting analysis more accessible to architects, lighting designers, researchers, and other interested parties.
The simulation engine is Radiance; and Lark is provided as an open source and freely available tool. 
Lark allows for simulations both in 3 and 9 channels. Along with photopic luminance and illuminance values, Equivalent melanopic illuminance (EML) and -luminance (EM.cd/m2) values are computed. 
Lark includes tools to interpolate spectral data, build spectral materials, and prepare spectral sky definitions for Radiance. 
Lark does not currently color the sun separate from the sky so should not be used with scenes that have direct beam light (yet).


Lark is developed as a collaboration between Mehlika Inanici, Ph.D. (University of Washington) and ZGF Architects LLP. The beta version of Lark was released in 2015. 
After 7 years of testing by the developers and third parties, Lark 1.0 was released in 2022. Lark is currently under redevelopment, and stay tuned for its new versions soon... 



### What is new in v1.0:


Lark v1.0 is a minor revision to the Beta release of Lark. Lucas curve now reports Equivalent Melanopic Lux (EML), 
luminous efficacy coefficient is scaled at 179. The 179 is the luminous efficacy coefficient used in calculating luminance and illuminance in Radiance
and it is driven from the V(λ). V(λ) peaks at a wavelength of 555 nm (V(λ) and the luminous efficiency is defined by scaling the normalized
V(λ) curve by 683 lm/W. The numerical integration of the area under the curve leads to 179. The conventional utilization of 683 lm/W dictates
that the luminous efficacy is determined at 555 as 683 lm/W, however given that this scaling leads to very high values with the spectral
circadian efficiency curves, the beta version scaled the Lucas curve to match the peak to 683 lm/W, resulting in 149 luminous efficacy
coefficient. This coefficient is scaled to 179 in this version to provide EML units.




## Lark Links:


- [Lark's homepage](http://faculty.washington.edu/inanici/Lark/Lark_home_page.html)
- [Lark on Github](https://github.com/larkspectral)
- [v1.0 tutorials](https://www.youtube.com/channel/UC3hiIWgMCPn3JfBO6J9UUfw) on Youtube
- [v2.0 tutorials](https://www.youtube.com/channel/UC3hiIWgMCPn3JfBO6J9UUfw) on Youtube




## Publications:


Inanici M, Brennan M, and Clark E. "[Multi-spectral Lighting Simulations: Computing Circadian Light](http://www.ibpsa.org/proceedings/BS2015/p2467.pdf)," International Building Performance Simulation Association (IBPSA) 2015 Conference, Hyderabad, India, December 7-9, 2015.

Gkaintatzi-Masouti M., Pierson C., Van Duijnhoven J., Andersen M., Aarts M. "A simulation tool for indoor lighting design considering ipRGC-induced responses". BuildSim Nordic Conference, Copenhagen, Denmark, Aug. 22-23, 2022




## Software:


Available online at: https://www.food4rhino.com/en/app/lark-spectral-lighting




## Presentations:

- "Lark 2.0 – a simulation tool to support the design of healthy indoor environments", IES Annual Conference, Aug. 18-20, 2022, New Orleans (LA), USA.
- "A simulation tool for indoor lighting design considering ipRGC-induced responses", BuildSim Nordic Conference, Aug. 22-23, 2022, Copenhagen, Denmark.
- Designing for Circadian Rhythms," Greenbuild 2016, Los Angeles, CA, October 5, 2016 (with E. Clark).
- [Working Smarter and Sleeping Better](https://metropolismag.com/programs/working-smarter-and-sleeping-better-circadian-rhythm-in-workplace-and-healthcare-design/): Circadian Rhythm in Workplace and Healthcare Design," Metropolis Magazine, Point of view, March 2016.
- Designing for Circadian Light and health Outcomes in Architectural Practice," 2016 AIBC (Architectural institute for British Columbia), Building a Resilient Future,  May 17th, 2016 (with M. Brennan and E. Clark), Vancouver, Canada.
- Designing for Circadian Friendly Built Environments,” 3 hour workshop, Lightfair International, Lightfair Institute, San Diego, CA, April 24-28, 2016 (with M. Brennan and E. Clark)
- UW Architecture news: Nov 19, 2015: http://arch.be.uw.edu/circadian-rhythms-it-is-all-about-a-day/
