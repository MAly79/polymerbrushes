This folder contains code written as part of my PhD at Imperial College London
on the Tribology of Polymer Brushes by Molecular Dynamics using LAMMPS.

[UNDER DEVELOPMENT]

Contents:

1- main.in: This is the primary script to interface with the simulation.
            - Setting Simulation Variables: Brush Topology, Compressive Pressure
            Shearing Velocity, Temperature, timestep and Number of timesteps to
            run each stage of the simulation.
            - It calls other scripts: MDPBB.in, ecs.in, post.py
            - It can perform a series of simulations on the same generated brush
            at different velocities and output the data to separate folders named
            "V=*"
            - Control which files to be saved in each run
2- MDPBB.in: This is a LAMMPS input script that creates the Polymer Brush Bilayer.
            - Two opposing polymer brushes are produced into a restart file MDPBB.rst
            - This script calls BSMolf.py to produce bsmol.txt which is the molecule file
            - The Chains are grafted randomly to two opposing FCC Walls
            - Here we Set the pair_style and create the bonds.

3- ecs.in: This is a LAMMPS script that performs the simulation (Equilibration, Compression and Shearing).
           - It starts by reading the MDPBB.rst file
           - Define the bond_style and bond_coeff for the FENE and harmonic potentials
           - Control the outputs with the thermo command
           - Output:
                    - log.lammps: the main log file from LAMMPS which also contains the thermo output
                    - full_**.dump: Dump files containing all the beads and wall atoms (**=eq,cp,sh)
                    - beads_**.dump: Dump files that contain only the beads (**=eq,cp,sh) (for eq only the bottom beads)
                    - *beads_*dz : Bead density profiles in the z direction (*=a,b,t ,*=e,c,s)
                    - *p_sz : Temp and velocity profiles in the z direction (*=tem, vel)
                    - ecs.rst: a restart file at the end of the run

4- post.py: This is a python script that extracts the data from LAMMPS output files to csv files.
            - Output:
                     - *.csv: Contains the thermo data for the different stages (*=equil,comp,shear) [Source: log.lammps]
                     - *bdp*.csv: Bead density profiles (*=a,b,t , *=e,c,s) [Source: *beads_*dz]
                     - *ps.csv: Temperature and velocity profiles  (*=tem, vel) [Source: *p_sz]

5- BSMolf.py: A python script that is called by MDPBB.in to write the molecule file.

6- *JS.pbs: job scripts for running on the Cx1 cluster in Serial, MPI and Debug modes.



REQUIRED LAMMPS PACKAGES: PYTHON


Author: Mohamed A. Abdelbar
PhD Student at Imperial College London in the Materials Department
email: maa4617@ic.ac.uk
