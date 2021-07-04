#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: E3C
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

class E3C(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "E3C")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("E3C")
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

        self.settings = Qt.QSettings("GNU Radio", "E3C")

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
        self.tlbw = tlbw = 62.8e-3
        self.sym_dly = sym_dly = 0
        self.ptype = ptype = "rrcf"
        self.pparms = pparms = [5, 0.5]
        self.nfilts = nfilts = 32
        self.gain = gain = 1
        self.Fs = Fs = FB * sps
        self.An = An = 0

        ##################################################
        # Blocks
        ##################################################
        self._tlbw_range = Range(0, 0.2, 0.1, 62.8e-3, 200)
        self._tlbw_win = RangeWidget(self._tlbw_range, self.set_tlbw, 'tlbw', "counter_slider", float)
        self.top_grid_layout.addWidget(self._tlbw_win)
        self._sym_dly_range = Range(0, 2 * sps, 1, 0, 200)
        self._sym_dly_win = RangeWidget(self._sym_dly_range, self.set_sym_dly, 'sym_dly', "counter_slider", int)
        self.top_grid_layout.addWidget(self._sym_dly_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._ptype_options = ("rrcf", "tri", "rcf", )
        # Create the labels list
        self._ptype_labels = ('rrcf', 'tri', "rcf", )
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
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            FB * sps, #samp_rate
            "", #name
            3 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(False)
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


        for i in range(3):
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
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win, 2, 1, 4, 1)
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
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_fff(sps, pampt(sps, ptype, pparms))
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_fff(sps, tlbw, 1/float(sps) * pampt(sps * nfilts, ptype, pparms), nfilts, nfilts / 2, 0.7, 1)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_vector_source_x_0 = blocks.vector_source_b(list(ord(i) for i in 'The quick brown fox...\n'), True, 1, [])
        self.blocks_unpacked_to_packed_xx_0 = blocks.unpacked_to_packed_bb(1, gr.GR_LSB_FIRST)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, FB * 4,True)
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(1, gr.GR_LSB_FIRST)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(gain)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, '/dev/pts/4', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_char*1, sym_dly)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 0.5)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff(-1)
        self.analog_noise_source_x_0 = analog.noise_source_f(analog.GR_GAUSSIAN, An, 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_unpacked_to_packed_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 2), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 1), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 3), (self.qtgui_time_sink_x_0, 2))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.qtgui_sink_x_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "E3C")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_Fs(self.FB * self.sps)
        self.digital_pfb_clock_sync_xxx_0.update_taps(1/float(self.sps) * pampt(self.sps * self.nfilts, self.ptype, self.pparms))
        self.interp_fir_filter_xxx_0.set_taps(pampt(self.sps, self.ptype, self.pparms))
        self.qtgui_time_sink_x_0.set_samp_rate(self.FB * self.sps)

    def get_FB(self):
        return self.FB

    def set_FB(self, FB):
        self.FB = FB
        self.set_Fs(self.FB * self.sps)
        self.blocks_throttle_0.set_sample_rate(self.FB * 4)
        self.qtgui_sink_x_0.set_frequency_range(0, self.FB)
        self.qtgui_time_sink_x_0.set_samp_rate(self.FB * self.sps)

    def get_tlbw(self):
        return self.tlbw

    def set_tlbw(self, tlbw):
        self.tlbw = tlbw
        self.digital_pfb_clock_sync_xxx_0.set_loop_bandwidth(self.tlbw)

    def get_sym_dly(self):
        return self.sym_dly

    def set_sym_dly(self, sym_dly):
        self.sym_dly = sym_dly
        self.blocks_delay_0.set_dly(self.sym_dly)

    def get_ptype(self):
        return self.ptype

    def set_ptype(self, ptype):
        self.ptype = ptype
        self._ptype_callback(self.ptype)
        self.digital_pfb_clock_sync_xxx_0.update_taps(1/float(self.sps) * pampt(self.sps * self.nfilts, self.ptype, self.pparms))
        self.interp_fir_filter_xxx_0.set_taps(pampt(self.sps, self.ptype, self.pparms))

    def get_pparms(self):
        return self.pparms

    def set_pparms(self, pparms):
        self.pparms = pparms
        self.digital_pfb_clock_sync_xxx_0.update_taps(1/float(self.sps) * pampt(self.sps * self.nfilts, self.ptype, self.pparms))
        self.interp_fir_filter_xxx_0.set_taps(pampt(self.sps, self.ptype, self.pparms))

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.digital_pfb_clock_sync_xxx_0.update_taps(1/float(self.sps) * pampt(self.sps * self.nfilts, self.ptype, self.pparms))

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.blocks_multiply_const_vxx_0.set_k(self.gain)

    def get_Fs(self):
        return self.Fs

    def set_Fs(self, Fs):
        self.Fs = Fs

    def get_An(self):
        return self.An

    def set_An(self, An):
        self.An = An
        self.analog_noise_source_x_0.set_amplitude(self.An)



def main(top_block_cls=E3C, options=None):

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
