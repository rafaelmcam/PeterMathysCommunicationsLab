#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: E3B
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

from ModuleLab3 import generate_signal_E3B
from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
import numpy as np
from gnuradio import qtgui

class E3B(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "E3B")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("E3B")
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

        self.settings = Qt.QSettings("GNU Radio", "E3B")

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
        self.samp_rate = samp_rate = 32000
        self.f1 = f1 = 1000
        self.duty_cycle = duty_cycle = 20

        ##################################################
        # Blocks
        ##################################################
        self._f1_range = Range(0, 5000, 1, 1000, 200)
        self._f1_win = RangeWidget(self._f1_range, self.set_f1, 'f1', "counter_slider", float)
        self.top_grid_layout.addWidget(self._f1_win)
        self._duty_cycle_range = Range(0, 100, 1, 20, 200)
        self._duty_cycle_win = RangeWidget(self._duty_cycle_range, self.set_duty_cycle, 'duty_cycle', "counter_slider", float)
        self.top_grid_layout.addWidget(self._duty_cycle_win)
        self.qtgui_sink_x_0 = qtgui.sink_f(
            1024 // 4, #fftsize
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
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
        self.blocks_vector_source_x_0 = blocks.vector_source_f(generate_signal_E3B(samp_rate, f1, duty_cycle), True, 1, [])
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, samp_rate,True)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_throttle_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "E3B")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.blocks_vector_source_x_0.set_data(generate_signal_E3B(self.samp_rate, self.f1, self.duty_cycle), [])
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_f1(self):
        return self.f1

    def set_f1(self, f1):
        self.f1 = f1
        self.blocks_vector_source_x_0.set_data(generate_signal_E3B(self.samp_rate, self.f1, self.duty_cycle), [])

    def get_duty_cycle(self):
        return self.duty_cycle

    def set_duty_cycle(self, duty_cycle):
        self.duty_cycle = duty_cycle
        self.blocks_vector_source_x_0.set_data(generate_signal_E3B(self.samp_rate, self.f1, self.duty_cycle), [])



def main(top_block_cls=E3B, options=None):

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
