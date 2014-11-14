'''
Created on May 27, 2014

@author: Francesco Nero
'''
from . import settings

network = None


class Network():
    def __init__(self, name):
        global network
        print "Creating network: "+name
        self.name = name
        self.nodes = {}
        self.connections = []
        network = self 
    
    def make(self, neuron_name, useless=None, also_useless=None, tau_rc=None, tau_ref=None, max_rate=None,
             intercept=None, radius=1.0):
        ex = radius > 0
        #print "Creating neuron: "+neuron_name+" | Excitatory: "+str(ex)
        self.nodes[neuron_name] = (Neuron(neuron_name, ex))

    def make_input(self, input_name, values=None):
        #print "Creating input: "+input_name
        self.nodes[input_name] = (Input(input_name))

    #TODO manage delay better
    def connect(self, nodeA, nodeB, transform=None, delay=None):
        delay = settings.default_connection_delay()
        #print "Connecting "+nodeA+" "+nodeB+"\tdelay="+str(delay)
        self.connections.append(Connection(self.nodes[nodeA], self.nodes[nodeB], delay=delay))
    
    def add_to_nengo(self):
        print "Finished creating network"
    
    def get_neurons(self):
        return [x for x in self.nodes if isinstance(network.nodes[x], Neuron)]
    
    def get_inputs(self):
        return [x for x in self.nodes if isinstance(network.nodes[x], Input)]

    def get_connections(self):
        return [x.nodeA.name+"\t"+x.nodeB.name+"\t"+("ECC" if x.excitatory else "INI")+"\tdelay:"+str(x.delay)
                for x in self.connections]


class Node():
    def __init__(self, name, excitatory=True):
        self.name = name
        self.excitatory = excitatory
        self.ID = None
        

class Neuron(Node):
    pass


class Input(Node):
    pass


class Connection():
    def __init__(self, nodeA, nodeB, delay):
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.excitatory = nodeA.excitatory
        self.delay = delay


class ConstantFunction():
    def __init__(self, number_of_outputs, value):
        self.number_of_outputs = number_of_outputs
        self.value = value