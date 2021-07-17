#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Main Schema
# Author: rcampello
# GNU Radio version: 3.8.2.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from ASKrcvr_cb import ASKrcvr_cb  # grc-generated hier_block
from ASKxmtr_bc import ASKxmtr_bc  # grc-generated hier_block
from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
from gnuradio import gr
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
import pmt

from gnuradio import qtgui

class ASK_test002(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Main Schema")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Main Schema")
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

        self.settings = Qt.QSettings("GNU Radio", "ASK_test002")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.thc_Xmtr = thc_Xmtr = 0
        self.tag0 = tag0 = gr.tag_utils.python_to_tag((0, pmt.intern("T"), pmt.intern("0x54"), pmt.intern("vec src")))
        self.sym_dly = sym_dly = 0
        self.sps = sps = 16
        self.samp_dly = samp_dly = 0
        self.ptype = ptype = 'rect'
        self.pparms = pparms = (5, 0.3)
        self.pol = pol = 0
        self.gain = gain = 1
        self.fc_Xmtr = fc_Xmtr = 50000
        self.fc = fc = 50000
        self.bpsym = bpsym = 1
        self.Q_gain = Q_gain = 1
        self.I_gain = I_gain = 1
        self.Fs = Fs = 512000
        self.FB = FB = 32000

        ##################################################
        # Blocks
        ##################################################
        self._thc_Xmtr_range = Range(-180, 180, 1, 0, 200)
        self._thc_Xmtr_win = RangeWidget(self._thc_Xmtr_range, self.set_thc_Xmtr, 'thc_Xmtr', "counter_slider", float)
        self.top_grid_layout.addWidget(self._thc_Xmtr_win)
        self._sym_dly_range = Range(0, 16, 1, 0, 200)
        self._sym_dly_win = RangeWidget(self._sym_dly_range, self.set_sym_dly, 'sym_dly', "counter_slider", float)
        self.top_grid_layout.addWidget(self._sym_dly_win)
        self._samp_dly_range = Range(0, 32, 1, 0, 200)
        self._samp_dly_win = RangeWidget(self._samp_dly_range, self.set_samp_dly, 'samp_dly', "counter_slider", float)
        self.top_grid_layout.addWidget(self._samp_dly_win)
        # Create the options list
        self._ptype_options = ('rect', 'tri', 'rcf', 'rrcf', )
        # Create the labels list
        self._ptype_labels = ('rect', 'tri', 'rcf', 'rrcf', )
        # Create the combo box
        # Create the radio buttons
        self._ptype_group_box = Qt.QGroupBox('ptype' + ": ")
        self._ptype_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._ptype_button_group = variable_chooser_button_group()
        self._ptype_group_box.setLayout(self._ptype_box)
        for i, _label in enumerate(self._ptype_labels):
            radio_button = Qt.QRadioButton(_label)
            self._ptype_box.addWidget(radio_button)
            self._ptype_button_group.addButton(radio_button, i)
        self._ptype_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ptype_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._ptype_options.index(i)))
        self._ptype_callback(self.ptype)
        self._ptype_button_group.buttonClicked[int].connect(
            lambda i: self.set_ptype(self._ptype_options[i]))
        self.top_grid_layout.addWidget(self._ptype_group_box)
        # Create the options list
        self._pol_options = (0, 1, )
        # Create the labels list
        self._pol_labels = ('0', '1', )
        # Create the combo box
        self._pol_tool_bar = Qt.QToolBar(self)
        self._pol_tool_bar.addWidget(Qt.QLabel('pol' + ": "))
        self._pol_combo_box = Qt.QComboBox()
        self._pol_tool_bar.addWidget(self._pol_combo_box)
        for _label in self._pol_labels: self._pol_combo_box.addItem(_label)
        self._pol_callback = lambda i: Qt.QMetaObject.invokeMethod(self._pol_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._pol_options.index(i)))
        self._pol_callback(self.pol)
        self._pol_combo_box.currentIndexChanged.connect(
            lambda i: self.set_pol(self._pol_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._pol_tool_bar)
        self._fc_Xmtr_range = Range(-100000, 100000, 0.1, 50000, 200)
        self._fc_Xmtr_win = RangeWidget(self._fc_Xmtr_range, self.set_fc_Xmtr, 'fc_Xmtr', "counter_slider", float)
        self.top_grid_layout.addWidget(self._fc_Xmtr_win)
        self._Q_gain_range = Range(0, 4, 0.1, 1, 200)
        self._Q_gain_win = RangeWidget(self._Q_gain_range, self.set_Q_gain, 'Q_gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._Q_gain_win)
        self._I_gain_range = Range(0, 4, 0.1, 1, 200)
        self._I_gain_win = RangeWidget(self._I_gain_range, self.set_I_gain, 'I_gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._I_gain_win)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_c(
            1024, #size
            Fs, #samp_rate
            "", #name
            2 #number of inputs
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1.enable_tags(True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(False)
        self.qtgui_time_sink_x_1.enable_grid(False)
        self.qtgui_time_sink_x_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1.enable_control_panel(False)
        self.qtgui_time_sink_x_1.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(4):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_1.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_1.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_1_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            1024, #size
            Fs, #samp_rate
            "", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            Fs, #bw
            "", #name
            1
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            1024, #size
            "", #name
            1 #number of inputs
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(False)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
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
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_win)
        self._gain_range = Range(0, 4, 0.1, 1, 200)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, 'gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._gain_win)
        self.blocks_vector_source_x_0 = blocks.vector_source_b(list(ord(i) for i in "The quick brown fox...\n"), True, 1, [tag0])
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, FB,True)
        self.blocks_null_sink_0_0_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_file_sink_0_0_0 = blocks.file_sink(gr.sizeof_char*1, '/dev/pts/7', False)
        self.blocks_file_sink_0_0_0.set_unbuffered(False)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_char*1, '/dev/pts/6', False)
        self.blocks_file_sink_0_0.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, '/dev/pts/5', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.ASKxmtr_bc_0 = ASKxmtr_bc(
            a_FB=FB,
            b_bpsym=bpsym,
            c_pol=pol,
            d_sps=sps,
            e_ptype=ptype,
            f_pparms=pparms,
            g_fcparms=(fc_Xmtr, thc_Xmtr),
        )
        self.ASKrcvr_cb_0 = ASKrcvr_cb(
            a_gain=1,
            b_FB=FB,
            c_bpsym=bpsym * (1 + 1j),
            d_pol=pol,
            e_sps=sps,
            f_ptype=ptype,
            g_pparms=pparms,
            h_fcparms=(fc_Xmtr, thc_Xmtr),
            i_IQgain=I_gain + 1j * Q_gain,
            j_samp_dly=samp_dly,
            k_sym_dly=sym_dly,
        )



        ##################################################
        # Connections
        ##################################################
        self.connect((self.ASKrcvr_cb_0, 3), (self.blocks_file_sink_0, 0))
        self.connect((self.ASKrcvr_cb_0, 4), (self.blocks_file_sink_0_0, 0))
        self.connect((self.ASKrcvr_cb_0, 5), (self.blocks_file_sink_0_0_0, 0))
        self.connect((self.ASKrcvr_cb_0, 3), (self.blocks_null_sink_0, 0))
        self.connect((self.ASKrcvr_cb_0, 4), (self.blocks_null_sink_0_0, 0))
        self.connect((self.ASKrcvr_cb_0, 5), (self.blocks_null_sink_0_0_0, 0))
        self.connect((self.ASKrcvr_cb_0, 2), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.ASKrcvr_cb_0, 0), (self.qtgui_time_sink_x_1, 0))
        self.connect((self.ASKrcvr_cb_0, 1), (self.qtgui_time_sink_x_1, 1))
        self.connect((self.ASKxmtr_bc_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.ASKrcvr_cb_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.ASKxmtr_bc_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ASK_test002")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_thc_Xmtr(self):
        return self.thc_Xmtr

    def set_thc_Xmtr(self, thc_Xmtr):
        self.thc_Xmtr = thc_Xmtr
        self.ASKrcvr_cb_0.set_h_fcparms((self.fc_Xmtr, self.thc_Xmtr))
        self.ASKxmtr_bc_0.set_g_fcparms((self.fc_Xmtr, self.thc_Xmtr))

    def get_tag0(self):
        return self.tag0

    def set_tag0(self, tag0):
        self.tag0 = tag0
        self.blocks_vector_source_x_0.set_data(list(ord(i) for i in "The quick brown fox...\n"), [self.tag0])

    def get_sym_dly(self):
        return self.sym_dly

    def set_sym_dly(self, sym_dly):
        self.sym_dly = sym_dly
        self.ASKrcvr_cb_0.set_k_sym_dly(self.sym_dly)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.ASKrcvr_cb_0.set_e_sps(self.sps)
        self.ASKxmtr_bc_0.set_d_sps(self.sps)

    def get_samp_dly(self):
        return self.samp_dly

    def set_samp_dly(self, samp_dly):
        self.samp_dly = samp_dly
        self.ASKrcvr_cb_0.set_j_samp_dly(self.samp_dly)

    def get_ptype(self):
        return self.ptype

    def set_ptype(self, ptype):
        self.ptype = ptype
        self._ptype_callback(self.ptype)
        self.ASKrcvr_cb_0.set_f_ptype(self.ptype)
        self.ASKxmtr_bc_0.set_e_ptype(self.ptype)

    def get_pparms(self):
        return self.pparms

    def set_pparms(self, pparms):
        self.pparms = pparms
        self.ASKrcvr_cb_0.set_g_pparms(self.pparms)
        self.ASKxmtr_bc_0.set_f_pparms(self.pparms)

    def get_pol(self):
        return self.pol

    def set_pol(self, pol):
        self.pol = pol
        self._pol_callback(self.pol)
        self.ASKrcvr_cb_0.set_d_pol(self.pol)
        self.ASKxmtr_bc_0.set_c_pol(self.pol)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain

    def get_fc_Xmtr(self):
        return self.fc_Xmtr

    def set_fc_Xmtr(self, fc_Xmtr):
        self.fc_Xmtr = fc_Xmtr
        self.ASKrcvr_cb_0.set_h_fcparms((self.fc_Xmtr, self.thc_Xmtr))
        self.ASKxmtr_bc_0.set_g_fcparms((self.fc_Xmtr, self.thc_Xmtr))

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc

    def get_bpsym(self):
        return self.bpsym

    def set_bpsym(self, bpsym):
        self.bpsym = bpsym
        self.ASKrcvr_cb_0.set_c_bpsym(self.bpsym * (1 + 1j))
        self.ASKxmtr_bc_0.set_b_bpsym(self.bpsym)

    def get_Q_gain(self):
        return self.Q_gain

    def set_Q_gain(self, Q_gain):
        self.Q_gain = Q_gain
        self.ASKrcvr_cb_0.set_i_IQgain(self.I_gain + 1j * self.Q_gain)

    def get_I_gain(self):
        return self.I_gain

    def set_I_gain(self, I_gain):
        self.I_gain = I_gain
        self.ASKrcvr_cb_0.set_i_IQgain(self.I_gain + 1j * self.Q_gain)

    def get_Fs(self):
        return self.Fs

    def set_Fs(self, Fs):
        self.Fs = Fs
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.Fs)
        self.qtgui_time_sink_x_0.set_samp_rate(self.Fs)
        self.qtgui_time_sink_x_1.set_samp_rate(self.Fs)

    def get_FB(self):
        return self.FB

    def set_FB(self, FB):
        self.FB = FB
        self.ASKrcvr_cb_0.set_b_FB(self.FB)
        self.ASKxmtr_bc_0.set_a_FB(self.FB)
        self.blocks_throttle_0.set_sample_rate(self.FB)





def main(top_block_cls=ASK_test002, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
