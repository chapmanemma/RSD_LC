/* #include "hdf5.h" */  
/* #include "hdf5_hl.h" */
#include <stdio.h>
#include <stdlib.h>
#include "hdf_util.h"

int group_count = 0;

herr_t group_counter (hid_t loc_id, const char *name, const H5O_info_t *info,
		void *operator_data) {
  herr_t          status;

  if (info->type == H5O_TYPE_GROUP) {
    if (name[0] != '.')  ++group_count;  // skip root group
  }
  return 0;
}


int get_group_count(hid_t hid) {
  herr_t status;
  
  group_count = 0;  // reset counter
  status = H5Ovisit3 (hid, H5_INDEX_NAME, H5_ITER_NATIVE, group_counter, NULL, 1);
  printf("-- found %d groups\n", group_count);

  return group_count;
}

void get_group_name(int i, char *group_name) {
  sprintf(group_name, "%05d", i);
}

hid_t open_group(hid_t hid, char *group_name) {
  hid_t gid;
    
  gid = H5Gopen2(hid, group_name, H5P_DEFAULT);

  if (gid == H5I_INVALID_HID) exit(1);

  return gid;
}

int check_group(hid_t hid, char *group_name) {
  hid_t gid;

  gid = H5Gopen2(hid, group_name, H5P_DEFAULT);

  if (gid == H5I_INVALID_HID) {
    // group does not exist
    return 0;
  } else {
    // group exists
    H5Gclose(gid);
    return 1;
  }
}

herr_t check_dataset(hid_t hid, char *group_name, char *dset_name) {
  hid_t gid;
  herr_t dset_ok;
  
  gid = open_group(hid, group_name);
  dset_ok = H5LTfind_dataset(gid, dset_name);
  H5Gclose(gid);

  return dset_ok;
}

void get_dataset_dims(hid_t hid, char *group_name, char *dset_name, hsize_t *dims) {
  H5T_class_t class_id;
  size_t size;
  hid_t gid;
  
  gid = open_group(hid, group_name);
  H5LTget_dataset_info(gid, dset_name, dims, &class_id, &size);
  H5Gclose(gid);
}

herr_t read_group(hid_t hid, char *group_name, char *dset_name, float *buf) {
  hid_t gid;
  herr_t read_ok;
  
  if (check_dataset(hid, group_name, dset_name)) {
    gid = open_group(hid, group_name);
    read_ok = H5LTread_dataset(gid, dset_name, H5T_NATIVE_FLOAT, buf);
    H5Gclose(gid);

    if (read_ok < 0) exit(1);
       
    printf("%s/%s exists and 0: %f 10000: %f\n", group_name, dset_name, buf[0], buf[9999]);
  }

  return read_ok;
}
