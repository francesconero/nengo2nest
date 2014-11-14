nengo2nest
==========
Tool to simulate with Nest a network exported from Nengo

Requirements
==========
This tool requires Nest to be already installed in the system.

Install it from http://www.nest-initiative.org/Software:Download

Installation
==========
You can install the package directly from github by running pip:

    pip install https://github.com/francesconero/nengo2nest/zipball/master

Usage
==========
See run_neocortical.py under the Examples folder for a basic usage of the package

Input
==========
A python script exported from the Nengo builder. Set a **positive radius** for neurons which you want to be **excitatory**, and a
**negative radius** for neurons which you want to be **inhibitory** (1.0 and -1.0 respectively for example).

Output
==========
You will get 5 files after a successful simulation:

- **\*.nod** contains info about nodes
- **\*.con** contains info about connections between nodes
- **\*.gdf** contains the spiking timings of the neurons and inputs
- **\*.dat** contains the voltage traces of the neurons
- **\*.set** contains info about the simulation settings (only resolution and simulation time for now)

Mind the fact that the *.gdf and *.dat file reference the nodes by ID, and not by their original Nengo name, so you
need to lookup these IDs in the *.nod file to get the original names.
