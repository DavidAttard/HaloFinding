# A python program which takes in a base directory "base_directory_1" and produces halo mass functions
# There are two functions in this package haloMFAHF which makes use of all halos found by AHF and
# haloMFAHF_cleanRegion which only makes use of the halos in the high res region.

import numpy as np
import pandas as pd
from pylab import *
from hmf import MassFunction 

import re

import os

def haloMFAHF(halodata_ahf):
    df = pd.read_csv(halodata_ahf, delim_whitespace=True)
    # halos_ahf = df[(df['hostHalo(2)']<1) & (df['fMhires(38)']==1)]
    halos_ahf = df[(df['hostHalo(2)']<1)]
    npart_less50 = df[df['npart(5)']<50]
    n_50_mass = np.average(npart_less50['Mhalo(4)'])


    lmmin = 5
    lmmax = 14
    dlm = 0.30
    nbins = int((lmmax - lmmin) / dlm) + 1
    log_bins = 10**np.linspace(lmmin, lmmax, num=nbins)
    
    dn = []
    dm = []

    for i in range(0,len(log_bins)-1):
        dn = np.append(dn, len(halos_ahf[ (halos_ahf['Mhalo(4)']>log_bins[i]) & (halos_ahf['Mhalo(4)']<=log_bins[i+1]) ]['Mhalo(4)']))
        dm = np.append(dm, log_bins[i+1]-log_bins[i])

    dndm = dn/dlm #np.log(dm)
    hmf_ahf = dndm / (100**3)
    # hmf_ahf = dndm / (0.25**3)
    log10M = (log_bins[1:] + log_bins[:-1]) / 2

    return hmf_ahf, log10M, n_50_mass

def haloMFAHF_cleanRegion(halodata_ahf):
    df = pd.read_csv(halodata_ahf, delim_whitespace=True)
    halos_ahf = df[(df['hostHalo(2)']<1) & (df['fMhires(38)']==1)]
    npart_less50 = df[df['npart(5)']<50]
    n_50_mass = np.average(npart_less50['Mhalo(4)'])


    lmmin = 5
    lmmax = 14
    dlm = 0.30
    nbins = int((lmmax - lmmin) / dlm) + 1
    log_bins = 10**np.linspace(lmmin, lmmax, num=nbins)
    
    dn = []
    dm = []

    for i in range(0,len(log_bins)-1):
        dn = np.append(dn, len(halos_ahf[ (halos_ahf['Mhalo(4)']>log_bins[i]) & (halos_ahf['Mhalo(4)']<=log_bins[i+1]) ]['Mhalo(4)']))
        dm = np.append(dm, log_bins[i+1]-log_bins[i])

    dndm = dn/dlm #np.log(dm)
    hmf_ahf = dndm / (100**3)
    # hmf_ahf = dndm / (0.25**3)
    log10M = (log_bins[1:] + log_bins[:-1]) / 2

    return hmf_ahf, log10M, n_50_mass

base_directory_1 = "/cosma7/data/dp004/dc-atta2/AHF_16384/"
# base_directory_2 = "/p/scratch/hestiaeor/david/AHF_4096_unbound/"

snap_template = "{:03d}"  # Use 3 digits, e.g., 001, 002, ..., 127
file_suffix = "_halos"

for snap_number in range(59):
    # Construct the directory path
    directory_path_1 = "{}{:03d}/halos/".format(base_directory_1, snap_number)
    # directory_path_2 = f"{base_directory_2}{snap_number:03d}/halos/"
    
    # Check if the directory exists
    if os.path.exists(directory_path_1):
        # List files in the directory ending with "_halos"
        matching_files = [f for f in os.listdir(directory_path_1) if f.endswith(file_suffix)]
        
        # Print the full paths of matching files
        for matching_file in matching_files:
            file_path_1 = os.path.join(directory_path_1, matching_file)
            print(file_path_1)

            # file_path_2 = os.path.join(directory_path_2, matching_file)
            # print(file_path_2)

            halodata_ahf_128_bound = file_path_1
            # halodata_ahf_128_unbound = file_path_2

            # Code to extract redshift from the input file name 
            pattern = re.compile(r'z(\d+\.\d+)')
            match = re.search(pattern, halodata_ahf_128_bound)
            if match:
                z = match.group(1)
  


            #for the analytical hmf
            lmmin = 5
            lmmax = 14
            dlm = 0.30
            nbins = int((lmmax - lmmin) / dlm) + 1
            log_bins = 10**np.linspace(lmmin, lmmax, num=nbins)
            log10M = (log_bins[1:] + log_bins[:-1]) / 2
            omega_m = 0.318
            omega_b = 0.01
            h = 0.677
            sigma_8 = 0.83
            n_s = 0.9611


            hmf = MassFunction(Mmin=lmmin, Mmax=lmmax, dlog10m=dlm, z = z ,hmf_model = 'Watson', cosmo_params={'Om0': omega_m,'Ob0': omega_b,'H0': h * 100.},sigma_8=sigma_8,n=n_s,)
            hmf_2 = MassFunction(Mmin=lmmin, Mmax=lmmax, dlog10m=dlm, z = z ,hmf_model = 'Tinker10', cosmo_params={'Om0': omega_m,'Ob0': omega_b,'H0': h * 100.},sigma_8=sigma_8,n=n_s,)

            # hmf = MassFunction(Mmin=lmmin, Mmax=lmmax, dlog10m=dlm, z = z ,hmf_model = 'Watson')
            # hmf_2 = MassFunction(Mmin=lmmin, Mmax=lmmax, dlog10m=dlm, z = z ,hmf_model = 'Tinker')

            mass_func = hmf.dndlog10m
            mass_func_m = hmf.m

            mass_func_2 = hmf_2.dndlog10m
            mass_func_m_2 = hmf_2.m

            # fig = figure()
            # ax = fig.add_subplot(111)

            # ax.plot(haloMFAHF(halodata_ahf_128_bound)[1], haloMFAHF(halodata_ahf_128_bound)[0], c="blue", label="AHF 4096 (bound)")
            # ax.plot(haloMFAHF(halodata_ahf_128_unbound)[1], haloMFAHF(halodata_ahf_128_unbound)[0], c="red", label="AHF 4096 (unbound)")
            # ax.plot(mass_func_m, mass_func, c="black", label="Watson")
            # ax.axvline(x = 64219029.925021565)
            # ax.set_xscale("log")
            # ax.set_yscale("log")
            # ax.legend()
            # ax.set_xlabel(r"(M)[$M_{\odot}]")
            # ax.set_ylabel(r"$\frac{dn}{d\log{M}}$ [$M_{\odot}^{-1} \, \mathrm{Mpc}^{-3}$]")
            


            fig = figure()
            fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [3, 1]})

            x1 = haloMFAHF(halodata_ahf_128_bound)[1]
            y1 = haloMFAHF(halodata_ahf_128_bound)[0]
            
            x2 = haloMFAHF_cleanRegion(halodata_ahf_128_bound)[1]
            y2 = haloMFAHF_cleanRegion(halodata_ahf_128_bound)[0]

            ax1.plot(x1, y1, c="blue", label="AHF")
            ax1.plot(x2, y2, c="red", label="AHF clean regions ONLY")

            # ax1.plot(x2, y2, c="red", label="AHF 4096 (unbound)")

            ax1.plot(mass_func_m, mass_func, c="black", label="Watson")
            ax1.plot(mass_func_m_2, mass_func_2, c="green", label="Tinker 10")

            non_zero_values = [value for value in y2 if value != 0]

            if non_zero_values:
                # Find the minimum value excluding zero
                min_value_excluding_zero = min(value for value in y2 if value != 0)
                max_value_excluding_zero = max(value for value in y2 if value != 0)

            
                # Set y-axis limits excluding zero
                ax1.set_ylim(min_value_excluding_zero * 10**(-2), max_value_excluding_zero * 10**(6))

            ax1.axvline(x = 64219029.925021565)
            ax1.set_xscale("log")
            ax1.set_yscale("log")
            

            ax1.legend()
            ax1.set_title('z = {}'.format(z))
            # ax1.set_xlabel(r"(M)[$M_{\odot}$]")
            ax1.set_ylabel(r"$\frac{dn}{d\log{M}}$ [$\mathrm{h}^3 \, \mathrm{M}_{\odot}^{-1} \, \mathrm{Mpc}^{-3}$]")

            ratio_1 = y1/  mass_func
            # ratio_2 = y2/  mass_func

            r_1=y1/mass_func_2
            # r_2=y2/mass_func_2
            
            non_zero_mask_1 = ratio_1 != 0
            # non_zero_mask_2 = ratio_2 != 0
            
            ax2.scatter(x1[non_zero_mask_1], ratio_1[non_zero_mask_1], label='bound', color='blue', marker='+')
            # ax2.scatter(x2[non_zero_mask_2], ratio_2[non_zero_mask_2], label='unbound', color='red', marker='+')
            
            ax2.scatter(x1[non_zero_mask_1], r_1[non_zero_mask_1], label='bound', color='blue', marker='x')
            # ax2.scatter(x2[non_zero_mask_2], r_2[non_zero_mask_2], label='unbound', color='red', marker='x')

            ax2.set_xlabel(r"M[$\mathrm{M}_{\odot} \, \mathrm{h}^{-1}$]")
            ax2.set_ylabel('Ratio')
            ax2.set_ylim(0, 1.5)
            plt.tight_layout()
            fig.savefig('/cosma7/data/dp004/dc-atta2/AHF_hmf/hmf_z_{}.jpg'.format(z))




