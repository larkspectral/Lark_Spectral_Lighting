# Lark v1.0


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



### Lark Links:

- [Lark's homepage](http://faculty.washington.edu/inanici/Lark/Lark_home_page.html)
- [Lark on Github](https://github.com/larkspectral)
- [tutorials](https://www.youtube.com/channel/UC3hiIWgMCPn3JfBO6J9UUfw) on Youtube



### Publications:

Inanici M, Brennan M, and Clark E. "[Multi-spectral Lighting Simulations: Computing Circadian Light](http://www.ibpsa.org/proceedings/BS2015/p2467.pdf)," International Building Performance Simulation Association (IBPSA) 2015 Conference, Hyderabad, India, December 7-9, 2015.



### Software:

University of Washington and ZGF Architects LLP Lark Spectral Lighting Software. (2015-2022). Available online at: https://www.food4rhino.com/en/app/lark-spectral-lighting (accessed July 4, 2022).



### Presentations:

- Designing for Circadian Rhythms," Greenbuild 2016, Los Angeles, CA, October 5, 2016 (with E. Clark).
- [Working Smarter and Sleeping Better](https://metropolismag.com/programs/working-smarter-and-sleeping-better-circadian-rhythm-in-workplace-and-healthcare-design/): Circadian Rhythm in Workplace and Healthcare Design," Metropolis Magazine, Point of view, March 2016.
- Designing for Circadian Light and health Outcomes in Architectural Practice," 2016 AIBC (Architectural institute for British Columbia), Building a Resilient Future,  May 17th, 2016 (with M. Brennan and E. Clark), Vancouver, Canada.
- Designing for Circadian Friendly Built Environments,” 3 hour workshop, Lightfair International, Lightfair Institute, San Diego, CA, April 24-28, 2016 (with M. Brennan and E. Clark)
- UW Architecture news: Nov 19, 2015: http://arch.be.uw.edu/circadian-rhythms-it-is-all-about-a-day/



