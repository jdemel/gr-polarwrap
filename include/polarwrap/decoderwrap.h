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


#ifndef INCLUDED_POLARWRAP_DECODERWRAP_H
#define INCLUDED_POLARWRAP_DECODERWRAP_H

#include <polarwrap/api.h>
#include <gnuradio/fec/generic_decoder.h>
#include <polarcode/decoding/decoder.h>

namespace gr {
  namespace polarwrap {

    /*!
     * \brief <+description+>
     *
     */
    class POLARWRAP_API decoderwrap: public gr::fec::generic_decoder
    {
    public:

        ~decoderwrap();

        static gr::fec::generic_decoder::sptr
        make(int block_size, int list_size, std::vector<unsigned> frozen_bit_positions, int frame_size, int error_detection_type, std::string decoder_impl);

        // FECAPI
        void generic_work(void *in_buffer, void *out_buffer);
        double rate() {return (1.0 * get_input_size() / get_output_size());};
        // int get_input_size(){return num_info_bits() / 8;};
        int get_input_size(){return d_frame_size;};
        int get_output_size(){return num_info_bits() / 8;};
        bool set_frame_size(unsigned int frame_size){return false;};
        const char* get_input_conversion(){return "none";};
        const char* get_output_conversion(){return "pack";};

    private:
        decoderwrap(int block_size, int list_size, std::vector<unsigned> frozen_bit_positions, int frame_size, int error_detection_type, std::string decoder_impl);
        PolarCode::Decoding::Decoder* d_decoder;
        int d_frame_size;
        int d_error_detection_type;
        float* d_input_buffer;
        char* d_output_buffer;

        void set_error_detection(int error_detection_type);
        int num_info_bits(){return output_size() - (d_error_detection_type ? 8 : 0);}
        int output_size(){return d_decoder->blockLength() - d_decoder->frozenBits().size();}
    };

  } // namespace polarwrap
} // namespace gr

#endif /* INCLUDED_POLARWRAP_DECODERWRAP_H */

