#!/usr/bin/env python3
#
#Copyright 2015 Pavel Yazev <pyazev@gmail.com>
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import sys
import pmt
from gnuradio import gr


try:
    from PyQt5 import QtCore, QtGui, QtWidgets

except ImportError:
    sys.stderr.write("Error: Program requires PyQt5 and gr-qtgui.\n")
    sys.exit(1)


class console(gr.basic_block, QtWidgets.QTextEdit):
    console_update = QtCore.pyqtSignal()

    def __init__(self, auto_scroll=True):
        gr.basic_block.__init__(self, name="console", in_sig=[], out_sig=[])
        QtWidgets.QTextEdit.__init__(self)
        self.message_port_register_in(pmt.intern("in"))
        self.set_msg_handler(pmt.intern("in"), self.handle_msg)
        self.message_port_register_in(pmt.intern("config"))
        self.set_msg_handler(pmt.intern("config"), self.handle_config)

        self.console_update.connect(self.update)

        self.font = self.document().defaultFont();
        self.font.setFamily("Courier New");
        self.font.setStyleStrategy(QtGui.QFont.NoAntialias);
        self.document().setDefaultFont(self.font);
        self.auto_scroll = auto_scroll

    def handle_msg(self, msg):
        if(pmt.dict_has_key( msg, pmt.to_pmt("log_msg"))):        
            log_msg = pmt.dict_ref( msg, pmt.to_pmt("log_msg"), pmt.PMT_NIL)
            self.console_msg = pmt.to_python(log_msg)
            self.console_update.emit()
    
    def handle_config(self, msg):
        value = pmt.to_python(msg)
        if isinstance(value, tuple):
            data = dict([value])
            if "auto_scroll" in data:
                self.auto_scroll = data["auto_scroll"]
        
    def update(self):
        scrollbar = self.verticalScrollBar()
        current_scroll_pos = scrollbar.value()        
        cursor = self.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        
        if not self.console_msg.endswith("\n"):
            self.console_msg += "\n"
        cursor.insertText(self.console_msg)
        
        if self.auto_scroll:
            scrollbar.setValue(scrollbar.maximum())
        else:
            scrollbar.setValue(current_scroll_pos)

    def work(self, input_items, output_items):
        pass
