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
#include <volk/volk.h>
#include <polarwrap/encoderwrap.h>
#include <polarcode/errordetection/crc8.h>
#include <cstring>

namespace gr {
  namespace polarwrap {

    gr::fec::generic_encoder::sptr
    encoderwrap::make(int block_size, std::vector<unsigned> frozen_bit_positions, int frame_size, int error_detection_type)
    {
        return gr::fec::generic_encoder::sptr(
            new encoderwrap(block_size, frozen_bit_positions, frame_size, error_detection_type));
    }

    encoderwrap::encoderwrap(int block_size, std::vector<unsigned> frozen_bit_positions, int frame_size, int error_detection_type)
        : d_frame_size(frame_size)
    {
        d_encoder = new PolarCode::Encoding::ButterflyFipPacked(block_size, frozen_bit_positions);
        set_error_detection(error_detection_type);
        d_input_buffer = (char*) volk_malloc(sizeof(char) * enc_input_size(), volk_get_alignment());
    }

    encoderwrap::~encoderwrap()
    {
        delete d_encoder;
        volk_free(d_input_buffer);
    }

    void
    encoderwrap::set_error_detection(int error_detection_type)
    {
        d_error_detection_type = error_detection_type;
        if(error_detection_type != 0){
            PolarCode::ErrorDetection::CRC8* detector = new PolarCode::ErrorDetection::CRC8();
            d_encoder->setErrorDetection(detector);
        }
    }

    void
    encoderwrap::generic_work(void *in_buffer, void *out_buffer)
    {
        std::memcpy(d_input_buffer, in_buffer, sizeof(char) * num_info_bits() / 8);
        d_encoder->encode_vector(d_input_buffer, out_buffer);
        std::memcpy((char*) out_buffer + (d_encoder->blockLength() / 8), out_buffer,
                    sizeof(char) * ((d_frame_size - d_encoder->blockLength()) / 8));
    }

  } /* namespace polarwrap */
} /* namespace gr */

