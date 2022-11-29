"""Splits up files in a 21cmFAST cache based on the value of a given
parameter"""

import os
import sys
import glob
import h5py

def get_out_dirs(vals, inp_dir):
    """Returns a dictionary of output directories for each key in
    vals, where each dictionary has a key for each val in vals
    
    Parameters
    ----------
    vals : dict
        Values to split the HDF5 files by, where the key is the
        parameter and it contains an iterable of values for that
        parameter

    inp_dir : str
        Path to the HDF5 files

    Examples
    --------
    vals = {'A_VCB': [0.0, 1.0]}
    out_dirs = get_out_dirs(vals, inp_dir)
    print(out_dirs)
    
    >>> {'A_VCB': {0.0:
        '/Users/lukeconaboy/projects/vbc/21cmvFAST/example_coeval/output/A_VCB_0.0',
        1.0:
        '/Users/lukeconaboy/projects/vbc/21cmvFAST/example_coeval/output/A_VCB_1.0'}}

    """
    out_dirs = {par: {val: os.path.join(inp_dir, par+'_'+str(val))
                      for val in vals[par]}
                for par in vals.keys()}

    return out_dirs


def get_par_val(hf, par):
    """Get the value of the parameter par in the HDF5 file hf, if that
    parameter does not exist returns None. Only works for astro_params
    currently

    Parameters
    ----------
    hf : str
        Path to HDF5 file
    par : str
        Name of the parameter to extract the value for

    Examples
    --------
    val = get_par_val('BrightnessTemp_8346578_r4573257.h5', 'A_VCB')
    print(val)

    >>> 1.0

    """
    with h5py.File(hf, 'r') as hid:
        try:
            val = hid['astro_params'].attrs[par]
        # some outputs do not have this parameter (e.g. PerturbedField
        # and InitialConditions do not care about astro_params), in
        # which case we just symlink
        except KeyError:
            val = None

        return val


def do_cmd_hf(inp_hf, out_dir, cmd):
    """Performs the command cmd on inp_hf (src) and out_hf (dst),
    which is created by combining out_dir and inp_hf

    Parameters
    ----------
    inp_hf : str
        Source file path
    out_dir : str
        Directory to output destination file
    cmd : func
        Either os.symlink or os.rename (no brackets)

    Examples
    --------
    do_cmd_hf(inp_hf, out_dir, os.symlink)

    """
    inp_hf_ = os.path.split(inp_hf)[1]
    out_hf = os.path.join(out_dir, inp_hf_)
    cmd(inp_hf, out_hf)

if __name__ == '__main__':
    vals = {'A_VCB': [0.0, 1.0]}
    inp_dir = sys.argv[1]
    out_dirs = get_out_dirs(vals, inp_dir)

    for par in out_dirs.keys():
        for out_dir in out_dirs[par].values():
            os.makedirs(out_dir, exist_ok=True)

    # Grab all the HDF5 filenames
    inp_hfs = glob.glob(os.path.join(inp_dir, '*.h5'))

    # Loop through and do the renaming
    for inp_hf in inp_hfs:
        for par in out_dirs.keys():
            val = get_par_val(hf=inp_hf, par=par)

            if val is None:
                # We symlink to each directory
                for out_dir in out_dirs[par].values():
                    do_cmd_hf(inp_hf, out_dir, os.symlink)

            else:
                # We move to the relevant directory
                out_dir = out_dirs[par][val]
                do_cmd_hf(inp_hf, out_dir, os.rename)

                    
                
