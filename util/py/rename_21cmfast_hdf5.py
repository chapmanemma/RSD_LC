import os
import sys
import glob
import h5py


def get_field_from_hf(hf):
    """Get the field (e.g. 'BrightnessTemp') from a 21cmFAST HDF5 filename

    Parameters
    ----------
    hf : str
        An HDF5 filename output by 21cmFAST's automatic caching

    Examples
    --------
    field = get_field_from_hf('BrightnessTemp_8346578_r4573257.h5')
    print(field)

    >>> 'BrightnessTemp'

    """
    idx = hf.find('_')

    return hf[0:idx]


def get_z_seed_from_hf(hf):
    """Extracts the redshift and random seed for a 21cmFAST output by
    reading the attributes of the HDF5 file

    Parameters
    ----------
    hf : str
        An HDF5 filename output by 21cmFAST's automatic caching

    Examples
    --------
    z, seed = get_z_seed_from_hf('BrightnessTemp_8346578_r4573257.h5')
    print(z, seed)

    >>> 6.0 731995

    """
    with h5py.File(hf, 'r') as hid:
        try:
            z = float(hid.attrs['redshift'])
        except KeyError:
            z = 0.0  # InitialConditions does not have a redshift
            assert('InitialConditions' in hf), hf  # ... and it should
                                                   # be the only one

        seed = hid.attrs['random_seed']

    return z, seed


def get_new_hf(hf):
    """Creates a new name for the HDF5 files based on the type of
    output ('field'), redshift of the output ('z') and the random seed
    used ('seed')

    Parameters
    ----------
    hf : str
        An HDF5 filename output by 21cmFAST's automatic caching

    Examples
    --------
    hf = get_new_hf('BrightnessTemp_8346578_r4573257.h5')
    print(hf)

    >>> 'BrightnessTemp_6.000_731995'

    """
    hf_str = '{0:s}_z{1:.3f}_s{2:d}.h5'
    field = get_field_from_hf(os.path.split(hf)[1])  # just want the h5 name
    z, seed = get_z_seed_from_hf(hf)  # need the full path

    return hf_str.format(field, z, seed)


if __name__ == '__main__':
    link = True  # symlink the files, or actually copy them?
    if link:
        cmd = os.symlink
        print('-- symlinking files')
    else:
        cmd = os.rename
        print('-- moving files')

    inp_dir = sys.argv[1]
    out_dir = os.path.join(inp_dir, 'renamed')
    os.makedirs(out_dir, exist_ok=True)

    # Grab all the HDF5 filenames
    inp_hfs = glob.glob(os.path.join(inp_dir, '*.h5'))

    # Loop through and perform cmd on all the new filenames
    for inp_hf in inp_hfs:
        out_hf = os.path.join(out_dir,
                              get_new_hf(inp_hf))
        cmd(inp_hf, out_hf)
