'''
Created on May 27, 2014

@author: Francesco Nero
'''
import random
import csv
import os

from . import settings
from . import nef
from . import utils


def from_nengo(filename):
    f = open(filename, "r")
    lines = f.readlines()
    f.close()

    lines = [line for line in lines if not line.startswith("from")]
    lines = "\n".join(lines)
    exec lines

    return nef.network


def random_network(number_of_neurons, probability_of_outgoing_connection=0.2,
                   excitatory_neurons_ratio=0.8, min_connection_delay=1, max_connection_delay=1):
    net_random = nef.Network('RandomNetwork')
    
    for i in range(1, number_of_neurons+1):
        neuron_name = utils.name_from_number(i)
        excitatory = 1 if random.random() < excitatory_neurons_ratio else -1
        net_random.make(neuron_name, radius=excitatory)
    
    for neuronA, neuronB in [(neuronA, neuronB) for neuronA in net_random.nodes for neuronB in net_random.nodes]:
        if neuronA != neuronB and random.random() < probability_of_outgoing_connection:
            net_random.connect(neuronA, neuronB, delay=random.uniform(min_connection_delay, max_connection_delay))
            
    no_input_neurons = dict(net_random.nodes)
    inputs = []
    
    for connection in net_random.connections:
        if connection.excitatory:
            no_input_neurons.pop(connection.nodeB.name, None)
    
    for idx, neuron in enumerate(no_input_neurons):
        input_name = 'Input'+str(idx+1)
        net_random.make_input(input_name)
        net_random.connect(input_name, neuron, delay=random.uniform(min_connection_delay, max_connection_delay))
        inputs = inputs+[input_name]
    
    if len(inputs) < 1:
        candidate = random.choice([x for x in net_random.get_neurons() if net_random.nodes[x].excitatory])
        net_random.make_input('Input')
        net_random.connect('Input', candidate, delay=random.uniform(min_connection_delay, max_connection_delay))

    return net_random


def nodes_to_file(network, filename):
    with open(settings.data_path+os.sep+filename+".nod", 'wb') as csvfile:
            csvwriter = csv.writer(csvfile, dialect='excel-tab')
            csvwriter.writerow(["name", "ID", "is.input", "type"])
            for node_name in network.nodes:
                node = network.nodes[node_name]
                name = node.name
                ID = node.ID
                is_input_type = isinstance(node, nef.Input)
                type_of_action = "E" if node.excitatory else "I"
                csvwriter.writerow([name, ID, is_input_type, type_of_action])


def connections_to_file(network, filename):
    with open(settings.data_path+os.sep+filename+".con", 'wb') as csvfile:
            csvwriter = csv.writer(csvfile, dialect='excel-tab')
            csvwriter.writerow(["node.A", "node.B", "delay"])
            for connection in network.connections:
                node_A = connection.nodeA.name 
                node_B = connection.nodeB.name
                delay = connection.delay
                csvwriter.writerow([node_A, node_B, delay])


