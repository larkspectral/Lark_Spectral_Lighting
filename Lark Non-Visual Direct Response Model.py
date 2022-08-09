# Relative and cumulative alerting response using the non-visual direct response model.

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
Use this to compute the relative and cumulative alerting response using the non-vidual direct response model (Amundadottir, 2016).
The nvRD model takes as input a time series of eye-level light stimuli and translates it to a predicted human alerting response. The model accounts for light quantity, spectrum, duration and history. Relative repsonse is calculated each timestep of the analysis period (which saturates after a level of light stimulus is reached) which is summed up to a cumulative response at the end of the analysis period.
-
More information about the model can be found in this PhD thesis:
Amundadottir, 2016, "Light-driven model for identifying indicators of non-visual health potential in the built environment", https://infoscience.epfl.ch/record/221429?ln=en
-
Provided by Lark 2.0.0

    Args:
        spectral_data:A path to a csv file with timeseries of spectral irradiance. 
            The csv file should include the following information:
            - point coordinates (in columns A,B,C)
            - vector coordinates (in columns D,E,F)
            - month, day and hour (in columns G,H,I)
            - alpha-opic irradiance, ELR and EDI (in columns J,K,L) (these are not necessary for the calculation)
            - spectral irradiance in W/m2/nm (in the next 400 columns)
            - each row is a new timestep
        calculate: A boolean toggle to run this component
        time_step: Time step for timeseries in hours (e.g. for data every 6 minutes, input 6/60 = 0.1)
    Returns:
        result: The nvRD outputs (relative and cumulative responses) in a tree data structure 
"""

__author__ = "cpierson"
__version__ = "2021.10.15"

ghenv.Component.Name = "Lark Non-Visual Direct Response Model"
ghenv.Component.NickName = 'nvRD'
ghenv.Component.Message = '2.0.0'
ghenv.Component.Category = "Lark"
ghenv.Component.SubCategory = "Timeseries"



#check all inputs
error_list = []
inputs = [spectral_data,calculate,time_step]
inputs_name = ["spectral_data","calculate","time_step"]

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



#apply nvRD model
if check != "error":
    
    import rhinoscriptsyntax as rs
    import scriptcontext
    import csv
    import collections
    import math
    from collections import OrderedDict
    from Grasshopper import DataTree
    from Grasshopper.Kernel.Data import GH_Path
    
    
    
    #define melanopic action spectra
    IPRGC_SENS_WEIGHTING = [1.40458103669806e-05,
                            1.70885602662509e-05,
                            2.07872194946997e-05,
                            2.52723036079605e-05,
                            3.06959011323138e-05,
                            3.72338574949650e-05,
                            4.50877896278921e-05,
                            5.44868055974823e-05,
                            6.56887874058060e-05,
                            7.89810842799403e-05,
                            9.46804605773228e-05,
                            0.000113132148989689,
                            0.000134707877688535,
                            0.000159802770356207,
                            0.000188831060635101,
                            0.000222220616172136,
                            0.000260406329652919,
                            0.000303822501342455,
                            0.000352894405052384,
                            0.000408029291932361,
                            0.000469607138736220,
                            0.000537971484397555,
                            0.000613420717012346,
                            0.000696200170260968,
                            0.000786495363254041,
                            0.000884426671966966,
                            0.000990045656819256,
                            0.00110333319401797,
                            0.00122419947351010,
                            0.00135248583974960,
                            0.00148796836886473,
                            0.00163036300247268,
                            0.00177933199854958,
                            0.00193449141630587,
                            0.00209541932636663,
                            0.00226166442970644,
                            0.00243275477746793,
                            0.00260820630672214,
                            0.00278753094143541,
                            0.00297024405006142,
                            0.00315587109789220,
                            0.00334395338040985,
                            0.00353405277061527,
                            0.00372575545644755,
                            0.00391867468231596,
                            0.00411245254041457,
                            0.00430676088239128,
                            0.00450130144009080,
                            0.00469580525584614,
                            0.00489003152879568,
                            0.00508376598476375,
                            0.00527681887426264,
                            0.00546902269706799,
                            0.00566022974345871,
                            0.00585030953239263,
                            0.00603914621629224,
                            0.00622663601131579,
                            0.00641268470143451,
                            0.00659720525466831,
                            0.00678011558068493,
                            0.00696133645079111,
                            0.00714078959421325,
                            0.00731839597849908,
                            0.00749407427684176,
                            0.00766773952107771,
                            0.00783930193595848,
                            0.00800866594795239,
                            0.00817572936019632,
                            0.00834038268419216,
                            0.00850250861833047,
                            0.00866198166323489,
                            0.00881866786417196,
                            0.00897242467128552,
                            0.00912310090912543,
                            0.00927053684778657,
                            0.00941456436890286,
                            0.00955500722070634,
                            0.00969168135732249,
                            0.00982439535839490,
                            0.00995295092598580,
                            0.0100771434564557,
                            0.0101967626856656,
                            0.0103115934063473,
                            0.0104214162568379,
                            0.0105260085805595,
                            0.0106251453556331,
                            0.0107186001938462,
                            0.0108061464078350,
                            0.0108875581448027,
                            0.0109626115843740,
                            0.0110310861972966,
                            0.0110927660606484,
                            0.0111474412240244,
                            0.0111949091198672,
                            0.0112349760097167,
                            0.0112674584566989,
                            0.0112921848131126,
                            0.0113089967105262,
                            0.0113177505384268,
                            0.0113183188962093,
                            0.0113105920022081,
                            0.0112944790426064,
                            0.0112699094424563,
                            0.0112368340407497,
                            0.0111952261515405,
                            0.0111450824935501,
                            0.0110864239715329,
                            0.0110192962939277,
                            0.0109437704129872,
                            0.0108599427756385,
                            0.0107679353757622,
                            0.0106678956013323,
                            0.0105599958728939,
                            0.0104444330730885,
                            0.0103214277703019,
                            0.0101912232429182,
                            0.0100540843140268,
                            0.00991029600965427,
                            0.00976016205660267,
                            0.00960400323866978,
                            0.00944215563234619,
                            0.00927496874495664,
                            0.00910280357959258,
                            0.00892603065203412,
                            0.00874502798516498,
                            0.00856017910614212,
                            0.00837187107080856,
                            0.00818049253856225,
                            0.00798643191916143,
                            0.00779007561081231,
                            0.00759180634641297,
                            0.00739200166208871,
                            0.00719103249922495,
                            0.00698926194815814,
                            0.00678704413860025,
                            0.00658472327881904,
                            0.00638263284264213,
                            0.00618109490055963,
                            0.00598041958862225,
                            0.00578090470651697,
                            0.00558283543419087,
                            0.00538648415471807,
                            0.00519211036979155,
                            0.00499996069328840,
                            0.00481026890781823,
                            0.00462325606902416,
                            0.00443913064266381,
                            0.00425808866014782,
                            0.00408031387923890,
                            0.00390597793799397,
                            0.00373524049173527,
                            0.00356824932482074,
                            0.00340514043120267,
                            0.00324603806015520,
                            0.00309105472604745,
                            0.00294029118356310,
                            0.00279383637223515,
                            0.00265176733648840,
                            0.00251414912947358,
                            0.00238103471075089,
                            0.00225246484925860,
                            0.00212846804391863,
                            0.00200906047463784,
                            0.00189424599633075,
                            0.00178401618791290,
                            0.00167835046701402,
                            0.00157721627948104,
                            0.00148056937065387,
                            0.00138835414298932,
                            0.00130050410198917,
                            0.00121694238967068,
                            0.00113758240212308,
                            0.00106232848513698,
                            0.000991076699581642,
                            0.000923715646228176,
                            0.000860127338145027,
                            0.000800188107672747,
                            0.000743769534340301,
                            0.000690739379913642,
                            0.000640962517044585,
                            0.000594301838671729,
                            0.000550619136356774,
                            0.000509775937051074,
                            0.000471634289304793,
                            0.000436057491579037,
                            0.000402910757028366,
                            0.000372061810820601,
                            0.000343381417695797,
                            0.000316743838989650,
                            0.000292027219722010,
                            0.000269113907553981,
                            0.000247890706432206,
                            0.000228249068561421,
                            0.000210085228978767,
                            0.000193300287455012,
                            0.000177800242732987,
                            0.000163495984249637,
                            0.000150303246495171,
                            0.000138142531060983,
                            0.000126939001238257,
                            0.000116622353770586,
                            0.000107126672055044,
                            9.83902647429017e-05,
                            9.03554933280295e-05,
                            8.29685919400051e-05,
                            7.61794821899259e-05,
                            6.99415855580766e-05,
                            6.42116354698873e-05,
                            5.89494908845704e-05,
                            5.41179529225379e-05,
                            4.96825857848649e-05,
                            4.56115429716332e-05,
                            4.18753995858377e-05,
                            3.84469913150812e-05,
                            3.53012605134129e-05,
                            3.24151096588775e-05,
                            2.97672623369975e-05,
                            2.73381317946982e-05,
                            2.51096970211940e-05,
                            2.30653862402975e-05,
                            2.11899676406233e-05,
                            1.94694471245595e-05,
                            1.78909728220270e-05,
                            1.64427460894767e-05,
                            1.51139386969055e-05,
                            1.38946158946840e-05,
                            1.27756650465772e-05,
                            1.17487295145357e-05,
                            1.08061474837691e-05,
                            9.94089542255343e-06,
                            9.14653587951156e-06,
                            8.41716933119752e-06,
                            7.74738980422747e-06,
                            7.13224400855155e-06,
                            6.56719373140358e-06,
                            6.04808125473909e-06,
                            5.57109757234028e-06,
                            5.13275319605860e-06,
                            4.72985135372937e-06,
                            4.35946339402177e-06,
                            4.01890622579238e-06,
                            3.70572163133157e-06,
                            3.41765730418287e-06,
                            3.15264947295106e-06,
                            2.90880698267512e-06,
                            2.68439671492658e-06,
                            2.47783023680393e-06,
                            2.28765157743717e-06,
                            2.11252603851208e-06,
                            1.95122995268638e-06,
                            1.80264131062329e-06,
                            1.66573118373392e-06,
                            1.53955587562419e-06,
                            1.42324974070835e-06,
                            1.31601861350573e-06,
                            1.21713379680570e-06,
                            1.12592656119086e-06,
                            1.04178311237639e-06,
                            9.64139986475195e-07,
                            8.92479836657872e-07,
                            8.26327577763544e-07,
                            7.65246858252820e-07,
                            7.08836831496063e-07,
                            6.56729200776859e-07,
                            6.08585514578513e-07,
                            5.64094690726326e-07,
                            5.22970749794461e-07,
                            4.84950739867450e-07,
                            4.49792836284998e-07,
                            4.17274601406358e-07,
                            3.87191390718240e-07,
                            3.59354892787527e-07,
                            3.33591791636594e-07,
                            3.09742541102874e-07,
                            2.87660241643591e-07,
                            2.67209610868210e-07,
                            2.48266039831927e-07,
                            2.30714727809335e-07,
                            2.14449888893941e-07,
                            1.99374024341513e-07,
                            1.85397255097875e-07,
                            1.72436709429308e-07,
                            1.60415961009673e-07,
                            1.49264513216717e-07,
                            1.38917325753733e-07,
                            1.29314380045003e-07,
                            1.20400280156962e-07,
                            1.12123886274166e-07,
                            1.04437978012406e-07,
                            9.72989450826439e-08,
                            9.06665030307496e-08,
                            8.45034319711577e-08,
                            7.87753364089801e-08,
                            7.34504244063617e-08,
                            6.84993044962312e-08,
                            6.38947988812856e-08,
                            5.96117715791790e-08,
                            5.56269702874580e-08,
                            5.19188808446972e-08,
                            4.84675932584252e-08,
                            4.52546783565069e-08,
                            4.22630741973801e-08,
                            3.94769814465934e-08,
                            3.68817669929844e-08,
                            3.44638751381613e-08,
                            3.22107457481439e-08,
                            3.01107388065528e-08,
                            2.81530648549914e-08,
                            2.63277208486282e-08,
                            2.46254309937757e-08,
                            2.30375921697945e-08]
    
    
    
    #define mathematical functions
    def trapz(y, x = False, delta = 1, initial = 0.0):
        '''
        Integrate along the given axis using the composite trapezoidal rule with delta = 1.
        '''
        area = cumtrapz(y, x, delta, initial)
        return area[len(y)-1]
    
    def cumtrapz(y, x = False, delta = 1, initial = 0.0):
        n_trapz = len(y)
        if not x:
            dx = [delta]*n_trapz
        else:
            dx = [j-i for i, j in zip(x[:-1], x[1:])] #https://stackoverflow.com/questions/2400840/python-finding-differences-between-elements-of-a-list
        area = []
        for i_trapz in range(n_trapz):
            if i_trapz == 0:
                area.append(initial)
            else:
                area.append( (((y[i_trapz]+y[i_trapz-1])/2)*dx[i_trapz-1]) + area[i_trapz-1] )
        return area
    
    def naive_convolve(g, f):
        vmax = len(f)
        smax = len(g)
        smid = smax // 2
        xmax = vmax + 2 * smid
        h = [0]*xmax
        for x in range(xmax):
            s_from = max(smid - x, -smid)
            s_to = min((xmax - x) - smid, smid + 1)
            value = 0
            for s in range(s_from, s_to):
                v = x - smid + s
                value += g[smid - s] * f[v]
            h[x] = value
        return h
    
    def lfilter_base(b, a, x):
        b = [i/a for i in b]
        y = naive_convolve(b,x)
        ind = slice(len(y) - len(b) + 1)
        return y[ind]
    
    def effective_irradiance(spectral_irradiance):
        '''
        Effective irradiance evaluation
        Parameters:
            spectral_irradiance (vec): between 390nm and 700nm and step of 1 nm
        Returns:
            eff_irradiance (float) (Amundadottir, 2016)
        '''
        n_ieff = len(spectral_irradiance)
        if n_ieff != 311:
            return "Error: Spectral irradiance should be within 390-700nm range!"
        for i in range(n_ieff):
            spectral_irradiance[i] = spectral_irradiance[i]*IPRGC_SENS_WEIGHTING[i]
        return trapz(spectral_irradiance)*311
    
    def filter_sma(filter_length, input_signal):
        '''
        Simple moving average (SMA) filter.
        Parameters:
            filter_length (int)
            input_signal (list)
        Returns:
            sma_filter (list)
        '''
        filter_length = int(filter_length)
        sma = [1.0/filter_length]*filter_length
        sma_filter = lfilter_base(sma, sum(sma), input_signal)
        return sma_filter
    
    def filter_ema(filter_length, input_signal):
        '''
        Exponential moving average (EMA) filter.
        Parameters:
            filter_length (int)
            input_signal (list)
        Returns:
            ema_filter (list)
        '''
        filter_length = int(filter_length)
        alpha = 2.0 / (filter_length + 1.0)
        a_vec = [1.0-alpha]*filter_length
        b_vec = range(1,filter_length+1)
        c_vec = [a**b for a, b in zip(a_vec, b_vec)]
        ema_filter = lfilter_base(c_vec, sum(c_vec), input_signal) # VERIFIED
        return ema_filter
    
    def relative_response(light_stimuli, sigma, rate_growth):
        '''
        Compute relative response.
        Parameters:
            light_stimuli (list): irradiance
            sigma (float): half max. response
            rate_growth
        Returns:
            relative response (list)
        '''
        return [1.0/(1.0+(s/ls)**rate_growth) if ls!=0 else 0.0 for s, ls in zip(sigma,light_stimuli)]
    
    def adaptive_response(I, Ieff, sigma, n, d, FLOOR):
        '''
        Compute adaptive response.
        Parameters:
            I: light stimuli [W/m2 eff.]
            sigma: half max. response
            n: rate growth
            d: filter length
            FLOOR: boolean
        Returns:
            r: relative response
        '''
        H = filter_sma(d, [math.log10(i*118.5*2.2) if i!=0 else 0.0 for i in I]) #VERIFIED
        H = [0 if h<0.0 else h for h in H] #VERIFIED
        # print H #VERIFIED
        if FLOOR == 1:
            H = [math.floor(h) if h>0.0 else h for h in H] #VERIFIED
        sigma = [sigma*2.0**(h-1) for h in H] #VERIFIED
        return relative_response(Ieff, sigma, n)
    
    def direct_response(eff_irradiance, delta):
        '''
        Direct relative response model
        Parameters:
            eff_irradiance
        Returns:
            RD_p: relative response during photoperiod
        '''
        if delta > 0.3:
            return "Error: Step size must be smaller or equal to 0.3"
        # Spectral sensitivity
        zeff = 310.0/683.0/118.5/1.42*0.91  # from lux to melanopic eff. irr (F11)
        # Intensity response
        EI50 = 106  # [lx]
        slope = 3.55
        # Filter L2
        dFL2 = round(2.3/delta)
        # Filter L1
        dFL1 = round(0.3/delta)
        # Filter LH
        dFLH = round(1.7/delta)
        # MODEL
        u = filter_sma(dFL1, eff_irradiance) # VERIFIED
        v = adaptive_response(eff_irradiance, u, EI50*zeff, slope, dFLH, 0) # VERIFIED
        RD = filter_ema(dFL2, v) # VERIFIED
        n_RD = len(RD)
        RD_p = []
        for i in range(n_RD):
            if eff_irradiance[i] > 0.0:
                RD_p.append(RD[i])
            else:
                RD_p.append(0)
        return RD_p
    
    
    
    if calculate != True:
        pass
    else:
        #run the nvRD model
        file = spectral_data
        with open(file,'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
            next(csv_reader) # skip the headings
            pts = []
            vecs = []
            month = []
            day = []
            pts_vecs_date = []
            hour = []
            data = []
            eff_irradiance_timeseries = []
            for line in csv_reader:
                pts.append(",".join(line[:3]))
                vecs.append(",".join(line[3:6]))
                month.append("%02d" % int(line[6])) # 2-digit number (needed for sorting)
                day.append("%02d" % int(line[7])) # 2-digit number (needed for sorting)
                pts_vecs_date.append(",".join([",".join(line[:3]), ",".join(line[3:6]), "%02d" % int(line[6]), "%02d" % int(line[7])]))
                hour.append(float(line[8]))
                data.append(",".join(line[12:]))
            n = len(data)
            for i in range(n):
                wl = [float(x) for x in data[i].split(",")]
                eff_irradiance_timeseries.append(effective_irradiance(wl[10:-80]))
            zipped = zip(pts_vecs_date,hour,data,eff_irradiance_timeseries)
            zipped.sort()
            Dict = dict()
            effIrrDict = dict()
            hourDict = dict()
            for item in zipped:
                key = item[0] # points and vectors
                if key in effIrrDict: # if the id exists in the dictionary
                    # the id is the key and the value is the id,time,data
                    Dict[key].append(item)
                    effIrrDict[key].append(item[3])
                    hourDict[key].append(item[1])
                else:
                    # the first time that the id appears
                    Dict[key]     = [item]
                    effIrrDict[key] = [item[3]]
                    hourDict[key] = [item[1]]
            
            for key in list(set(pts_vecs_date)): # identify unique orientations
                rD = direct_response(effIrrDict[key], 0.1)
                RD = cumtrapz(rD, hourDict[key], initial=0.0)
                Dict[key] = [old + (new1,new2,) for old, new1, new2 in zip(Dict[key], rD, RD)]
                
            oDict = collections.OrderedDict(sorted(Dict.items()))
        
        
        
        #put the values in a data tree structure to use them in GH
        result = DataTree[str]()
        pathCount = 0 
        keys = oDict.keys()
        for key in keys:
            subPathCount = 0
            for index, row in enumerate(oDict[key]):
                new_sub_path = GH_Path(pathCount, subPathCount)
                for v in row:
                    result.Add(str(v), new_sub_path)
                subPathCount +=1
            pathCount += 1
