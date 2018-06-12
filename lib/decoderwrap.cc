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
#include <polarwrap/decoderwrap.h>
#include <volk/volk.h>
#include <cstring>

namespace gr {
namespace polarwrap {

gr::fec::generic_decoder::sptr
decoderwrap::make(int block_size,
                  int list_size,
                  std::vector<unsigned> frozen_bit_positions,
                  int error_detection_type,
                  std::string decoder_impl)
{
    return generic_decoder::sptr(new decoderwrap(
        block_size, list_size, frozen_bit_positions, error_detection_type, decoder_impl));
}

decoderwrap::decoderwrap(int block_size,
                         int list_size,
                         std::vector<unsigned> frozen_bit_positions,
                         int error_detection_type,
                         std::string decoder_impl)
    : generic_decoder("polar"),
      d_puncturer(new PolarCode::Puncturer(block_size, frozen_bit_positions))
{
    if (block_size % 8 != 0) {
        throw std::invalid_argument("block_size MUST be a multiple of 8!");
    }
    int parent_block_size = PolarCode::round_up_power_of_two(block_size);
    make_decoder(parent_block_size, list_size, frozen_bit_positions, decoder_impl);
    set_error_detection(error_detection_type);

    d_input_buffer = (float*)volk_malloc(sizeof(float) * d_decoder->blockLength(),
                                         volk_get_alignment());
    d_output_buffer =
        (char*)volk_malloc(sizeof(char) * output_size(), volk_get_alignment());
}

decoderwrap::~decoderwrap()
{
    volk_free(d_input_buffer);
    volk_free(d_output_buffer);
}

void decoderwrap::make_decoder(const int parent_block_size,
                               const int list_size,
                               const std::vector<unsigned>& frozen_bit_positions,
                               const std::string& decoder_impl)
{
    d_decoder = std::unique_ptr<PolarCode::Decoding::Decoder>(PolarCode::Decoding::create(
        parent_block_size, list_size, frozen_bit_positions, decoder_impl));
}

void decoderwrap::set_error_detection(int error_detection_type)
{
    d_error_detection_type = error_detection_type;
    d_decoder->setErrorDetection(
        PolarCode::ErrorDetection::create(error_detection_type, std::string("CRC")));
}

void decoderwrap::generic_work(void* in_buffer, void* out_buffer)
{
    // auto start = std::chrono::high_resolution_clock::now();
    d_puncturer->depuncture(d_input_buffer, (float*)in_buffer);
    d_decoder->setSignal(d_input_buffer);
    d_decoder->decode();
    d_decoder->getDecodedInformationBits(d_output_buffer);
    memcpy(out_buffer, d_output_buffer, sizeof(char) * num_info_bits() / 8);

    // auto end = std::chrono::high_resolution_clock::now();
    // auto du = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start);
    // std::cout << "decoder duration: " << du.count() << "ns\n";
}

} /* namespace polarwrap */
} /* namespace gr */
