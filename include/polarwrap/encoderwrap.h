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


#ifndef INCLUDED_POLARWRAP_ENCODERWRAP_H
#define INCLUDED_POLARWRAP_ENCODERWRAP_H

#include <gnuradio/fec/generic_encoder.h>
#include <polarcode/encoding/butterfly_fip_packed.h>
#include <polarcode/puncturer.h>
#include <polarwrap/api.h>
#include <memory>

namespace gr {
namespace polarwrap {

/*!
 * \brief <+description+>
 *
 */
class POLARWRAP_API encoderwrap : public gr::fec::generic_encoder
{
public:
    ~encoderwrap();

    static gr::fec::generic_encoder::sptr make(int block_size,
                                               std::vector<unsigned> frozen_bit_positions,
                                               int error_detection_type);

    // FECAPI
    void generic_work(void* in_buffer, void* out_buffer);
    double rate() { return (1.0 * get_input_size() / get_output_size()); };
    int get_input_size() { return num_info_bits() / 8; };
    int get_output_size() { return d_puncturer->blockLength() / 8; };
    bool set_frame_size(unsigned int frame_size) { return false; };
    const char* get_input_conversion() { return "pack"; };
    const char* get_output_conversion() { return "pack"; };

private:
    encoderwrap(int block_size,
                std::vector<unsigned> frozen_bit_positions,
                int error_detection_type);
    std::unique_ptr<PolarCode::Encoding::ButterflyFipPacked> d_encoder;
    std::unique_ptr<PolarCode::Puncturer> d_puncturer;
    int d_error_detection_type;
    int num_info_bits() { return enc_input_size() - d_error_detection_type; }
    int enc_input_size() { return d_encoder->infoLength(); }
    void set_error_detection(int error_detection_type);
    char* d_input_buffer;
    unsigned char* d_output_buffer;
};

} // namespace polarwrap
} // namespace gr

#endif /* INCLUDED_POLARWRAP_ENCODERWRAP_H */
