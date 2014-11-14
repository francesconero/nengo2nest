'''
Created on May 27, 2014

@author: Francesco Nero
'''
import os
import csv
import random

data_path = "."

#simulation parameters
dt = 0.1
simulation_time = 100000
noise_current_std_dev = 500.0  # pA
default_connection_delay = lambda: random.uniform(1.0, 1.5)  # ms

#neuron parameters
C_m = 200.0  # pF Can be fixed
gL = 10.0  # nS
taum = C_m / gL
tau_w = 30.0  # ms
EL = -70.0  # mV # Same as changing I
VT = -50  # mV
DeltaT = 2.0  # mV
Vcut = VT + 5 * DeltaT  # mV
a = 2.0  # ns
b = 0.0  # pA
Vr = -58.0  # mV
Vth = -50.0  # mV

t_ref = 1.0  # ms refractory period
J = 500.0  # weight of synapses

rate = 100.0  # Hz rate of inputs

neuron_model = "aeif_cond_exp"


#write settings to file
def to_file(filename):
    with open(data_path + os.sep + filename + ".set", 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='excel-tab')
        csvwriter.writerow(["resolution", "simulation.time"])
        csvwriter.writerow([dt, simulation_time])