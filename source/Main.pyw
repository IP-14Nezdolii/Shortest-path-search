#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import MainWindow

app =  MainWindow.QApplication(sys.argv)
window =  MainWindow.MainWindow()
window.show()
sys.exit(app.exec())
