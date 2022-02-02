#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Johannes Demel.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from collections import namedtuple
import numpy as np
import pypolar
from symbolmapping import create_interleaver_indices
import pprint


def round_up_power_of_2(value):
    return int(2 ** np.ceil(np.log2(float(value))))


def get_polar_configuration(frame_size, info_size, design_SNR=0.0, interleaver_type='random'):
    # make sure, we operate on byte multiples of bits.
    frame_size = 8 * (frame_size // 8)
    info_size = 8 * (info_size // 8)

    block_size = round_up_power_of_2(frame_size)
    polar_info_size = info_size
    frozen_bit_positions = pypolar.frozen_bits(
        block_size, polar_info_size, design_SNR)
    interleaver_indices = create_interleaver_indices(
        frame_size, interleaver_type)
    assert np.all(np.arange(frame_size, dtype=interleaver_indices.dtype)
                  == np.sort(interleaver_indices))
    pconf = {
        'frame_size': frame_size,
        'frame_byte_size': frame_size // 8,
        'info_size': info_size,
        'info_byte_size': info_size // 8,
        'design_SNR': design_SNR,
        'block_size': block_size,
        'polar_info_size': polar_info_size,
        'frozen_bit_positions': frozen_bit_positions,
        'interleaver_indices': interleaver_indices
    }
    # pprint.pprint(pconf)
    po = namedtuple("code_configuration", pconf.keys())(*pconf.values())
    return po
