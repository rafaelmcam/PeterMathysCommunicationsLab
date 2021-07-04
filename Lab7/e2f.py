#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: e2f
# Author: rcampello
# GNU Radio version: 3.8.1.0

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

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
import pmt
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
import cmath
from gnuradio import qtgui

class e2f(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "e2f")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("e2f")
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

        self.settings = Qt.QSettings("GNU Radio", "e2f")

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
        self.theta = theta = 0
        self.samp_rate2 = samp_rate2 = 240000
        self.samp_rate1 = samp_rate1 = 48000
        self.real_mult = real_mult = 1
        self.imag_mult = imag_mult = 0
        self.fc_fine = fc_fine = 0
        self.fc = fc = -23000

        ##################################################
        # Blocks
        ##################################################
        self._theta_range = Range(0, 360, 1, 0, 200)
        self._theta_win = RangeWidget(self._theta_range, self.set_theta, 'theta', "counter_slider", float)
        self.top_grid_layout.addWidget(self._theta_win)
        self._real_mult_range = Range(0, 1, 0.1, 1, 200)
        self._real_mult_win = RangeWidget(self._real_mult_range, self.set_real_mult, 'real_mult', "counter_slider", float)
        self.top_grid_layout.addWidget(self._real_mult_win)
        self._imag_mult_range = Range(0, 1, 0.1, 0, 200)
        self._imag_mult_win = RangeWidget(self._imag_mult_range, self.set_imag_mult, 'imag_mult', "counter_slider", float)
        self.top_grid_layout.addWidget(self._imag_mult_win)
        self._fc_fine_range = Range(-1, 1, 1e-6, 0, 200)
        self._fc_fine_win = RangeWidget(self._fc_fine_range, self.set_fc_fine, 'fc_fine', "counter_slider", float)
        self.top_grid_layout.addWidget(self._fc_fine_win)
        self._fc_range = Range(-120000, 0, 1, -23000, 200)
        self._fc_win = RangeWidget(self._fc_range, self.set_fc, 'fc', "counter_slider", float)
        self.top_grid_layout.addWidget(self._fc_win)
        self.qtgui_sink_x_0_0 = qtgui.sink_c(
            4096, #fftsize
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate1 // 8, #bw
            "RCV", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True #plotconst
        )
        self.qtgui_sink_x_0_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_0_win = sip.wrapinstance(self.qtgui_sink_x_0_0.pyqwidget(), Qt.QWidget)

        self.qtgui_sink_x_0_0.enable_rf_freq(False)

        self.top_grid_layout.addWidget(self._qtgui_sink_x_0_0_win)
        self.qtgui_sink_x_0 = qtgui.sink_c(
            4096, #fftsize
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate1 // 8, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(False)

        self.top_grid_layout.addWidget(self._qtgui_sink_x_0_win)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            int(samp_rate2 / samp_rate1),
            firdes.low_pass(
                1,
                samp_rate2,
                3000,
                2000,
                firdes.WIN_HAMMING,
                6.76))
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate2,True)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_1_0 = blocks.multiply_const_ff(imag_mult)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_ff(real_mult)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(cmath.exp(1j * cmath.pi / 180 * theta))
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/rcampello/Main/3m/Simulação de sistemas de comunicação/Labs/Lab7/Files/AMsignal_005.bin', True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.audio_sink_0_0 = audio.sink(samp_rate1, '', True)
        self.audio_sink_0 = audio.sink(samp_rate1, '', True)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate2, analog.GR_COS_WAVE, fc_fine, 1, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate2, analog.GR_COS_WAVE, fc, 1, 0, 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_complex_to_float_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_complex_to_float_0, 1), (self.blocks_multiply_const_vxx_1_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_sink_x_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1_0, 0), (self.audio_sink_0_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_sink_x_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "e2f")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_theta(self):
        return self.theta

    def set_theta(self, theta):
        self.theta = theta
        self.blocks_multiply_const_vxx_0.set_k(cmath.exp(1j * cmath.pi / 180 * self.theta))

    def get_samp_rate2(self):
        return self.samp_rate2

    def set_samp_rate2(self, samp_rate2):
        self.samp_rate2 = samp_rate2
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate2)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate2)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate2)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate2, 3000, 2000, firdes.WIN_HAMMING, 6.76))

    def get_samp_rate1(self):
        return self.samp_rate1

    def set_samp_rate1(self, samp_rate1):
        self.samp_rate1 = samp_rate1
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate1 // 8)
        self.qtgui_sink_x_0_0.set_frequency_range(0, self.samp_rate1 // 8)

    def get_real_mult(self):
        return self.real_mult

    def set_real_mult(self, real_mult):
        self.real_mult = real_mult
        self.blocks_multiply_const_vxx_1.set_k(self.real_mult)

    def get_imag_mult(self):
        return self.imag_mult

    def set_imag_mult(self, imag_mult):
        self.imag_mult = imag_mult
        self.blocks_multiply_const_vxx_1_0.set_k(self.imag_mult)

    def get_fc_fine(self):
        return self.fc_fine

    def set_fc_fine(self, fc_fine):
        self.fc_fine = fc_fine
        self.analog_sig_source_x_0_0.set_frequency(self.fc_fine)

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc
        self.analog_sig_source_x_0.set_frequency(self.fc)



def main(top_block_cls=e2f, options=None):

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
