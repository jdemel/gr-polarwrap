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

#include <gnuradio/fec/generic_decoder.h>
#include <polarcode/decoding/decoder.h>
#include <polarcode/puncturer.h>
#include <polarwrap/api.h>
#include <memory>


namespace gr {
namespace polarwrap {

/*!
 * \brief <+description+>
 *
 */
class POLARWRAP_API decoderwrap : public gr::fec::generic_decoder
{
public:
    ~decoderwrap();

    static gr::fec::generic_decoder::sptr make(int block_size,
                                               int list_size,
                                               std::vector<unsigned> frozen_bit_positions,
                                               int error_detection_type,
                                               std::string decoder_impl);

    // FECAPI
    void generic_work(void* in_buffer, void* out_buffer);
    double rate() { return (1.0 * num_info_bits() / get_input_size()); };
    int get_input_size() { return d_puncturer->blockLength(); };
    int get_output_size() { return num_info_bits() / 8; };
    bool set_frame_size(unsigned int frame_size) { return false; };
    const char* get_input_conversion() { return "none"; };
    const char* get_output_conversion() { return "pack"; };

private:
    decoderwrap(int block_size,
                int list_size,
                std::vector<unsigned> frozen_bit_positions,
                int error_detection_type,
                std::string decoder_impl);

    std::unique_ptr<PolarCode::Decoding::Decoder> d_decoder;
    std::unique_ptr<PolarCode::Puncturer> d_puncturer;
    int d_error_detection_type;
    float* d_input_buffer;
    char* d_output_buffer;

    void make_decoder(const int parent_block_size,
                      const int list_size,
                      const std::vector<unsigned>& frozen_bit_positions,
                      const std::string& decoder_impl);
    void set_error_detection(int error_detection_type);
    int num_info_bits() { return output_size(); }
    int output_size() { return d_decoder->infoLength(); }
};

} // namespace polarwrap
} // namespace gr

#endif /* INCLUDED_POLARWRAP_DECODERWRAP_H */
