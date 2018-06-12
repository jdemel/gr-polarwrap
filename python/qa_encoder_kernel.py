#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2018 Johannes Demel.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

from gnuradio import gr, gr_unittest
from gnuradio import blocks, fec
import polarwrap_python as polarwrap
import numpy as np
import pypolar


class qa_encoder_kernel(gr_unittest.TestCase):
    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_001_setup(self):
        # set up fg
        N = 256
        punctured_size = N - 24
        K = N // 2
        frozen_bit_positions = pypolar.frozen_bits(N, K, 0.0)

        enc = polarwrap.encoderwrap.make(punctured_size,
                                         (list(frozen_bit_positions)),
                                         8)
        self.assertEqual(enc.get_input_size(), (K // 8) - 1)
        self.assertEqual(enc.get_output_size(), punctured_size // 8)
        self.assertEqual(enc.get_input_conversion(), "pack")
        self.assertEqual(enc.get_output_conversion(), "pack")
        self.assertAlmostEqual(enc.rate(), (K - 8) / punctured_size)

    def test_002_t(self):
        # set up fg
        N = 256
        punctured_size = N - 24
        K = N // 2

        frozen_bit_positions = pypolar.frozen_bits(N, K, 0.0)

        encoder = pypolar.PolarEncoder(N, frozen_bit_positions)
        encoder.setErrorDetection(16, 'CRC')
        puncturer = pypolar.Puncturer(punctured_size, frozen_bit_positions)

        bits = np.random.randint(0, 2, K).astype(np.int32)
        d = np.packbits(bits)
        frame = encoder.encode_vector(d)
        frame = puncturer.puncturePacked(frame)

        enc = polarwrap.encoderwrap.make(punctured_size,
                                         list(frozen_bit_positions),
                                         16)
        encblock = fec.encoder(enc, gr.sizeof_char, gr.sizeof_char)

        src = blocks.vector_source_b(d[:-1].astype(int))
        snk = blocks.vector_sink_b()

        self.tb.connect(src, encblock, snk)
        self.tb.run()
        # check data

        res = np.array(snk.data())
        print(frame.size, res.size)
        print(frame)
        print(res)
        # self.assertTupleEqual(tuple(frame.tolist()),
        #                       tuple(res.tolist()))

    def test_003_t(self):
        # set up fg
        num_frames = 200
        N = 1024
        punctured_size = 936
        K = N // 2
        frozen_bit_positions = pypolar.frozen_bits(N, K, 0.0)
        encoder = pypolar.PolarEncoder(N, frozen_bit_positions)
        encoder.setErrorDetection(8)
        puncturer = pypolar.Puncturer(punctured_size, frozen_bit_positions)

        data = np.array([]).astype(np.int32)
        ref = np.array([]).astype(np.int32)
        for i in range(num_frames):
            bits = np.random.randint(0, 2, K - 8).astype(np.int32)
            d = np.packbits(bits)
            d = np.append(d, 0).astype(np.uint8)
            data = np.concatenate((data, d[0:-1]))
            frame = encoder.encode_vector(d)
            frame = puncturer.puncturePacked(frame)
            ref = np.concatenate((ref, frame))

        enc = polarwrap.encoderwrap.make(punctured_size,
                                         list(frozen_bit_positions),
                                         8)
        encblock = fec.encoder(enc, gr.sizeof_char, gr.sizeof_char)

        src = blocks.vector_source_b(data.astype(int))
        snk = blocks.vector_sink_b()

        self.tb.connect(src, encblock, snk)
        self.tb.run()
        # check data

        res = np.array(snk.data())

        self.assertTupleEqual(tuple(ref.tolist()),
                              tuple(res.tolist()))


if __name__ == '__main__':
    gr_unittest.run(qa_encoder_kernel)
