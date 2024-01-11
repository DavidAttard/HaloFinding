# A python program used to create a directory called Trees containing N folders where each folder will have a file 
# mergerTree_code.sh which is used to run and generate the merger tree.

# To run the the python program use: python gen_MergerTree_files.py N
# Note Replace N by the number of snaps
# Replace all the direcotry paths 

import os
import sys

def write_cfg(path, ioutput):
    '''
    Internal function to write an appropriate AHF input file
    '''

    full_path = "{0}/Trees/{1:03d}/".format(path, ioutput)
    if os.path.isdir(full_path) is False:
        if os.path.isdir("{0}/Trees/".format(path)) is False:
            os.mkdir("{0}/Trees/".format(path))
        os.mkdir(full_path)


    with open("{0}/mergerTree_code.sh".format(full_path), "w") as f:
        f.write("#!/bin/bash\n")
        
        f.write("MERGERTREE_PROGRAM=\"/p/project/hestiaeor/david/ahf-v1.0-114/bin/MergerTree\"\n")
        
        f.write("DIRECTORY1=\"/p/project/hestiaeor/david/hestiaeor/AHF_4096/{0:03d}/halos/\"\n".format(ioutput))
        f.write("DIRECTORY2=\"/p/project/hestiaeor/david/hestiaeor/AHF_4096/{0:03d}/halos/\"\n".format(ioutput-1))
        
        f.write("SUFFIX=\"_particles\"\n")
        f.write("PREFIX=\"test\"\n")
        
        f.write("FILE1=$(find \"$DIRECTORY1\" -type f -name \"*$SUFFIX\" -print -quit)\n")
        f.write("FILE2=$(find \"$DIRECTORY2\" -type f -name \"*$SUFFIX\" -print -quit)\n")
        
        f.write("$MERGERTREE_PROGRAM <<EOF\n")
        f.write("2\n")
        f.write("$FILE1\n")
        f.write("$FILE2\n")
        f.write("$PREFIX\n")
        f.write("EOF\n")



def run_write_cfg():
    path = os.getcwd()
    input_number = int(sys.argv[1])

    for ioutput in range(input_number + 1):
        write_cfg(path, ioutput)

run_write_cfg()
