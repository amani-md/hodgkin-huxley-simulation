#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import numpy as np
from HodgkinHuxleyEquations import *


# In[2]:


def plotVoltage(V, sim_time, vrest = True, vmax = True, vmin = True): 
    
    plt.plot(sim_time, V[:-1])
    
    if vmax == True :
        plt.axhline(y=np.max(V[:-1]), linestyle = "--", color = "green",  label = fr"$V_{{\mathrm{{max}}}}$ = {np.max(V[:-1]):.2f}")

    if vrest == True :
        plt.axhline(y=Vrest, linestyle = "--", color = "orange",  label = fr"$V_{{\mathrm{{rest}}}}$ = {Vrest:.2f}")

    if vmin == True :
        plt.axhline(y=np.min(V[:-1]), linestyle = "--", color = "red",  label = fr"$V_{{\mathrm{{min}}}}$ = {np.min(V[:-1]):.2f}")

    plt.legend()
    plt.show()


# In[3]:


def plotAll(results, I_input, sim_time):
    
    fig, (ax0, ax3, ax1, ax2, ax4) = plt.subplots(5,1, figsize = (10,10))
    plt.subplots_adjust(hspace=1)
    
    # Input
    ax0.plot(sim_time, I_input)
    ax0.set_title('Input current')
    ax0.set_ylabel('Amplitude $(μA/cm^2)$')
    ax0.set_xlabel('Time $(ms)$')
    
    # Potential
    ax3.plot(sim_time, results["V"][:-1])
    ax3.set_title('Time evolution of the membrane potential')
    ax3.set_ylabel('Voltage $(mV)$')
    ax3.set_xlabel('Time $(ms)$')
    
    # Currents
    ax1.plot(sim_time, results["INa"][:-1], color = '#ff7f0e', label='$I_{Na^+}$')
    ax1.plot(sim_time, results["IK"][:-1], color = '#1f77b4', label='$I_{K^+}$')
    ax1.plot(sim_time, results["IL"][:-1], color = '#2ca02c', label='$I_l$')
    ax1.set_title('Time evolution of the ionic currents')
    ax1.set_ylabel('Current $(μA/cm^2)$')
    ax1.set_xlabel('Time $(ms)$')
    ax1.legend()
    
    # Conductances
    ax2.plot(sim_time, results["gK"][:-1], color = '#1f77b4', label='$g_{K^+}$')
    ax2.plot(sim_time, results["gNa"][:-1], color = '#ff7f0e', label='$g_{Na^+}$')
    ax2.set_title('Time evolution of conductances ')
    ax2.set_ylabel('Conductance $(mS/cm^2)$')
    ax2.set_xlabel('Time $(ms)$')
    ax2.legend()
    
    # Activation & inactivation
    ax4.plot(sim_time, results["n"][:-1], color = '#1f77b4', label = '$n$')
    ax4.plot(sim_time, results["m"][:-1], color = '#7f7f7f', label = '$m$')
    ax4.plot(sim_time, results["h"][:-1], color = '#9467bd', label = '$h$')
    ax4.set_title('Time evolution of the activation and inactivation variable')
    ax4.set_xlabel('Time $(ms)$')
    ax4.set_ylabel('Probability')
    ax4.legend()
    plt.show()

