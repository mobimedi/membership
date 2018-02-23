#!/usr/bin/python
# -*- coding: utf-8 -*-


__author__ = 'nagexiucai.com'

import wx as UI
import sqlite3 as DB
import os
import sys
import string

FIXED = 0
DEFAULT = AUTO = -1

class Database:
    CONNECT = None
    def __init__(self):
        if Database.CONNECT is None:
            Database.CONNECT = DB.connect(":memory:")
    def __del__(self):
        if Database.CONNECT is not None:
            Database.CONNECT.close()
    def Initialize(self):
        CREATE = (
            "CREATE TABLE Member (PhoneNumber TEXT, Name TEXT, Balance FLOAT);",
            "CREATE TABLE DanXiang (Number TEXT, Name TEXT, Price FLOAT);"
        )
        INSERT = (
            "INSERT INTO Member VALUES ('086182029*****', '那个秀才', 33.33);",
            "INSERT INTO Member VALUES ('086182918*****', '大海', 77.77);",
            "INSERT INTO DanXiang VALUES ('X', '吹一', 30.00);",
            "INSERT INTO DanXiang VALUES ('Y', '染一', 90.00);",
            "INSERT INTO DanXiang VALUES ('Z', '洗二', 88.00);",
            "INSERT INTO DanXiang VALUES ('A', '洗一', 10.00);",
            "INSERT INTO DanXiang VALUES ('B', '染二', 11.00);",
            "INSERT INTO DanXiang VALUES ('C', '染三', 12.00);",
            "INSERT INTO DanXiang VALUES ('D', '吹二', 13.00);",
            "INSERT INTO DanXiang VALUES ('E', '烫一', 14.00);",
            "INSERT INTO DanXiang VALUES ('F', '烫二', 15.00);",
            "INSERT INTO DanXiang VALUES ('G', '烫三', 16.00);",
            "INSERT INTO DanXiang VALUES ('H', '拉一', 17.00);",
            "INSERT INTO DanXiang VALUES ('I', '拉二', 18.00);",
            "INSERT INTO DanXiang VALUES ('J', '剪一', 19.00);",
            "INSERT INTO DanXiang VALUES ('K', '剪二', 20.00);"
        )
        for _ in CREATE:
            self.Execute(_)
        for _ in INSERT:
            self.Execute(_)
    def Clear(self):pass
    def Execute(self, sql): # TODO: make many
        assert isinstance(sql, basestring)
        cursor = Database.CONNECT.cursor()
        cursor.execute(sql)
        if sql.upper().startswith("SELECT "):
            return cursor.fetchall()
        else:
            Database.CONNECT.commit()
        cursor.close()
        return []
    @classmethod
    def Test(cls):
        self = cls()
        self.Initialize()
        print self.Execute("SELECT * FROM Member")
        print self.Execute("SELECT * FROM DanXiang")
        self.Execute("INSERT INTO DanXiang VALUES ('H', 'What', 22.22)")
        print self.Execute("SELECT * FROM DanXiang")

class TextValidator(UI.PyValidator):
    def __init__(self, flag):
        UI.PyValidator.__init__(self)
        self.flag = flag
        self.Bind(UI.EVT_CHAR, self.OnChar)
    def Clone(self):
        return TextValidator(self.flag)
    def Validate(self, w):
        return True
    def TransferToWindow(self):
        return True
    def TransferFromWindow(self):

        return True
    def OnChar(self, evt):
        keycode = evt.GetKeyCode()
        if self.flag is float:
            if keycode < 256 and chr(keycode) in "."+string.digits:
                evt.Skip()

class Record(UI.Dialog):
    IdOK = UI.NewId()
    IdCancel = UI.NewId()
    def __init__(self, parent, title, data):
        UI.Dialog.__init__(self, parent, title=title)
        self.sizer = UI.BoxSizer(UI.VERTICAL)
        assert isinstance(data, dict)
        for k, v in data.iteritems():
            st = UI.StaticText(self, label=k, size=(60, 20))
            if isinstance(v, float): # for price etc
                tc = UI.TextCtrl(self, value=unicode(v), name=k, size=(120, 20), validator=TextValidator(float))
                tc.Validate()
            else:
                tc = UI.TextCtrl(self, value=v, name=k, size=(120, 20))
            sizer = UI.BoxSizer(UI.HORIZONTAL)
            sizer.Add(st, proportion=FIXED, flag=UI.EXPAND|UI.ALL)
            sizer.Add(tc, proportion=FIXED, flag=UI.EXPAND|UI.ALL)
            self.sizer.Add(sizer, proportion=FIXED, flag=UI.EXPAND|UI.ALL)
        ok = UI.Button(self, id=Record.IdOK, label=u"确认")
        self.sizer.Add(ok, proportion=FIXED, flag=UI.EXPAND|UI.ALL)
        cancel = UI.Button(self, id=Record.IdCancel, label=u"放弃")
        self.sizer.Add(cancel, proportion=FIXED, flag=UI.EXPAND|UI.ALL)
        self.SetSizerAndFit(self.sizer)
        self.Bind(UI.EVT_BUTTON, self.OnButton)
        self.Bind(UI.EVT_TEXT, self.OnText)
        self.UserData = data
        self.DirtyUserData = {}
    def OnButton(self, evt):
        _ = evt.GetId()
        if _ == Record.IdOK:
            self.UserData.update(self.DirtyUserData)
        self.Destroy()
    def OnText(self, evt):
        _ = self.FindWindowById(evt.GetId())
        self.DirtyUserData[_.GetName()] = _.GetValue() # FIXME: need format price to float

class DanXiang(UI.Panel):
    ColumnNumber = 11
    IdPlus = UI.NewId()
    IdMinus = UI.NewId()
    def __init__(self, parent):
        UI.Panel.__init__(self, parent)
        self.sizer = UI.GridBagSizer(5, 5)
        i = c = r = 0
        _ = parent.database.Execute("SELECT * FROM DanXiang")
        column = []
        row = []
        font = UI.Font(22, UI.DEFAULT, UI.NORMAL, UI.NORMAL)
        for number, name, price in _:
            c = i%DanXiang.ColumnNumber
            column.append(c)
            r = i/DanXiang.ColumnNumber
            row.append(r)
            i += 1
            b = UI.Button(self, label=name)
            setattr(b, "UserData", {"Number": number, "Name": name, "Price": price})
            b.SetOwnFont(font)
            self.sizer.Add(b, pos=(r, c), flag=UI.EXPAND|UI.ALL)
        font = UI.Font(24, UI.DEFAULT, UI.NORMAL, UI.NORMAL)
        b = UI.Button(self, id=DanXiang.IdPlus, label="+")
        b.SetOwnFont(font)
        r, c = divmod(i, DanXiang.ColumnNumber)
        row.append(r)
        column.append(c)
        self.sizer.Add(b, pos=(r, c), flag=UI.EXPAND|UI.ALL)
        b = UI.Button(self, id=DanXiang.IdMinus, label="-")
        b.SetOwnFont(font)
        r, c = divmod(i+1, DanXiang.ColumnNumber)
        row.append(r)
        column.append(c)
        self.sizer.Add(b, pos=(r, c), flag=UI.EXPAND|UI.ALL)
        for r in set(row):
            self.sizer.AddGrowableRow(r, AUTO)
        for c in set(column):
            self.sizer.AddGrowableCol(c, AUTO)
        self.SetSizerAndFit(self.sizer)
        self.Bind(UI.EVT_BUTTON, self.OnButton)
    def OnButton(self, evt):
        _ = evt.GetId()
        if _ == DanXiang.IdPlus:
            pass
        elif _ == DanXiang.IdMinus:
            pass
        else:
            data = self.FindWindowById(_).UserData
            Record(self, data.get("Name", u"缺失异常"), data).ShowModal()
            print data

class InOut(UI.Dialog):
    IdAccount = UI.NewId()
    IdPassword = UI.NewId()
    IdOK = UI.NewId()
    def __init__(self, parent):
        UI.Dialog.__init__(self, parent, title=u"管理")
        self.accountLabel = UI.StaticText(self, label=u"账户", size=(AUTO, 20))
        self.account = UI.TextCtrl(self, id=InOut.IdAccount, name=u"账户", size=(AUTO, 20), value="Administrator")
        self.passwordLabel = UI.StaticText(self, label=u"密码", size=(AUTO, 20))
        self.password = UI.TextCtrl(self, id=InOut.IdPassword, name=u"密码", size=(AUTO, 20), style=UI.TE_PASSWORD)
        self.password.SetFocus()
        self.kidSizerA = UI.BoxSizer(UI.HORIZONTAL)
        self.kidSizerA.Add(self.accountLabel, proportion=FIXED, flag=UI.EXPAND|UI.ALL)
        self.kidSizerA.Add(self.account, proportion=AUTO, flag=UI.EXPAND|UI.ALL)
        self.kidSizerB = UI.BoxSizer(UI.HORIZONTAL)
        self.kidSizerB.Add(self.passwordLabel, proportion=FIXED, flag=UI.EXPAND|UI.ALL)
        self.kidSizerB.Add(self.password, proportion=AUTO, flag=UI.EXPAND|UI.ALL)
        self.sizer = UI.BoxSizer(UI.VERTICAL)
        self.sizer.Add(self.kidSizerA, proportion=FIXED, flag=UI.EXPAND|UI.ALL)
        self.sizer.Add(self.kidSizerB, proportion=FIXED, flag=UI.EXPAND|UI.ALL)
        self.ok = UI.Button(self, id=InOut.IdOK, label=u"确认", size=(160, 30))
        self.sizer.Add(self.ok, proportion=FIXED, flag=UI.EXPAND|UI.ALL)
        self.SetSizerAndFit(self.sizer)
        self.CenterOnParent()

class Frame(UI.Frame):
    IdZhangHuTimer = UI.NewId()
    IdDengRu = UI.NewId()
    IdTuiChu = UI.NewId()
    IdDaoRu = UI.NewId()
    IdDaoChu = UI.NewId()
    IdShengJi = UI.NewId()
    IdHuiYuan = UI.NewId()
    IdDanXiang = UI.NewId()
    IdTaoCan = UI.NewId()
    IdYouHui = UI.NewId()
    IdJieZhang = UI.NewId()
    IdQingDan = UI.NewId()
    IdJiHuo = UI.NewId()
    IdZuoZhe = UI.NewId()
    def __init__(self):
        UI.Frame.__init__(self, None, title=u"会员管理")
        self.database = Database()
        self.database.Initialize()
        self.SetMinSize((640, 480))
        self.icon = UI.Icon("./app.ico") # FIXME: WX3.0 need a name parameter
        # self.icon.LoadFile("./app.ico")
        self.SetIcon(self.icon)
        self.sb = UI.StatusBar(self)
        self.sb.SetFieldsCount()
        self.sb.SetStatusWidths([AUTO]) # FIXME: WX3.0 need list parameter
        # self.sb.SetStatusWidths((AUTO,))
        self.sb.SetStatusText(u"未激活")
        self.SetStatusBar(self.sb)
        self.mb = UI.MenuBar()
        self.SetMenuBar(self.mb)
        self.inout = UI.Menu()
        self.mb.Append(self.inout, u"管理")
        self.dengru = UI.MenuItem(self.inout, id=Frame.IdDengRu, text=u"登入")
        self.inout.AppendItem(self.dengru) # FIXME: WX3.0 need AppendItem
        # self.inout.Append(self.dengru)
        self.tuichu = UI.MenuItem(self.inout, id=Frame.IdTuiChu, text=u"退出")
        self.inout.AppendItem(self.tuichu)
        self.huiyuan = UI.MenuItem(self.inout, id=Frame.IdHuiYuan, text=u"会员")
        self.inout.AppendItem(self.huiyuan)
        self.setting = UI.Menu()
        self.mb.Append(self.setting, u"设置")
        self.xitong = UI.Menu()
        self.daoru = UI.MenuItem(self.setting, id=Frame.IdDaoRu, text=u"导入")
        self.xitong.AppendItem(self.daoru)
        self.daochu = UI.MenuItem(self.setting, id=Frame.IdDaoChu, text=u"导出")
        self.xitong.AppendItem(self.daochu)
        self.shengji = UI.MenuItem(self.setting, id=Frame.IdShengJi, text=u"升级")
        self.xitong.AppendItem(self.shengji)
        self.setting.AppendMenu(UI.NewId(), u"系统", self.xitong) # FIXME: WX3.0 need AppendMenu
        # self.setting.Append(UI.NewId(), u"系统", self.xitong)
        self.fuwu = UI.Menu()
        self.danxiang = UI.MenuItem(self.setting, id=Frame.IdDanXiang, text=u"单项")
        self.fuwu.AppendItem(self.danxiang)
        self.taocan = UI.MenuItem(self.setting, id=Frame.IdTaoCan, text=u"套餐")
        self.fuwu.AppendItem(self.taocan)
        self.setting.AppendMenu(UI.NewId(), u"服务", self.fuwu)
        self.youhui = UI.MenuItem(self.setting, id=Frame.IdYouHui, text=u"优惠")
        self.setting.AppendItem(self.youhui)
        self.bill = UI.Menu()
        self.mb.Append(self.bill, u"账单")
        self.jiezhang = UI.MenuItem(self.bill, id=Frame.IdJieZhang, text=u"结账")
        self.bill.AppendItem(self.jiezhang)
        self.qingdan = UI.MenuItem(self.bill, id=Frame.IdQingDan, text=u"清单")
        self.bill.AppendItem(self.qingdan)
        self.about = UI.Menu()
        self.mb.Append(self.about, u"关于")
        self.jihuo = UI.MenuItem(self.about, id=Frame.IdJiHuo, text=u"激活")
        self.about.AppendItem(self.jihuo)
        self.zuozhe = UI.MenuItem(self.about, id=Frame.IdZuoZhe, text=u"作者")
        self.about.AppendItem(self.zuozhe)
        self.Bind(UI.EVT_MENU, self.OnMenu)
        self.timerA = UI.Timer(owner=self, id=Frame.IdZhangHuTimer)
        self.timerA.Start(600, True) # FIXME: WX3.0 has no StartOnce
        # self.timerA.StartOnce(600)
        self.Bind(UI.EVT_TIMER, self.OnTimer)
        self.sizer = UI.BoxSizer(UI.VERTICAL)
    def OnMenu(self, evt):
        _ = evt.GetId()
        if _ == Frame.IdDengRu:
            InOut(self).ShowModal()
        elif _ == Frame.IdZuoZhe:
            UI.MessageBox(u"那个秀才［www.nagexiucai.com］", u"作者")
        elif _ == Frame.IdJiHuo:
            UI.TextEntryDialog(self, u"激活码（微信添加nagexiucai好友申请）", u"激活").ShowModal()
        elif _ == Frame.IdDanXiang:
            self.sizer.Add(DanXiang(self), proportion=AUTO, flag=UI.EXPAND|UI.ALL)
            self.sizer.SetMinSize(self.GetClientSize())
            self.SetSizerAndFit(self.sizer)
    def OnTimer(self, evt):
        _ = evt.GetId()
        if _ == Frame.IdZhangHuTimer:
            InOut(self).ShowModal()

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
