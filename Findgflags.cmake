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
  gflags_nothreads
  libgflags_nothreads
  gflags_static
  libgflags_static
  gflags_nothreads_static
  libgflags_nothreads_static
  PATHS
  lib)

include(FindPackageHandleStandardArgs)

find_package_handle_standard_args(gflags REQUIRED_VARS gflags_LIBRARIES gflags_INCLUDE_DIR)
