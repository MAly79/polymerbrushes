#!/usr/bin/python
#$: chmod 755 yourfile.py
#$: dos2unix yourfile.py
#$: ./yourfile.py
# This is a python script that will generate a LAMMPS molecule file for use in
# Polymer Brush

def BSMolf(n_m):
    # Number of atoms to create along the main chain
    #n_m = 10
    # Number of atoms on the side chains
    n_s = 0

    # Number of atom types
    Ntype = 1


    # Write LAMMPS data file
    with open('bsmol.txt','w') as fdata:
        # First line is a description
        fdata.write('Bead-Spring Polymer molecule\n\n')

        #--- Header ---#
        #Specify number of atoms and atom types
        fdata.write('{} atoms\n' .format(n_m + n_s))
        #Specify the number of bonds
        fdata.write('{} bonds\n' .format(n_m - 1))

        #--- Body ---#

        # Coords assignment
        fdata.write('Coords\n\n')
        # Write the line format for the Coords:
        # atom-ID x y z
        for i in range(n_m):
            fdata.write('{} {} {} {}\n' .format(i+1,0,0,i))


        # Type assignment
        fdata.write('Types\n\n')
        fdata.write('{} {}\n' .format(1,1))
        for i in range(n_m-2):
            fdata.write('{} {}\n' .format(i+2,2))
        fdata.write('{} {}\n' .format(n_m,3))


        # Bonds section
        fdata.write('Bonds\n\n')
        # Write the line format for the bonds:
        # bond-ID type atom1 atom2
        for i in range(n_m-1):
            fdata.write('{} 1 {} {}\n' .format(i+1,i+1,i+2))

        # Special Bond Counts assignment
        fdata.write('Special Bond Counts\n\n')
        # Write the line format for the Coords:
        # ID N1 N2 N3
        fdata.write('{} {} {} {}\n' .format(1,1,0,0))
        for i in range(n_m-2):
            fdata.write('{} {} {} {}\n' .format(i+2,2,0,0))
        fdata.write('{} {} {} {}\n' .format(n_m,1,0,0))

        # Special Bonds assignment
        fdata.write('Special Bonds\n\n')
        # Write the line format for the Coords:
        # ID a b c d
        fdata.write('{} {}\n' .format(1,2))
        for i in range(n_m-2):
            fdata.write('{} {} {}\n' .format(i+2,i+1,i+3))
        fdata.write('{} {}\n' .format(n_m,n_m-1))
        return None

if __name__ == '__main__':
    print('BSMolf used')
