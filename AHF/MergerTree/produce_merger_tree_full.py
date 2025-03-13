# This code will produce a full merger tree of a given halo
# Change the direcotries for the the AHF halo catalogues as well as
# the merger tree files (created using merger tree)
# The output of such code will be a text file with all the information about the merger tree.
# Change the halo_traced, start_snap and end_snap values

import os
import glob
import numpy as np
import pandas as pd 
import re 

def parse_merger_tree(snapshot):
    """
    Parse the merger tree file for the given snapshot.
    Returns a dictionary mapping each halo id (from snapshot 'snapshot')
    to a list of its progenitor halo ids (which belong to snapshot 'snapshot-1').
    """
    tree_file = f"/p/project/lgreion/david/DMO_256_4096/MergerTree/Trees/{snapshot:03d}/test_mtree"
    tree = {}
    try:
        with open(tree_file, 'r') as f:
            # First line: number of merger trees in this snapshot.
            num_trees = int(f.readline().strip())
            # Process each tree.
            for _ in range(num_trees):
                # Header: "halo_id num_progenitors"
                header = f.readline().strip()
                while header == "":
                    header = f.readline().strip()
                parts = header.split()
                if len(parts) < 2:
                    continue
                halo_id = int(parts[0])
                num_progen = int(parts[1])
                progenitors = []
                for _ in range(num_progen):
                    line = f.readline().strip()
                    while line == "":
                        line = f.readline().strip()
                    progenitors.append(int(line))
                tree[halo_id] = progenitors
    except Exception as e:
        print(f"Error reading merger tree file for snapshot {snapshot}: {e}")
    return tree

def load_halo_catalog(snapshot):
    """
    Load the halo catalog for the given snapshot.
    Returns a dictionary mapping halo id to its mass.
    The catalog file is assumed to be located in:
    /p/project/lgreion/david/DMO_256_4096/AHF/<snapshot>/halos/
    and has a filename matching: ahf_*.AHF_halos
    """
    pattern = f"/p/project/lgreion/david/DMO_256_4096/AHF/{snapshot:03d}/halos/ahf_*.AHF_halos"
    files = glob.glob(pattern)
    if not files:
        print(f"No halo catalog file found for snapshot {snapshot:03d} (pattern: {pattern}).")
        return {}
    catalog_file = files[0]
    try:
        data = pd.read_csv(catalog_file, sep='\s+')
        pattern = r'z(\d+\.\d+)'

        # Use re.search to find the match
        match = re.search(pattern, catalog_file)

        # Extract the number from the match
        if match:
            redshift = match.group(1)
            redshift = float(redshift)
        
    except Exception as e:
        print(f"Error reading halo catalog file {catalog_file}: {e}")
        return {}
    
    # Here, we assume the catalog contains columns named "#ID(1)" for the halo id and "Mhalo(4)" for the mass.
    halo_mass = data.set_index("#ID(1)")["Mhalo(4)"].to_dict()
    halo_xc = data.set_index("#ID(1)")["Xc(6)"].to_dict()
    halo_yc = data.set_index("#ID(1)")["Yc(7)"].to_dict()
    halo_zc = data.set_index("#ID(1)")["Zc(8)"].to_dict()

    return redshift, halo_mass, halo_xc, halo_yc, halo_zc

def get_halo_mass(snapshot, halo_id):
    """Return a dictionary of mass, xc, yc, and zc for the given halo in the specified snapshot."""
    redshift, halo_mass, halo_xc, halo_yc, halo_zc = load_halo_catalog(snapshot)
    
    # Instead of using .get() on a float (which caused the error), we now directly use the values.
    return {
        'redshift': redshift,  # Return the redshift directly, as it's a float.
        'mass': halo_mass.get(halo_id, None),
        'xc': halo_xc.get(halo_id, None),
        'yc': halo_yc.get(halo_id, None),
        'zc': halo_zc.get(halo_id, None),
    }

def trace_progenitors(snapshot, halo_id, snapshot_end=128):
    """
    Recursively trace the progenitors of a halo from the given snapshot down to snapshot_end.
    Returns a dictionary representing the branch of the merger tree, where each node has:
      - 'snapshot': the snapshot number
      - 'halo_id': the halo id in that snapshot
      - 'mass': the halo mass (if available)
      - 'progenitors': a list of similar dictionaries for progenitor halos
    """
    # Get halo data as a dictionary
    halo_data = get_halo_mass(snapshot, halo_id)
    result = {
        'snapshot': snapshot,
        'redshift': halo_data['redshift'], 
        'halo_id': halo_id, 
        'mass': halo_data['mass'], 
        'xc': halo_data['xc'], 
        'yc': halo_data['yc'], 
        'zc': halo_data['zc'],  
        'progenitors': []
    }

    # Stop if we have reached the final snapshot.
    if snapshot <= snapshot_end:
        return result
    
    # For snapshot N, the merger tree file gives progenitors in snapshot N-1.
    tree = parse_merger_tree(snapshot)
    if halo_id not in tree:
        return result  # No progenitor information available.
    
    progenitor_ids = tree[halo_id]
    for prog in progenitor_ids:
        child_tree = trace_progenitors(snapshot - 1, prog, snapshot_end)
        result['progenitors'].append(child_tree)
    
    return result

def write_tree_to_file(tree, file_handle):
    """
    Write a node from the merger tree (and its subtree) to file_handle.
    Each node is written as a single line with the following tab-separated fields:
    snapshot, halo_id, mass, and immediate progenitor halo ids (comma-separated).
    """
    snapshot = tree.get('snapshot', 'NA')
    redshift = tree.get('redshift', 'NA')
    halo_id = tree.get('halo_id', 'NA')
    mass = tree.get('mass', 'NA')
    xc = tree.get('xc', 'NA')
    yc = tree.get('yc', 'NA')
    zc = tree.get('zc', 'NA')
    
    # Ensure snapshot is an integer if possible
    snapshot = int(snapshot) if snapshot != 'NA' else -1

    # Get progenitors and filter out None values
    progenitors = tree.get('progenitors', [])
    valid_progenitors = [p for p in progenitors if isinstance(p, dict) and 'snapshot' in p]

    # Sort progenitors by snapshot in descending order
    sorted_progenitors = sorted(valid_progenitors, key=lambda x: int(x.get('snapshot', 0)), reverse=True)

    # Collect only the halo ids of the sorted progenitors
    progenitor_ids = [str(child.get('halo_id', 'NA')) for child in sorted_progenitors]
    progenitors_str = ", ".join(progenitor_ids)
    
    file_handle.write(f"{snapshot}\t{redshift}\t{halo_id}\t{mass}\t{xc}\t{yc}\t{zc}\t{progenitors_str}\n")
    
    # Recursively write each sorted progenitor
    for child in sorted_progenitors:
        write_tree_to_file(child, file_handle)



halo_traced = 188
start_snap = 129
end_snap = 21
tree = trace_progenitors(start_snap, halo_traced, end_snap)

# Write the tree to a text file.
output_file = "merger_tree_{}.txt".format(halo_traced)
with open(output_file, "w") as f:
    # Write the header line.
    f.write("snapshot\tredshift\thalo_id\tmass\txc\tyc\tzc\tprogenitors\n")
    write_tree_to_file(tree, f)

print(f"Merger tree written to {output_file}")

# Define the file path
file_path = output_file

df = pd.read_csv(file_path, sep='\t', dtype={'snapshot': int, 'redshift': float, 'halo_id': int, 'mass': float, 'xc': float, 'yc': float, 'zc': float}, keep_default_na=False)
df['progenitors'] = df['progenitors'].apply(lambda x: [int(i) for i in x.split(', ')] if x else [])
df['mass'] = df['mass'].astype(int)  # Convert to int if no decimal values are needed

# Sort the DataFrame by snapshot in descending order
df = df.sort_values(by=['snapshot', 'halo_id'], ascending=[False, True])
df.to_csv(output_file, sep='\t', index=False)
print(f"Sorted merger tree saved to {output_file}")
