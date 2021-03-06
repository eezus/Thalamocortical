TITLE Mod file for component: Component(id=EctopicStimL23RS_TO_CG3D_L23PyrRS_PoiSyn0 type=poissonFiringSynapse)

COMMENT

    This NEURON file has been generated by org.neuroml.export (see https://github.com/NeuroML/org.neuroml.export)
         org.neuroml.export  v1.5.0
         org.neuroml.model   v1.5.0
         jLEMS               v0.9.8.7

ENDCOMMENT

NEURON {
    POINT_PROCESS EctopicStimL23RS_TO_CG3D_L23PyrRS_PoiSyn0
    ELECTRODE_CURRENT i
    RANGE averageRate                       : parameter
    RANGE averageIsi                        : parameter
    
    RANGE i                                 : exposure
    RANGE SynForEctStim_tauRise             : parameter
    RANGE SynForEctStim_tauDecay            : parameter
    RANGE SynForEctStim_peakTime            : parameter
    RANGE SynForEctStim_waveformFactor      : parameter
    RANGE SynForEctStim_gbase               : parameter
    RANGE SynForEctStim_erev                : parameter
    
    RANGE SynForEctStim_g                   : exposure
    
    RANGE SynForEctStim_i                   : exposure
    
}

UNITS {
    
    (nA) = (nanoamp)
    (uA) = (microamp)
    (mA) = (milliamp)
    (A) = (amp)
    (mV) = (millivolt)
    (mS) = (millisiemens)
    (uS) = (microsiemens)
    (molar) = (1/liter)
    (kHz) = (kilohertz)
    (mM) = (millimolar)
    (um) = (micrometer)
    (umol) = (micromole)
    (S) = (siemens)
    
}

PARAMETER {
    
    averageRate = 1.00000005E-4 (kHz)
    averageIsi = 10000 (ms)
    SynForEctStim_tauRise = 0.099999994 (ms)
    SynForEctStim_tauDecay = 0.19999999 (ms)
    SynForEctStim_peakTime = 0.13862944 (ms)
    SynForEctStim_waveformFactor = 4 
    SynForEctStim_gbase = 0.01 (uS)
    SynForEctStim_erev = 0 (mV)
}

ASSIGNED {
    v (mV)
    
    SynForEctStim_g (uS)                   : derived variable
    
    SynForEctStim_i (nA)                   : derived variable
    
    i (nA)                                 : derived variable
    rate_tsince (ms/ms)
    rate_SynForEctStim_A (/ms)
    rate_SynForEctStim_B (/ms)
    
}

STATE {
    tsince (ms) 
    isi (ms) 
    SynForEctStim_A  
    SynForEctStim_B  
    
}

INITIAL {
    rates()
    rates() ? To ensure correct initialisation.
    
    tsince = 0
    
    isi = -  averageIsi  * log(1 - random_float(1))
    
    net_send(0, 1) : go to NET_RECEIVE block, flag 1, for initial state
    
    SynForEctStim_A = 0
    
    SynForEctStim_B = 0
    
}

BREAKPOINT {
    
    SOLVE states METHOD cnexp
    
    
}

NET_RECEIVE(flag) {
    
    LOCAL weight
    
    
    if (flag == 1) { : Setting watch for top level OnCondition...
        WATCH (tsince  >  isi) 1000
    }
    if (flag == 1000) {
    
        tsince = 0
    
        isi = -  averageIsi  * log(1 - random_float(1))
    
        : Child: Component(id=SynForEctStim type=expTwoSynapse)
    
        : This child is a synapse; defining weight
        weight = 1
    
        : paramMappings: {SynForEctStim_notes={}, EctopicStimL23RS_TO_CG3D_L23PyrRS_PoiSyn0={averageRate=averageRate, i=i, tsince=tsince, isi=isi, averageIsi=averageIsi}, SynForEctStim={A=SynForEctStim_A, tauRise=SynForEctStim_tauRise, gbase=SynForEctStim_gbase, erev=SynForEctStim_erev, B=SynForEctStim_B, peakTime=SynForEctStim_peakTime, g=SynForEctStim_g, i=SynForEctStim_i, tauDecay=SynForEctStim_tauDecay, waveformFactor=SynForEctStim_waveformFactor}}
    ?    state_discontinuity(SynForEctStim_A, SynForEctStim_A  + (weight *  SynForEctStim_waveformFactor ))
        SynForEctStim_A = SynForEctStim_A  + (weight *  SynForEctStim_waveformFactor )
    
        : paramMappings: {SynForEctStim_notes={}, EctopicStimL23RS_TO_CG3D_L23PyrRS_PoiSyn0={averageRate=averageRate, i=i, tsince=tsince, isi=isi, averageIsi=averageIsi}, SynForEctStim={A=SynForEctStim_A, tauRise=SynForEctStim_tauRise, gbase=SynForEctStim_gbase, erev=SynForEctStim_erev, B=SynForEctStim_B, peakTime=SynForEctStim_peakTime, g=SynForEctStim_g, i=SynForEctStim_i, tauDecay=SynForEctStim_tauDecay, waveformFactor=SynForEctStim_waveformFactor}}
    ?    state_discontinuity(SynForEctStim_B, SynForEctStim_B  + (weight *  SynForEctStim_waveformFactor ))
        SynForEctStim_B = SynForEctStim_B  + (weight *  SynForEctStim_waveformFactor )
    
        net_event(t)
        WATCH (tsince  >  isi) 1000
    
    }
    
}

DERIVATIVE states {
    rates()
    tsince' = rate_tsince 
    SynForEctStim_A' = rate_SynForEctStim_A 
    SynForEctStim_B' = rate_SynForEctStim_B 
    
}

PROCEDURE rates() {
    
    SynForEctStim_g = SynForEctStim_gbase  * ( SynForEctStim_B  -  SynForEctStim_A ) ? evaluable
    SynForEctStim_i = SynForEctStim_g  * ( SynForEctStim_erev  - v) ? evaluable
    ? DerivedVariable is based on path: synapse/i, on: Component(id=EctopicStimL23RS_TO_CG3D_L23PyrRS_PoiSyn0 type=poissonFiringSynapse), from synapse; Component(id=SynForEctStim type=expTwoSynapse)
    i = SynForEctStim_i ? path based
    
    rate_tsince = 1 ? Note units of all quantities used here need to be consistent!
    
     
    rate_SynForEctStim_A = - SynForEctStim_A  /  SynForEctStim_tauRise ? Note units of all quantities used here need to be consistent!
    rate_SynForEctStim_B = - SynForEctStim_B  /  SynForEctStim_tauDecay ? Note units of all quantities used here need to be consistent!
    
     
    
}


: Returns a float between 0 and max
FUNCTION random_float(max) {
    
    random_float = scop_random()*max
    
}

