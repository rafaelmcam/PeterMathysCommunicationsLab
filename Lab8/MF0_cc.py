#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Basic Complex MF
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

from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import ModuleLab6

from gnuradio import qtgui

class MF0_cc(gr.top_block, Qt.QWidget):

    def __init__(self, a_gain=1, b_FB=32000, c_sps=8, d_ptype="rectd", e_pparms=(5, 0.3), f_fcparms=0, g_samp_dly=0):
        gr.top_block.__init__(self, "Basic Complex MF")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Basic Complex MF")
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

        self.settings = Qt.QSettings("GNU Radio", "MF0_cc")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Parameters
        ##################################################
        self.a_gain = a_gain
        self.b_FB = b_FB
        self.c_sps = c_sps
        self.d_ptype = d_ptype
        self.e_pparms = e_pparms
        self.f_fcparms = f_fcparms
        self.g_samp_dly = g_samp_dly

        ##################################################
        # Variables
        ##################################################
        self.Fs = Fs = 256000

        ##################################################
        # Blocks
        ##################################################
        self.fir_filter_xxx_0 = filter.fir_filter_ccc(1, [5])
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self.blocks_vector_source_x_0 = blocks.vector_source_c((0, 0, 0), True, 1, [])
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_vector_source_x_0, 0), (self.fir_filter_xxx_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.blocks_null_sink_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "MF0_cc")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_a_gain(self):
        return self.a_gain

    def set_a_gain(self, a_gain):
        self.a_gain = a_gain

    def get_b_FB(self):
        return self.b_FB

    def set_b_FB(self, b_FB):
        self.b_FB = b_FB

    def get_c_sps(self):
        return self.c_sps

    def set_c_sps(self, c_sps):
        self.c_sps = c_sps

    def get_d_ptype(self):
        return self.d_ptype

    def set_d_ptype(self, d_ptype):
        self.d_ptype = d_ptype

    def get_e_pparms(self):
        return self.e_pparms

    def set_e_pparms(self, e_pparms):
        self.e_pparms = e_pparms

    def get_f_fcparms(self):
        return self.f_fcparms

    def set_f_fcparms(self, f_fcparms):
        self.f_fcparms = f_fcparms

    def get_g_samp_dly(self):
        return self.g_samp_dly

    def set_g_samp_dly(self, g_samp_dly):
        self.g_samp_dly = g_samp_dly

    def get_Fs(self):
        return self.Fs

    def set_Fs(self, Fs):
        self.Fs = Fs

def snipfcn_snippet_0(self):
    import sys
    from inspect import getmembers, isfunction

    print(sys.path)

    print(getmembers(ModuleLab6, isfunction))


    print(ModuleLab6)


def snippets_main_after_init(tb):
    snipfcn_snippet_0(tb)



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--a-gain", dest="a_gain", type=eng_float, default="1.0",
        help="Set Gain [default=%(default)r]")
    parser.add_argument(
        "--b-FB", dest="b_FB", type=intx, default=32000,
        help="Set Baud Rate [default=%(default)r]")
    parser.add_argument(
        "--c-sps", dest="c_sps", type=intx, default=8,
        help="Set Samples per Symbol [default=%(default)r]")
    parser.add_argument(
        "--d-ptype", dest="d_ptype", type=str, default="rectd",
        help="Set Pulse Type [default=%(default)r]")
    parser.add_argument(
        "--g-samp-dly", dest="g_samp_dly", type=intx, default=0,
        help="Set Sample Delay [default=%(default)r]")
    return parser


def main(top_block_cls=MF0_cc, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(a_gain=options.a_gain, b_FB=options.b_FB, c_sps=options.c_sps, d_ptype=options.d_ptype, g_samp_dly=options.g_samp_dly)
    snippets_main_after_init(tb)
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
