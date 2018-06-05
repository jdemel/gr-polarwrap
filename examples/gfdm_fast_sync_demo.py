#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: GFDM Fast Sync
# Author: Johannes Demel
# Generated: Tue Jun  5 17:44:56 2018
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

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt4 import Qt
from gfdm.pygfdm import cyclic_prefix
from gfdm.pygfdm import filters
from gfdm.pygfdm import mapping
from gfdm.pygfdm import preamble as pre_module
from gfdm.pygfdm import utils
from gfdm.pygfdm import validation_utils as vu
from gnuradio import blocks
from gnuradio import channels
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import fec
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from hier_gfdm_fastsync import hier_gfdm_fastsync  # grc-generated hier_block
from hier_gfdm_receiver_tagged import hier_gfdm_receiver_tagged  # grc-generated hier_block
from hier_packet_formatter import hier_packet_formatter  # grc-generated hier_block
from hier_packet_parser import hier_packet_parser  # grc-generated hier_block
from optparse import OptionParser
import gfdm
import numpy as np
import pmt
import polarwrap
import pypolar
import sip
from gnuradio import qtgui


class gfdm_fast_sync_demo(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "GFDM Fast Sync")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("GFDM Fast Sync")
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

        self.settings = Qt.QSettings("GNU Radio", "gfdm_fast_sync_demo")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.timeslots = timeslots = 5
        self.fft_len = fft_len = 64
        self.active_subcarriers = active_subcarriers = 52

        self.gfdm_constellation = gfdm_constellation = digital.constellation_qpsk().base()

        self.cp_len = cp_len = fft_len // 2
        self.active_symbols = active_symbols = timeslots * active_subcarriers
        self.cs_len = cs_len = cp_len // 2
        self.bits_per_frame = bits_per_frame = int(np.log2(len(gfdm_constellation.points() ) )) * active_symbols
        self.subcarrier_map = subcarrier_map = mapping.get_subcarrier_map(fft_len, active_subcarriers, dc_free=True)
        self.seed = seed = utils.generate_seed('awesome preamble')
        self.ramp_len = ramp_len = cs_len
        self.overlap = overlap = 2
        self.bytes_per_frame = bytes_per_frame = int(bits_per_frame // 8)
        self.polar_block_size = polar_block_size = 8 * 8 * (bytes_per_frame // 8)
        self.modulated_preambles = modulated_preambles = pre_module.mapped_preamble(seed, 'rrc', .2, active_subcarriers, fft_len, subcarrier_map, overlap, cp_len, ramp_len)
        self.block_len = block_len = timeslots * fft_len
        self.window_len = window_len = block_len + cp_len + cs_len
        self.preamble = preamble = modulated_preambles[0]
        self.polar_info_size = polar_info_size = polar_block_size // 2
        self.samp_rate = samp_rate = 3.125e6 * 8
        self.frozen_bit_positions = frozen_bit_positions = pypolar.frozen_bits(polar_block_size, polar_info_size, 0.0)
        self.frame_len = frame_len = window_len + len(preamble)
        self.f_taps = f_taps = filters.get_frequency_domain_filter('rrc', .2, timeslots, fft_len, overlap)
        self.window_taps = window_taps = cyclic_prefix.get_raised_cosine_ramp(ramp_len, cyclic_prefix.get_window_len(cp_len, timeslots, fft_len, cs_len))
        self.variable_qtgui_label_0_0 = variable_qtgui_label_0_0 = samp_rate / fft_len
        self.variable_qtgui_label_0 = variable_qtgui_label_0 = block_len

        self.var_encoder = var_encoder = polarwrap.encoderwrap.make(polar_block_size, (frozen_bit_positions.tolist()), bits_per_frame, 1)

        self.var_decoder = var_decoder = polarwrap.decoderwrap.make(polar_block_size, 1, (frozen_bit_positions.tolist()), bits_per_frame, 1, 'float')
        self.rx_f_taps = rx_f_taps = np.conjugate(f_taps)
        self.preamble_len = preamble_len = len(preamble)
        self.polar_info_bytes = polar_info_bytes = polar_info_size // 8 - 1
        self.noise_voltage = noise_voltage = 0.01
        self.ic_iter_range = ic_iter_range = 4
        self.frame_gap = frame_gap = np.zeros(int(1. * samp_rate / 1000.) - frame_len)
        self.frame_dur = frame_dur = 1. * frame_len / samp_rate
        self.fq_off = fq_off = 0.0
        self.data_rate = data_rate = int(1000. * bits_per_frame)
        self.chan_taps = chan_taps = [1. + 1.j, .7 - .1j, .1 + .01j, 0.04+.05j, 0.1+0.01j]
        self.chan_epsilon = chan_epsilon = 1.

        ##################################################
        # Blocks
        ##################################################
        self.ctrl_tab = Qt.QTabWidget()
        self.ctrl_tab_widget_0 = Qt.QWidget()
        self.ctrl_tab_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.ctrl_tab_widget_0)
        self.ctrl_tab_grid_layout_0 = Qt.QGridLayout()
        self.ctrl_tab_layout_0.addLayout(self.ctrl_tab_grid_layout_0)
        self.ctrl_tab.addTab(self.ctrl_tab_widget_0, 'Simulation Control')
        self.top_grid_layout.addWidget(self.ctrl_tab, 3, 4, 2, 1)
        for r in range(3, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 5):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.sync_tab = Qt.QTabWidget()
        self.sync_tab_widget_0 = Qt.QWidget()
        self.sync_tab_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.sync_tab_widget_0)
        self.sync_tab_grid_layout_0 = Qt.QGridLayout()
        self.sync_tab_layout_0.addLayout(self.sync_tab_grid_layout_0)
        self.sync_tab.addTab(self.sync_tab_widget_0, 'Synchronization')
        self.top_grid_layout.addWidget(self.sync_tab, 3, 0, 4, 4)
        for r in range(3, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._noise_voltage_range = Range(0, 1, 0.001, 0.01, 200)
        self._noise_voltage_win = RangeWidget(self._noise_voltage_range, self.set_noise_voltage, 'Noise', "counter_slider", float)
        self.ctrl_tab_grid_layout_0.addWidget(self._noise_voltage_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.ctrl_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.ctrl_tab_grid_layout_0.setColumnStretch(c, 1)
        self._ic_iter_range_range = Range(0, 256, 1, 4, 50)
        self._ic_iter_range_win = RangeWidget(self._ic_iter_range_range, self.set_ic_iter_range, 'IC Iterations', "counter_slider", int)
        self.ctrl_tab_grid_layout_0.addWidget(self._ic_iter_range_win, 3, 0, 1, 1)
        for r in range(3, 4):
            self.ctrl_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.ctrl_tab_grid_layout_0.setColumnStretch(c, 1)
        self._fq_off_range = Range(-10.e4, 10.e4, 1., 0.0, 200)
        self._fq_off_win = RangeWidget(self._fq_off_range, self.set_fq_off, 'F Offset', "counter_slider", float)
        self.ctrl_tab_grid_layout_0.addWidget(self._fq_off_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.ctrl_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.ctrl_tab_grid_layout_0.setColumnStretch(c, 1)
        self.demod_tab = Qt.QTabWidget()
        self.demod_tab_widget_0 = Qt.QWidget()
        self.demod_tab_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.demod_tab_widget_0)
        self.demod_tab_grid_layout_0 = Qt.QGridLayout()
        self.demod_tab_layout_0.addLayout(self.demod_tab_grid_layout_0)
        self.demod_tab.addTab(self.demod_tab_widget_0, 'Demodulation')
        self.demod_tab_widget_1 = Qt.QWidget()
        self.demod_tab_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.demod_tab_widget_1)
        self.demod_tab_grid_layout_1 = Qt.QGridLayout()
        self.demod_tab_layout_1.addLayout(self.demod_tab_grid_layout_1)
        self.demod_tab.addTab(self.demod_tab_widget_1, 'Stats')
        self.top_grid_layout.addWidget(self.demod_tab, 0, 0, 2, 5)
        for r in range(0, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 5):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._chan_epsilon_range = Range(0, 10., 1./samp_rate, 1., 200)
        self._chan_epsilon_win = RangeWidget(self._chan_epsilon_range, self.set_chan_epsilon, 'epsilon', "counter_slider", float)
        self.ctrl_tab_grid_layout_0.addWidget(self._chan_epsilon_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.ctrl_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.ctrl_tab_grid_layout_0.setColumnStretch(c, 1)
        self._variable_qtgui_label_0_0_tool_bar = Qt.QToolBar(self)

        if None:
          self._variable_qtgui_label_0_0_formatter = None
        else:
          self._variable_qtgui_label_0_0_formatter = lambda x: eng_notation.num_to_str(x)

        self._variable_qtgui_label_0_0_tool_bar.addWidget(Qt.QLabel('subcarrier spacing'+": "))
        self._variable_qtgui_label_0_0_label = Qt.QLabel(str(self._variable_qtgui_label_0_0_formatter(self.variable_qtgui_label_0_0)))
        self._variable_qtgui_label_0_0_tool_bar.addWidget(self._variable_qtgui_label_0_0_label)
        self.demod_tab_grid_layout_1.addWidget(self._variable_qtgui_label_0_0_tool_bar, 1, 1, 1, 1)
        for r in range(1, 2):
            self.demod_tab_grid_layout_1.setRowStretch(r, 1)
        for c in range(1, 2):
            self.demod_tab_grid_layout_1.setColumnStretch(c, 1)
        self._variable_qtgui_label_0_tool_bar = Qt.QToolBar(self)

        if None:
          self._variable_qtgui_label_0_formatter = None
        else:
          self._variable_qtgui_label_0_formatter = lambda x: str(x)

        self._variable_qtgui_label_0_tool_bar.addWidget(Qt.QLabel('Block length'+": "))
        self._variable_qtgui_label_0_label = Qt.QLabel(str(self._variable_qtgui_label_0_formatter(self.variable_qtgui_label_0)))
        self._variable_qtgui_label_0_tool_bar.addWidget(self._variable_qtgui_label_0_label)
        self.demod_tab_grid_layout_1.addWidget(self._variable_qtgui_label_0_tool_bar, 0, 0, 1, 1)
        for r in range(0, 1):
            self.demod_tab_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.demod_tab_grid_layout_1.setColumnStretch(c, 1)
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
        self.qtgui_time_sink_x_0_0_0_2_0_1.set_trigger_mode(qtgui.TRIG_MODE_TAG, qtgui.TRIG_SLOPE_POS, 0.05, 0, 0, 'packet_len')
        self.qtgui_time_sink_x_0_0_0_2_0_1.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_0_2_0_1.enable_grid(True)
        self.qtgui_time_sink_x_0_0_0_2_0_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0_2_0_1.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0_2_0_1.enable_stem_plot(False)

        if not False:
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
        self.sync_tab_grid_layout_0.addWidget(self._qtgui_time_sink_x_0_0_0_2_0_1_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.sync_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.sync_tab_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0_0_2_0_0 = qtgui.time_sink_c(
        	frame_len * 12, #size
        	samp_rate, #samp_rate
        	"Synced Frames", #name
        	2 #number of inputs
        )
        self.qtgui_time_sink_x_0_0_0_2_0_0.set_update_time(0.1)
        self.qtgui_time_sink_x_0_0_0_2_0_0.set_y_axis(-.5, .5)

        self.qtgui_time_sink_x_0_0_0_2_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0_2_0_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_0_0_2_0_0.set_trigger_mode(qtgui.TRIG_MODE_TAG, qtgui.TRIG_SLOPE_POS, 0.05, 0, 0, 'frame_start')
        self.qtgui_time_sink_x_0_0_0_2_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_0_2_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0_0_2_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0_2_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0_2_0_0.enable_stem_plot(False)

        if not False:
          self.qtgui_time_sink_x_0_0_0_2_0_0.disable_legend()

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

        for i in xrange(4):
            if len(labels[i]) == 0:
                if(i % 2 == 0):
                    self.qtgui_time_sink_x_0_0_0_2_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0_0_2_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0_0_2_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0_2_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0_2_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0_2_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0_2_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0_2_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_2_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0_2_0_0.pyqwidget(), Qt.QWidget)
        self.sync_tab_grid_layout_0.addWidget(self._qtgui_time_sink_x_0_0_0_2_0_0_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.sync_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.sync_tab_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0_0_2_0 = qtgui.time_sink_c(
        	frame_len * 12, #size
        	samp_rate, #samp_rate
        	"Fast Sync", #name
        	2 #number of inputs
        )
        self.qtgui_time_sink_x_0_0_0_2_0.set_update_time(0.1)
        self.qtgui_time_sink_x_0_0_0_2_0.set_y_axis(-.5, .5)

        self.qtgui_time_sink_x_0_0_0_2_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0_2_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_0_0_2_0.set_trigger_mode(qtgui.TRIG_MODE_TAG, qtgui.TRIG_SLOPE_POS, 0.05, 2e-5, 2, 'frame_start')
        self.qtgui_time_sink_x_0_0_0_2_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_0_2_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0_0_2_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0_2_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0_2_0.enable_stem_plot(False)

        if not False:
          self.qtgui_time_sink_x_0_0_0_2_0.disable_legend()

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

        for i in xrange(4):
            if len(labels[i]) == 0:
                if(i % 2 == 0):
                    self.qtgui_time_sink_x_0_0_0_2_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0_0_2_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0_0_2_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0_2_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0_2_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0_2_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0_2_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0_2_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_2_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0_2_0.pyqwidget(), Qt.QWidget)
        self.sync_tab_grid_layout_0.addWidget(self._qtgui_time_sink_x_0_0_0_2_0_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.sync_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.sync_tab_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0_0_1 = qtgui.time_sink_c(
        	block_len, #size
        	samp_rate * 0 + 1, #samp_rate
        	"Channel Estimate", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0_0_0_1.set_update_time(0.1)
        self.qtgui_time_sink_x_0_0_0_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0_0_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0_1.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_0_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.05, 0, 0, "frame_start")
        self.qtgui_time_sink_x_0_0_0_1.enable_autoscale(True)
        self.qtgui_time_sink_x_0_0_0_1.enable_grid(True)
        self.qtgui_time_sink_x_0_0_0_1.enable_axis_labels(False)
        self.qtgui_time_sink_x_0_0_0_1.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0_1.enable_stem_plot(False)

        if not True:
          self.qtgui_time_sink_x_0_0_0_1.disable_legend()

        labels = ['Re{estimate}', 'Im{estimate}', '', '', '',
                  '', '', '', '', '']
        widths = [4, 4, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["yellow", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(2):
            if len(labels[i]) == 0:
                if(i % 2 == 0):
                    self.qtgui_time_sink_x_0_0_0_1.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0_0_1.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0_0_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_1_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0_1.pyqwidget(), Qt.QWidget)
        self.demod_tab_grid_layout_0.addWidget(self._qtgui_time_sink_x_0_0_0_1_win, 0, 2, 2, 3)
        for r in range(0, 2):
            self.demod_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(2, 5):
            self.demod_tab_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
        	timeslots * active_subcarriers, #size
        	"RX Constellation", #name
        	2 #number of inputs
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(True)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)

        if not False:
          self.qtgui_const_sink_x_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["green", "red", "red", "red", "red",
                  "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(2):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.pyqwidget(), Qt.QWidget)
        self.demod_tab_grid_layout_0.addWidget(self._qtgui_const_sink_x_0_win, 0, 0, 2, 2)
        for r in range(0, 2):
            self.demod_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 2):
            self.demod_tab_grid_layout_0.setColumnStretch(c, 1)
        self.hier_packet_parser_0 = hier_packet_parser(
            tag_key="rx_len",
        )
        self.hier_packet_formatter_0 = hier_packet_formatter(
            dst_id=84,
            length_tag_name="packet_len",
            src_id=42,
        )
        self.hier_gfdm_receiver_tagged_0 = hier_gfdm_receiver_tagged(
            active_subcarriers=active_subcarriers,
            cp_len=cp_len,
            frame_len=frame_len,
            frame_start_tag_key="frame_start",
            gfdm_constellation=gfdm_constellation,
            ic_iterations=ic_iter_range,
            overlap=overlap,
            ramp_len=ramp_len,
            rx_filter_taps=rx_f_taps,
            subcarrier_map=subcarrier_map,
            subcarriers=fft_len,
            timeslots=timeslots,
            which_estimator=1,
        )
        self.hier_gfdm_fastsync_0 = hier_gfdm_fastsync(
            cp_len=cp_len,
            frame_len=frame_len,
            output_tag_key="frame_start",
            ref_preamble=modulated_preambles[1],
            sc_high_thr=.7,
            sc_low_thr=.6,
            xcorr_det_thr=10.,
        )
        self.gfdm_transmitter_cc_0 = gfdm.transmitter_cc(timeslots, fft_len, active_subcarriers,
                                          cp_len, cs_len, ramp_len, subcarrier_map,
                                          True, overlap, f_taps, window_taps, preamble)
        self.frame_gap_vector_insert = blocks.vector_insert_c((frame_gap), frame_len + len(frame_gap), 0)
        self._frame_dur_tool_bar = Qt.QToolBar(self)

        if None:
          self._frame_dur_formatter = None
        else:
          self._frame_dur_formatter = lambda x: eng_notation.num_to_str(x)

        self._frame_dur_tool_bar.addWidget(Qt.QLabel('Frame Duration'+": "))
        self._frame_dur_label = Qt.QLabel(str(self._frame_dur_formatter(self.frame_dur)))
        self._frame_dur_tool_bar.addWidget(self._frame_dur_label)
        self.demod_tab_grid_layout_1.addWidget(self._frame_dur_tool_bar, 1, 0, 1, 1)
        for r in range(1, 2):
            self.demod_tab_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.demod_tab_grid_layout_1.setColumnStretch(c, 1)
        self.fec_generic_encoder_0 = fec.encoder(var_encoder, gr.sizeof_char, gr.sizeof_char)
        self.fec_generic_decoder_0 = fec.decoder(var_decoder, gr.sizeof_float, gr.sizeof_char)
        self.digital_constellation_soft_decoder_cf_0 = digital.constellation_soft_decoder_cf(gfdm_constellation)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc((gfdm_constellation.points()), 1)
        self._data_rate_tool_bar = Qt.QToolBar(self)

        if None:
          self._data_rate_formatter = None
        else:
          self._data_rate_formatter = lambda x: str(x)

        self._data_rate_tool_bar.addWidget(Qt.QLabel('Data Rate'+": "))
        self._data_rate_label = Qt.QLabel(str(self._data_rate_formatter(self.data_rate)))
        self._data_rate_tool_bar.addWidget(self._data_rate_label)
        self.demod_tab_grid_layout_1.addWidget(self._data_rate_tool_bar, 0, 3, 1, 1)
        for r in range(0, 1):
            self.demod_tab_grid_layout_1.setRowStretch(r, 1)
        for c in range(3, 4):
            self.demod_tab_grid_layout_1.setColumnStretch(c, 1)
        self.channels_channel_model_0 = channels.channel_model(
        	noise_voltage=noise_voltage,
        	frequency_offset=1. * fq_off / samp_rate,
        	epsilon=chan_epsilon,
        	taps=(chan_taps / np.sqrt(np.linalg.norm(chan_taps))),
        	noise_seed=0,
        	block_tags=False
        )
        self.blocks_tag_gate_0 = blocks.tag_gate(gr.sizeof_char * 1, False)
        self.blocks_tag_gate_0.set_single_key("")
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, polar_info_bytes, "rx_len")
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(8, gfdm_constellation.bits_per_symbol(), "", False, gr.GR_MSB_FIRST)
        self.blocks_random_pdu_0 = blocks.random_pdu(polar_info_bytes - 20, polar_info_bytes - 20, chr(0xFF), 1)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vff((-1., ))
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.intern("TEST"), 4.)
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, len(preamble) * 2 + cp_len - 1)
        self.blocks_char_to_float_0_0 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self._bits_per_frame_tool_bar = Qt.QToolBar(self)

        if None:
          self._bits_per_frame_formatter = None
        else:
          self._bits_per_frame_formatter = lambda x: str(x)

        self._bits_per_frame_tool_bar.addWidget(Qt.QLabel('Num bits'+": "))
        self._bits_per_frame_label = Qt.QLabel(str(self._bits_per_frame_formatter(self.bits_per_frame)))
        self._bits_per_frame_tool_bar.addWidget(self._bits_per_frame_label)
        self.demod_tab_grid_layout_1.addWidget(self._bits_per_frame_tool_bar, 0, 2, 1, 1)
        for r in range(0, 1):
            self.demod_tab_grid_layout_1.setRowStretch(r, 1)
        for c in range(2, 3):
            self.demod_tab_grid_layout_1.setColumnStretch(c, 1)
        self._active_symbols_tool_bar = Qt.QToolBar(self)

        if None:
          self._active_symbols_formatter = None
        else:
          self._active_symbols_formatter = lambda x: str(x)

        self._active_symbols_tool_bar.addWidget(Qt.QLabel('Active Symbols'+": "))
        self._active_symbols_label = Qt.QLabel(str(self._active_symbols_formatter(self.active_symbols)))
        self._active_symbols_tool_bar.addWidget(self._active_symbols_label)
        self.demod_tab_grid_layout_1.addWidget(self._active_symbols_tool_bar, 0, 1, 1, 1)
        for r in range(0, 1):
            self.demod_tab_grid_layout_1.setRowStretch(r, 1)
        for c in range(1, 2):
            self.demod_tab_grid_layout_1.setColumnStretch(c, 1)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.blocks_random_pdu_0, 'generate'))
        self.msg_connect((self.blocks_random_pdu_0, 'pdus'), (self.hier_packet_formatter_0, 'in'))
        self.msg_connect((self.hier_packet_parser_0, 'pdu'), (self.blocks_message_debug_0, 'print_pdu'))
        self.connect((self.blocks_char_to_float_0, 0), (self.qtgui_time_sink_x_0_0_0_2_0_1, 0))
        self.connect((self.blocks_char_to_float_0_0, 0), (self.qtgui_time_sink_x_0_0_0_2_0_1, 1))
        self.connect((self.blocks_delay_0, 0), (self.qtgui_time_sink_x_0_0_0_2_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.fec_generic_decoder_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.blocks_char_to_float_0_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.hier_packet_parser_0, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.hier_gfdm_fastsync_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.gfdm_transmitter_cc_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.digital_constellation_soft_decoder_cf_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.fec_generic_decoder_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.fec_generic_encoder_0, 0), (self.blocks_tag_gate_0, 0))
        self.connect((self.frame_gap_vector_insert, 0), (self.blocks_delay_0, 0))
        self.connect((self.frame_gap_vector_insert, 0), (self.channels_channel_model_0, 0))
        self.connect((self.gfdm_transmitter_cc_0, 0), (self.frame_gap_vector_insert, 0))
        self.connect((self.gfdm_transmitter_cc_0, 0), (self.qtgui_time_sink_x_0_0_0_2_0_0, 1))
        self.connect((self.hier_gfdm_fastsync_0, 0), (self.hier_gfdm_receiver_tagged_0, 0))
        self.connect((self.hier_gfdm_fastsync_0, 1), (self.qtgui_time_sink_x_0_0_0_2_0, 1))
        self.connect((self.hier_gfdm_fastsync_0, 0), (self.qtgui_time_sink_x_0_0_0_2_0_0, 0))
        self.connect((self.hier_gfdm_receiver_tagged_0, 1), (self.digital_constellation_soft_decoder_cf_0, 0))
        self.connect((self.hier_gfdm_receiver_tagged_0, 1), (self.qtgui_const_sink_x_0, 1))
        self.connect((self.hier_gfdm_receiver_tagged_0, 0), (self.qtgui_time_sink_x_0_0_0_1, 0))
        self.connect((self.hier_packet_formatter_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.hier_packet_formatter_0, 0), (self.fec_generic_encoder_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "gfdm_fast_sync_demo")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_timeslots(self):
        return self.timeslots

    def set_timeslots(self, timeslots):
        self.timeslots = timeslots
        self.set_window_taps(cyclic_prefix.get_raised_cosine_ramp(self.ramp_len, cyclic_prefix.get_window_len(self.cp_len, self.timeslots, self.fft_len, self.cs_len)))
        self.set_f_taps(filters.get_frequency_domain_filter('rrc', .2, self.timeslots, self.fft_len, self.overlap))
        self.set_block_len(self.timeslots * self.fft_len)
        self.hier_gfdm_receiver_tagged_0.set_timeslots(self.timeslots)
        self.set_active_symbols(self._active_symbols_formatter(self.timeslots * self.active_subcarriers))

    def get_fft_len(self):
        return self.fft_len

    def set_fft_len(self, fft_len):
        self.fft_len = fft_len
        self.set_window_taps(cyclic_prefix.get_raised_cosine_ramp(self.ramp_len, cyclic_prefix.get_window_len(self.cp_len, self.timeslots, self.fft_len, self.cs_len)))
        self.set_subcarrier_map(mapping.get_subcarrier_map(self.fft_len, self.active_subcarriers, dc_free=True))
        self.set_modulated_preambles(pre_module.mapped_preamble(self.seed, 'rrc', .2, self.active_subcarriers, self.fft_len, self.subcarrier_map, self.overlap, self.cp_len, self.ramp_len))
        self.set_f_taps(filters.get_frequency_domain_filter('rrc', .2, self.timeslots, self.fft_len, self.overlap))
        self.set_cp_len(self.fft_len // 2)
        self.set_block_len(self.timeslots * self.fft_len)
        self.set_variable_qtgui_label_0_0(self._variable_qtgui_label_0_0_formatter(self.samp_rate / self.fft_len))
        self.hier_gfdm_receiver_tagged_0.set_subcarriers(self.fft_len)

    def get_active_subcarriers(self):
        return self.active_subcarriers

    def set_active_subcarriers(self, active_subcarriers):
        self.active_subcarriers = active_subcarriers
        self.set_subcarrier_map(mapping.get_subcarrier_map(self.fft_len, self.active_subcarriers, dc_free=True))
        self.set_modulated_preambles(pre_module.mapped_preamble(self.seed, 'rrc', .2, self.active_subcarriers, self.fft_len, self.subcarrier_map, self.overlap, self.cp_len, self.ramp_len))
        self.hier_gfdm_receiver_tagged_0.set_active_subcarriers(self.active_subcarriers)
        self.set_active_symbols(self._active_symbols_formatter(self.timeslots * self.active_subcarriers))

    def get_gfdm_constellation(self):
        return self.gfdm_constellation

    def set_gfdm_constellation(self, gfdm_constellation):
        self.gfdm_constellation = gfdm_constellation
        self.hier_gfdm_receiver_tagged_0.set_gfdm_constellation(self.gfdm_constellation)

    def get_cp_len(self):
        return self.cp_len

    def set_cp_len(self, cp_len):
        self.cp_len = cp_len
        self.set_window_taps(cyclic_prefix.get_raised_cosine_ramp(self.ramp_len, cyclic_prefix.get_window_len(self.cp_len, self.timeslots, self.fft_len, self.cs_len)))
        self.set_modulated_preambles(pre_module.mapped_preamble(self.seed, 'rrc', .2, self.active_subcarriers, self.fft_len, self.subcarrier_map, self.overlap, self.cp_len, self.ramp_len))
        self.set_cs_len(self.cp_len // 2)
        self.set_window_len(self.block_len + self.cp_len + self.cs_len)
        self.hier_gfdm_receiver_tagged_0.set_cp_len(self.cp_len)
        self.hier_gfdm_fastsync_0.set_cp_len(self.cp_len)
        self.blocks_delay_0.set_dly(len(self.preamble) * 2 + self.cp_len - 1)

    def get_active_symbols(self):
        return self.active_symbols

    def set_active_symbols(self, active_symbols):
        self.active_symbols = active_symbols
        self.set_bits_per_frame(self._bits_per_frame_formatter(int(np.log2(len(gfdm_constellation.points() ) )) * self.active_symbols))
        Qt.QMetaObject.invokeMethod(self._active_symbols_label, "setText", Qt.Q_ARG("QString", self.active_symbols))

    def get_cs_len(self):
        return self.cs_len

    def set_cs_len(self, cs_len):
        self.cs_len = cs_len
        self.set_window_taps(cyclic_prefix.get_raised_cosine_ramp(self.ramp_len, cyclic_prefix.get_window_len(self.cp_len, self.timeslots, self.fft_len, self.cs_len)))
        self.set_ramp_len(self.cs_len)
        self.set_window_len(self.block_len + self.cp_len + self.cs_len)

    def get_bits_per_frame(self):
        return self.bits_per_frame

    def set_bits_per_frame(self, bits_per_frame):
        self.bits_per_frame = bits_per_frame
        self.set_bytes_per_frame(int(self.bits_per_frame // 8))
        self.set_data_rate(self._data_rate_formatter(int(1000. * self.bits_per_frame)))
        Qt.QMetaObject.invokeMethod(self._bits_per_frame_label, "setText", Qt.Q_ARG("QString", self.bits_per_frame))

    def get_subcarrier_map(self):
        return self.subcarrier_map

    def set_subcarrier_map(self, subcarrier_map):
        self.subcarrier_map = subcarrier_map
        self.set_modulated_preambles(pre_module.mapped_preamble(self.seed, 'rrc', .2, self.active_subcarriers, self.fft_len, self.subcarrier_map, self.overlap, self.cp_len, self.ramp_len))
        self.hier_gfdm_receiver_tagged_0.set_subcarrier_map(self.subcarrier_map)

    def get_seed(self):
        return self.seed

    def set_seed(self, seed):
        self.seed = seed
        self.set_modulated_preambles(pre_module.mapped_preamble(self.seed, 'rrc', .2, self.active_subcarriers, self.fft_len, self.subcarrier_map, self.overlap, self.cp_len, self.ramp_len))

    def get_ramp_len(self):
        return self.ramp_len

    def set_ramp_len(self, ramp_len):
        self.ramp_len = ramp_len
        self.set_window_taps(cyclic_prefix.get_raised_cosine_ramp(self.ramp_len, cyclic_prefix.get_window_len(self.cp_len, self.timeslots, self.fft_len, self.cs_len)))
        self.set_modulated_preambles(pre_module.mapped_preamble(self.seed, 'rrc', .2, self.active_subcarriers, self.fft_len, self.subcarrier_map, self.overlap, self.cp_len, self.ramp_len))
        self.hier_gfdm_receiver_tagged_0.set_ramp_len(self.ramp_len)

    def get_overlap(self):
        return self.overlap

    def set_overlap(self, overlap):
        self.overlap = overlap
        self.set_modulated_preambles(pre_module.mapped_preamble(self.seed, 'rrc', .2, self.active_subcarriers, self.fft_len, self.subcarrier_map, self.overlap, self.cp_len, self.ramp_len))
        self.set_f_taps(filters.get_frequency_domain_filter('rrc', .2, self.timeslots, self.fft_len, self.overlap))
        self.hier_gfdm_receiver_tagged_0.set_overlap(self.overlap)

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

    def get_modulated_preambles(self):
        return self.modulated_preambles

    def set_modulated_preambles(self, modulated_preambles):
        self.modulated_preambles = modulated_preambles
        self.set_preamble(self.modulated_preambles[0])
        self.hier_gfdm_fastsync_0.set_ref_preamble(self.modulated_preambles[1])

    def get_block_len(self):
        return self.block_len

    def set_block_len(self, block_len):
        self.block_len = block_len
        self.set_window_len(self.block_len + self.cp_len + self.cs_len)
        self.set_variable_qtgui_label_0(self._variable_qtgui_label_0_formatter(self.block_len))

    def get_window_len(self):
        return self.window_len

    def set_window_len(self, window_len):
        self.window_len = window_len
        self.set_frame_len(self.window_len + len(self.preamble))

    def get_preamble(self):
        return self.preamble

    def set_preamble(self, preamble):
        self.preamble = preamble
        self.set_frame_len(self.window_len + len(self.preamble))
        self.set_preamble_len(len(self.preamble))
        self.blocks_delay_0.set_dly(len(self.preamble) * 2 + self.cp_len - 1)

    def get_polar_info_size(self):
        return self.polar_info_size

    def set_polar_info_size(self, polar_info_size):
        self.polar_info_size = polar_info_size
        self.set_polar_info_bytes(self.polar_info_size // 8 - 1)
        self.set_frozen_bit_positions(pypolar.frozen_bits(self.polar_block_size, self.polar_info_size, 0.0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_frame_gap(np.zeros(int(1. * self.samp_rate / 1000.) - self.frame_len))
        self.set_variable_qtgui_label_0_0(self._variable_qtgui_label_0_0_formatter(self.samp_rate / self.fft_len))
        self.qtgui_time_sink_x_0_0_0_2_0_1.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0_0_2_0_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0_0_2_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0_0_1.set_samp_rate(self.samp_rate * 0 + 1)
        self.set_frame_dur(self._frame_dur_formatter(1. * self.frame_len / self.samp_rate))
        self.channels_channel_model_0.set_frequency_offset(1. * self.fq_off / self.samp_rate)

    def get_frozen_bit_positions(self):
        return self.frozen_bit_positions

    def set_frozen_bit_positions(self, frozen_bit_positions):
        self.frozen_bit_positions = frozen_bit_positions

    def get_frame_len(self):
        return self.frame_len

    def set_frame_len(self, frame_len):
        self.frame_len = frame_len
        self.set_frame_gap(np.zeros(int(1. * self.samp_rate / 1000.) - self.frame_len))
        self.hier_gfdm_receiver_tagged_0.set_frame_len(self.frame_len)
        self.hier_gfdm_fastsync_0.set_frame_len(self.frame_len)
        self.set_frame_dur(self._frame_dur_formatter(1. * self.frame_len / self.samp_rate))

    def get_f_taps(self):
        return self.f_taps

    def set_f_taps(self, f_taps):
        self.f_taps = f_taps
        self.set_rx_f_taps(np.conjugate(self.f_taps))

    def get_window_taps(self):
        return self.window_taps

    def set_window_taps(self, window_taps):
        self.window_taps = window_taps

    def get_variable_qtgui_label_0_0(self):
        return self.variable_qtgui_label_0_0

    def set_variable_qtgui_label_0_0(self, variable_qtgui_label_0_0):
        self.variable_qtgui_label_0_0 = variable_qtgui_label_0_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_0_label, "setText", Qt.Q_ARG("QString", self.variable_qtgui_label_0_0))

    def get_variable_qtgui_label_0(self):
        return self.variable_qtgui_label_0

    def set_variable_qtgui_label_0(self, variable_qtgui_label_0):
        self.variable_qtgui_label_0 = variable_qtgui_label_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_label, "setText", Qt.Q_ARG("QString", self.variable_qtgui_label_0))

    def get_var_encoder(self):
        return self.var_encoder

    def set_var_encoder(self, var_encoder):
        self.var_encoder = var_encoder

    def get_var_decoder(self):
        return self.var_decoder

    def set_var_decoder(self, var_decoder):
        self.var_decoder = var_decoder

    def get_rx_f_taps(self):
        return self.rx_f_taps

    def set_rx_f_taps(self, rx_f_taps):
        self.rx_f_taps = rx_f_taps
        self.hier_gfdm_receiver_tagged_0.set_rx_filter_taps(self.rx_f_taps)

    def get_preamble_len(self):
        return self.preamble_len

    def set_preamble_len(self, preamble_len):
        self.preamble_len = preamble_len

    def get_polar_info_bytes(self):
        return self.polar_info_bytes

    def set_polar_info_bytes(self, polar_info_bytes):
        self.polar_info_bytes = polar_info_bytes
        self.blocks_stream_to_tagged_stream_0.set_packet_len(self.polar_info_bytes)
        self.blocks_stream_to_tagged_stream_0.set_packet_len_pmt(self.polar_info_bytes)

    def get_noise_voltage(self):
        return self.noise_voltage

    def set_noise_voltage(self, noise_voltage):
        self.noise_voltage = noise_voltage
        self.channels_channel_model_0.set_noise_voltage(self.noise_voltage)

    def get_ic_iter_range(self):
        return self.ic_iter_range

    def set_ic_iter_range(self, ic_iter_range):
        self.ic_iter_range = ic_iter_range
        self.hier_gfdm_receiver_tagged_0.set_ic_iterations(self.ic_iter_range)

    def get_frame_gap(self):
        return self.frame_gap

    def set_frame_gap(self, frame_gap):
        self.frame_gap = frame_gap

    def get_frame_dur(self):
        return self.frame_dur

    def set_frame_dur(self, frame_dur):
        self.frame_dur = frame_dur
        Qt.QMetaObject.invokeMethod(self._frame_dur_label, "setText", Qt.Q_ARG("QString", self.frame_dur))

    def get_fq_off(self):
        return self.fq_off

    def set_fq_off(self, fq_off):
        self.fq_off = fq_off
        self.channels_channel_model_0.set_frequency_offset(1. * self.fq_off / self.samp_rate)

    def get_data_rate(self):
        return self.data_rate

    def set_data_rate(self, data_rate):
        self.data_rate = data_rate
        Qt.QMetaObject.invokeMethod(self._data_rate_label, "setText", Qt.Q_ARG("QString", self.data_rate))

    def get_chan_taps(self):
        return self.chan_taps

    def set_chan_taps(self, chan_taps):
        self.chan_taps = chan_taps
        self.channels_channel_model_0.set_taps((self.chan_taps / np.sqrt(np.linalg.norm(self.chan_taps))))

    def get_chan_epsilon(self):
        return self.chan_epsilon

    def set_chan_epsilon(self, chan_epsilon):
        self.chan_epsilon = chan_epsilon
        self.channels_channel_model_0.set_timing_offset(self.chan_epsilon)


def main(top_block_cls=gfdm_fast_sync_demo, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start(1024)
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
