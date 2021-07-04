#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: T2
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

from ModuleLab6 import pamhRt
from ModuleLab6 import pampt
from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from gnuradio import qtgui

class T2(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "T2")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("T2")
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

        self.settings = Qt.QSettings("GNU Radio", "T2")

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
        self.sps = sps = 8
        self.FB = FB = 32000
        self.sym_dly = sym_dly = 0
        self.samp_dly = samp_dly = 1
        self.ptype = ptype = "rrcf"
        self.pparms = pparms = [5, 0.5]
        self.gain = gain = 1
        self.Fs = Fs = FB * sps
        self.An = An = 0

        ##################################################
        # Blocks
        ##################################################
        self._sym_dly_range = Range(0, 2 * sps, 1, 0, 200)
        self._sym_dly_win = RangeWidget(self._sym_dly_range, self.set_sym_dly, 'sym_dly', "counter_slider", int)
        self.top_grid_layout.addWidget(self._sym_dly_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._samp_dly_range = Range(0, 2 * sps, 1, 1, 200)
        self._samp_dly_win = RangeWidget(self._samp_dly_range, self.set_samp_dly, 'samp_dly', "counter_slider", int)
        self.top_grid_layout.addWidget(self._samp_dly_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._ptype_options = ("rrcf", "rect", "man", )
        # Create the labels list
        self._ptype_labels = ('rrcf', 'rect', "man", )
        # Create the combo box
        # Create the radio buttons
        self._ptype_group_box = Qt.QGroupBox('ptype' + ": ")
        self._ptype_box = Qt.QHBoxLayout()
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
        self.top_grid_layout.addWidget(self._ptype_group_box, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._gain_range = Range(0, 2, 0.1, 1, 200)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, 'gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._gain_win)
        self._An_range = Range(0, 2, 0.1, 0, 200)
        self._An_win = RangeWidget(self._An_range, self.set_An, 'An', "counter_slider", float)
        self.top_grid_layout.addWidget(self._An_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_f(
            1024 // 4, #size
            Fs, #samp_rate
            "", #name
            2 #number of inputs
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-1.3, 1.3)

        self.qtgui_time_sink_x_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1.enable_tags(True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(True)
        self.qtgui_time_sink_x_1.enable_grid(True)
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
        styles = [1, 0, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, 0, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_1_win, 2, 1, 4, 1)
        for r in range(2, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_sink_x_0 = qtgui.sink_f(
            1024, #fftsize
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            FB, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(False)

        self.top_grid_layout.addWidget(self._qtgui_sink_x_0_win, 2, 0, 4, 1)
        for r in range(2, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title("")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0.set_min(i, -1)
            self.qtgui_number_sink_0.set_max(i, 1)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(False)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_win)
        self.low_pass_filter_0_0 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                FB,
                10,
                10,
                firdes.WIN_HAMMING,
                6.76))
        self.interp_fir_filter_xxx_1 = filter.interp_fir_filter_fff(sps, [1])
        self.interp_fir_filter_xxx_1.declare_sample_delay(0)
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_fff(sps, pampt(sps, ptype, pparms))
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.fir_filter_xxx_0_0 = filter.fir_filter_fff(sps, [1])
        self.fir_filter_xxx_0_0.declare_sample_delay(0)
        self.fir_filter_xxx_0 = filter.fir_filter_fff(1, pamhRt(sps, ptype, pparms))
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_vector_source_x_0 = blocks.vector_source_b(list(ord(i) for i in 'The quick brown fox...\n'), True, 1, [])
        self.blocks_unpacked_to_packed_xx_0 = blocks.unpacked_to_packed_bb(1, gr.GR_LSB_FIRST)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, FB * 4,True)
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(1, gr.GR_LSB_FIRST)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(gain)
        self.blocks_float_to_complex_0_0 = blocks.float_to_complex(1)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, '/dev/pts/0', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_float*1, samp_dly)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_char*1, sym_dly)
        self.blocks_complex_to_mag_squared_0_0 = blocks.complex_to_mag_squared(1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 0.5)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff(-1)
        self.analog_noise_source_x_0 = analog.noise_source_f(analog.GR_GAUSSIAN, An, 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.fir_filter_xxx_0, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_unpacked_to_packed_xx_0, 0))
        self.connect((self.blocks_delay_0_0, 0), (self.fir_filter_xxx_0_0, 0))
        self.connect((self.blocks_delay_0_0, 0), (self.qtgui_time_sink_x_1, 0))
        self.connect((self.blocks_float_to_complex_0_0, 0), (self.blocks_complex_to_mag_squared_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.blocks_delay_0_0, 0))
        self.connect((self.fir_filter_xxx_0_0, 0), (self.blocks_float_to_complex_0_0, 0))
        self.connect((self.fir_filter_xxx_0_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.fir_filter_xxx_0_0, 0), (self.interp_fir_filter_xxx_1, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.interp_fir_filter_xxx_1, 0), (self.qtgui_time_sink_x_1, 1))
        self.connect((self.low_pass_filter_0_0, 0), (self.qtgui_number_sink_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "T2")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_Fs(self.FB * self.sps)
        self.fir_filter_xxx_0.set_taps(pamhRt(self.sps, self.ptype, self.pparms))
        self.interp_fir_filter_xxx_0.set_taps(pampt(self.sps, self.ptype, self.pparms))

    def get_FB(self):
        return self.FB

    def set_FB(self, FB):
        self.FB = FB
        self.set_Fs(self.FB * self.sps)
        self.blocks_throttle_0.set_sample_rate(self.FB * 4)
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.FB, 10, 10, firdes.WIN_HAMMING, 6.76))
        self.qtgui_sink_x_0.set_frequency_range(0, self.FB)

    def get_sym_dly(self):
        return self.sym_dly

    def set_sym_dly(self, sym_dly):
        self.sym_dly = sym_dly
        self.blocks_delay_0.set_dly(self.sym_dly)

    def get_samp_dly(self):
        return self.samp_dly

    def set_samp_dly(self, samp_dly):
        self.samp_dly = samp_dly
        self.blocks_delay_0_0.set_dly(self.samp_dly)

    def get_ptype(self):
        return self.ptype

    def set_ptype(self, ptype):
        self.ptype = ptype
        self._ptype_callback(self.ptype)
        self.fir_filter_xxx_0.set_taps(pamhRt(self.sps, self.ptype, self.pparms))
        self.interp_fir_filter_xxx_0.set_taps(pampt(self.sps, self.ptype, self.pparms))

    def get_pparms(self):
        return self.pparms

    def set_pparms(self, pparms):
        self.pparms = pparms
        self.fir_filter_xxx_0.set_taps(pamhRt(self.sps, self.ptype, self.pparms))
        self.interp_fir_filter_xxx_0.set_taps(pampt(self.sps, self.ptype, self.pparms))

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.blocks_multiply_const_vxx_0.set_k(self.gain)

    def get_Fs(self):
        return self.Fs

    def set_Fs(self, Fs):
        self.Fs = Fs
        self.qtgui_time_sink_x_1.set_samp_rate(self.Fs)

    def get_An(self):
        return self.An

    def set_An(self, An):
        self.An = An
        self.analog_noise_source_x_0.set_amplitude(self.An)



def main(top_block_cls=T2, options=None):

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
