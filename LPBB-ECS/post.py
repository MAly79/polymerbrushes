# This is a python script that reads LAMMPS output files for LPBB-ECS
# And then writes them to .csv files
import numpy as np
import pandas as pd
import os


def find_lines(filename):
    with open(filename,'r') as f:

        start = []
        for n, line in enumerate(f):
            if ('Step TotEng' in line[:11]):
                start.append(n)
    return start

def find_Ns(filename):
    N_data = np.genfromtxt(filename, dtype=int, skip_header=12, max_rows=5)
    Nequil = N_data[0,3]
    Npre = N_data[1,3]
    Ncomp = N_data[2,3]
    Nshear = N_data[3,3]
    Nthermo = N_data[4,3]
    return Nequil,Npre,Ncomp,Nshear,Nthermo

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f, 1):
            pass
    return i

def read_chunk(filename):
    with open(filename,'r') as f:
        c_info = np.genfromtxt(filename,comments='#', dtype=float, max_rows=1)
        Nchunks = int(c_info[1])
        lines = file_len(filename)
        for i, line in enumerate(f):
            if i == 0:
                data =  np.genfromtxt(filename, dtype=float, comments='#', usecols= (1,3), skip_header=(4+(i+(i/Nchunks))) ,max_rows=Nchunks)
            elif (i % Nchunks == 0 and i < (lines-Nchunks-1)  and i > 0):
                get = np.genfromtxt(filename, dtype=float, comments='#', usecols= (3), skip_header=(4+(i+(i/Nchunks))) ,max_rows=Nchunks)
                data = np.column_stack((data, get))
    return data

def read_mop(filename):
    data= np.genfromtxt(filename, comments='#', usecols=(1,2,3,4), dtype=float, skip_header=4)
    return data


if __name__ == '__main__':
    Nequil,Npre, Ncomp, Nshear, Nthermo = find_Ns('main.in')
    #print(Ncomp)
    #print(Nshear)
    #print(Nthermo)
    starts = find_lines('log.lammps')
    #print(starts)
    # Read in the equilibrium thermo data from log file
    equil_data = np.genfromtxt('log.lammps',comments=None, dtype=float, skip_header=(starts[0]+2), max_rows=(int(Nequil/Nthermo)+1))
    equil_df = pd.DataFrame(equil_data)
    equil_df.to_csv('equil.csv')

    #comp_data = read_thermo('log.lammps', starts[1], Ncomp, Nthermo)
    comp_data = np.genfromtxt('log.lammps',comments=None, dtype=float, skip_header=(starts[2]+1), max_rows=(int(Ncomp/Nthermo)+1))
    comp_df = pd.DataFrame(comp_data)
    comp_df.to_csv('comp.csv')

    #comp_data = read_thermo('log.lammps', starts[1], Ncomp, Nthermo)
    shear_data = np.genfromtxt('log.lammps',comments=None, dtype=float, skip_header=(starts[3]+1), max_rows=(int(Nshear/Nthermo)+1))
    shear_df = pd.DataFrame(shear_data)
    shear_df.to_csv('shear.csv')

    # Read in the number density profile of bottom beads
    bbdens_data = read_chunk('bbeads_edz')
    bbdens_df = pd.DataFrame(bbdens_data)
    bbdens_df.to_csv('bbdpe.csv')
    # Read in the number density profile for the top beads
    tbdens_data = read_chunk('tbeads_edz')
    tbdens_df = pd.DataFrame(tbdens_data)
    tbdens_df.to_csv('tbdpe.csv')
    # Read in the number density of all the beads combined
    abdens_data = read_chunk('abeads_edz')
    abdens_df = pd.DataFrame(abdens_data)
    abdens_df.to_csv('abdpe.csv')
    # Read in the number density profile of bottom beads
    bbdens_data = read_chunk('bbeads_cdz')
    bbdens_df = pd.DataFrame(bbdens_data)
    bbdens_df.to_csv('bbdpc.csv')
    # Read in the number density profile for the top beads
    tbdens_data = read_chunk('tbeads_cdz')
    tbdens_df = pd.DataFrame(tbdens_data)
    tbdens_df.to_csv('tbdpc.csv')
    # Read in the number density of all the beads combined
    abdens_data = read_chunk('abeads_cdz')
    abdens_df = pd.DataFrame(abdens_data)
    abdens_df.to_csv('abdpc.csv')
    # Read in the number density profile of bottom beads
    bbdens_data = read_chunk('bbeads_sdz')
    bbdens_df = pd.DataFrame(bbdens_data)
    bbdens_df.to_csv('bbdps.csv')
    # Read in the number density profile for the top beads
    tbdens_data = read_chunk('tbeads_sdz')
    tbdens_df = pd.DataFrame(tbdens_data)
    tbdens_df.to_csv('tbdps.csv')
    # Read in the number density of all the beads combined
    abdens_data = read_chunk('abeads_sdz')
    abdens_df = pd.DataFrame(abdens_data)
    abdens_df.to_csv('abdps.csv')
    
    #Read in the velocity profile for shear
    velp_data = read_chunk('velp_sz')
    velp_df = pd.DataFrame(velp_data)
    velp_df.to_csv('velps.csv')

    #Read in the velocity profile for shear
    temp_data = read_chunk('temp_sz')
    temp_df = pd.DataFrame(temp_data)
    temp_df.to_csv('temps.csv')
