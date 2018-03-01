#!/usr/bin/env python
# -*- coding:utf-8 -*-
# MOaS == Membership Open-and-Shut

import wx
from resource import ICON
from db import Database
import datetime
import base64
import re


TIMESTAMP = lambda: datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
DELTATIMESTAMP = lambda t: (datetime.datetime.now() + t).strftime('%Y-%m-%d %H:%M:%S')
DELTADAYS = lambda d: datetime.timedelta(days=d)
PHONENUMBER = re.compile("^1([358][0-9]|4[579]|66|7[0135678]|9[89])[0-9]{8}$")
ISPHONENUMBER = lambda pn: PHONENUMBER.match(pn)
EventQingDanType = wx.NewEventType()
EventQingDanBinder = wx.PyEventBinder(EventQingDanType, 1)


def IMHO(db):
    if not db.Execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table';")[0][0]:
        CREATE = (
            "CREATE TABLE Manager (Name TEXT, Password TEXT, Expired TEXT, PhoneNumber TEXT, Address TEXT, VerifyCode TEXT);",
            "CREATE TABLE Member (PhoneNumber TEXT, Name TEXT, Balance FLOAT);",
            "CREATE TABLE Log (PhoneNumber TEXT, Name TEXT, Consume FLOAT, Balance FLOAT, Time TEXT);"
        )
        INSERT = (
            u"INSERT INTO Manager VALUES ('nagexiucai', 'nagexiucai', '{0}', '182029*****', '中国西安', 'IGNORED');".format(DELTATIMESTAMP(DELTADAYS(30))),
            u"INSERT INTO Member VALUES ('182029*****', '那个秀才', 888.0);",
            u"INSERT INTO Log VALUES ('182029*****', '那个秀才', 111.0, 888.0, '{0}');".format(TIMESTAMP())
        )
        for _ in CREATE:
            db.Execute(_)
        for _ in INSERT:
            db.Execute(_)


class Frame(wx.Frame):
    FontPointSize = 9
    IdBill = wx.NewId()

    # TODO: 将一票同质布局类归一
    class Register(wx.Dialog):
        IdOK = wx.NewId()
        def __init__(self, parent, title, data):
            wx.Dialog.__init__(self, parent, title=title)
            self.data = data
            font = self.GetFont()
            font.SetPointSize(Frame.FontPointSize * 1.5)
            self.CenterOnParent()
            sizerV = wx.BoxSizer(wx.VERTICAL)
            sizerH = wx.BoxSizer(wx.HORIZONTAL)
            sizerH.Add(wx.StaticText(self, label=u"店长姓名"), 0, wx.EXPAND)
            self.name = wx.TextCtrl(self, size=(160, 20), name="Name")
            sizerH.Add(self.name, 0, wx.EXPAND)
            sizerV.Add(sizerH, 0, wx.EXPAND)
            sizerH = wx.BoxSizer(wx.HORIZONTAL)
            sizerH.Add(wx.StaticText(self, label=u"登陆密码"), 0, wx.EXPAND)
            self.password = wx.TextCtrl(self, size=(160, 20), name="Password")
            sizerH.Add(self.password, 0, wx.EXPAND)
            sizerV.Add(sizerH, 0, wx.EXPAND)
            sizerH = wx.BoxSizer(wx.HORIZONTAL)
            sizerH.Add(wx.StaticText(self, label=u"手机号码"), 0, wx.EXPAND)
            self.phonenumber = wx.TextCtrl(self, size=(160, 20), name="PhoneNumber")
            sizerH.Add(self.phonenumber, 0, wx.EXPAND)
            sizerV.Add(sizerH, 0, wx.EXPAND)
            sizerH = wx.BoxSizer(wx.HORIZONTAL)
            sizerH.Add(wx.StaticText(self, label=u"地址招牌"), 0, wx.EXPAND)
            self.addresssign = wx.TextCtrl(self, size=(160, 20), name="Address")
            sizerH.Add(self.addresssign, 0, wx.EXPAND)
            sizerV.Add(sizerH, 0, wx.EXPAND)
            sizerH = wx.BoxSizer(wx.HORIZONTAL)
            sizerH.Add(wx.StaticText(self, label=u"验证编码"), 0, wx.EXPAND)
            self.verifycode = wx.TextCtrl(self, size=(160, 20), name="VerifyCode")
            sizerH.Add(self.verifycode, 0, wx.EXPAND)
            sizerV.Add(sizerH, 0, wx.EXPAND)
            button = wx.Button(self, id=Frame.Register.IdOK, label=u"确认")
            button.Bind(wx.EVT_BUTTON, self.OnOK)
            sizerV.Add(button, 0, wx.EXPAND)
            self.SetSizerAndFit(sizerV)
            self.Bind(wx.EVT_TEXT, self.OnText)
            self.status = None
        def OnText(self, evt):
            _ = evt.GetEventObject()
            self.data[_.GetName()] = _.GetValue()
        def OnOK(self, evt):
            _ = self.verifycode.GetValue()
            try:
                __ = base64.b64decode(_)
                i, ii, iii = __.split("#")
                i = int(i)
                ii = int(ii)
                iii = int(iii)
                assert i%9527 == 0 and ii%9527 == 0
                self.data[self.verifycode.GetName()] = DELTATIMESTAMP(DELTADAYS(iii))
                self.data["VC"] = _
            except (TypeError, ValueError, AssertionError) as e:
                wx.MessageBox(u"验证编码错误", u"警告")
            else:
                try:
                    assert ISPHONENUMBER(self.phonenumber.GetValue())
                except AssertionError as e:
                    wx.MessageBox(u"手机号码错误", u"警告")
                else:
                    self.status = Frame.Register.IdOK
                    self.Destroy()


    class Login(wx.Dialog):
        IdOK = wx.NewId()
        def __init__(self, parent, title):
            wx.Dialog.__init__(self, parent, title=title)
            font = self.GetFont()
            font.SetPointSize(Frame.FontPointSize * 1.5)
            self.CenterOnParent()
            sizerV = wx.BoxSizer(wx.VERTICAL)
            sizerH = wx.BoxSizer(wx.HORIZONTAL)
            sizerH.Add(wx.StaticText(self, label=u"用户"), 0, wx.EXPAND)
            name = parent.database.Execute("SELECT Name FROM Manager;")[0][0]
            self.account = wx.TextCtrl(self, size=(160, 20), value=name)
            sizerH.Add(self.account, 0, wx.EXPAND)
            sizerV.Add(sizerH, 0, wx.EXPAND)
            sizerH = wx.BoxSizer(wx.HORIZONTAL)
            sizerH.Add(wx.StaticText(self, label=u"密码"), 0, wx.EXPAND)
            self.password = wx.TextCtrl(self, size=(160, 20))
            sizerH.Add(self.password, 0, wx.EXPAND)
            sizerV.Add(sizerH, 0, wx.EXPAND)
            self.ok = wx.Button(self, id=Frame.Login.IdOK, label=u"登陆")
            sizerV.Add(self.ok, 0, wx.EXPAND)
            self.SetSizerAndFit(sizerV)
            self.ok.Bind(wx.EVT_BUTTON, self.OnOK)
            self.status = None

        def OnOK(self, evt):
            self.status = evt.GetId()
            if self.status == Frame.Login.IdOK:
                account = self.account.GetValue()
                password = self.password.GetValue()
                _ = self.Parent.database.Execute(u"SELECT * FROM Manager WHERE (PhoneNumber='{account}' OR Name='{account}') AND Password='{password}';"
                                                 .format(account=account, password=password))
                if _:
                    name, password, expired, phonenumber, address, verifycode = _[0]
                    now = datetime.datetime.now()
                    expired = datetime.datetime.strptime(expired, "%Y-%m-%d %H:%M:%S")
                    if now > expired:
                        wx.MessageBox(u"试用期结束请微信加友nagexiucai申请注册", u"警告")
                        data = {}
                        dlg = Frame.Register(self, u"注册", data)
                        dlg.ShowModal()
                        if dlg.status == Frame.Register.IdOK:
                            vc = data.get("VC")
                            verifycode = data.get("VerifyCode")
                            address = data.get("Address")
                            phonenumber = data.get("PhoneNumber")
                            expired = verifycode
                            password = data.get("Password")
                            name = data.get("Name")
                            self.Parent.database.Execute(u"INSERT INTO Manager VALUES ('{name}', '{password}', '{expired}', '{phonenumber}', '{address}', '{verifycode}');"
                                                         .format(name=name, password=password, expired=expired, phonenumber=phonenumber, address=address, verifycode=verifycode))
                            self.Parent.database.Execute(u"DELETE FROM Manager WHERE PhoneNumber='182029*****';")
                            wx.MessageBox(u"已完成注册请新用户登陆", u"恭喜")
                            self.Parent.mark.SetLabel(u"已注册")
                        else:
                            wx.MessageBox(u"未完成注册", u"警告")
                    else:
                        self.Destroy()
                else:
                    wx.MessageBox(u"用户或密码错误", u"警告")

    class Recharge(wx.Dialog):
        IdOK = wx.NewId()
        IdCancel = wx.NewId()
        def __init__(self, parent, title, fresher=False):
            wx.Dialog.__init__(self, parent, title=title)
            self.fresher = fresher
            self.data = {}
            font = self.GetFont()
            font.SetPointSize(Frame.FontPointSize * 3.5)
            self.CenterOnParent()
            sizerV = wx.BoxSizer(wx.VERTICAL)
            sizerH = wx.BoxSizer(wx.HORIZONTAL)
            sizerH.Add(wx.StaticText(self, label=u"会员账号："), 0, wx.EXPAND)
            phonenumber = parent.text.GetValue()
            self.phonenumber = phonenumber
            sizerH.Add(wx.StaticText(self, label=phonenumber), -1, wx.EXPAND)
            sizerV.Add(sizerH, 0, wx.EXPAND)
            sizerH = wx.BoxSizer(wx.HORIZONTAL)
            sizerH.Add(wx.StaticText(self, label=u"会员姓名："), 0, wx.EXPAND)
            if fresher:
                name, balance = u"新会员", 0.0
                sizerH.Add(wx.TextCtrl(self, value=name, name="Name"), -1, wx.EXPAND)
            else:
                name, balance = parent.database.Execute("SELECT Name, Balance FROM Member WHERE PhoneNumber='{0}';".format(phonenumber))[0]
                sizerH.Add(wx.StaticText(self, label=name), -1, wx.EXPAND)
            sizerV.Add(sizerH, 0, wx.EXPAND)
            sizerH = wx.BoxSizer(wx.HORIZONTAL)
            self.data["BalanceReserved"] = balance
            if fresher:
                sizerH.Add(wx.StaticText(self, label=u"账户预存："), 0, wx.EXPAND)
                sizerH.Add(wx.TextCtrl(self, value=unicode(balance), name="Balance"), -1, wx.EXPAND)
            else:
                sizerH.Add(wx.StaticText(self, label=u"账户余额："), 0, wx.EXPAND)
                sizerH.Add(wx.StaticText(self, label=unicode(balance)), -1, wx.EXPAND)
            sizerV.Add(sizerH, 0, wx.EXPAND)
            if not fresher:
                self.figure = wx.TextCtrl(self, size=(120, 20), name="Balance")
                sizerV.Add(self.figure, 0, wx.EXPAND)
            sizerH = wx.BoxSizer(wx.HORIZONTAL)
            sizerH.Add(wx.Button(self, id=Frame.Recharge.IdOK, label=u"确认"), 0, wx.EXPAND)
            sizerH.Add(wx.Button(self, id=Frame.Recharge.IdCancel, label=u"取消"), 0, wx.EXPAND)
            sizerV.Add(sizerH, 0, wx.EXPAND)
            self.SetFont(font)
            self.SetSizerAndFit(sizerV)
            self.Bind(wx.EVT_TEXT, self.OnText)
            self.Bind(wx.EVT_BUTTON, self.OnButton)
        def OnText(self, evt):
            _ = evt.GetEventObject()
            self.data[_.GetName()] = _.GetValue()
        def OnButton(self, evt):
            _ = evt.GetId()
            if _ == Frame.Recharge.IdOK:
                money = self.data.get("Balance")
                try:
                    money = float(money)
                except (TypeError, ValueError) as e:
                    wx.MessageBox(u"金额错误", u"警告")
                else:
                    if self.fresher:
                        if self.data.get("Name"):
                            self.Parent.database.Execute(u"INSERT INTO Member VALUES ('{phonenumber}', '{name}', {balance});"
                                                         .format(phonenumber=self.phonenumber, name=self.data.get("Name"), balance=money))
                            self.Destroy()
                        else:
                            wx.MessageBox(u"请填写会员姓名", u"警告")
                    else:
                        balance = self.data.get("BalanceReserved") + money
                        self.Parent.database.Execute("UPDATE Member SET Balance={balance} WHERE PhoneNumber='{phonenumber}';"
                                                     .format(balance=balance, phonenumber=self.phonenumber))
                        self.Destroy()
            elif _ == Frame.Recharge.IdCancel:
                self.Destroy()

    Member = Recharge

    class Pay(wx.Dialog):
        IdOK = wx.NewId()
        IdCancel = wx.NewId()
        def __init__(self, parent, title):
            wx.Dialog.__init__(self, parent, title=title)
            font = self.GetFont()
            font.SetPointSize(Frame.FontPointSize * 1.5)
            self.CenterOnParent()
            sizerV = wx.BoxSizer(wx.VERTICAL)
            sizerH = wx.BoxSizer(wx.HORIZONTAL)
            sizerH.Add(wx.StaticText(self, label=u"会员账号："), 0, wx.EXPAND)
            self.phonenumber = parent.text.GetValue()
            sizerH.Add(wx.StaticText(self, label=self.phonenumber), -1, wx.EXPAND)
            sizerV.Add(sizerH, 0, wx.EXPAND)
            sizerH = wx.BoxSizer(wx.HORIZONTAL)
            sizerH.Add(wx.StaticText(self, label=u"会员姓名："), 0, wx.EXPAND)
            self.name, self.balance = parent.database.Execute("SELECT Name, Balance FROM Member WHERE PhoneNumber='{0}';".format(self.phonenumber))[0]
            sizerH.Add(wx.StaticText(self, label=self.name), -1, wx.EXPAND)
            sizerV.Add(sizerH, 0, wx.EXPAND)
            sizerH = wx.BoxSizer(wx.HORIZONTAL)
            sizerH.Add(wx.StaticText(self, label=u"本次消费："), 0, wx.EXPAND)
            self.consume = wx.TextCtrl(self, size=(120, 20))
            sizerH.Add(self.consume, -1, wx.EXPAND)
            sizerV.Add(sizerH, 0, wx.EXPAND)
            sizerH = wx.BoxSizer(wx.HORIZONTAL)
            sizerH.Add(wx.Button(self, id=Frame.Pay.IdOK, label=u"支付"), 0, wx.EXPAND)
            sizerH.Add(wx.Button(self, id=Frame.Pay.IdCancel, label=u"放弃"), 0, wx.EXPAND)
            sizerV.Add(sizerH, 0, wx.EXPAND)
            self.SetFont(font)
            self.SetSizerAndFit(sizerV)
            self.Bind(wx.EVT_BUTTON, self.OnButton)
        def OnButton(self, evt):
            _ = evt.GetId()
            if _ == Frame.Pay.IdOK:
                try:
                    consume = float(self.consume.GetValue())
                except ValueError as e:
                    wx.MessageBox(u"金额错误", u"警告")
                else:
                    if self.balance < consume:
                        wx.MessageBox(u"余额不足请充值", u"警告")
                    else:
                        balance = self.balance - consume
                        self.Parent.database.Execute("UPDATE Member SET Balance={balance} WHERE PhoneNumber='{phonenumber}';"
                                                     .format(balance=balance, phonenumber=self.phonenumber))
                        self.Parent.database.Execute(u"INSERT INTO Log VALUES ('{phonenumber}', '{name}', {consume}, {balance}, '{time}');"
                                                 .format(phonenumber=self.phonenumber, name=self.name, consume=consume, balance=balance, time=TIMESTAMP()))
                        self.Destroy()
                        event = wx.PyCommandEvent(eventType=EventQingDanType, id=Frame.IdBill)
                        wx.PostEvent(self.GetParent(), event)
            elif _ == Frame.Pay.IdCancel:
                self.Destroy()

    class Bill(wx.Dialog):
        def __init__(self, parent, title):
            wx.Dialog.__init__(self, parent, title=title)
            font = self.GetFont()
            font.SetPointSize(Frame.FontPointSize * 1.5)
            self.CenterOnParent()
            sizer = wx.BoxSizer(wx.VERTICAL)
            self.list = wx.ListCtrl(self, style=wx.LC_REPORT)
            self.list.InsertColumn(0, u"账号", width=240)
            self.list.InsertColumn(1, u"姓名", width=160)
            self.list.InsertColumn(2, u"消费", width=120)
            self.list.InsertColumn(3, u"余额", width=120)
            self.list.InsertColumn(4, u"时间", width=200)
            _ = parent.database.Execute("SELECT * FROM Log WHERE PhoneNumber='{0}' ORDER BY Time DESC;".format(parent.text.GetValue()))
            count = len(_)
            for phonenumber, name, consume, balance, time in _:
                i = self.list.InsertStringItem(count, phonenumber)
                self.list.SetStringItem(i, 1, name)
                self.list.SetStringItem(i, 2, unicode(consume))
                self.list.SetStringItem(i, 3, unicode(balance))
                self.list.SetStringItem(i, 4, time)
            sizer.Add(self.list, 0, wx.EXPAND)
            self.SetSizerAndFit(sizer)

    def __init__(self):
        wx.Frame.__init__(self, None, title=u"会员管理")
        self.database = Database()
        IMHO(self.database)
        self.SetIcon(ICON.GetIcon())
        self.SetMinSize((1200, 600))
        font = self.GetFont()
        Frame.FontPointSize = fontPointSize = font.GetPointSize()
        panel = wx.Panel(self)
        self.sizer = wx.GridSizer(3, 3, 5, 5)
        if self.database.Execute("SELECT * FROM Manager WHERE PhoneNumber!='182029*****';"):
            self.mark = wx.StaticText(panel, label=u"已注册", style=wx.ALIGN_CENTRE)
        else:
            self.mark = wx.StaticText(panel, label=u"未注册", style=wx.ALIGN_CENTER)
        font.SetPointSize(fontPointSize * 2.0)
        self.mark.SetOwnFont(font)
        self.brand = wx.StaticText(panel, label=u"极陋会员管理", style=wx.ALIGN_CENTER)
        font.SetPointSize(fontPointSize * 4.5)
        self.brand.SetOwnFont(font)
        sizerV = wx.BoxSizer(wx.VERTICAL)
        self.text = wx.TextCtrl(panel, style=wx.TE_CENTER)
        self.text.Disable()
        self.text.SetToolTipString(u"手机号码")
        font.SetPointSize(fontPointSize * 2.5)
        self.text.SetOwnFont(font)
        sizerV.Add(self.text, 0, wx.EXPAND)
        sizerH = wx.BoxSizer(wx.HORIZONTAL)
        self.recharge = wx.Button(panel, label=u"充值")
        self.recharge.Bind(wx.EVT_BUTTON, self.OnRecharge)
        self.pay = wx.Button(panel, label=u"结账")
        self.pay.Bind(wx.EVT_BUTTON, self.OnPay)
        self.bill = wx.Button(panel, label=u"账单", id=Frame.IdBill)
        self.bill.Bind(wx.EVT_BUTTON, self.OnBill)
        font.SetPointSize(fontPointSize * 3.0)
        self.recharge.SetOwnFont(font)
        self.pay.SetOwnFont(font)
        self.bill.SetOwnFont(font)
        sizerH.Add(self.recharge, 0, wx.EXPAND)
        sizerH.Add((-1, -1), -1, wx.EXPAND)
        sizerH.Add(self.pay, 0, wx.EXPAND)
        sizerH.Add((-1, -1), -1, wx.EXPAND)
        sizerH.Add(self.bill, 0, wx.EXPAND)
        sizerV.Add(sizerH, 0, wx.EXPAND)
        sizerVV = wx.BoxSizer(wx.VERTICAL)
        ngxc = wx.StaticText(panel, label=u"那个秀才", style=wx.ALIGN_CENTER)
        domain = wx.StaticText(panel, label=u"www.nagexiucai.com", style=wx.ALIGN_CENTER)
        font.SetPointSize(fontPointSize * 1.8)
        ngxc.SetOwnFont(font)
        domain.SetOwnFont(font)
        sizerVV.Add(ngxc, 0, wx.EXPAND)
        sizerVV.Add(domain, 0, wx.EXPAND)
        self.sizer.AddMany((
            (self.mark, 0, wx.ALIGN_LEFT | wx.ALIGN_TOP),
            (self.brand, 0, wx.ALIGN_CENTER),
            ((-1, -1), 0, wx.EXPAND),
            ((-1, -1), 0, wx.EXPAND),
            (sizerV, 0, wx.EXPAND),
            ((-1, -1), 0, wx.EXPAND),
            ((-1, -1), 0, wx.EXPAND),
            (sizerVV, 0, wx.ALIGN_CENTER),
            ((-1, -1), 0, wx.EXPAND)))
        panel.SetSizer(self.sizer)
        self.sizer.Fit(panel)
        self.Fit()
        self.CenterOnScreen()
        self.Show(True)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnLogin)
        self.timer.Start(600, True)
        self.Bind(EventQingDanBinder, self.OnBill)

    def Check(self):
        phonenumber = self.text.GetValue()
        if ISPHONENUMBER(phonenumber):
            if self.database.Execute("SELECT Name, Balance FROM Member WHERE PhoneNumber='{0}';".format(phonenumber)):
                return True
            else:
                wx.MessageBox(u"非会员请注册", u"抱歉")
                dlg = Frame.Member(self, u"注册", True)
                dlg.ShowModal()
        else:
            wx.MessageBox(u"不是手机号码", u"警告")

    def OnRecharge(self, evt):
        if self.Check():
            dlg = Frame.Recharge(self, u"充值")
            dlg.ShowModal()

    def OnPay(self, evt):
        if self.Check():
            dlg = Frame.Pay(self, u"结账")
            dlg.ShowModal()

    def OnBill(self, evt):
        if self.Check():
            dlg = Frame.Bill(self, u"账单")
            dlg.ShowModal()

    def OnLogin(self, evt=None):
        dlg = Frame.Login(self, u"登陆")
        dlg.ShowModal()
        if dlg.status == Frame.Login.IdOK:
            self.text.Enable()
        else:
            wx.MessageBox(u"必须登陆", u"警告")
            self.Destroy()


app = wx.App()
frame = Frame()
app.MainLoop()
