#!/usr/bin/env python
# -*- coding:utf-8 -*-
# MOaS == Membership Open-and-Shut

import wx
from wx.lib.embeddedimage import PyEmbeddedImage


ICON = PyEmbeddedImage(
    "AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAABAT/AQYG/wIICP8FDQ7/CBIU/wwWG/8SHiT/FiQs/xssNf8WJiz/ITM8/xwsNv8ZKDD/EiMt/wg"
    "WG/8BDA7/AQUE/wEGBv8FDAz/CRMW/wwWGv8QGyH/FiQs/x4uOf8qPUv/MERU/ys/TP8rPk3/JzxK/yI0Qv8RISr/BRMU/wAFBP8FDAz/CBIS/woTGP8TICf/GCUt/xopMv8eMDr/KT5N/y9FUv89U2T/PVhs/yc"
    "7Sf8dMUD/Gi46/wYVF/8BBgf/BAsL/wYQEf8QHSH/ER8k/xcmK/8dLjX/KD1J/yo9Sv8zSVr/QVpr/0RgeP9Qcov/NEte/x8zPv8PICb/AQQE/wUMDv8KExf/EB0g/xEeIf8fLzX/HS44/zFGUf8sPkr/QFls/zp"
    "PXv9La4T/RmV8/01tg/8wSVr/ESIm/wIEBf8ECgv/DBca/w4aHf8PGx7/IDA5/xssNP8fMTj/KTpG/0Faa/9JZn3/TnCL/1J0jv8tR1r/IztJ/xosNP8AAQH/BAkL/wYPE/8LFhr/Dx0g/x0tOP8cLDf/Fict/xw"
    "rN/82TF//Plx0/1Byjf9FZn//WXyN/0Fgcf8dMTj/AQMD/wMHCf8FDRD/ChUZ/w8cI/8RHiX/FCIn/xAeJP8YJy//JjxL/zxadP9DZYH/VnyW/12Gm/9EZ3f/Gi82/wABAf8CBQb/BQwP/wgRFv8LFx//EiAp/xI"
    "eKP8VIzD/FiUt/yI4Sv8vTGb/QWSB/1F4lP9KcIT/NVRi/xcqMP8BAQH/AgUG/wMMDv8GERX/BxIZ/wwXHv8XJDH/FiMw/xYkMv8iN0j/KERe/zxfe/9BZoH/P2J0/zpYaP8QIST/AAAA/wMHCP8ECg7/BhAV/wg"
    "RGP8OGiX/DBgh/xQjM/8PGiP/Giw8/yZBW/89X3r/RWmD/0pvg/8uTVn/EiIk/wABAf8AAgL/AwgK/wQOEf8GDxT/ChYg/xMhMP8WKD7/GStB/x84Tv8qRl7/RGeD/0Vnfv80VGb/LUdU/wkVFv8AAAD/AQIC/wI"
    "GBv8CCAv/Bg4T/wgRGv8HFB3/EB4s/xQoOP8lP1b/JT5V/zpXcv82VWz/Ollu/x4zPv8CCQn/AAEA/wAAAP8CBQb/AwgI/wQKDv8HEBr/BhEX/w4ZI/8XKDn/HzNH/y1EYP8tSF//KEFV/yI6Sv8NHCH/AAIC/wA"
    "BAP8AAAD/AAAA/wIFBv8CCAv/AwsQ/wUMEv8HERr/FCAu/xgnOf8WJjn/JTpO/xQoNv8WKTT/BhMW/wABAf8BAQD/AAAA/wAAAP8BAQH/AQUG/wEFB/8BBQf/BAkO/wcNE/8LExz/Dxgj/woWH/8PHCX/CBMZ/wI"
    "JCv8AAQH/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=="
)

class Frame(wx.Frame):
    FontPointSize = 9

    # TODO: 将一票同质布局类归一
    class Register(wx.Dialog):
        def __init__(self, parent, title):
            wx.Dialog.__init__(self, parent, title=title)
            font = self.GetFont()
            font.SetPointSize(Frame.FontPointSize * 1.5)
            self.CenterOnParent()
            sizerV = wx.BoxSizer(wx.VERTICAL)
            sizerH = wx.BoxSizer(wx.HORIZONTAL)
            sizerH.Add(wx.StaticText(self, label=u"店长姓名"), 0, wx.EXPAND)
            self.leaadername = wx.TextCtrl(self, size=(160, 20))
            sizerH.Add(self.leaadername, 0, wx.EXPAND)
            sizerV.Add(sizerH, 0, wx.EXPAND)
            sizerH = wx.BoxSizer(wx.HORIZONTAL)
            sizerH.Add(wx.StaticText(self, label=u"手机号码"), 0, wx.EXPAND)
            self.phonenumber = wx.TextCtrl(self, size=(160, 20))
            sizerH.Add(self.phonenumber, 0, wx.EXPAND)
            sizerV.Add(sizerH, 0, wx.EXPAND)
            sizerH = wx.BoxSizer(wx.HORIZONTAL)
            sizerH.Add(wx.StaticText(self, label=u"地址招牌"), 0, wx.EXPAND)
            self.addresssign = wx.TextCtrl(self, size=(160, 20))
            sizerH.Add(self.addresssign, 0, wx.EXPAND)
            sizerV.Add(sizerH, 0, wx.EXPAND)
            sizerH = wx.BoxSizer(wx.HORIZONTAL)
            sizerH.Add(wx.StaticText(self, label=u"验证编码"), 0, wx.EXPAND)
            self.verifycode = wx.TextCtrl(self, size=(160, 20))
            sizerH.Add(self.verifycode, 0, wx.EXPAND)
            sizerV.Add(sizerH, 0, wx.EXPAND)
            button = wx.Button(self, id=wx.ID_OK, label=u"确认")
            sizerV.Add(button, 0, wx.EXPAND)
            self.SetSizerAndFit(sizerV)

    class Login(wx.Dialog):
        def __init__(self, parent, title):
            wx.Dialog.__init__(self, parent, title=title)
            font = self.GetFont()
            font.SetPointSize(Frame.FontPointSize * 1.5)
            self.CenterOnParent()
            sizerV = wx.BoxSizer(wx.VERTICAL)
            sizerH = wx.BoxSizer(wx.HORIZONTAL)
            sizerH.Add(wx.StaticText(self, label=u"用户"), 0, wx.EXPAND)
            self.user = wx.TextCtrl(self, size=(160, 20))
            sizerH.Add(self.user, 0, wx.EXPAND)
            sizerV.Add(sizerH, 0, wx.EXPAND)
            sizerH = wx.BoxSizer(wx.HORIZONTAL)
            sizerH.Add(wx.StaticText(self, label=u"密码"), 0, wx.EXPAND)
            self.password = wx.TextCtrl(self, size=(160, 20), style=wx.TE_PASSWORD)
            sizerH.Add(self.password, 0, wx.EXPAND)
            sizerV.Add(sizerH, 0, wx.EXPAND)
            self.ok = wx.Button(self, id=wx.ID_OK, label=u"登陆")
            sizerV.Add(self.ok, 0, wx.EXPAND)
            self.SetSizerAndFit(sizerV)
            self.ok.Bind(wx.EVT_BUTTON, self.OnOK)
            self.status = None

        def OnOK(self, evt):
            self.status = evt.GetId()
            if self.status == wx.ID_OK:
                pass
            self.Destroy()

    class Recharge(wx.Dialog):
        def __init__(self, parent, title):
            wx.Dialog.__init__(self, parent, title=title)
            font = self.GetFont()
            font.SetPointSize(Frame.FontPointSize * 3.5)
            self.CenterOnParent()
            sizerV = wx.BoxSizer(wx.VERTICAL)
            sizerH = wx.BoxSizer(wx.HORIZONTAL)
            sizerH.Add(wx.StaticText(self, label=u"会员账号："), 0, wx.EXPAND)
            account = "33388886666"
            sizerH.Add(wx.StaticText(self, label=account), -1, wx.EXPAND)
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
            sizerH.Add(wx.Button(self, id=wx.ID_OK, label=u"确认"), 0, wx.EXPAND)
            sizerH.Add(wx.Button(self, id=wx.ID_CANCEL, label=u"取消"), 0, wx.EXPAND)
            sizerV.Add(sizerH, 0, wx.EXPAND)
            self.SetFont(font)
            self.SetSizerAndFit(sizerV)

    class Pay(wx.Dialog):
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
            sizerH.Add(wx.Button(self, id=wx.ID_OK, label=u"支付"), 0, wx.EXPAND)
            sizerH.Add(wx.Button(self, id=wx.ID_CANCEL, label=u"放弃"), 0, wx.EXPAND)
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
        if dlg.status == wx.ID_OK: pass
        # self.text.Enable()

    def OnRegister(self, evt):
        dlg = Frame.Register(self, u"激活")
        dlg.ShowModal()


app = wx.App()
frame = Frame()
app.MainLoop()
