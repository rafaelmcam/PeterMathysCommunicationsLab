#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: teste
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

from ASKxmtr_bc import ASKxmtr_bc  # grc-generated hier_block
from PyQt5 import Qt
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
from mfzerocc import mfzerocc  # grc-generated hier_block

from gnuradio import qtgui

class teste(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "teste")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("teste")
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

        self.settings = Qt.QSettings("GNU Radio", "teste")

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
        self.sps = sps = 16
        self.samp_rate = samp_rate = 32000
        self.pparms = pparms = (5, 0.3)
        self.gain = gain = 1
        self.fc = fc = 50000
        self.dly = dly = 0
        self.bpsym = bpsym = 1
        self.Fs = Fs = 512000
        self.FB = FB = 32000

        ##################################################
        # Blocks
        ##################################################
        self._gain_range = Range(0, 1000, 1, 1, 200)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, 'gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._gain_win)
        self._dly_range = Range(0, 100, 1, 0, 200)
        self._dly_win = RangeWidget(self._dly_range, self.set_dly, 'dly', "counter_slider", int)
        self.top_grid_layout.addWidget(self._dly_win)
        self.qtgui_time_sink_x_2_1_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "Tx", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_2_1_0.set_update_time(0.10)
        self.qtgui_time_sink_x_2_1_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_2_1_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_2_1_0.enable_tags(True)
        self.qtgui_time_sink_x_2_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_2_1_0.enable_autoscale(False)
        self.qtgui_time_sink_x_2_1_0.enable_grid(False)
        self.qtgui_time_sink_x_2_1_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_2_1_0.enable_control_panel(False)
        self.qtgui_time_sink_x_2_1_0.enable_stem_plot(False)


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
                    self.qtgui_time_sink_x_2_1_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_2_1_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_2_1_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_2_1_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_2_1_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_2_1_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_2_1_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_2_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_2_1_0_win = sip.wrapinstance(self.qtgui_time_sink_x_2_1_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_2_1_0_win)
        self.qtgui_time_sink_x_2_1 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "Probe", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_2_1.set_update_time(0.10)
        self.qtgui_time_sink_x_2_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_2_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_2_1.enable_tags(True)
        self.qtgui_time_sink_x_2_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_2_1.enable_autoscale(False)
        self.qtgui_time_sink_x_2_1.enable_grid(False)
        self.qtgui_time_sink_x_2_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_2_1.enable_control_panel(False)
        self.qtgui_time_sink_x_2_1.enable_stem_plot(False)


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


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_2_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_2_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_2_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_2_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_2_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_2_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_2_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_2_1_win = sip.wrapinstance(self.qtgui_time_sink_x_2_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_2_1_win)
        self.qtgui_time_sink_x_2 = qtgui.time_sink_f(
            1024, #size
            Fs, #samp_rate
            "Final", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_2.set_update_time(0.10)
        self.qtgui_time_sink_x_2.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_2.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_2.enable_tags(True)
        self.qtgui_time_sink_x_2.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_2.enable_autoscale(True)
        self.qtgui_time_sink_x_2.enable_grid(False)
        self.qtgui_time_sink_x_2.enable_axis_labels(True)
        self.qtgui_time_sink_x_2.enable_control_panel(False)
        self.qtgui_time_sink_x_2.enable_stem_plot(False)


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


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_2.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_2.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_2.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_2.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_2.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_2.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_2.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_2_win = sip.wrapinstance(self.qtgui_time_sink_x_2.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_2_win)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_c(
            1024, #size
            Fs, #samp_rate
            "", #name
            1 #number of inputs
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


        for i in range(2):
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
        self.mfzerocc_0 = mfzerocc(
            a_gain=gain,
            b_FB=32000,
            c_sps=16,
            d_ptype="rect",
            e_pparms=[5, 0.3],
            f_fcparms=[50000, 0],
            g_samp_dly=0,
        )
        self.blocks_vector_source_x_0_1 = blocks.vector_source_b(list(ord(i) for i in "The quick brown fox...\n"), True, 1, [])
        self.blocks_unpacked_to_packed_xx_0 = blocks.unpacked_to_packed_bb(1, gr.GR_MSB_FIRST)
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_throttle_0_1 = blocks.throttle(gr.sizeof_gr_complex*1, Fs,True)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_ff(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(1)
        self.blocks_float_to_uchar_0 = blocks.float_to_uchar()
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, '/dev/pts/5', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_char*1, dly)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff(0)
        self.ASKxmtr_bc_0_0 = ASKxmtr_bc(
            a_FB=32000,
            b_bpsym=1,
            c_pol=1,
            d_sps=16,
            e_ptype="rect",
            f_pparms=[5, 0.3],
            g_fcparms=(50000, 0),
        )



        ##################################################
        # Connections
        ##################################################
        self.connect((self.ASKxmtr_bc_0_0, 0), (self.blocks_throttle_0_1, 0))
        self.connect((self.ASKxmtr_bc_0_0, 0), (self.mfzerocc_0, 0))
        self.connect((self.ASKxmtr_bc_0_0, 0), (self.qtgui_time_sink_x_2_1_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_unpacked_to_packed_xx_0, 0))
        self.connect((self.blocks_float_to_uchar_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_time_sink_x_2_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_float_to_uchar_0, 0))
        self.connect((self.blocks_throttle_0_1, 0), (self.qtgui_time_sink_x_1, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.qtgui_time_sink_x_2, 0))
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.blocks_uchar_to_float_0, 0))
        self.connect((self.blocks_vector_source_x_0_1, 0), (self.ASKxmtr_bc_0_0, 0))
        self.connect((self.mfzerocc_0, 1), (self.blocks_complex_to_mag_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "teste")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_time_sink_x_2_1.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_2_1_0.set_samp_rate(self.samp_rate)

    def get_pparms(self):
        return self.pparms

    def set_pparms(self, pparms):
        self.pparms = pparms

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.mfzerocc_0.set_a_gain(self.gain)

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc

    def get_dly(self):
        return self.dly

    def set_dly(self, dly):
        self.dly = dly
        self.blocks_delay_0.set_dly(self.dly)

    def get_bpsym(self):
        return self.bpsym

    def set_bpsym(self, bpsym):
        self.bpsym = bpsym

    def get_Fs(self):
        return self.Fs

    def set_Fs(self, Fs):
        self.Fs = Fs
        self.blocks_throttle_0_1.set_sample_rate(self.Fs)
        self.qtgui_time_sink_x_1.set_samp_rate(self.Fs)
        self.qtgui_time_sink_x_2.set_samp_rate(self.Fs)

    def get_FB(self):
        return self.FB

    def set_FB(self, FB):
        self.FB = FB





def main(top_block_cls=teste, options=None):

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
