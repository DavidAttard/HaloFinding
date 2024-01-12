# Creates a plot of the mass evolution of a single halo as a function of redshift.
# Change the "halo_id" paramter to the halo you want to analyse 
# Change the full path variable to the path where the AHF data is stored.

import os
import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

halo_id = 0
z = []
mass = []

for i in range(128):
    full_path = "/p/project/hestiaeor/david/hestiaeor/AHF_4096/{0:03d}/halos/".format(i)
    
    # getting the path of the "*_halos" file
    for filename in os.listdir(full_path):
        # Check if the file name ends with "_halos"
        if filename.endswith("_halos"):
            # Construct the full file path
            file_path = os.path.join(full_path, filename)

            # Code to extract redshift from the input file name 
            pattern = re.compile(r'z(\d+\.\d+)')
            match = re.search(pattern, file_path)
            if match:
                z_file = float(match.group(1))  # Convert to float

    print(z_file)

    # Loading the "*_halos" file
    df = pd.read_csv(file_path, delim_whitespace=True)

    # Selecting the data for halo i
    halo_data = df[df['#ID(1)'] == halo_id]['Mhalo(4)']
    
    if not halo_data.empty:
        mass = np.append(mass, halo_data)
        print(halo_data)
        z = np.append(z, z_file)

# Save z and mass arrays to a file
np.savez('z_mass_data.npz', z=z, mass=mass)

Load z and mass arrays from the file
loaded_data = np.load('z_mass_data.npz')
z_loaded = loaded_data['z']
mass_loaded = loaded_data['mass']

# Plot using loaded data
plt.plot(z_loaded, np.log10(mass_loaded))
plt.xlabel("z")
plt.ylabel(r"$\log_{10}\mathrm{M}$")
plt.title('Halo {}'.format(halo_id))
plt.savefig('Mass_z_relation.png')
