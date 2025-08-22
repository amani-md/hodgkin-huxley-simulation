#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np


# In[2]:


# Paramters
Vrest = -70 #Potential at rest (mV)
gNa_max = 120 #Na+ maximum conductance (mS/cm**2)
gK_max = 36 #K+ maximum conductance (mS/cm**2)
gl_max = 0.3 #Leakage conductance (mS/cm**2)
ENa = 45 #Na+ Equilibrium potential (mV)
EK = -82 #K+ Equilibrium potential (mV)
El = -59 #Leakage Equilibrium potential (mV)


# In[ ]:


# Simulation parameters
dt = 0.001 #Time-step (ms)
tmax = 200 #Duration of simulation (ms)
n_steps = int(tmax / dt) #Number of steps
sim_time = np.linspace(0, tmax, n_steps)


# In[3]:


# Gating variables
def alpha_n(V):
    return (0.01*(V+55))/(1-np.exp(-0.1*(V+55)))

def beta_n(V):
    return (0.125*np.exp(-0.0125*(V+65)))

def alpha_m(V):
    return (0.1*(V+40))/(1-np.exp(-0.1*(V+40)))

def beta_m(V):
    return 4*np.exp(-0.0556*(V+65))

def alpha_h(V):
    return 0.07*np.exp(-0.05*(V+65))

def beta_h(V):
    return 1/(1+np.exp(-0.1*(V+35)))


# In[4]:


def initialisation(sim_time, gNa_simu, gK_simu, gL_simu):
    
    ini = {name: np.empty(len(sim_time)+1) for name in ["V","n","m","h","gNa","gK","gL","INa","IK","IL"]}

    # Potential
    ini["V"][0] = Vrest

    # Activation & inactivation parameters
    ini["n"][0] = alpha_n(Vrest) / (alpha_n(Vrest) + beta_n(Vrest))
    ini["m"][0] = alpha_m(Vrest) / (alpha_m(Vrest) + beta_m(Vrest))
    ini["h"][0] = alpha_h(Vrest) / (alpha_h(Vrest) + beta_h(Vrest))

    # Conductances
    ini["gNa"][0] = gNa_simu
    ini["gK"][0] = gK_simu
    ini["gL"][0] = gL_simu

    # Currents
    ini["INa"][0] = ini["gNa"][0]*ini["m"][0]**3*ini["h"][0]*(ini["V"][0]-ENa)
    ini["IK"][0] = ini["gK"][0]*ini["n"][0]**4*(ini["V"][0]-EK)
    ini["IL"][0] = ini["gL"][0]*(ini["V"][0]-El)
    
    return (ini["V"], ini["n"], ini["m"], ini["h"],
            ini["gNa"], ini["gK"], ini["gL"],
            ini["INa"], ini["IK"], ini["IL"])


# In[5]:


def runSimulation(I_input, sim_time, gNa_simu = gNa_max, gK_simu = gK_max, gL_simu = gl_max):

    V, n, m, h, gNa, gK, gL, INa, IK, IL = initialisation(sim_time, gNa_simu, gK_simu, gL_simu)
    
    res = {name: np.empty(len(sim_time)+1) for name in ["V","n","m","h","gNa","gK","gL","INa","IK","IL"]}

    for i in range(len(sim_time)) : 

        # Potential over time 
        V[i+1] = V[i] + dt*(I_input[i] - (gK_simu*n[i]**4*(V[i]-EK)) - (gNa_simu*m[i]**3*h[i]*(V[i]-ENa)) - (gL_simu*(V[i]-El)))
        res["V"][i] = V[i]
        
        # n over time 
        n[i+1] = n[i] + dt*(alpha_n(V[i])*(1-n[i]) - beta_n(V[i])*n[i])
        res["n"][i] = n[i]

        # m over time 
        m[i+1] = m[i] + dt*(alpha_m(V[i])*(1-m[i]) - beta_m(V[i])*m[i])
        res["m"][i] = m[i]

        # h over time 
        h[i+1] = h[i] + dt* (alpha_h(V[i])*(1-h[i]) - beta_h(V[i])*h[i])
        res["h"][i] = h[i]

        # Na+ conductance over time 
        gNa[i]= gNa_simu*m[i]**3*h[i]
        res["gNa"][i] = gNa[i]
        
        # K+ conductance over time 
        gK[i]= gK_simu*n[i]**4
        res["gK"][i] = gK[i]

        # Leakage conductance over time 
        gL[i]= gL_simu*n[i]**4
        res["gL"][i] = gL[i]

        # Na+ current over time 
        INa[i]= gNa[i]*m[i]**3*h[i]*(V[i]-ENa)
        res["INa"][i] = INa[i]
        
        # K+ current over time 
        IK[i]= gK[i]*n[i]**4*(V[i]-EK)
        res["IK"][i] = IK[i]

        # Leakage current over time 
        IL[i] = gL[i]*(V[i]-El)
        res["IL"][i] = IL[i]
        
    return res

