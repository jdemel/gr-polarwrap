/* -*- c++ -*- */
/*
 * Copyright 2018, 2021 Johannes Demel.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */


#ifndef INCLUDED_POLARWRAP_ENCODERWRAP_H
#define INCLUDED_POLARWRAP_ENCODERWRAP_H

#include <gnuradio/fec/generic_encoder.h>
#include <polarcode/encoding/butterfly_fip_packed.h>
#include <polarcode/puncturer.h>
#include <polarwrap/api.h>
#include <volk/volk_alloc.hh>
#include <memory>

namespace gr {
namespace polarwrap {

/*!
 * \brief GNU Radio wrapper for polar-codes encoder
 *
 * \param block_size punctured code block size
 * \param frozen_bit_positions sorted list of frozen bit positions
 * \param error_detection_type Integer that specifies CRC size {0, 8, 16, 32}
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
    volk::vector<char> d_input_buffer;
    volk::vector<unsigned char> d_output_buffer;
};

} // namespace polarwrap
} // namespace gr

#endif /* INCLUDED_POLARWRAP_ENCODERWRAP_H */
