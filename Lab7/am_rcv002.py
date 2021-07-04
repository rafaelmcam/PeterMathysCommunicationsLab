#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: am_rcv002
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
from PyQt5.QtCore import QObject, pyqtSlot
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
from gnuradio import qtgui

class am_rcv002(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "am_rcv002")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("am_rcv002")
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

        self.settings = Qt.QSettings("GNU Radio", "am_rcv002")

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
        self.samp_rate2 = samp_rate2 = 512000
        self.samp_rate = samp_rate = 32000
        self.fcorr = fcorr = 0
        self.fc = fc = int(124e3)

        ##################################################
        # Blocks
        ##################################################
        self._fcorr_range = Range(-10, 10, 0.01, 0, 200)
        self._fcorr_win = RangeWidget(self._fcorr_range, self.set_fcorr, 'Fine Tune', "counter_slider", float)
        self.top_grid_layout.addWidget(self._fcorr_win)
        # Create the options list
        self._fc_options = (int(124e3), int(144e3), )
        # Create the labels list
        self._fc_labels = ('Station 1', 'Station 2', )
        # Create the combo box
        self._fc_tool_bar = Qt.QToolBar(self)
        self._fc_tool_bar.addWidget(Qt.QLabel('fc' + ": "))
        self._fc_combo_box = Qt.QComboBox()
        self._fc_tool_bar.addWidget(self._fc_combo_box)
        for _label in self._fc_labels: self._fc_combo_box.addItem(_label)
        self._fc_callback = lambda i: Qt.QMetaObject.invokeMethod(self._fc_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._fc_options.index(i)))
        self._fc_callback(self.fc)
        self._fc_combo_box.currentIndexChanged.connect(
            lambda i: self.set_fc(self._fc_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._fc_tool_bar)
        self.qtgui_sink_x_1 = qtgui.sink_c(
            1024, #fftsize
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True #plotconst
        )
        self.qtgui_sink_x_1.set_update_time(1.0/10)
        self._qtgui_sink_x_1_win = sip.wrapinstance(self.qtgui_sink_x_1.pyqwidget(), Qt.QWidget)

        self.qtgui_sink_x_1.enable_rf_freq(False)

        self.top_grid_layout.addWidget(self._qtgui_sink_x_1_win)
        self.qtgui_sink_x_0 = qtgui.sink_c(
            1024, #fftsize
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate2, #bw
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
            16,
            firdes.low_pass(
                2,
                samp_rate2,
                4000,
                2000,
                firdes.WIN_HAMMING,
                6.76))
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate2,True)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_float*1, '/home/rcampello/Main/3m/Simulação de sistemas de comunicação/Labs/Lab7/Files/AMsignal_002.bin', True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.audio_sink_0 = audio.sink(samp_rate, '', False)
        self.analog_sig_source_x_1 = analog.sig_source_c(samp_rate2, analog.GR_COS_WAVE, fcorr, 1, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate2, analog.GR_COS_WAVE, fc, 1, 0, 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_sig_source_x_1, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.blocks_complex_to_float_0, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_sink_x_1, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "am_rcv002")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate2(self):
        return self.samp_rate2

    def set_samp_rate2(self, samp_rate2):
        self.samp_rate2 = samp_rate2
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate2)
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate2)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate2)
        self.low_pass_filter_0.set_taps(firdes.low_pass(2, self.samp_rate2, 4000, 2000, firdes.WIN_HAMMING, 6.76))
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate2)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_sink_x_1.set_frequency_range(0, self.samp_rate)

    def get_fcorr(self):
        return self.fcorr

    def set_fcorr(self, fcorr):
        self.fcorr = fcorr
        self.analog_sig_source_x_1.set_frequency(self.fcorr)

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc
        self._fc_callback(self.fc)
        self.analog_sig_source_x_0.set_frequency(self.fc)



def main(top_block_cls=am_rcv002, options=None):

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
