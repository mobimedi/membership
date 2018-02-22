#!/usr/bin/python
# -*- coding: utf-8 -*-


__author__ = 'nagexiucai.com'

import wx as UI
import sqlite3 as DB
import os
import sys

class Frame(UI.Frame):
    def __init__(self):
        UI.Frame.__init__(self, None, title=u"会员管理")
        self.SetMinSize((640,480))
        icon = UI.Icon()
        icon.LoadFile("./app.ico")
        self.SetIcon(icon)

class App(UI.App):
    def __init__(self, frame):
        self.frame = frame
        UI.App.__init__(self)
    def OnInit(self):
        self.frame = self.frame()
        self.frame.Show(True)
        self.frame.CenterOnScreen()
        return True

app = App(Frame)
app.MainLoop()
