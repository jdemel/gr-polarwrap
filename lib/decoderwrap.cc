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
#include <polarwrap/decoderwrap.h>
#include <polarcode/errordetection/crc8.h>
#include <cstring>

namespace gr {
  namespace polarwrap {

    gr::fec::generic_decoder::sptr
    decoderwrap::make(int block_size, int list_size, std::vector<unsigned> frozen_bit_positions, int frame_size, int error_detection_type, std::string decoder_impl)
    {
        return generic_decoder::sptr(
            new decoderwrap(block_size, list_size, frozen_bit_positions, frame_size, error_detection_type, decoder_impl));
    }

    decoderwrap::decoderwrap(int block_size, int list_size, std::vector<unsigned> frozen_bit_positions, int frame_size, int error_detection_type, std::string decoder_impl)
            : d_frame_size(frame_size)
    {
        if(decoder_impl.compare("float")){
            d_decoder = PolarCode::Decoding::makeDecoder(block_size, list_size, frozen_bit_positions, 1);
        }
        else if(decoder_impl.compare("scan")){
            d_decoder = PolarCode::Decoding::makeDecoder(block_size, list_size, frozen_bit_positions, 3);
        }
        else{
            d_decoder = PolarCode::Decoding::makeDecoder(block_size, list_size, frozen_bit_positions, 0);
        }

        d_input_buffer = (float*) volk_malloc(sizeof(float) * d_decoder->blockLength(), volk_get_alignment());
        d_output_buffer = (char*) volk_malloc(sizeof(char) * output_size(), volk_get_alignment());

    }

    decoderwrap::~decoderwrap()
    {
        delete d_decoder;
    }

    void
    decoderwrap::set_error_detection(int error_detection_type)
    {
        d_error_detection_type = error_detection_type;
        if(error_detection_type != 0){
            PolarCode::ErrorDetection::CRC8* detector = new PolarCode::ErrorDetection::CRC8();
            d_decoder->setErrorDetection(detector);
        }
    }

    void
    decoderwrap::generic_work(void *in_buffer, void *out_buffer)
    {
        memcpy(d_input_buffer, in_buffer, sizeof(float) * d_decoder->blockLength());
        volk_32f_x2_add_32f(d_input_buffer, d_input_buffer, (float*)in_buffer + d_decoder->blockLength(), d_frame_size - d_decoder->blockLength());
        d_decoder->setSignal(d_input_buffer);
        d_decoder->decode();
        d_decoder->getDecodedInformationBits(d_output_buffer);
        memcpy(out_buffer, d_output_buffer, sizeof(char) * num_info_bits() / 8);
    }

  } /* namespace polarwrap */
} /* namespace gr */

