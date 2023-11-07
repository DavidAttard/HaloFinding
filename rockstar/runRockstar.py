# run the following code using the command: mpirun -n 4 python ~/runRockstar.py

import sys, os, time
from subprocess import call
from mpi4py import MPI


MPIcomm = MPI.COMM_WORLD
pId = MPIcomm.Get_rank()
nProc = MPIcomm.Get_size()
currentDirectory = os.getcwd()

# path to location where snapshots/folder of snapshots are saved 
INBASE="/mnt/lustre/users/astro/da500/06p25Mpc_128_dg"
# location where the ouput files will be stored
OUTBASE = "/mnt/lustre/users/astro/da500/sim_analyses/halo_finding/rockstar_halos"

# path to the rockstar executable 
rockstarComand ='/mnt/lustre/users/astro/da500/rockstar-ramses/rockstar'

rockstarConf = {
'FILE_FORMAT': '"GADGET2"',
'GADGET_LENGTH_CONVERSION' :1e-3,  #convert from kpc to Mpc 
'GADGET_MASS_CONVERSION': 1e+10,
'FORCE_RES': 0.001,                 #Mpc/h
'OUTBASE': OUTBASE,
}

parallelConf = {
'PARALLEL_IO': 1,
'INBASE':  INBASE ,               #"/directory/where/files/are/located"
'NUM_BLOCKS': 96,                              # <number of files per snapshot>
'NUM_SNAPS': 45,                               # <total number of snapshots>
'STARTING_SNAP': 37,
'FILENAME': '"/snap_<snap>/ramses2gadget_<snap>.<block>"',              #"my_sim.<snap>.<block>"
'NUM_WRITERS': 1,                             #<number of CPUs> in multiples of 8
'FORK_READERS_FROM_WRITERS': 1,
'FORK_PROCESSORS_PER_MACHINE': 1,             #<number of processors per node>
}


if pId == 0:
  if not os.path.exists( rockstarConf['OUTBASE']): os.makedirs(rockstarConf['OUTBASE'])
  rockstarconfigFile = rockstarConf['OUTBASE'] + '/rockstar_param.cfg'
  rckFile = open( rockstarconfigFile, "w" )
  for key in list(rockstarConf.keys()):
    rckFile.write( key + " = " + str(rockstarConf[key]) + "\n" )
  for key in list(parallelConf.keys()):
    rckFile.write( key + " = " + str(parallelConf[key]) + "\n" )
  rckFile.close()
  #Run ROCKSTAR finder
  print("\nFinding halos...")
  print(" Parallel configuration")
  print("Output: ", rockstarConf['OUTBASE'] + '\n')


MPIcomm.Barrier()

if pId == 0: call([rockstarComand, "-c", rockstarconfigFile ])
if pId == 1:
  time.sleep(5)
  call([rockstarComand, "-c", rockstarConf['OUTBASE'] + '/auto-rockstar.cfg' ])
