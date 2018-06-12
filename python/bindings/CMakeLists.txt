# Copyright 2020 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

GR_PYTHON_CHECK_MODULE_RAW(
    "pygccxml"
    "import pygccxml"
    PYGCCXML_FOUND
    )

include(GrPybind)

########################################################################
# Python Bindings
########################################################################

list(APPEND polarwrap_python_files
    decoderwrap_python.cc
    encoderwrap_python.cc
    python_bindings.cc)

GR_PYBIND_MAKE_OOT(polarwrap
   ../..
   gr::polarwrap
   "${polarwrap_python_files}")

target_link_libraries(polarwrap_python PUBLIC gnuradio-fec)

install(TARGETS polarwrap_python DESTINATION ${GR_PYTHON_DIR}/polarwrap COMPONENT pythonapi)
