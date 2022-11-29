#include "hdf5.h"
#include "hdf5_hl.h"

// int group_count = 0;

herr_t group_counter (hid_t loc_id, const char *name, const H5O_info_t *info,
            void *operator_data);
int get_group_count(hid_t hid);
void  get_group_name(int i, char *group_name);
int check_group(hid_t hid, char *group_name);
hid_t open_group(hid_t hid, char *group_name);
herr_t check_dataset(hid_t hid, char *group_name, char *dset_name);
void get_dataset_dims(hid_t hid, char *group_name, char *dset_name, hsize_t *dims);
herr_t read_group(hid_t hid, char *group_name, char *dset_name, float *buf);
