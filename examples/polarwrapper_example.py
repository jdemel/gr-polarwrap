#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Wrapper Example
# Author: Johannes Demel
# Generated: Tue Jun  5 17:39:28 2018
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gfdm.pygfdm import cyclic_prefix
from gfdm.pygfdm import filters
from gfdm.pygfdm import mapping
from gfdm.pygfdm import preamble as pre_module
from gfdm.pygfdm import utils
from gfdm.pygfdm import validation_utils as vu
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import fec
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import numpy as np
import polarwrap
import pypolar
import sip
import sys
from gnuradio import qtgui


class polarwrapper_example(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Wrapper Example")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Wrapper Example")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "polarwrapper_example")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.bits_per_frame = bits_per_frame = 512
        self.bytes_per_frame = bytes_per_frame = int(bits_per_frame // 8)
        self.polar_block_size = polar_block_size = 8 * 8 * (bytes_per_frame // 8)
        self.fft_len = fft_len = 64
        self.polar_info_size = polar_info_size = polar_block_size // 2
        self.cp_len = cp_len = fft_len // 2
        self.frozen_bit_positions = frozen_bit_positions = pypolar.frozen_bits(polar_block_size, polar_info_size, 0.0)
        self.cs_len = cs_len = cp_len // 2

        self.var_encoder = var_encoder = polarwrap.encoderwrap.make(polar_block_size, (frozen_bit_positions.tolist()), bits_per_frame + 16, 1)

        self.var_decoder = var_decoder = polarwrap.decoderwrap.make(polar_block_size, 1, (frozen_bit_positions.tolist()), bits_per_frame + 16, 1, 'float')
        self.timeslots = timeslots = 5
        self.samp_rate = samp_rate = 3.125e6 * 2
        self.ramp_len = ramp_len = cs_len
        self.polar_info_bytes = polar_info_bytes = polar_info_size // 8
        self.overlap = overlap = 2

        self.gfdm_constellation = gfdm_constellation = digital.constellation_qpsk().base()

        self.active_subcarriers = active_subcarriers = 52

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_time_sink_x_0_0_0_2_0_1 = qtgui.time_sink_f(
        	bytes_per_frame * 4, #size
        	samp_rate, #samp_rate
        	"bits", #name
        	2 #number of inputs
        )
        self.qtgui_time_sink_x_0_0_0_2_0_1.set_update_time(0.1)
        self.qtgui_time_sink_x_0_0_0_2_0_1.set_y_axis(-160, 160)

        self.qtgui_time_sink_x_0_0_0_2_0_1.set_y_label('value', "")

        self.qtgui_time_sink_x_0_0_0_2_0_1.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_0_0_2_0_1.set_trigger_mode(qtgui.TRIG_MODE_AUTO, qtgui.TRIG_SLOPE_POS, 0.05, 0, 0, 'packet_len')
        self.qtgui_time_sink_x_0_0_0_2_0_1.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_0_2_0_1.enable_grid(True)
        self.qtgui_time_sink_x_0_0_0_2_0_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0_2_0_1.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0_2_0_1.enable_stem_plot(False)

        if not True:
          self.qtgui_time_sink_x_0_0_0_2_0_1.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_0_2_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_0_2_0_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0_2_0_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0_2_0_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0_2_0_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0_2_0_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0_2_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_2_0_1_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0_2_0_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_0_2_0_1_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	512, #size
        	samp_rate, #samp_rate
        	"LLRs", #name
        	2 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)

        if not True:
          self.qtgui_time_sink_x_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.fec_generic_encoder_0 = fec.encoder(var_encoder, gr.sizeof_char, gr.sizeof_char)
        self.fec_generic_decoder_0 = fec.decoder(var_decoder, gr.sizeof_float, gr.sizeof_char)
        self.digital_constellation_soft_decoder_cf_0 = digital.constellation_soft_decoder_cf(gfdm_constellation)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc((gfdm_constellation.points()), 1)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, samp_rate,True)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(8, gfdm_constellation.bits_per_symbol(), "", False, gr.GR_MSB_FIRST)
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(1, gr.GR_MSB_FIRST)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((-.9, ))
        self.blocks_char_to_float_1 = blocks.char_to_float(1, -.5)
        self.blocks_char_to_float_0_0 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.blocks_add_const_vxx_0 = blocks.add_const_vff((1., ))
        self.analog_random_uniform_source_x_0 = analog.random_uniform_source_b(0, 256, 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_uniform_source_x_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.qtgui_time_sink_x_0_0_0_2_0_1, 0))
        self.connect((self.blocks_char_to_float_0_0, 0), (self.qtgui_time_sink_x_0_0_0_2_0_1, 1))
        self.connect((self.blocks_char_to_float_1, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.fec_generic_decoder_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.blocks_char_to_float_1, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.fec_generic_encoder_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.digital_constellation_soft_decoder_cf_0, 0))
        self.connect((self.digital_constellation_soft_decoder_cf_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.fec_generic_decoder_0, 0), (self.blocks_char_to_float_0_0, 0))
        self.connect((self.fec_generic_encoder_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))
        self.connect((self.fec_generic_encoder_0, 0), (self.blocks_repack_bits_bb_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "polarwrapper_example")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_bits_per_frame(self):
        return self.bits_per_frame

    def set_bits_per_frame(self, bits_per_frame):
        self.bits_per_frame = bits_per_frame
        self.set_bytes_per_frame(int(self.bits_per_frame // 8))

    def get_bytes_per_frame(self):
        return self.bytes_per_frame

    def set_bytes_per_frame(self, bytes_per_frame):
        self.bytes_per_frame = bytes_per_frame
        self.set_polar_block_size(8 * 8 * (self.bytes_per_frame // 8))

    def get_polar_block_size(self):
        return self.polar_block_size

    def set_polar_block_size(self, polar_block_size):
        self.polar_block_size = polar_block_size
        self.set_polar_info_size(self.polar_block_size // 2)
        self.set_frozen_bit_positions(pypolar.frozen_bits(self.polar_block_size, self.polar_info_size, 0.0))

    def get_fft_len(self):
        return self.fft_len

    def set_fft_len(self, fft_len):
        self.fft_len = fft_len
        self.set_cp_len(self.fft_len // 2)

    def get_polar_info_size(self):
        return self.polar_info_size

    def set_polar_info_size(self, polar_info_size):
        self.polar_info_size = polar_info_size
        self.set_polar_info_bytes(self.polar_info_size // 8)
        self.set_frozen_bit_positions(pypolar.frozen_bits(self.polar_block_size, self.polar_info_size, 0.0))

    def get_cp_len(self):
        return self.cp_len

    def set_cp_len(self, cp_len):
        self.cp_len = cp_len
        self.set_cs_len(self.cp_len // 2)

    def get_frozen_bit_positions(self):
        return self.frozen_bit_positions

    def set_frozen_bit_positions(self, frozen_bit_positions):
        self.frozen_bit_positions = frozen_bit_positions

    def get_cs_len(self):
        return self.cs_len

    def set_cs_len(self, cs_len):
        self.cs_len = cs_len
        self.set_ramp_len(self.cs_len)

    def get_var_encoder(self):
        return self.var_encoder

    def set_var_encoder(self, var_encoder):
        self.var_encoder = var_encoder

    def get_var_decoder(self):
        return self.var_decoder

    def set_var_decoder(self, var_decoder):
        self.var_decoder = var_decoder

    def get_timeslots(self):
        return self.timeslots

    def set_timeslots(self, timeslots):
        self.timeslots = timeslots

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_time_sink_x_0_0_0_2_0_1.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_ramp_len(self):
        return self.ramp_len

    def set_ramp_len(self, ramp_len):
        self.ramp_len = ramp_len

    def get_polar_info_bytes(self):
        return self.polar_info_bytes

    def set_polar_info_bytes(self, polar_info_bytes):
        self.polar_info_bytes = polar_info_bytes

    def get_overlap(self):
        return self.overlap

    def set_overlap(self, overlap):
        self.overlap = overlap

    def get_gfdm_constellation(self):
        return self.gfdm_constellation

    def set_gfdm_constellation(self, gfdm_constellation):
        self.gfdm_constellation = gfdm_constellation

    def get_active_subcarriers(self):
        return self.active_subcarriers

    def set_active_subcarriers(self, active_subcarriers):
        self.active_subcarriers = active_subcarriers


def main(top_block_cls=polarwrapper_example, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
