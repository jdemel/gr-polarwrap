/* -*- c++ -*- */
/*
 * Copyright 2018, 2021 Johannes Demel.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_POLARWRAP_DECODERWRAP_H
#define INCLUDED_POLARWRAP_DECODERWRAP_H

#include <gnuradio/fec/generic_decoder.h>
#include <polarcode/decoding/decoder.h>
#include <polarcode/puncturer.h>
#include <polarwrap/api.h>
#include <volk/volk_alloc.hh>
#include <memory>


namespace gr {
namespace polarwrap {

/*!
 * \brief GNU Radio wrapper for polar-codes decoder
 *
 * \param block_size punctured code block size
 * \param list_size CA-SCL list size ( >= 1 ). 1 implies SC decoder
 * \param frozen_bit_positions sorted list of frozen bit positions
 * \param error_detection_type Integer that specifies CRC size {0, 8, 16, 32}
 * \param decoder_impl std::string that specifies the desired impl (e.g. mixed, float,
 * char)
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

    volk::vector<float> d_input_buffer;
    volk::vector<char> d_output_buffer;

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
