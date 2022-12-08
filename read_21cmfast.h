#include "util/h5/hdf_util.h"

herr_t read_velocity(char *path, float z, long int seed, float *temp);
herr_t read_velocity_gradient(char *path, float z, long int seed, float *temp);
herr_t read_density(char *path, float z, long int seed, float *temp);
herr_t read_ionized_fraction(char *path, float z, long int seed, float *temp);
herr_t read_spin_temperature(char *path, float z, long int seed, float *temp);
