#!/usr/bin/python
#$: chmod 755 yourfile.py
#$: dos2unix yourfile.py
#$: ./yourfile.py
# This is a python script that will generate a LAMMPS molecule file for use in
# Polymer Brush


def BSMolf(N,N_s,G):
    # N is the Number of atoms to create along the main chain
    # N_s is the Number of atoms per side chain
    # G is the gap between side chains (0=no gaps, 1=alternating)
    # The sequence of side chains starts with the gap
    import math
    M_s = int(math.floor(N/(G+1)))
    print(M_s)

    if N_s == 0:

        # Write LAMMPS data file
        with open('bsmol.txt','w') as fdata:
            # First line is a description
            fdata.write('Bead-Spring Polymer molecule\n\n')

            #--- Header ---#
            #Specify number of atoms and atom types
            fdata.write('{} atoms\n' .format(N))
            #Specify the number of bonds
            fdata.write('{} bonds\n' .format(N - 1))

            #--- Body ---#

            # Coords assignment
            fdata.write('Coords\n\n')
            # Write the line format for the Coords:
            # atom-ID x y z
            for i in range(N):
                fdata.write('{} {} {} {}\n' .format(i+1,0,0,i))


            # Type assignment
            fdata.write('Types\n\n')
            fdata.write('{} {}\n' .format(1,1))
            for i in range(N-2):
                fdata.write('{} {}\n' .format(i+2,2))
            fdata.write('{} {}\n' .format(N,3))


            # Bonds section
            fdata.write('Bonds\n\n')
            # Write the line format for the bonds:
            # bond-ID type atom1 atom2
            for i in range(N-1):
                fdata.write('{} 1 {} {}\n' .format(i+1,i+1,i+2))

            # Special Bond Counts assignment
            fdata.write('Special Bond Counts\n\n')
            # Write the line format for the Coords:
            # ID N1 N2 N3
            fdata.write('{} {} {} {}\n' .format(1,1,0,0))
            for i in range(N-2):
                fdata.write('{} {} {} {}\n' .format(i+2,2,0,0))
            fdata.write('{} {} {} {}\n' .format(N,1,0,0))

            # Special Bonds assignment
            fdata.write('Special Bonds\n\n')
            # Write the line format for the Coords:
            # ID a b c d
            fdata.write('{} {}\n' .format(1,2))
            for i in range(N-2):
                fdata.write('{} {} {}\n' .format(i+2,i+1,i+3))
            fdata.write('{} {}\n' .format(N,N-1))
            return None

    else:
        # Write LAMMPS data file
        with open('bsmol.txt','w') as fdata:
            # First line is a description
            fdata.write('Bead-Spring Polymer molecule\n\n')

            #--- Header ---#
            #Specify number of atoms and atom types
            fdata.write('{} atoms\n' .format(int(N + (M_s * N_s))))
            #Specify the number of bonds
            fdata.write('{} bonds\n' .format(int((N - 1) + (M_s * N_s))))

            #--- Body ---#

            # Coords assignment
            # Write the line format for the Coords:
            # atom-ID x y z

            fdata.write('Coords\n\n')
            # Backbone Atoms
            for i in range(N):
                fdata.write('{} {} {} {}\n' .format(i+1,0,0,i))

            # Sidechain Atoms
            z_s = G
            for i in range(N,int(N + (M_s * N_s)),N_s):

                for j in range(N_s):
                    fdata.write('{} {} {} {}\n' .format(i+j+1,j+1,0,z_s))
                z_s = z_s + (G+1)

            # Type assignment
            # atom-ID type
            fdata.write('Types\n\n')

            # Backbone Atoms
            fdata.write('{} {}\n' .format(1,1))
            for i in range(N-2):
                fdata.write('{} {}\n' .format(i+2,2))
            fdata.write('{} {}\n' .format(N,3))

            # Sidechain Atoms
            for i in range(N,int(N + (M_s * N_s))):
                fdata.write('{} {}\n' .format(i+1,2))

            # Bonds section
            fdata.write('Bonds\n\n')
            # Write the line format for the bonds:
            # bond-ID type atom1 atom2
            # Backbone Bonds
            for i in range(N-1):
                fdata.write('{} 1 {} {}\n' .format(i+1,i+1,i+2))
            # Sidechain Bonds
            a_s = G+1
            tribonds = []
            for i in range(N-1,int((N-1) + (M_s * N_s)),N_s):
                for j in range(N_s):
                    if j==0:
                        fdata.write('{} 1 {} {}\n' .format(i+j+1,a_s,i+j+2))
                    else:
                        fdata.write('{} 1 {} {}\n' .format(i+j+1,i+j+1,i+j+2))
                tribonds.append(a_s)
                a_s = a_s + (G+1)
                
            print(tribonds)
            # Special Bond Counts assignment
            fdata.write('Special Bond Counts\n\n')
            # Create an array of special bond values for all the atoms
            A = [2] * N
            A[0] = 1
            A[-1] = 1
            B = [0] * N
            for i in range(1,N+1):
                if i%(G+1) == 0:
                    B[i-1] = 1
            BB = [x + y for x, y in zip(A,B)]
            S = [2] * N_s
            S[-1] = 1
            BBS = BB
            for i in range(M_s):
                BBS.extend(S)


            # Write the line format for the Special Bonds:
            # ID N1 N2 N3
            for i in range(int(N + (M_s * N_s))):
                fdata.write('{} {} 0 0\n' .format(i+1,BBS[i]))

            # Create an array of all the atom ids of the first side chain atoms
            SCatom = range(N+1,int(N + (M_s * N_s))+1,N_s)
            print(SCatom)

            # Special Bonds assignment
            fdata.write('Special Bonds\n\n')
            # Write the line format for the Coords:
            # ID a b c d
            j=0
            k=0
            if BBS[0]==1:
                fdata.write('{} {}\n' .format(1,2))
            elif BBS[0]==2:
                fdata.write('{} {} {}\n' .format(1,2,N+1))
            for i in range(1,int(N + (M_s * N_s))):
                if BBS[i] == 1:
                    fdata.write('{} {}\n' .format(i+1,i))
                elif BBS[i] == 2:
                    if i+1 in SCatom: # if they are the start of the side chains
                        fdata.write('{} {} {}\n' .format(i+1,tribonds[j],i+2))
                        j = j + 1
                    else:
                        fdata.write('{} {} {}\n' .format(i+1,i,i+2))
                elif BBS[i] == 3: #3 bonds
                    fdata.write('{} {} {} {}\n' .format(i+1,i,i+2,SCatom[k]))

            return None

if __name__ == '__main__':
    print('BSMolf used')