/* -*- c++ -*- */
/*
 * Copyright 2018, 2021 Johannes Demel.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include <polarcode/errordetection/crc8.h>
#include <polarwrap/encoderwrap.h>
#include <volk/volk.h>
#include <chrono>
#include <cstring>
#include <stdexcept>

namespace gr {
namespace polarwrap {

gr::fec::generic_encoder::sptr encoderwrap::make(
    int block_size, std::vector<unsigned> frozen_bit_positions, int error_detection_type)
{
    return gr::fec::generic_encoder::sptr(
        new encoderwrap(block_size, frozen_bit_positions, error_detection_type));
}

encoderwrap::encoderwrap(int block_size,
                         std::vector<unsigned> frozen_bit_positions,
                         int error_detection_type)
    : d_puncturer(
          std::make_unique<PolarCode::Puncturer>(block_size, frozen_bit_positions))
{
    if (block_size % 8 != 0) {
        throw std::invalid_argument("block_size MUST be a multiple of 8!");
    }
    int parent_block_size = PolarCode::round_up_power_of_two(block_size);

    d_encoder = std::make_unique<PolarCode::Encoding::ButterflyFipPacked>(
        parent_block_size, frozen_bit_positions);

    set_error_detection(error_detection_type);
    d_input_buffer.resize(enc_input_size());
    d_output_buffer.resize(parent_block_size);
}

encoderwrap::~encoderwrap() {}

void encoderwrap::set_error_detection(int error_detection_type)
{
    d_error_detection_type = error_detection_type;
    d_encoder->setErrorDetection(
        PolarCode::ErrorDetection::create(error_detection_type, std::string("CRC")));
}

void encoderwrap::generic_work(void* in_buffer, void* out_buffer)
{
    // auto start = std::chrono::high_resolution_clock::now();
    // ATTENTION: CRC is added to input buffer!
    std::memcpy(d_input_buffer.data(), in_buffer, sizeof(char) * get_input_size());
    d_encoder->setInformation(d_input_buffer.data());
    d_encoder->encode();
    d_encoder->getEncodedData(d_output_buffer.data());
    d_puncturer->puncturePacked((unsigned char*)out_buffer, d_output_buffer.data());
    // auto end = std::chrono::high_resolution_clock::now();
    // auto du = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start);
    // std::cout << "enc dur: " << du.count() << "ns\n";
}

} /* namespace polarwrap */
} /* namespace gr */
