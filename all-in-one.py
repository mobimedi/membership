#!/usr/bin/python
# -*- coding: utf-8 -*-


__author__ = 'nagexiucai.com'

import wx as UI
import wx.dataview as UIDV
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
            "CREATE TABLE DanXiang (Number TEXT, Name TEXT, Price FLOAT);",
            "CREATE TABLE TaoCan (Combination TEXT, Name TEXT, Price FLOAT);"
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
            "INSERT INTO DanXiang VALUES ('K', '剪二', 20.00);",
            "INSERT INTO TaoCan VALUES ('X+Y', '吹一加染一', 55.55);",
            "INSERT INTO TaoCan VALUES ('Y+Z+D', '染一加洗二加吹二', 99.99);",
            "INSERT INTO TaoCan VALUES ('G+H+J', '烫三加垃一加剪一', 29.90);"
        )
        for _ in CREATE:
            self.Execute(_)
        for _ in INSERT:
            self.Execute(_)
    def Clear(self):pass
    def Execute(self, sql): # TODO: make many
        print "[SQL]", sql
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
        print keycode
        if self.flag is float:
            if keycode < 256 and chr(keycode) in "."+string.digits or keycode in (314, 315, 316, 317, 8):
                evt.Skip()

class JieZhang(UI.Panel):
    RowNumber = 3
    ColumnNumber = 3
    def __init__(self, parent):
        UI.Panel.__init__(self, parent)
        self.sizer = UI.GridSizer(JieZhang.RowNumber, JieZhang.ColumnNumber)

class HuiYuan(UI.Panel):
    def __init__(self, parent):
        UI.Panel.__init__(self, parent)
        self.sizer = UI.BoxSizer(UI.VERTICAL)
        self.dvlc = UIDV.DataViewListCtrl(self)
        self.dvlc.AppendTextColumn("PhoneNumber", width=160)
        self.dvlc.AppendTextColumn("Name", width=240)
        self.dvlc.AppendTextColumn("Balance", width=120)
        _ = parent.database.Execute("SELECT * FROM Member;")
        for phonenumber, name, balance in _:
            self.dvlc.AppendItem((phonenumber, name, unicode(balance)))
        self.sizer.Add(self.dvlc, proportion=AUTO, flag=UI.EXPAND|UI.ALL)
        self.SetSizerAndFit(self.sizer)
        self.Bind(UIDV.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self.OnDataViewItemContextMenu)
    def OnDataViewItemContextMenu(self, evt):
        pass

class Record(UI.Dialog):
    IdOK = UI.NewId()
    IdCancel = UI.NewId()
    IdRemove = UI.NewId()
    def __init__(self, parent, title, data):
        UI.Dialog.__init__(self, parent, title=title)
        self.sizer = UI.BoxSizer(UI.VERTICAL)
        assert isinstance(data, dict)
        for k, v in data.iteritems():
            st = UI.StaticText(self, label=k, size=(80, 20))
            if isinstance(v, float): # for price etc
                tc = UI.TextCtrl(self, value=unicode(v), name=k, size=(120, 20), validator=TextValidator(float)) # TODO: 主键禁止修改
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
        remove = UI.Button(self, id=Record.IdRemove, label=u"删除")
        self.sizer.Add(remove, proportion=FIXED, flag=UI.EXPAND | UI.ALL)
        self.SetSizerAndFit(self.sizer)
        self.Bind(UI.EVT_BUTTON, self.OnButton)
        self.Bind(UI.EVT_TEXT, self.OnText)
        self.UserData = data
        self.DirtyUserData = {}
        cancel.SetFocus()
        self.status = None
    def OnButton(self, evt):
        _ = evt.GetId()
        self.status = _
        if _ == Record.IdOK:
            self.UserData.update(self.DirtyUserData)
        self.Destroy()
    def OnText(self, evt):
        _ = self.FindWindowById(evt.GetId())
        self.DirtyUserData[_.GetName()] = _.GetValue() # FIXME: need format price to float

class TaoCan(UI.Panel):
    IdGenerate = UI.NewId()
    def __init__(self, parent):
        UI.Panel.__init__(self, parent)
        self.sizer = UI.BoxSizer(UI.HORIZONTAL)
        self.sizerLeft = UI.BoxSizer(UI.VERTICAL)
        self.sizerRight = UI.BoxSizer(UI.VERTICAL)
        b = UI.Button(self, id=TaoCan.IdGenerate, label=u"生成")
        _ = parent.database.Execute("SELECT * FROM DanXiang;")
        __ = []
        self.UserDataDX = {}
        for number, name, price in _:
            __.append(name)
            self.UserDataDX[name] = {"Number": number, "Price": price}
        clb = UI.CheckListBox(self, choices=__)
        self.sizerLeft.Add(clb, proportion=AUTO, flag=UI.EXPAND|UI.ALL)
        self.sizerLeft.Add(b, proportion=FIXED, flag=UI.EXPAND|UI.ALL)
        _ = parent.database.Execute("SELECT * FROM TaoCan;")
        self.UserDataTC = {}
        font = UI.Font(26, UI.DEFAULT, UI.NORMAL, UI.NORMAL)
        for combination, name, price in _:
            data = {"Combination": combination, "Name": name, "Price": price}
            b = UI.Button(self, label=name)
            b.SetToolTipString(unicode(price))
            b.SetFont(font)
            setattr(b, "UserData", data)
            self.UserDataTC[combination] = data
            self.sizerRight.Add(b, proportion=AUTO, flag=UI.EXPAND|UI.ALL)
        self.sizerLeft.SetMinSize((160, 80))
        self.sizerRight.SetMinSize((200, 80))
        self.sizer.Add(self.sizerLeft, proportion=FIXED, flag=UI.EXPAND|UI.ALL)
        self.sizer.Add(self.sizerRight, proportion=AUTO, flag=UI.EXPAND|UI.ALL)
        self.SetSizerAndFit(self.sizer)
        self.Bind(UI.EVT_BUTTON, self.OnButton)
    def OnButton(self, evt):
        _ = evt.GetId()
        if _ == TaoCan.IdGenerate:
            print u"新增"
        else:
            __ = self.FindWindowById(_)
            data = __.UserData
            dlg = Record(self, data.get("Name", u"缺失异常"), data)
            dlg.ShowModal()
            if dlg.status == Record.IdRemove:
                print u"删除"
            elif dlg.status == Record.IdOK:
                print u"修改"

class DanXiang(UI.Panel):
    ColumnNumber = 11
    IdPlus = UI.NewId()
    def __init__(self, parent):
        UI.Panel.__init__(self, parent)
        self.sizer = UI.GridBagSizer(5, 5) # TODO: 找一种行列不固定且会根据元素总数及尺寸自适应的布局框架
        i = c = r = 0
        _ = parent.database.Execute("SELECT * FROM DanXiang;")
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
            b.SetToolTipString(unicode(price))
            setattr(b, "UserData", {"Number": number, "Name": name, "Price": price})
            b.SetFont(font)
            self.sizer.Add(b, pos=(r, c), flag=UI.EXPAND|UI.ALL)
        font = UI.Font(24, UI.DEFAULT, UI.NORMAL, UI.NORMAL)
        b = UI.Button(self, id=DanXiang.IdPlus, label="+")
        b.SetFont(font)
        r, c = divmod(i, DanXiang.ColumnNumber)
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
        __ = self.FindWindowById(_)
        if _ == DanXiang.IdPlus:
            here = self.sizer.GetItemCount()
            data = {"Number": "?", "Name": "?", "Price": 0.0}
            dlg = Record(self, u"添加", data)
            dlg.ShowModal()
            # TODO: 去重（也可以放在Validator中做）
            if dlg.status == Record.IdOK:
                b = UI.Button(self, label=data.get("Name", u"缺失异常"))
                b.SetFont(__.GetFont())
                setattr(b, "UserData", data)
                r, c = self.sizer.GetItemPosition(__)
                self.sizer.Detach(__) # FIXME: Insert can not used by GridBagSizer
                self.sizer.Add(b, pos=(r, c), flag=UI.EXPAND|UI.ALL)
                r, c = divmod(here, DanXiang.ColumnNumber)
                self.sizer.Add(__, pos=(r, c), flag=UI.EXPAND|UI.ALL)
                if not self.sizer.IsRowGrowable(r):
                    self.sizer.AddGrowableRow(r, AUTO)
                if not self.sizer.IsColGrowable(c):
                    self.sizer.AddGrowableCol(c, AUTO)
                self.sizer.Layout()
                self.Parent.database.Execute(u"INSERT INTO DanXiang VALUES ('{Number}', '{Name}', {Price});".format(**data))
        else:
            data = __.UserData
            dlg = Record(self, data.get("Name", u"缺失异常"), data)
            dlg.ShowModal()
            if dlg.status == Record.IdOK:
                __.SetLabel(data.get("Name", u"缺失异常"))
                # FIXME: 按钮标注文字加长窗口不能自适应（需手动触发）
                self.PostSizeEventToParent()
                self.Parent.database.Execute(u"UPDATE DanXiang SET Name='{Name}', Price={Price} WHERE Number='{Number}';".format(**data))
            elif dlg.status == Record.IdRemove:
                # self.sizer.Remove(__) # FIXME: why does not work
                __.Destroy()
                self.sizer.Layout()
                self.Parent.database.Execute(u"DELETE FROM DanXiang WHERE Number='{Number}';".format(**data))

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
        self.status = None
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
        self.sizer.SetMinSize((620, 400))
        self.SetSizer(self.sizer)
    def OnMenu(self, evt):
        _ = evt.GetId()
        self.sb.SetStatusText(self.mb.FindItemById(_).GetText())
        self.sizer.Clear(True)
        if _ == Frame.IdDengRu:
            InOut(self).ShowModal()
        elif _ == Frame.IdZuoZhe:
            UI.MessageBox(u"那个秀才［www.nagexiucai.com］", u"作者")
        elif _ == Frame.IdJiHuo:
            UI.TextEntryDialog(self, u"激活码（微信添加nagexiucai好友申请）", u"激活").ShowModal()
        elif _ == Frame.IdDanXiang and self.status != Frame.IdDanXiang:
            self.sizer.Add(DanXiang(self), proportion=AUTO, flag=UI.EXPAND|UI.ALL)
        elif _ == Frame.IdTaoCan and self.status != Frame.IdTaoCan:
            self.sizer.Add(TaoCan(self), proportion=AUTO, flag=UI.EXPAND|UI.ALL)
        elif _ == Frame.IdHuiYuan and self.status != Frame.IdHuiYuan:
            self.sizer.Add(HuiYuan(self), proportion=AUTO, flag=UI.EXPAND|UI.ALL)
        elif _ == Frame.IdJieZhang and self.status != Frame.IdJieZhang:
            self.sizer.Add(JieZhang(self), proportion=AUTO, flag=UI.EXPAND|UI.ALL)
        self.Fit()
        self.PostSizeEvent()
        self.status = _
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
