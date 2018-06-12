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


class qa_decoder_kernel(gr_unittest.TestCase):
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

        dec = polarwrap.decoderwrap.make(punctured_size, 1,
                                         list(frozen_bit_positions),
                                         8, 'mixed')

        self.assertEqual(dec.get_input_size(), punctured_size)
        self.assertEqual(dec.get_output_size(), (K // 8))
        self.assertEqual(dec.get_input_conversion(), "none")
        self.assertEqual(dec.get_output_conversion(), "pack")
        self.assertAlmostEqual(dec.rate(), K / punctured_size)

    def test_002_frame(self):
        print('single frame test')
        # set up fg
        N = 256
        punctured_size = N - 24
        K = N // 2
        frozen_bit_positions = pypolar.frozen_bits(N, K, 0.0)

        detector = pypolar.Detector(8, 'CRC')
        encoder = pypolar.PolarEncoder(N, frozen_bit_positions)
        encoder.setErrorDetection(0)
        puncturer = pypolar.Puncturer(punctured_size, frozen_bit_positions)

        bits = np.random.randint(
            0, 2, K - detector.getCheckBitCount()).astype(np.int32)
        d = np.packbits(bits)
        print('data:', d)
        # print(len(d))
        crcd = detector.generate(d)
        print('crcd:', crcd)
        frame = encoder.encode_vector(crcd)
        frame = puncturer.puncturePacked(frame)
        # print(d)
        # d = d[0:-1]

        data = -2. * np.unpackbits(frame) + 1.
        data += np.random.uniform(-.2, .2, data.size)
        # data *= -1.
        src = blocks.vector_source_f(data)
        snk = blocks.vector_sink_b()

        dec = polarwrap.decoderwrap.make(punctured_size, 8,
                                         list(frozen_bit_positions),
                                         8, 'mixed')
        decblock = fec.decoder(dec, gr.sizeof_float, gr.sizeof_char)

        self.tb.connect(src, decblock, snk)
        self.tb.run()
        # check data
        res = np.array(snk.data())

        # print(crcd)
        print('resd:', res)

        print('single frame test END')
        self.assertTupleEqual(tuple(crcd.tolist()),
                              tuple(res.tolist()))

    def test_003_t(self):
        # set up fg
        num_frames = 200
        N = 1024
        punctured_size = 936
        K = N // 2
        crc_size = 16
        frozen_bit_positions = pypolar.frozen_bits(N, K, 0.0)

        detector = pypolar.Detector(crc_size, 'CRC')
        encoder = pypolar.PolarEncoder(N, frozen_bit_positions)
        encoder.setErrorDetection(0)
        puncturer = pypolar.Puncturer(punctured_size, frozen_bit_positions)

        data = np.array([]).astype(np.int32)
        ref = np.array([]).astype(np.int32)
        for i in range(num_frames):
            bits = np.random.randint(0, 2, K - crc_size).astype(np.int32)
            d = np.packbits(bits)
            crcd = detector.generate(d)
            data = np.concatenate((data, crcd))
            frame = encoder.encode_vector(crcd)
            frame = puncturer.puncturePacked(frame)
            ref = np.concatenate((ref, frame))

        ref = -2. * np.unpackbits(ref.astype(np.uint8)) + 1.
        awgn_ref = ref + np.random.uniform(-.2, .2, ref.size)
        src = blocks.vector_source_f(awgn_ref)
        snk = blocks.vector_sink_b()

        dec = polarwrap.decoderwrap.make(punctured_size, 8,
                                         list(frozen_bit_positions),
                                         crc_size, 'mixed')
        decblock = fec.decoder(dec, gr.sizeof_float, gr.sizeof_char)

        self.tb.connect(src, decblock, snk)
        self.tb.run()
        # check data
        res = np.array(snk.data())

        self.assertTupleEqual(tuple(data.tolist()),
                              tuple(res.tolist()))


if __name__ == '__main__':
    gr_unittest.run(qa_decoder_kernel)
