INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_POLARWRAP polarwrap)

FIND_PATH(
    POLARWRAP_INCLUDE_DIRS
    NAMES polarwrap/api.h
    HINTS $ENV{POLARWRAP_DIR}/include
        ${PC_POLARWRAP_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    POLARWRAP_LIBRARIES
    NAMES gnuradio-polarwrap
    HINTS $ENV{POLARWRAP_DIR}/lib
        ${PC_POLARWRAP_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/polarwrapTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(POLARWRAP DEFAULT_MSG POLARWRAP_LIBRARIES POLARWRAP_INCLUDE_DIRS)
MARK_AS_ADVANCED(POLARWRAP_LIBRARIES POLARWRAP_INCLUDE_DIRS)
