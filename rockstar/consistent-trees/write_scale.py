# Program to generate the scales.txt file to be used in consistent-trees
# Important to be cautious since the following program was written such that snap51 in AHF corresponds to snap 50 in rockstar format!!! (Thisis because in my case the snaps go from 51 till 1 not 0)
# If the files in AHF go from 51 to 0 then remove the -1 in f.write(fmt_str.format(snap_number-1, a))

# write_scales.py
import re
import glob
import os
fmt_str = '{0:3d} {1:6.8f}\n'
base_directory_1 = '/p/scratch/hestiaeor/david/AHF_RT_256_4096_CRAL_MF_PAD_LMAX17/'

start_snap = 51
end_snap = 1
with open('scales.txt', 'w') as f:
    for snap_number in range(end_snap, start_snap+1):

        file_suffix = "_halos"

        directory_path_1 = "{}{:03d}/halos/".format(base_directory_1, snap_number)
        # Check if the directory exists
        if os.path.exists(directory_path_1):
            # List files in the directory ending with "_halos"
            matching_files = [f for f in os.listdir(directory_path_1) if f.endswith(file_suffix)]
            
            # Print the full paths of matching files
            for matching_file in matching_files:
                file_path_1 = os.path.join(directory_path_1, matching_file)

            # Code to extract redshift from the input file name 
            pattern = re.compile(r'z(\d+\.\d+)')
            match = re.search(pattern, file_path_1)
            if match:
                z_redshift = match.group(1)
                a = 1. / (1. + float(z_redshift))
                print(snap_number-1, a)
                f.write(fmt_str.format(snap_number-1, a))
