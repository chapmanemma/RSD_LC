import re
import sys
import glob
import h5py
import numpy as np

# Following functions taken from vel.c
H0 = 3.24078e-18 # h/sec */
def dzdt(z):
    return (-Hz(z)*(1.0+z))


def dgrowthdt(redshift):
    dz = 1e-3
    dg = (getGrowth(redshift+dz/2.)-getGrowth(redshift-dz/2.))/dz*dzdt(redshift)

    return dg


def getGrowth(z):
    return Hz(z)/Hz(0)*intGrowth(z)/intGrowth(0.)


def intGrowth(zz):
    dz = 0.001
    intg = 0
    Hz0 = Hz(0.)
    zs = np.arange(zz+dz/2., zz+100., dz)
    for z in zs:
        Hubz=Hz(z)/Hz0
        intg+=(1.+z)/Hubz/Hubz/Hubz
    
    intg=intg*dz

    return intg


def Hz(z, h, omega_matter):
    return h*H0*np.sqrt(omega_matter*(1.+z)*(1.+z)*(1.+z)+
                        (1. - omega_matter))


def compute_vel_gradient(vel, HII_DIM, BOX_LEN):
    """Computes the velocity gradient in configuration space, assuming that the velocity field passed is for the z-direction

    Parameters
    ----------
    vel : arr
        Array of size (HII_DIM, HII_DIM, HII_DIM) containing the
        velocity in units of [BOX_LEN] s^-1
    HII_DIM : int
        Dimension of velocity array
    BOX_LEN : float
        Box size in the same units as the length dimension of vel

    """
    vel = np.fft.fft(vel)  # velocity in Fourier space

    kk = np.fft.fftfreq(HII_DIM) * HII_DIM * 2 * np.pi / BOX_LEN
    kx, ky, kz = np.meshgrid(kk, kk, kk)

    vel *= 1j * kz  # velocity gradient in Fourier space
    vel = np.fft.ifft(vel)
    vel = vel.real.astype(np.float32)  # velocity gradient in
                                       # configuration space

    return vel


def write_vel_gradient(z, seed):
    """Reads the z-velocity from a PerturbedField HDF5 file (that has been renamed with rename_21cmfast_hdf5.py) and computes the velocity gradient (dv/dr)/H, writing it out to an HDF5 file in the same directory called VelocityGradient

    Parameters
    ----------
    z : float
        Redshift of the velocity file
    seed : int
        Random seed of the velocity file

    Examples
    --------
    FIXME: Add docs.

    """

    hf_inp = f'PerturbedField_z{z:.3f}_s{seed:d}.h5'
    hf_out = f'VelocityGradient_z{z:.3f}_s{seed:d}.h5'

    # hf_inp = 'PerturbedField_bc9fb18cdbf1223a3377b5dd7fb03fe4_r731995.h5'
    # hf_out = 'VelocityGradient_bc9fb18cdbf1223a3377b5dd7fb03fe4_r731995.h5'

    with h5py.File(hf_inp, 'r') as hid_inp, h5py.File(hf_out, 'a') as hid_out:
        # v in configuration space
        vel = np.array(hid_inp['PerturbedField/velocity'])
        HII_DIM = hid_inp['user_params'].attrs['HII_DIM']
        BOX_LEN = hid_inp['user_params'].attrs['BOX_LEN']
        h = hid_inp['cosmo_params'].attrs['hlittle']
        omega_matter = hid_inp['cosmo_params'].attrs['OMm']

        # Write out all the attrs
        for g_inp in hid_inp:
            if g_inp == 'PerturbedField': continue
            g_out = hid_out.create_group(g_inp)
            for k, v in hid_inp[g_inp].attrs.items():
                g_out.attrs[k] = v

    vel = compute_vel_gradient(vel, HII_DIM, BOX_LEN)
    vel /= Hz(z, h, omega_matter)  # divide by H(z) as in vel.c
            
    with h5py.File(hf_out, 'a') as hid_out:
        g = hid_out.create_group('VelocityGradient')
        d = g.create_dataset('velocity_gradient', data=vel)


def write_vel_gradient_all():
    z_pattern = re.compile(r'z(\d+\.\d{3})')
    seed_pattern = re.compile(r's(\d+)')

    inp_hfs = glob.glob('./PerturbedField*.h5')
    inp_seeds = [int(seed_pattern.search(inp_hf).group(1)) for inp_hf in inp_hfs]
    inp_zs = [float(z_pattern.search(inp_hf).group(1)) for inp_hf in inp_hfs]

    for inp_hf, z, seed in zip(inp_hfs, inp_zs, inp_seeds):
        print(f'-- working on {inp_hf:s} at z = {z:.3f} with seed {seed:d}')
        write_vel_gradient(z, seed)
    
    
if __name__ == '__main__':
    # z = float(sys.argv[1])
    # seed = int(sys.argv[2])
    # write_vel_gradient(z, seed)

    write_vel_gradient_all()
