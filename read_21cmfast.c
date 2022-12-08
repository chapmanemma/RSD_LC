#include "read_21cmfast.h"
#include "Input_variables.h"

herr_t read_density(char *path, float z, long int seed, float *temp) {
  char hf[256];
  hid_t hid;
  herr_t hid_err;
  
  sprintf(hf, "%s/PerturbedField_z%.3f_s%ld.h5", path, z, seed);
  hid = open_hf(hf, H5F_ACC_RDONLY);
  hid_err = read_dataset_float(hid, "PerturbedField", "density", temp);
  hid_err = close_hf(hid);

  return hid_err;
}

herr_t read_velocity(char *path, float z, long int seed, float *temp) {
  char hf[256];
  hid_t hid;
  herr_t hid_err;
  float Mpc_to_m = 3.08567758e22;  // converts Mpc to m
  float c = 299792458.0;           // speed of light in m s^-1
  
  sprintf(hf, "%s/PerturbedField_z%.3f_s%ld.h5", path, z, seed);
  hid = open_hf(hf, H5F_ACC_RDONLY);
  hid_err = read_dataset_float(hid, "PerturbedField", "velocity", temp);
  hid_err = close_hf(hid);

  // LC convert from 21cmFAST units (comoving Mpc s^-1) to simfast21
  // units (proper m s^-1 c^-1)
  for(long int i=0;i<global_N3_smooth;i++) {
    temp[i] = temp[i] * Mpc_to_m / c / (z + 1.);
  }
  
  return hid_err;
}

herr_t read_velocity_gradient(char *path, float z, long int seed, float *temp) {
  char hf[256];
  hid_t hid;
  herr_t hid_err;

  // LC this is already in the correct units, because the different
  // units in the velocity get divided out
  sprintf(hf, "%s/VelocityGradient_z%.3f_s%ld.h5", path, z, seed);
  hid = open_hf(hf, H5F_ACC_RDONLY);
  hid_err = read_dataset_float(hid, "VelocityGradient", "velocity_gradient", temp);
  hid_err = close_hf(hid);

  return hid_err;
}

herr_t read_ionized_fraction(char *path, float z, long int seed, float *temp) {
  char hf[256];
  hid_t hid;
  herr_t hid_err;

  sprintf(hf, "%s/IonizedBox_z%.3f_s%ld.h5", path, z, seed);
  hid = open_hf(hf, H5F_ACC_RDONLY);
  hid_err = read_dataset_float(hid, "IonizedBox", "xH_box", temp);
  hid_err = close_hf(hid);
  // LC we actually convert back to xHI later, but let's be consistent here
  for(long int i=0;i<global_N3_smooth;i++) {
    // printf("xHII %f", temp[i]);
    temp[i] = (1. - temp[i]);
    // printf("xHI %f", temp[i]);
  }
  return hid_err;
}

herr_t read_spin_temperature(char *path, float z, long int seed, float *temp) {
  char hf[256];
  hid_t hid;
  herr_t hid_err;
  
  sprintf(hf, "%s/TsBox_z%.3f_s%ld.h5", path, z, seed);
  hid = open_hf(hf, H5F_ACC_RDONLY);
  hid_err = read_dataset_float(hid, "TsBox", "Ts_box", temp);
  hid_err = close_hf(hid);

  // LC we just need to read in the Ts box from 21cmFAST, no extra
  // computation required, apart from converting from mK to K

  // LC actually I think Ts might be in K
  /* for(long int i=0;i<global_N3_smooth;i++) { */
  /*   printf("Ts (mK) %f\n", temp[i]); */
  /*   temp[i] = (temp[i]) * 1e-3; */
  /*   printf("Ts (K) %f\n", temp[i]); */
  /* } */
  return hid_err;
}
