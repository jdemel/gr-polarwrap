/*
 * Copyright 2020 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

/***********************************************************************************/
/* This file is automatically generated using bindtool and can be manually edited  */
/* The following lines can be configured to regenerate this file during cmake      */
/* If manual edits are made, the following tags should be modified accordingly.    */
/* BINDTOOL_GEN_AUTOMATIC(0)                                                       */
/* BINDTOOL_USE_PYGCCXML(0)                                                        */
/* BINDTOOL_HEADER_FILE(encoderwrap.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(c07c45623c8512174807e743406191df)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <polarwrap/encoderwrap.h>
// pydoc.h is automatically generated in the build directory
#include <encoderwrap_pydoc.h>

void bind_encoderwrap(py::module& m)
{

    using encoderwrap = ::gr::polarwrap::encoderwrap;


    py::class_<encoderwrap, gr::fec::generic_encoder, std::shared_ptr<encoderwrap>>(
        m, "encoderwrap", D(encoderwrap))
        .def_static("make",
                    &encoderwrap::make,
                    py::arg("block_size"),
                    py::arg("frozen_bit_positions"),
                    py::arg("error_detection_type"),
                    D(encoderwrap, make))

        .def("generic_work",
             &encoderwrap::generic_work,
             py::arg("in_buffer"),
             py::arg("out_buffer"),
             D(encoderwrap, generic_work))

        .def("rate", &encoderwrap::rate, D(encoderwrap, rate))

        .def("get_input_size",
             &encoderwrap::get_input_size,
             D(encoderwrap, get_input_size))

        .def("get_output_size",
             &encoderwrap::get_output_size,
             D(encoderwrap, get_output_size))

        .def("set_frame_size",
             &encoderwrap::set_frame_size,
             py::arg("frame_size"),
             D(encoderwrap, set_frame_size))

        .def("get_input_conversion",
             &encoderwrap::get_input_conversion,
             D(encoderwrap, get_input_conversion))

        .def("get_output_conversion",
             &encoderwrap::get_output_conversion,
             D(encoderwrap, get_output_conversion))

        ;
}
