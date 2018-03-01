#!/usr/bin/env python
# -*- coding:utf-8 -*-
# MOaS == Membership Open-and-Shut

import wx
from resource import ICON
from db import Database
import datetime
import base64


TIMESTAMP = lambda: datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
DELTATIMESTAMP = lambda t: (datetime.datetime.now() + t).strftime('%Y-%m-%d %H:%M:%S')
DELTADAYS = lambda d: datetime.timedelta(days=d)


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
            self.account = wx.TextCtrl(self, size=(160, 20))
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
                print _
                if _:
                    name, password, expired, phonenumber, address, verifycode = _[0]
                    now = datetime.datetime.now()
                    expired = datetime.datetime.strptime(expired, "%Y-%m-%d %H:%M:%S")
                    if now > expired:
                        wx.MessageBox(u"试用期结束请注册", u"警告")
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
                            self.Parent.database.Execute(u"DELETE FROM Manager WHERE Name='nagexiucai';")
                            wx.MessageBox(u"已完成注册请新用户登陆", u"恭喜")
                        else:
                            wx.MessageBox(u"未完成注册", u"警告")
                    else:
                        self.Destroy()
                else:
                    wx.MessageBox(u"用户或密码错误", u"警告")

    class Recharge(wx.Dialog):
        IdOK = wx.NewId()
        IdCancel = wx.NewId()
        def __init__(self, parent, title):
            wx.Dialog.__init__(self, parent, title=title)
            font = self.GetFont()
            font.SetPointSize(Frame.FontPointSize * 3.5)
            self.CenterOnParent()
            sizerV = wx.BoxSizer(wx.VERTICAL)
            sizerH = wx.BoxSizer(wx.HORIZONTAL)
            sizerH.Add(wx.StaticText(self, label=u"会员账号："), 0, wx.EXPAND)
            phonenumber = "33388886666"
            sizerH.Add(wx.StaticText(self, label=phonenumber), -1, wx.EXPAND)
            sizerV.Add(sizerH, 0, wx.EXPAND)
            sizerH = wx.BoxSizer(wx.HORIZONTAL)
            sizerH.Add(wx.StaticText(self, label=u"会员姓名："), 0, wx.EXPAND)
            name = "nagexiucai.com"
            sizerH.Add(wx.StaticText(self, label=name), -1, wx.EXPAND)
            sizerV.Add(sizerH, 0, wx.EXPAND)
            sizerH = wx.BoxSizer(wx.HORIZONTAL)
            sizerH.Add(wx.StaticText(self, label=u"账户余额："), 0, wx.EXPAND)
            balance = 0.00
            sizerH.Add(wx.StaticText(self, label=unicode(balance)), -1, wx.EXPAND)
            sizerV.Add(sizerH, 0, wx.EXPAND)
            self.figure = wx.TextCtrl(self, size=(120, 20))
            sizerV.Add(self.figure, 0, wx.EXPAND)
            sizerH = wx.BoxSizer(wx.HORIZONTAL)
            sizerH.Add(wx.Button(self, id=Frame.Recharge.IdOK, label=u"确认"), 0, wx.EXPAND)
            sizerH.Add(wx.Button(self, id=Frame.Recharge.IdCancel, label=u"取消"), 0, wx.EXPAND)
            sizerV.Add(sizerH, 0, wx.EXPAND)
            self.SetFont(font)
            self.SetSizerAndFit(sizerV)
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
            self.account = "33388886666"
            sizerH.Add(wx.StaticText(self, label=self.account), -1, wx.EXPAND)
            sizerV.Add(sizerH, 0, wx.EXPAND)
            sizerH = wx.BoxSizer(wx.HORIZONTAL)
            sizerH.Add(wx.StaticText(self, label=u"会员姓名："), 0, wx.EXPAND)
            self.name = "nagexiucai.com"
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
            count = 999
            i = self.list.InsertStringItem(count, "zzzzz")
            self.list.SetStringItem(i, 1, "xxxxx")
            self.list.SetStringItem(i, 2, "yyyyy")
            self.list.SetStringItem(i, 3, "90")
            self.list.SetStringItem(i, 4, "2000-01-01 00:00:00")
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
        self.mark = wx.StaticText(panel, label=u"未注册", style=wx.ALIGN_CENTER)
        font.SetPointSize(fontPointSize * 2.0)
        self.mark.SetOwnFont(font)
        self.brand = wx.StaticText(panel, label=u"极陋会员管理", style=wx.ALIGN_CENTER)
        font.SetPointSize(fontPointSize * 4.5)
        self.brand.SetOwnFont(font)
        sizerV = wx.BoxSizer(wx.VERTICAL)
        self.text = wx.TextCtrl(panel, style=wx.TE_CENTER | wx.TE_PROCESS_ENTER)
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
        self.bill = wx.Button(panel, label=u"账单")
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

    def OnRecharge(self, evt):
        dlg = Frame.Recharge(self, u"充值")
        dlg.ShowModal()

    def OnPay(self, evt):
        dlg = Frame.Pay(self, u"结账")
        dlg.ShowModal()

    def OnBill(self, evt):
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

    def OnRegister(self, evt):
        dlg = Frame.Register(self, u"激活")
        dlg.ShowModal()


app = wx.App()
frame = Frame()
app.MainLoop()
