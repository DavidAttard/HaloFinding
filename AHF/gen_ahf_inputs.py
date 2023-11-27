import os
import sys

# A Python Program which generates that takes in an input number (e.g. 4) and generates
# the appropriate input files for snapshots 0 up to the input number in a folder called AHF.
# Run using "pyton gen_ahf_inputs.py 4" replace 4 with the appropriate number 

def write_cfg(path, ioutput):
    '''
    Internal function to write an appropriate AHF input file
    '''

    full_path = "{0}/AHF/{1:03d}/".format(path, ioutput)
    if os.path.isdir(full_path) is False:
        if os.path.isdir("{0}/AHF/".format(path)) is False:
            os.mkdir("{0}/AHF/".format(path))
        os.mkdir(full_path)

    # Make the halos/ dir
    os.mkdir(os.path.join(full_path, 'halos'))

    with open("{0}/ahf.input".format(full_path), "w") as f:
        f.write("[AHF]\n")
        f.write("ic_filename       = {0}/snap_{1:03d}/ramses2gadget_{1:03d}.\n".format(path, ioutput))
        f.write("ic_filetype       = 61\n")  # GADGET
        f.write("outfile_prefix    = {0}/AHF/{1:03d}/halos/ahf_\n".format(path, ioutput))

        LgridDomain = 64
        LgridMax = 16777216
        NperDomCell = 5.0
        NperRefCell = 5.0
        VescTune = 1.5
        NminPerHalo = 20
        RhoVir = 0
        Dvir = 200
        MaxGatherRad = 3.0
        LevelDomainDecomp = 3
        NcpuReading = 1

        GADGET_LUNIT = 1e-3
        GADGET_MUNIT = 1e10

        f.write("LgridDomain       = {0:d}\n".format(LgridDomain))
        f.write("LgridMax       = {0:d}\n".format(LgridMax))
        f.write("NperDomCell       = {0:.1f}\n".format(NperDomCell))
        f.write("NperRefCell       = {0:.1f}\n".format(NperRefCell))
        f.write("VescTune       = {0:.1f}\n".format(VescTune))
        f.write("NminPerHalo       = {0:d}\n".format(NminPerHalo))
        f.write("RhoVir       = {0:.1f}\n".format(RhoVir))
        f.write("Dvir       = {0:.1f}\n".format(Dvir))
        f.write("MaxGatherRad       = {0:.1f}\n".format(MaxGatherRad))
        f.write("LevelDomainDecomp       = {0:d}\n".format(LevelDomainDecomp))
        f.write("NcpuReading       = {0:d}\n".format(NcpuReading))

        f.write("[GADGET]\n")
        f.write("GADGET_LUNIT       = {0:.0e}\n".format(GADGET_LUNIT))
        f.write("GADGET_MUNIT       = {0:.0e}\n".format(GADGET_MUNIT))

def run_write_cfg():
    path = os.getcwd()
    input_number = int(sys.argv[1])

    for ioutput in range(input_number + 1):
        write_cfg(path, ioutput)

run_write_cfg()
