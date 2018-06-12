/* -*- c++ -*- */
/*
 * Copyright 2018 Johannes Demel.
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
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
    : d_puncturer(new PolarCode::Puncturer(block_size, frozen_bit_positions))
{
    if (block_size % 8 != 0) {
        throw std::invalid_argument("block_size MUST be a multiple of 8!");
    }
    int parent_block_size = PolarCode::round_up_power_of_two(block_size);

    d_encoder = std::unique_ptr<PolarCode::Encoding::ButterflyFipPacked>(
        new PolarCode::Encoding::ButterflyFipPacked(parent_block_size,
                                                    frozen_bit_positions));

    set_error_detection(error_detection_type);

    d_input_buffer =
        (char*)volk_malloc(sizeof(char) * enc_input_size(), volk_get_alignment());
    d_output_buffer = (unsigned char*)volk_malloc(
        sizeof(unsigned char) * parent_block_size, volk_get_alignment());
    // std::cout << "block_size=" << d_puncturer->blockLength() << std::endl
    //           << "parent_block_size=" << d_puncturer->parentBlockLength() << std::endl
    //           << "code_block_size=" << d_encoder->blockLength() << std::endl
    //           << "get_input_size=" << get_input_size() << std::endl
    //           << "get_output_size=" << get_output_size() << std::endl;
}

encoderwrap::~encoderwrap()
{
    volk_free(d_input_buffer);
    volk_free(d_output_buffer);
}

void encoderwrap::set_error_detection(int error_detection_type)
{
    d_error_detection_type = error_detection_type;
    d_encoder->setErrorDetection(
        PolarCode::ErrorDetection::create(error_detection_type, std::string("CRC")));
    // std::cout << "encoder: " << d_encoder->getErrorDetectionMode() << std::endl;
    // if(error_detection_type != 0){
    //     PolarCode::ErrorDetection::CRC8* detector = new
    //     PolarCode::ErrorDetection::CRC8(); d_encoder->setErrorDetection(detector);
    // }
}

void encoderwrap::generic_work(void* in_buffer, void* out_buffer)
{
    // auto start = std::chrono::high_resolution_clock::now();
    // ATTENTION: CRC is added to input buffer!
    std::memcpy(d_input_buffer, in_buffer, sizeof(char) * get_input_size());
    d_encoder->setInformation(d_input_buffer);
    d_encoder->encode();
    d_encoder->getEncodedData(d_output_buffer);
    d_puncturer->puncturePacked((unsigned char*)out_buffer, d_output_buffer);
    // auto end = std::chrono::high_resolution_clock::now();
    // auto du = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start);
    // std::cout << "enc dur: " << du.count() << "ns\n";
}

} /* namespace polarwrap */
} /* namespace gr */
