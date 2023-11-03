#!/bin/bash

# Specify the directory where the snapshots are stored 
search_directory="/mnt/lustre/users/astro/da500/06p25Mpc_128_dg"

# Use 'find' to locate all folders starting with "snap_"
# Then, extract the numbers following the underscore and print them
find "$search_directory" -type d -name 'snap_*' | while read -r folder; do
    # Extract the number using 'sed' and regular expressions
    number=$(echo "$folder" | sed -n 's/.*snap_\([0-9]*\).*/\1/p')
    
    # Check if a number was found and print it
    if [ -n "$number" ]; then
        echo "Folder: $folder, Number: $number"
        
        # Path to the AHF input file 
        ahf_input_file="/mnt/lustre/users/astro/da500/ahf-v1.0-114/AHF.input"
        
        # command to change the ic_filename variable in the input file 
        sed -i "s|ic_filename = .*$|ic_filename = $folder/ramses2gadget_$number.|" "$ahf_input_file"
        
        # Define the command to run (change directory of the AHF executable and the AHF input file)
        ahf_command="/mnt/lustre/users/astro/da500/ahf-v1.0-114/bin/AHF-v1.0-114 /mnt/lustre/users/astro/da500/ahf-v1.0-114/AHF.input"

        # Run the command
        $ahf_command

    fi
done
