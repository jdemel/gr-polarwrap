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
/* BINDTOOL_HEADER_FILE(decoderwrap.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(ee9979160188d42dff651749ba0d050a)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <polarwrap/decoderwrap.h>
// pydoc.h is automatically generated in the build directory
#include <decoderwrap_pydoc.h>

void bind_decoderwrap(py::module& m)
{

    using decoderwrap = ::gr::polarwrap::decoderwrap;

    py::class_<decoderwrap, gr::fec::generic_decoder, std::shared_ptr<decoderwrap>>(
        m, "decoderwrap", D(decoderwrap))

        .def_static("make",
                    &decoderwrap::make,
                    py::arg("block_size"),
                    py::arg("list_size"),
                    py::arg("frozen_bit_positions"),
                    py::arg("error_detection_type"),
                    py::arg("decoder_impl"),
                    D(decoderwrap, make))


        .def("generic_work",
             &decoderwrap::generic_work,
             py::arg("in_buffer"),
             py::arg("out_buffer"),
             D(decoderwrap, generic_work))

        .def("rate", &decoderwrap::rate, D(decoderwrap, rate))

        .def("get_input_size",
             &decoderwrap::get_input_size,
             D(decoderwrap, get_input_size))

        .def("get_output_size",
             &decoderwrap::get_output_size,
             D(decoderwrap, get_output_size))

        .def("set_frame_size",
             &decoderwrap::set_frame_size,
             py::arg("frame_size"),
             D(decoderwrap, set_frame_size))

        .def("get_input_conversion",
             &decoderwrap::get_input_conversion,
             D(decoderwrap, get_input_conversion))

        .def("get_output_conversion",
             &decoderwrap::get_output_conversion,
             D(decoderwrap, get_output_conversion))

        ;
}
