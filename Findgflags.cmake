find_path(
  gflags_INCLUDE_DIR
  NAMES
  gflags
  PATHS
  include)

find_library(
  gflags_LIBRARIES
  NAMES
  gflags
  libgflags
  gflags_nothread
  libgflags_nothread
  gflags_static
  libgflags_static
  gflags_nothread_static
  libgflags_nothread_static
  PATHS
  lib)

include(FindPackageHandleStandardArgs)

find_package_handle_standard_args(gflags REQUIRED_VARS gflags_LIBRARIES gflags_INCLUDE_DIR)
