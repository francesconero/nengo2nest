'''
Created on May 27, 2014

@author: Francesco Nero
'''
import time
import random

import nest.voltage_trace

from . import nef
from . import settings as s


voltmeter = None
spikeDetector = None
filename = None
watched = None


def setup(network, tofile, label='', voltage_watch=None):
    nest.ResetKernel()
    nest.SetKernelStatus({"resolution": s.dt, "overwrite_files": True,
                          "data_prefix": label,
                          "data_path": s.data_path})

    # Crea tipi statici
    nest.CopyModel("static_synapse", "excitatory", {"weight": s.J})
    nest.CopyModel("static_synapse", "inhibitory", {"weight": -s.J})
    poisson_generator = nest.Create('poisson_generator')
    nest.SetStatus(poisson_generator, [{"rate": s.rate}])

    #breaking free
    global nengo_toNest_nodes
    nengo_toNest_nodes = {}
    global nest_toNengo_nodes
    nest_toNengo_nodes = {}

    #create nodes
    for node_name in network.nodes:
        if isinstance(network.nodes[node_name], nef.Neuron):
            temp_neuron = nest.Create(s.neuron_model)
            nest.SetStatus(temp_neuron, [{"V_peak": s.Vcut, "a": s.a, "b": s.b, "V_reset": s.Vr, "tau_w": s.tau_w,
                                          "Delta_T": s.DeltaT, "V_th": s.Vth, "E_L": s.EL, "g_L": s.gL, "C_m": s.C_m,
                                          "t_ref": s.t_ref}])
            nest_toNengo_nodes[temp_neuron[0]] = network.nodes[node_name]
            network.nodes[node_name].ID = temp_neuron[0]
            nengo_toNest_nodes[node_name] = temp_neuron
        elif isinstance(network.nodes[node_name], nef.Input):
            temp_input = nest.Create("parrot_neuron")
            nest.Connect(poisson_generator, temp_input)
            nest_toNengo_nodes[temp_input[0]] = network.nodes[node_name]
            network.nodes[node_name].ID = temp_input[0]
            nengo_toNest_nodes[node_name] = temp_input

    #now neurons are nest-neurons
    input_nodes = nengo_toNest_nodes.copy()

    for connection in network.connections:
        nodeA = nengo_toNest_nodes[connection.nodeA.name]
        nodeB = nengo_toNest_nodes[connection.nodeB.name]
        input_nodes.pop(connection.nodeB.name, None)  # not a free neuron anymore
        if connection.excitatory:
            nest.Connect(nodeA, nodeB, params={"weight": s.J, "delay": connection.delay})
        else:
            nest.Connect(nodeA, nodeB, params={"weight": -s.J, "delay": connection.delay})

    #add some noise and detectors
    noise_current = nest.Create('noise_generator')
    nest.SetStatus(noise_current, [{"std": s.noise_current_std_dev, "dt": s.dt, "mean": 0.0}])

    global spikeDetector
    spikeDetector = nest.Create("spike_detector")
    nest.SetStatus(spikeDetector,
                   [{"label": "S", "to_file": tofile, "to_memory": False, "withgid": True, "precise_times": True}])
    spike_vp = nest.GetStatus(spikeDetector, "vp")[0]
    spike_gid = nest.GetStatus(spikeDetector, "global_id")[0]

    for node_name in nengo_toNest_nodes:
        if isinstance(nest_toNengo_nodes[nengo_toNest_nodes[node_name][0]], nef.Neuron):
            nest.Connect(noise_current, nengo_toNest_nodes[node_name])
        nest.Connect(nengo_toNest_nodes[node_name], spikeDetector)

    global voltmeter
    voltmeter = nest.Create("voltmeter")
    nest.SetStatus(voltmeter, [
        {"label": "V", "to_file": tofile, "to_screen": False, "to_memory": False, "withtime": False, "interval": s.dt,
         "start": 0.0, "stop": float('Inf'), "withgid": True}])
    volt_vp = nest.GetStatus(voltmeter, "vp")[0]
    volt_gid = nest.GetStatus(voltmeter, "global_id")[0]

    global watched

    if voltage_watch is None:
        watched = random.choice(nengo_toNest_nodes.keys())
    else:
        watched = voltage_watch

    for node_watched in watched:
        nest.Connect(voltmeter, nengo_toNest_nodes[node_watched])

    return [spike_gid, spike_vp, volt_gid, volt_vp]


def simulate(duration):
    print "Starting simulation"
    simulation_time = duration
    time_sim = time.time()
    nest.Simulate(duration)
    print "Simulation took " + str(time.time() - time_sim) + " seconds"