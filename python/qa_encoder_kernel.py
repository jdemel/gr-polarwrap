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
import polarwrap_swig as polarwrap
import numpy as np
import pypolar


class qa_encoder_kernel(gr_unittest.TestCase):
    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_001_t(self):
        # set up fg
        N = 256
        K = N // 2
        rep_bits = 8
        frozen_bit_positions = pypolar.frozen_bits(N, K, 0.0)
        encoder = pypolar.PolarEncoder(N, frozen_bit_positions)
        encoder.setErrorDetection()

        bits = np.random.randint(0, 2, K).astype(np.int32)
        d = np.packbits(bits)
        frame = encoder.encode_vector(d)
        frame = np.concatenate((frame, frame[0:rep_bits // 8]))

        enc = polarwrap.encoderwrap.make(N, (frozen_bit_positions.tolist()),
                                         N + rep_bits, 1)
        encblock = fec.encoder(enc, gr.sizeof_char, gr.sizeof_char)

        src = blocks.vector_source_b(d.astype(int))
        snk = blocks.vector_sink_b()

        self.tb.connect(src, encblock, snk)
        self.tb.run()
        # check data

        res = np.array(snk.data())

        self.assertComplexTuplesAlmostEqual(frame, res)

    def test_002_t(self):
        # set up fg
        num_frames = 200
        N = 2048
        K = N // 2
        rep_bits = 24
        frozen_bit_positions = pypolar.frozen_bits(N, K, 0.0)
        encoder = pypolar.PolarEncoder(N, frozen_bit_positions)
        encoder.setErrorDetection()

        data = np.array([]).astype(np.int32)
        ref = np.array([]).astype(np.int32)
        for i in range(num_frames):
            bits = np.random.randint(0, 2, K - 8).astype(np.int32)
            d = np.packbits(bits)
            d = np.append(d, 0).astype(np.uint8)
            data = np.concatenate((data, d[0:-1]))
            frame = encoder.encode_vector(d)
            frame = np.concatenate((frame, frame[0:rep_bits // 8]))
            ref = np.concatenate((ref, frame))

        enc = polarwrap.encoderwrap.make(N, (frozen_bit_positions.tolist()),
                                         N + rep_bits, 1)
        encblock = fec.encoder(enc, gr.sizeof_char, gr.sizeof_char)

        src = blocks.vector_source_b(data.astype(int))
        snk = blocks.vector_sink_b()

        self.tb.connect(src, encblock, snk)
        self.tb.run()
        # check data

        res = np.array(snk.data())
        self.assertComplexTuplesAlmostEqual(ref, res)


if __name__ == '__main__':
    gr_unittest.run(qa_encoder_kernel)
