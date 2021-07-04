#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: E3D
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
from gnuradio import blocks
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import numpy as np
import ptfun as pf
from gnuradio import qtgui

class E3D(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "E3D")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("E3D")
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

        self.settings = Qt.QSettings("GNU Radio", "E3D")

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
        self.sps = sps = 30
        self.samp_rate = samp_rate = 32000
        self.ptype = ptype = 'rect'
        self.k = k = 1
        self.dly = dly = 320
        self.beta = beta = 2.5

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            dly  * 3, #size
            samp_rate, #samp_rate
            "", #name
            10 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-0.2, 1.2)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(True)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'blue', 'blue', 'blue', 'blue',
            'blue', 'blue', 'blue', 'blue', 'blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(10):
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
        # Create the options list
        self._ptype_options = ('rect', 'sinc', 'tri', )
        # Create the labels list
        self._ptype_labels = ('rect', 'sinc', 'tri', )
        # Create the combo box
        self._ptype_tool_bar = Qt.QToolBar(self)
        self._ptype_tool_bar.addWidget(Qt.QLabel('Select PAM pulse: p(t)' + ": "))
        self._ptype_combo_box = Qt.QComboBox()
        self._ptype_tool_bar.addWidget(self._ptype_combo_box)
        for _label in self._ptype_labels: self._ptype_combo_box.addItem(_label)
        self._ptype_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ptype_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._ptype_options.index(i)))
        self._ptype_callback(self.ptype)
        self._ptype_combo_box.currentIndexChanged.connect(
            lambda i: self.set_ptype(self._ptype_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._ptype_tool_bar)
        self.blocks_wavfile_source_0_0 = blocks.wavfile_source('/home/rcampello/Main/3m/Simulação de sistemas de comunicação/Labs/Lab4/pamsig403_rcv_dot2.wav', True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, samp_rate * 5,True)
        self.blocks_delay_0_0_0_0_0_0_0_0_0_0_0_0 = blocks.delay(gr.sizeof_float*1, dly)
        self.blocks_delay_0_0_0_0_0_0_0_0_0_0_0 = blocks.delay(gr.sizeof_float*1, dly)
        self.blocks_delay_0_0_0_0_0_0_0_0_0_0 = blocks.delay(gr.sizeof_float*1, dly)
        self.blocks_delay_0_0_0_0_0_0_0_0_0 = blocks.delay(gr.sizeof_float*1, dly)
        self.blocks_delay_0_0_0_0_0_0_0_0 = blocks.delay(gr.sizeof_float*1, dly)
        self.blocks_delay_0_0_0_0_0_0_0 = blocks.delay(gr.sizeof_float*1, dly)
        self.blocks_delay_0_0_0_0_0_0 = blocks.delay(gr.sizeof_float*1, dly)
        self.blocks_delay_0_0_0_0_0 = blocks.delay(gr.sizeof_float*1, dly)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_float*1, dly)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_delay_0, 0), (self.blocks_delay_0_0_0_0_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.blocks_delay_0_0_0_0_0, 0), (self.blocks_delay_0_0_0_0_0_0, 0))
        self.connect((self.blocks_delay_0_0_0_0_0, 0), (self.qtgui_time_sink_x_0, 2))
        self.connect((self.blocks_delay_0_0_0_0_0_0, 0), (self.blocks_delay_0_0_0_0_0_0_0, 0))
        self.connect((self.blocks_delay_0_0_0_0_0_0, 0), (self.qtgui_time_sink_x_0, 3))
        self.connect((self.blocks_delay_0_0_0_0_0_0_0, 0), (self.blocks_delay_0_0_0_0_0_0_0_0, 0))
        self.connect((self.blocks_delay_0_0_0_0_0_0_0, 0), (self.qtgui_time_sink_x_0, 4))
        self.connect((self.blocks_delay_0_0_0_0_0_0_0_0, 0), (self.blocks_delay_0_0_0_0_0_0_0_0_0, 0))
        self.connect((self.blocks_delay_0_0_0_0_0_0_0_0, 0), (self.qtgui_time_sink_x_0, 5))
        self.connect((self.blocks_delay_0_0_0_0_0_0_0_0_0, 0), (self.blocks_delay_0_0_0_0_0_0_0_0_0_0, 0))
        self.connect((self.blocks_delay_0_0_0_0_0_0_0_0_0, 0), (self.qtgui_time_sink_x_0, 6))
        self.connect((self.blocks_delay_0_0_0_0_0_0_0_0_0_0, 0), (self.blocks_delay_0_0_0_0_0_0_0_0_0_0_0, 0))
        self.connect((self.blocks_delay_0_0_0_0_0_0_0_0_0_0, 0), (self.qtgui_time_sink_x_0, 7))
        self.connect((self.blocks_delay_0_0_0_0_0_0_0_0_0_0_0, 0), (self.blocks_delay_0_0_0_0_0_0_0_0_0_0_0_0, 0))
        self.connect((self.blocks_delay_0_0_0_0_0_0_0_0_0_0_0, 0), (self.qtgui_time_sink_x_0, 8))
        self.connect((self.blocks_delay_0_0_0_0_0_0_0_0_0_0_0_0, 0), (self.qtgui_time_sink_x_0, 9))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_wavfile_source_0_0, 0), (self.blocks_throttle_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "E3D")
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
        self.blocks_throttle_0.set_sample_rate(self.samp_rate * 5)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_ptype(self):
        return self.ptype

    def set_ptype(self, ptype):
        self.ptype = ptype
        self._ptype_callback(self.ptype)

    def get_k(self):
        return self.k

    def set_k(self, k):
        self.k = k

    def get_dly(self):
        return self.dly

    def set_dly(self, dly):
        self.dly = dly
        self.blocks_delay_0.set_dly(self.dly)
        self.blocks_delay_0_0_0_0_0.set_dly(self.dly)
        self.blocks_delay_0_0_0_0_0_0.set_dly(self.dly)
        self.blocks_delay_0_0_0_0_0_0_0.set_dly(self.dly)
        self.blocks_delay_0_0_0_0_0_0_0_0.set_dly(self.dly)
        self.blocks_delay_0_0_0_0_0_0_0_0_0.set_dly(self.dly)
        self.blocks_delay_0_0_0_0_0_0_0_0_0_0.set_dly(self.dly)
        self.blocks_delay_0_0_0_0_0_0_0_0_0_0_0.set_dly(self.dly)
        self.blocks_delay_0_0_0_0_0_0_0_0_0_0_0_0.set_dly(self.dly)

    def get_beta(self):
        return self.beta

    def set_beta(self, beta):
        self.beta = beta



def main(top_block_cls=E3D, options=None):

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
