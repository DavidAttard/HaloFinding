# The following program takes is run via: "python gen_rockstar_inputs.py <num>" where <num> should be replaced by the number of snapshots.
# The code will in turn generate a folder called rockstar where it will contain several folders numbered 000 up to <num> where in each
# folder you find that snapshots config file for rockstar.

# NOTE: Depending on the simulation make sure to change the Force Resolution

import os
import sys

def write_cfg(path, ioutput):
    '''
    Internal function to write an appropriate AHF input file
    '''

    full_path = "{0}/rockstar/{1:03d}/".format(path, ioutput)
    if os.path.isdir(full_path) is False:
        if os.path.isdir("{0}/rockstar/".format(path)) is False:
            os.mkdir("{0}/rockstar/".format(path))
        os.mkdir(full_path)


    with open("{0}/parallel.cfg".format(full_path), "w") as f:

        f.write("FILE_FORMAT = \"GADGET2\" \n")
      
        GADGET_LENGTH_CONVERSION = 1e+00
        GADGET_MASS_CONVERSION = 1e10
        FORCE_RES=0.0005

        NUM_BLOCKS = 8  # <number of files per snapshot>
        NUM_SNAPS=1

        FILENAME = "snapdir_<snap>/snapshot_<snap>.<block>"
        PRELOAD_PARTICLES = 0

        PARALLEL_IO = 1

        NUM_WRITERS = 384 #<number of CPUs>
        FORK_READERS_FROM_WRITERS = 1
        FORK_PROCESSORS_PER_MACHINE = 48

        f.write("GADGET_LENGTH_CONVERSION       = {0:.0e}\n".format(GADGET_LENGTH_CONVERSION))
        f.write("GADGET_MASS_CONVERSION       = {0:.0e}\n".format(GADGET_MASS_CONVERSION))

        f.write("INBASE = \"/p/scratch/hestiaeor/runs/LG_09_18/AREPO/DMO_256_4096\" \n")
        f.write("OUTBASE = \"{0}/rockstar/{1:03d}\" \n".format(path, ioutput))
        f.write("FORCE_RES       = {0}\n".format(FORCE_RES))

        # f.write("STARTING_SNAP       = {0:3d}\n".format(ioutput))
        f.write("NUM_BLOCKS       = {0:d}\n".format(NUM_BLOCKS))
        # f.write("NUM_SNAPS       = {0:d}\n".format(NUM_SNAPS))
        
        f.write("FILENAME       = \"snapdir_{0:03d}/snapshot_{0:03d}.<block>\" \n".format(ioutput))
        f.write("PRELOAD_PARTICLES       = {0:d}\n".format(PRELOAD_PARTICLES))
        
        f.write("PARALLEL_IO       = {0:d}\n".format(PARALLEL_IO))
        f.write("NUM_WRITERS       = {0:d}\n".format(NUM_WRITERS))
        f.write("FORK_READERS_FROM_WRITERS       = {0:d}\n".format(FORK_READERS_FROM_WRITERS))
        f.write("FORK_PROCESSORS_PER_MACHINE       = {0:d}\n".format(FORK_PROCESSORS_PER_MACHINE))



def run_write_cfg():
    path = os.getcwd()
    input_number = int(sys.argv[1])

    for ioutput in range(input_number + 1):
        write_cfg(path, ioutput)

run_write_cfg()
