#!/usr/bin/python
# -*- coding: utf-8 -*-


__author__ = 'nagexiucai.com'

import wx as UI
import wx.dataview as UIDV
import sqlite3 as DB
import os
import sys
import string
import datetime
import wmi
import base64
import uuid

DBFILE = "./aio.dll"
TIMESTAMP = lambda: datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

UNIQUE = 1
FIXED = 0
DEFAULT = AUTO = -1

PhoneNumberLength = 11
PasswordLengthMax = 12
PasswordLengthMin = 6
MagicNumber = 9527
MagicAlgorithm = lambda i, ii: i%MagicNumber == 0 and ii%MagicNumber == 0

class Database:
    CONNECT = None
    def __init__(self):
        if Database.CONNECT is None:
            Database.CONNECT = DB.connect(DBFILE)
    def __del__(self):
        if Database.CONNECT is not None:
            Database.CONNECT.close()
    def Initialize(self):
        CREATE = (
            "CREATE TABLE Trojan (UUID TEXT, SN TEXT);",
            "CREATE TABLE GuanLi (ZunXingDaMing TEXT, DaSiDouBuShuo TEXT, ExpiredDate TEXT, Power TEXT, PhoneNumber TEXT, Signboard TEXT, Address TEXT, SN TEXT);",

            "CREATE TABLE HuiYuan (PhoneNumber TEXT, Name TEXT, Balance FLOAT, Credit INT);",
            "CREATE TABLE DanXiang (Number TEXT, Name TEXT, Price FLOAT);",
            "CREATE TABLE TaoCan (Combination TEXT, Name TEXT, Price FLOAT);",
            "CREATE TABLE YouHui (Number TEXT, Activity TEXT, Factor FLOAT);",
            "CREATE TABLE QingDan (PhoneNumber TEXT, Service TEXT, Discount TEXT, Fee FLOAT, Balance FLOAT, Timestamp TEXT);"
        )
        expiredDate = (datetime.datetime.now() + datetime.timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
        INSERT = (
            "INSERT INTO Trojan VALUES ('{UUID}', '{SN}');".format(UUID=str(uuid.uuid1()), SN=InOut.MainboardSN()),
            u"INSERT INTO GuanLi VALUES ('nagexiucai.com', 'nagexiucai.com', '{0}', 'ALL', 'nagexiucai.com', 'nagexiucai.com', 'nagexiucai.com', 'IGNORED');".format(expiredDate),

            u"INSERT INTO HuiYuan VALUES ('182029*****', '那个秀才', 33.33, 0);",
            u"INSERT INTO HuiYuan VALUES ('182918*****', '大海', 77.77, 0);",
            u"INSERT INTO HuiYuan VALUES ('88888888888', '狗娃', 228.22, 7);",

            u"INSERT INTO DanXiang VALUES ('X', '吹一', 30.00);",
            u"INSERT INTO DanXiang VALUES ('Y', '染一', 90.00);",
            u"INSERT INTO DanXiang VALUES ('Z', '洗二', 88.00);",
            u"INSERT INTO DanXiang VALUES ('A', '洗一', 10.00);",
            u"INSERT INTO DanXiang VALUES ('B', '染二', 11.00);",
            u"INSERT INTO DanXiang VALUES ('C', '染三', 12.00);",
            u"INSERT INTO DanXiang VALUES ('D', '吹二', 13.00);",
            u"INSERT INTO DanXiang VALUES ('E', '烫一', 14.00);",
            u"INSERT INTO DanXiang VALUES ('F', '烫二', 15.00);",
            u"INSERT INTO DanXiang VALUES ('G', '烫三', 16.00);",
            u"INSERT INTO DanXiang VALUES ('H', '拉一', 17.00);",
            u"INSERT INTO DanXiang VALUES ('I', '拉二', 18.00);",
            u"INSERT INTO DanXiang VALUES ('J', '剪一', 19.00);",
            u"INSERT INTO DanXiang VALUES ('K', '剪二', 20.00);",

            u"INSERT INTO TaoCan VALUES ('Z', '无', 0.00);",
            u"INSERT INTO TaoCan VALUES ('X+Y', '吹一加染一', 55.55);",
            u"INSERT INTO TaoCan VALUES ('Y+Z+D', '染一加洗二加吹二', 99.99);",
            u"INSERT INTO TaoCan VALUES ('G+H+J', '烫三加垃一加剪一', 29.90);",

            u"INSERT INTO YouHui VALUES ('z', '议价', 1.00);",
            u"INSERT INTO YouHui VALUES ('i', '新春五折特惠', 0.50);",
            u"INSERT INTO YouHui VALUES ('j', '开业八八折券', 0.88);",

            u"INSERT INTO QingDan VALUES ('88888888888', '吹一加染一，洗二', '新春五折特惠', 71.78, 228.22, '2018-02-15 20:30:00');"
        )
        for _ in CREATE:
            self.Execute(_)
        for _ in INSERT:
            self.Execute(_)
    def Clear(self):pass
    def Execute(self, sql): # TODO: make many
        # print "[SQL]", sql
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
        print self.Execute("SELECT * FROM HuiYuan;")
        print self.Execute("SELECT * FROM DanXiang;")
        self.Execute("INSERT INTO DanXiang VALUES ('H', 'What', 22.22);")
        print self.Execute("SELECT * FROM DanXiang;")

# XXX: quirk of wx(WX3.0 at least)
# Must be a subclass of PyValidator will call TransferToWindow automatically
# Must be close by builtin OK button will call TransferFromWindow automatically

class TextValidator(UI.PyValidator): # FIXME: WX3.0
# class TextValidator(UI.Validator):
    KeyArrow = (UI.WXK_UP, UI.WXK_DOWN, UI.WXK_LEFT, UI.WXK_RIGHT)
    KeyDecimalPoint = (UI.WXK_DECIMAL, UI.WXK_NUMPAD_DECIMAL)
    KeyNumberInKeypad = (UI.WXK_NUMPAD0, UI.WXK_NUMPAD1, UI.WXK_NUMPAD2, UI.WXK_NUMPAD3, UI.WXK_NUMPAD4, UI.WXK_NUMPAD5, UI.WXK_NUMPAD6, UI.WXK_NUMPAD7, UI.WXK_NUMPAD8, UI.WXK_NUMPAD9)
    def __init__(self, f, k, data):
        UI.PyValidator.__init__(self)
        # UI.Validator.__init__(self)
        self.f = f
        self.k = k
        self.data = data
        self.Bind(UI.EVT_CHAR, self.OnChar)
    def Clone(self):
        return TextValidator(self.f, self.k, self.data)
    def Validate(self, parent):
        return True
    def TransferToWindow(self):
        self.GetWindow().SetValue(unicode(self.data.get(self.k))) # TODO: 无论何种类型展示到窗体一律文本
        return True
    def TransferFromWindow(self):
        self.data[self.k] = self.f(self.GetWindow().GetValue())
        return True
    def OnChar(self, evt):
        keycode = evt.GetKeyCode() # TODO: use wxk
        if self.f is float:
            if keycode < 256 and chr(keycode) in "+-."+string.digits or keycode in (314, 315, 316, 317, 8, 13, 127):
                evt.Skip()
        elif self.f is int:
            if keycode < 256 and chr(keycode) in "+-"+string.digits or keycode in (314, 315, 316, 317, 8, 13, 127):
                evt.Skip()
        else:
            evt.Skip()

class JiHuo(UI.Dialog):
    IdOK = UI.NewId()
    def __init__(self, parent, title, data):
        UI.Dialog.__init__(self, parent)
        self.UserData = data
        self.status = None
        sizerV = UI.BoxSizer(UI.VERTICAL)
        sizerH = UI.BoxSizer(UI.HORIZONTAL)
        sizerH.Add(UI.StaticText(self, label=u"尊姓大名"), proportion=FIXED, flag=UI.EXPAND|UI.LEFT|UI.RIGHT)
        sizerH.Add(UI.TextCtrl(self, name="ZunXingDaMing", size=(160, 20)), proportion=FIXED, flag=UI.EXPAND|UI.LEFT|UI.RIGHT)
        sizerV.Add(sizerH, proportion=FIXED, flag=UI.EXPAND|UI.ALL)
        sizerH = UI.BoxSizer(UI.HORIZONTAL)
        sizerH.Add(UI.StaticText(self, label=u"账户密码"), proportion=FIXED, flag=UI.EXPAND|UI.LEFT|UI.RIGHT)
        sizerH.Add(UI.TextCtrl(self, name="DaSiDouBuShuo", size=(160, 20)), proportion=FIXED, flag=UI.EXPAND|UI.LEFT|UI.RIGHT)
        sizerV.Add(sizerH, proportion=FIXED, flag=UI.EXPAND|UI.ALL)
        sizerH = UI.BoxSizer(UI.HORIZONTAL)
        sizerH.Add(UI.StaticText(self, label=u"手机号码"), proportion=FIXED, flag=UI.EXPAND|UI.LEFT|UI.RIGHT)
        sizerH.Add(UI.TextCtrl(self, name="PhoneNumber", size=(160, 20)), proportion=FIXED, flag=UI.EXPAND|UI.LEFT|UI.RIGHT)
        sizerV.Add(sizerH, proportion=FIXED, flag=UI.EXPAND|UI.ALL)
        sizerH = UI.BoxSizer(UI.HORIZONTAL)
        sizerH.Add(UI.StaticText(self, label=u"招牌字号"), proportion=FIXED, flag=UI.EXPAND|UI.LEFT|UI.RIGHT)
        sizerH.Add(UI.TextCtrl(self, name="Signboard", size=(160, 20)), proportion=FIXED, flag=UI.EXPAND|UI.LEFT|UI.RIGHT)
        sizerV.Add(sizerH, proportion=FIXED, flag=UI.EXPAND|UI.ALL)
        sizerH = UI.BoxSizer(UI.HORIZONTAL)
        sizerH.Add(UI.StaticText(self, label=u"贵店地址"), proportion=FIXED, flag=UI.EXPAND|UI.LEFT|UI.RIGHT)
        sizerH.Add(UI.TextCtrl(self, name="Address", size=(160, 20)), proportion=FIXED, flag=UI.EXPAND|UI.LEFT|UI.RIGHT)
        sizerV.Add(sizerH, proportion=FIXED, flag=UI.EXPAND|UI.ALL)
        sizerV.Add(UI.Button(self, id=JiHuo.IdOK, label=u"确认"), proportion=FIXED, flag=UI.EXPAND|UI.ALL)
        self.SetSizerAndFit(sizerV)
        self.Bind(UI.EVT_TEXT, self.OnText)
        self.Bind(UI.EVT_BUTTON, self.OnOK)
    def OnText(self, evt):
        _ = evt.GetEventObject()
        self.UserData[_.GetName()] = _.GetValue()
    def OnOK(self, evt):
        self.status = JiHuo.IdOK
        zxdm = self.UserData.get("ZunXingDaMing")
        dsdbs = self.UserData.get("DaSiDouBuShuo")
        pn = self.UserData.get("PhoneNumber")
        s = self.UserData.get("Signboard")
        a = self.UserData.get("Address")
        if zxdm and dsdbs and pn and s and a:
            try:
                assert len(pn) == PhoneNumberLength # TODO: 手机号码位数
                int(pn)
            except AssertionError, ValueError:
                UI.MessageBox(u"手机号码可能不正确", u"警告")
            else:
                try:
                    assert PasswordLengthMax >= len(dsdbs) >= PasswordLengthMin
                    for c in dsdbs:
                        assert c in string.letters or c in string.digits
                except AssertionError:
                    UI.MessageBox(u"账户密码必须六位到十二位数字或字母", u"警告")
                else:
                    self.Destroy()
        else:
            UI.MessageBox(u"全部必填", u"注意")

class QingDan(UI.Panel):
    def __init__(self, parent, who=None):
        UI.Panel.__init__(self, parent)
        self.sizer = UI.BoxSizer(UI.VERTICAL)
        self.dvlc = UIDV.DataViewListCtrl(self)
        self.dvlc.AppendTextColumn("PhoneNumber", width=130)
        self.dvlc.AppendTextColumn("Service", width=180)
        self.dvlc.AppendTextColumn("Discount", width=120)
        self.dvlc.AppendTextColumn("Fee", width=90)
        self.dvlc.AppendTextColumn("Balance", width=90)
        self.dvlc.AppendTextColumn("Timestamp", width=160)
        _ = parent.database.Execute("SELECT * FROM QingDan WHERE PhoneNumber='{0}' ORDER BY Timestamp DESC;".format(who))
        for phonenumber, service, discount, fee, balance, timestamp in _:
            self.dvlc.AppendItem((phonenumber, service, discount, unicode(fee), unicode(balance), timestamp))
        self.sizer.Add(self.dvlc, proportion=AUTO, flag=UI.EXPAND|UI.ALL)
        self.SetSizerAndFit(self.sizer)

class JieZhang(UI.Panel):
    RowNumber = 0
    ColumnNumber = 3
    HorizontalGap = 5
    VerticalGap = 5
    IdDue = UI.NewId()
    IdSearch = UI.NewId()
    IdBalance = UI.NewId()
    IdPay = UI.NewId()
    MajorDimension = 5
    def __init__(self, parent):
        UI.Panel.__init__(self, parent)
        self.sizer = UI.BoxSizer(UI.VERTICAL)
        staticBoxDX = UI.StaticBox(self, label=u"单项")
        staticBoxSizerDX = UI.StaticBoxSizer(staticBoxDX, UI.VERTICAL)
        _dx = parent.database.Execute("SELECT * FROM DanXiang;")
        sizerDX = UI.GridSizer(JieZhang.RowNumber, JieZhang.ColumnNumber) # FIXME: WX3.0 has a __init__(int, int) overload
        # sizerDX = UI.GridSizer(JieZhang.ColumnNumber, gap=(JieZhang.HorizontalGap, JieZhang.VerticalGap))
        self.checkbox = []
        for number, name, price in _dx:
            cb = UI.CheckBox(self, label=name)
            setattr(cb, "UserData", {"Number": number, "Name": name, "Price": price})
            self.checkbox.append(cb)
            sizerDX.Add(cb, proportion=FIXED, flag=UI.EXPAND|UI.ALL)
        staticBoxSizerDX.Add(sizerDX, proportion=FIXED, flag=UI.EXPAND|UI.ALL)
        _tc = parent.database.Execute("SELECT * FROM TaoCan;")
        item = []
        data = {}
        for combination, name, price in _tc:
            item.append(name)
            data[name] = {"Combination": combination, "Name": name, "Price": price}
        radioBoxTC = UI.RadioBox(self, label=u"套餐", choices=item, majorDimension=JieZhang.MajorDimension)
        setattr(radioBoxTC, "UserData", data)
        self.sizer.Add(staticBoxSizerDX, proportion=FIXED, flag=UI.EXPAND|UI.ALL)
        self.sizer.Add(radioBoxTC, proportion=FIXED, flag=UI.EXPAND|UI.LEFT|UI.RIGHT)
        _yh = parent.database.Execute("SELECT * FROM YouHui;")
        item = []
        data = {}
        for number, activity, factor in _yh:
            item.append(activity)
            data[activity] = {"Number": number, "Activity": activity, "Factor": factor}
        radioBoxYH = UI.RadioBox(self, label=u"优惠", choices=item, majorDimension=JieZhang.MajorDimension)
        setattr(radioBoxYH, "UserData", data)
        self.sizer.Add(radioBoxYH, proportion=FIXED, flag=UI.EXPAND|UI.LEFT|UI.RIGHT)
        sizerH = UI.BoxSizer(UI.HORIZONTAL)
        sizerV = UI.BoxSizer(UI.VERTICAL)
        self.due = UI.StaticText(self, id=JieZhang.IdDue, label=u"应付：0.00")
        self.search = UI.SearchCtrl(self, id=JieZhang.IdSearch, style=UI.TE_PROCESS_ENTER) # FIXME: 禁止输入SQL敏感字符
        self.balance = UI.StaticText(self, id=JieZhang.IdBalance, label=u"姓名：余额")
        self.pay = UI.Button(self, id=JieZhang.IdPay, label=u"支付")
        sizerV.Add(self.due, proportion=FIXED, flag=UI.EXPAND|UI.LEFT|UI.RIGHT)
        sizerV.Add(self.search, proportion=FIXED, flag=UI.EXPAND|UI.LEFT|UI.RIGHT)
        sizerV.Add(self.balance, proportion=FIXED, flag=UI.EXPAND|UI.LEFT|UI.RIGHT)
        sizerV.Add(self.pay, proportion=FIXED, flag=UI.EXPAND|UI.LEFT|UI.RIGHT)
        sizerH.Add((AUTO, AUTO), proportion=AUTO, flag=UI.EXPAND|UI.ALL) # FIXME: WX3.0 has no Add(int,int,proportion=0,flag=0) compatible
        # sizerH.Add(AUTO, AUTO, proportion=AUTO, flag=UI.EXPAND | UI.ALL)
        sizerH.Add(sizerV, proportion=FIXED, flag=UI.EXPAND|UI.ALL)
        sizerH.Add((AUTO, AUTO), proportion=AUTO, flag=UI.EXPAND|UI.ALL)
        self.sizer.Add(sizerH, proportion=AUTO, flag=UI.EXPAND|UI.ALL)
        self.SetSizerAndFit(self.sizer)
        self.search.ShowCancelButton(True)
        self.search.Bind(UI.EVT_SEARCHCTRL_CANCEL_BTN, self.OnCancel)
        self.search.Bind(UI.EVT_SEARCHCTRL_SEARCH_BTN, self.OnSearch)
        self.search.Bind(UI.EVT_TEXT_ENTER, self.OnSearch)
        self.pay.Disable()
        self.pay.Bind(UI.EVT_BUTTON, self.OnPay)
        self.keyword = None
        self.dx = 0.00
        self.dxItem = []
        self.tc = 0.00
        self.tcItem = None
        self.yh = 1.00
        self.yhItem = None
        self.total = 0.00
        self.Bind(UI.EVT_CHECKBOX, self.OnCheckBox)
        radioBoxTC.Bind(UI.EVT_RADIOBOX, self.OnRadioBoxTC)
        radioBoxYH.Bind(UI.EVT_RADIOBOX, self.OnRadioBoxYH)
    def OnCancel(self, evt):
        self.keyword = None
        self.pay.Disable()
        self.balance.SetLabelText(u"姓名：余额")
        self.search.SetValue(UI.EmptyString)
    def OnSearch(self, evt):
        keyword = phonenumber = self.search.GetValue()
        if keyword:
            record = self.Parent.database.Execute("SELECT * FROM HuiYuan WHERE PhoneNumber='{0}';".format(keyword))
            if record:
                phonenumber, name, balance, credit = record[0] # 前提逻辑保证keyword为主键（不重复）
                assert phonenumber == keyword
                self.balance.SetLabelText(u"：".join((name, unicode(balance))))
                self.keyword = keyword
                self.pay.Enable()
            else:
                UI.MessageBox(u"号码‘{0}’还未注册为会员".format(phonenumber), u"抱歉")
    def OnPay(self, evt):
        if UI.MessageBox(u"客户{user}同意扣款{money}么".format(user=self.keyword, money=self.total), u"警告", style=UI.OK|UI.CANCEL) == UI.OK:
            # print u"扣款", TIMESTAMP()
            _ = self.Parent.database.Execute("SELECT Balance FROM HuiYuan WHERE PhoneNumber='{0}'".format(self.keyword))[0][0]
            if self.total > _:
                UI.MessageBox(u"余额不足请充值", u"天呐")
                return None
            self.Parent.database.Execute("UPDATE HuiYuan SET Balance={balance} WHERE PhoneNumber='{0}';".format(self.keyword, balance=_ - self.total))
            # TODO: 需要把Service字段做成“单项（单价）加单项（单价）……·套价，单项（单价）”以应对本次交易后单项或套餐可能的修改否
            service = []
            if self.tcItem is not None:
                service.append(self.tcItem)
            service.extend(self.dxItem)
            self.Parent.database.Execute(u"INSERT INTO QingDan VALUES ('{phonenumber}', '{service}', '{discount}', {fee}, {balance}, '{timestamp}');"
                                         .format(phonenumber=self.keyword, service=u"，".join(service), discount=self.yhItem, fee=self.total, balance=_ - self.total, timestamp=TIMESTAMP()))
            # TODO: 转向清单页签
            # event = UI.MenuEvent(type=UI.wxEVT_MENU, id=Frame.IdQingDan, menu=self.Parent.bill) # TODO: why a sensitive keyword parameter named type
            event = Frame.CustomizedEvent(eventType=Frame.EventQingDanType, id=Frame.IdQingDan)
            event._SetUserData(self.keyword)
            UI.PostEvent(self.GetParent(), event)
            self.OnCancel(None) # XXX: 早于自定义事件传递self.keyword值会把self.keyword置为None的
    def OnCheckBox(self, evt):
        cb = evt.GetEventObject()
        _ = cb.UserData.get("Price")
        __ = cb.UserData.get("Name")
        if cb.IsChecked():
            self.dx += _
            self.dxItem.append(__)
        else:
            self.dx -= _
            self.dxItem.pop(self.dxItem.index(__))
        self.UpdateTotal()
    def OnRadioBoxTC(self, evt):
        rb = evt.GetEventObject()
        name = evt.GetString()
        _ = rb.UserData.get(name).get("Price")
        __ = rb.UserData.get(name).get("Name")
        self.tc = _
        self.tcItem = __
        self.UpdateTotal()
    def OnRadioBoxYH(self, evt):
        rb = evt.GetEventObject()
        name = evt.GetString()
        _ = rb.UserData.get(name).get("Factor")
        __ = rb.UserData.get(name).get("Activity")
        self.yh = _
        self.yhItem = __
        self.UpdateTotal()
    def UpdateTotal(self):
        self.total = (self.dx + self.tc) * self.yh
        self.due.SetLabelText(u"应付：%.2f" % self.total)

class HuiYuan(UI.Panel):
    IdCreate = UI.NewId()
    IdDelete = UI.NewId()
    IdModify = UI.NewId()
    def __init__(self, parent):
        UI.Panel.__init__(self, parent)
        self.sizer = UI.BoxSizer(UI.VERTICAL)
        self.dvlc = UIDV.DataViewListCtrl(self)
        self.title = ("PhoneNumber", "Name", "Balance", "Credit")
        self.dvlc.AppendTextColumn("PhoneNumber", width=130)
        self.dvlc.AppendTextColumn("Name", width=180)
        self.dvlc.AppendTextColumn("Balance", width=90)
        self.dvlc.AppendTextColumn("Credit", width=70)
        _ = parent.database.Execute("SELECT * FROM HuiYuan ORDER BY PhoneNumber;")
        for phonenumber, name, balance, credit in _:
            self.dvlc.AppendItem((phonenumber, name, unicode(balance), unicode(credit)))
        self.sizer.Add(self.dvlc, proportion=AUTO, flag=UI.EXPAND|UI.ALL)
        # sizerH = UI.BoxSizer(UI.HORIZONTAL)
        # b = UI.Button(self, id=HuiYuan.IdCreate, label="+")
        # sizerH.Add(b, proportion=FIXED)
        # b = UI.Button(self, id=HuiYuan.IdDelete, label="-")
        # sizerH.Add(b, proportion=FIXED)
        # b = UI.Button(self, id=HuiYuan.IdModify, label="/")
        # sizerH.Add(b, proportion=FIXED)
        # self.sizer.Add(sizerH, proportion=FIXED, flag=UI.EXPAND|UI.LEFT|UI.RIGHT)
        self.SetSizerAndFit(self.sizer)
        # self.Bind(UI.EVT_BUTTON, self.OnButton)
        self.dvlc.Bind(UIDV.EVT_DATAVIEW_ITEM_ACTIVATED, self.OnDataViewItem)
    def OnDataViewItem(self, evt):
        _ = evt.GetEventObject()
        r = _.GetSelectedRow()
        n = _.GetColumnCount()
        data = {}
        for i, k in enumerate(self.title):
            data[k] = _.GetValue(r, i)
        # XXX: PATCH START
        data["Balance"] = float(data.get("Balance"))
        data["Credit"] = int(data.get("Credit"))
        # XXX: PATH END
        dlg = Record(self, u"信息", data)
        dlg.ShowModal()
        if dlg.status == Record.IdRemove:
            UI.MessageBox(u"删除会员需要激活", u"可惜")
            # self.Parent.database.Execute("DELETE FROM HuiYuan WHERE PhoneNumber='{0}';".format(data.get("PhoneNumber")))
            # _.DeleteItem(r)
        elif dlg.status == Record.IdOK:
            phonenumber = data.get("PhoneNumber")
            if phonenumber != _.GetValue(r, 0): # TODO: 如果主键被修改认为是新增
                if self.Parent.database.Execute("SELECT * FROM HuiYuan WHERE PhoneNumber='{0}';".format(phonenumber)):
                    UI.MessageBox(u"号码重复请更新已注册的", u"注意")
                    return None
                record = []
                for x in self.title:
                    xx = data.get(x)
                    record.append(float(xx) if x == "Balance" else int(xx) if x == "Credit" else xx)
                record = tuple(record)
                _.AppendItem(record)
                self.Parent.database.Execute(u"INSERT INTO HuiYuan VALUES ('%s', '%s', %0.2f, %d);" % record)
            else:
                for i, x in enumerate(self.title):
                    _.SetValue(data.get(x), r, i)
                # XXX: PATCH START
                data["Balance"] = float(data.get("Balance"))
                data["Credit"] = int(data.get("Credit"))
                phonenumber = data.pop("PhoneNumber")
                # XXX: PATCH END
                accusative = u", ".join(["=".join((k, `v`)) if not isinstance(v, unicode) else "%s='%s'" % (k, v) for k, v in data.iteritems()])
                self.Parent.database.Execute("UPDATE HuiYuan SET %s WHERE PhoneNumber='{0}';".format(phonenumber) % accusative)
    # def OnButton(self, evt):
    #     _ = evt.GetId()
    #     if _ == HuiYuan.IdCreate:
    #         print u"新增"
    #     elif _ == HuiYuan.IdDelete:
    #         print u"删除"
    #     elif _ == HuiYuan.IdModify:
    #         print u"修改"

class Record(UI.Dialog):
    IdOK = UI.ID_OK
    IdCancel = UI.ID_CANCEL
    IdRemove = UI.NewId()
    def __init__(self, parent, title, data):
        UI.Dialog.__init__(self, parent, title=title)
        self.sizer = UI.BoxSizer(UI.VERTICAL)
        assert isinstance(data, dict)
        for k, v in data.iteritems():
            st = UI.StaticText(self, label=k, size=(80, 20))
            if isinstance(v, float): # for price etc
                tc = UI.TextCtrl(self, value=unicode(v), name=k, size=(120, 20), validator=TextValidator(float, k, data), style=UI.TE_PROCESS_ENTER) # TODO: 主键禁止修改
                tc.Validate()
            elif isinstance(v, int):
                tc = UI.TextCtrl(self, value=unicode(v), name=k, size=(120, 20), validator=TextValidator(int, k, data), style=UI.TE_PROCESS_ENTER)
                tc.Validate()
            else:
                tc = UI.TextCtrl(self, value=v, name=k, size=(120, 20), validator=TextValidator(unicode, k, data), style=UI.TE_PROCESS_ENTER)
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
        # self.Bind(UI.EVT_TEXT, self.OnText)
        self.UserData = data
        # self.DirtyUserData = {}
        cancel.SetFocus()
        self.status = None
        self.Bind(UI.EVT_TEXT_ENTER, self.OnOK)
    def OnOK(self, evt):
        self.status = Record.IdOK
        # self.UserData.update(self.DirtyUserData)
        # self.Destroy()
        self.ProcessEvent(UI.PyCommandEvent(UI.wxEVT_COMMAND_BUTTON_CLICKED, self.status))
    def OnButton(self, evt):
        _ = evt.GetId()
        self.status = _
        # if _ == Record.IdOK:
        #     self.UserData.update(self.DirtyUserData)
        if _ == Record.IdRemove:
            self.Destroy()
        else:
            evt.Skip()
    # def OnText(self, evt):
    #     _ = self.FindWindowById(evt.GetId())
    #     self.DirtyUserData[_.GetName()] = _.GetValue()

class TaoCan(UI.Panel):
    IdGenerate = UI.NewId()
    def __init__(self, parent):
        UI.Panel.__init__(self, parent)
        self.sizer = UI.BoxSizer(UI.HORIZONTAL)
        self.sizerLeft = UI.BoxSizer(UI.VERTICAL)
        self.sizerRight = UI.BoxSizer(UI.VERTICAL)
        b = UI.Button(self, id=TaoCan.IdGenerate, label=u"生成")
        b.Disable() #
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
            b.SetToolTipString(unicode(price)) # FIXME: WX3.0
            # b.SetToolTip(unicode(price))
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
        # if _ == TaoCan.IdGenerate:
        #     print u"新增"
        # else:
        #     __ = self.FindWindowById(_)
        #     data = __.UserData
        #     dlg = Record(self, data.get("Name", u"缺失异常"), data)
        #     dlg.ShowModal()
        #     if dlg.status == Record.IdRemove:
        #         print u"删除"
        #     elif dlg.status == Record.IdOK:
        #         print u"修改"

class DanXiang(UI.Panel):
    ColumnNumber = 5
    IdPlus = UI.NewId()
    HorizontalGap = 5
    VerticalGap = 5
    def __init__(self, parent):
        UI.Panel.__init__(self, parent)
        self.sizer = UI.GridBagSizer(DanXiang.VerticalGap, DanXiang.HorizontalGap) # FIXME: GridBagSizer -> GridSizer
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
            b.SetToolTipString(unicode(price)) # FIXME: WX3.0
            # b.SetToolTip(unicode(price))
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
                if self.Parent.database.Execute(u"SELECT * FROM DanXiang WHERE Number='{number}' OR Name='{name}';"
                                                .format(number=data.get("Number"), name=data.get("Name"))):
                    UI.MessageBox(u"编号或名称重复", u"注意")
                    return None
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
            _number = data.get("Number")
            _name = data.get("Name")
            _price = data.get("Price")
            dlg = Record(self, data.get("Name", u"缺失异常"), data)
            dlg.ShowModal()
            # TODO: 参与套餐的单项禁止删改
            if dlg.status == Record.IdOK:
                if _number == data.get("Number") and _name == data.get("Name") and _price == data.get("Price"):
                    return None
                if _number != data.get("Number"): # FIXME: 禁止修改单项编号
                    UI.MessageBox(u"单项编号禁止变更（请删除后或直接新增单项）", u"抱歉")
                    data["Number"] = _number
                    data["Name"] = _name
                    return None
                    # if self.Parent.database.Execute(u"SELECT * FROM TaoCan WHERE Combination LIKE '%{0}%';".format(_number)):
                    #     UI.MessageBox(u"该单项存在绑定的套餐", u"注意")
                    #     data["Number"] = _number
                    #     return None
                if _name != data.get("Name"): # FIXME: 单项名称在套餐名称是否存在绑定关系有待检查（涉及复杂场景：有套餐‘吹一加染一’恰好有单项‘加染’）
                    if self.Parent.database.Execute(u"SELECT * FROM DanXiang WHERE Name='{name}';"
                                                    .format(name=data.get("Name"))):
                        UI.MessageBox(u"名称重复", u"注意")
                        data["Number"] = _number
                        data["Name"] = _name
                        return None
                __.SetLabel(data.get("Name", u"缺失异常"))
                __.SetToolTipString(unicode(data.get("Price", u"缺失异常")))  # FIXME: WX3.0
                # __.SetToolTip(unicode(data.get("Price", u"缺失异常")))
                # FIXME: 按钮标注文字加长窗口不能自适应（需手动触发）
                self.PostSizeEventToParent()
                self.Parent.database.Execute(u"UPDATE DanXiang SET Name='{Name}', Price={Price} WHERE Number='{Number}';".format(**data))
            elif dlg.status == Record.IdRemove:
                # self.sizer.Remove(__) # FIXME: why does not work
                # self.sizer.Detach(__)
                # __.Destroy()
                # self.sizer.Layout()
                __.Disable() # TODO: 由于剔除一个元素后不能自适应布局导致有个空位进而引起新增元素时越界问题的临时方案
                self.Parent.database.Execute(u"DELETE FROM DanXiang WHERE Number='{Number}';".format(**data))

class InOut(UI.Dialog):
    IdAccount = UI.NewId()
    IdPassword = UI.NewId()
    IdOK = UI.NewId()
    User = None
    def __init__(self, parent):
        UI.Dialog.__init__(self, parent, title=u"管理")
        self.accountLabel = UI.StaticText(self, label=u"账户", size=(AUTO, 20))
        _ = self.Parent.database.Execute("SELECT * FROM GuanLi;")[0]
        zxdm, dsdbs, ed, p, pn, s, a, sn = _ # ZunXingDaMing DaSiDouBuShuo ExpiredDate Power PhoneNumber Signboard Address SN
        self.account = UI.TextCtrl(self, id=InOut.IdAccount, name=u"账户", size=(AUTO, 20), value=zxdm)
        self.passwordLabel = UI.StaticText(self, label=u"密码", size=(AUTO, 20))
        self.password = UI.TextCtrl(self, id=InOut.IdPassword, name=u"密码", size=(AUTO, 20), style=UI.TE_PASSWORD|UI.TE_PROCESS_ENTER)
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
        self.ok.Bind(UI.EVT_BUTTON, self.OnOK)
        self.password.Bind(UI.EVT_TEXT_ENTER, self.OnOK)
    def OnOK(self, evt):
        account = self.account.GetValue()
        password = self.password.GetValue()
        _ = self.Parent.database.Execute(u"SELECT * FROM GuanLi WHERE ZunXingDaMing='{account}' AND DaSiDouBuShuo='{password}';".format(account=account, password=password))
        if _:
            InOut.User = account
            self.Destroy()
        else:
            UI.MessageBox(u"请核实账户和密码", u"提示")
    @staticmethod
    def Authenticate(): # TODO: 制作和许可位码相关的鉴权
        if InOut.User is None:
            UI.MessageBox(u"请登录管理账户", u"警告")
            return False
        else:
            # TODO: 未激活是否过期、已激活是否迁移（暂时放在界面逻辑内）
            return True
    @staticmethod
    def MainboardSN():
        # os.system("wmic bios get SerialNumber > sn.txt") # XXX: 导致界面进程停机而丢失数据
        # with open("./sn.txt") as sn:
        #     return "#".join([line.strip() for line in sn.readlines()])
        aga = wmi.WMI()
        m = aga.Win32_BaseBoard()[0] # FIXME: 假定普通机器都是一块主板
        return m.SerialNumber.strip()

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
    EventQingDanType = UI.NewEventType()
    EventQingDanBinder = UI.PyEventBinder(EventQingDanType, UNIQUE)
    class CustomizedEvent(UI.PyCommandEvent):
        def __init__(self, *args, **kwargs):
            UI.PyCommandEvent.__init__(self, eventType=kwargs.get("eventType", UI.wxEVT_NULL), id=kwargs.get("id", 0))
            self.UserData = kwargs.get("userData")
        def _SetUserData(self, userData):
            self.UserData = userData
        def _GetUserData(self):
            return self.UserData
    def __init__(self):
        UI.Frame.__init__(self, None, title=u"会员管理")
        self.database = Database()
        _ = self.database.Execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table';")[0][0]
        if not _:
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
        if self.database.Execute("SELECT * FROM GuanLi WHERE ZunXingDaMing!='nagexiucai.com';"):
            self.sb.SetStatusText(u"已激活")
        else:
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
        self.Bind(Frame.EventQingDanBinder, self.OnMenu)
    def OnMenu(self, evt): # 登入、激活、作者、清单、导入、导出、升级等弹框菜单允许响应连续点击
        _ = evt.GetId()
        if _ == self.status and _ not in (Frame.IdDengRu, Frame.IdJiHuo, Frame.IdZuoZhe, Frame.IdQingDan, Frame.IdDaoRu, Frame.IdDaoChu, Frame.IdShengJi):
            return None
        __ = self.mb.FindItemById(_)
        if __ is None: # TODO: 尚未复现（在结账页签输入号码然后选择单项接着敲Enter键居然触发菜单动作）
            return None
        self.sb.SetStatusText(__.GetText())
        self.sizer.Clear(True)
        if _ == Frame.IdDengRu:
            InOut.User = None
            InOut(self).ShowModal()
            self.OnAuthenticate()
        elif _ == Frame.IdZuoZhe:
            UI.MessageBox(u"那个秀才［www.nagexiucai.com］", u"作者")
        elif _ == Frame.IdJiHuo:
            dlg = UI.TextEntryDialog(self, u"激活码（微信添加nagexiucai好友申请）", u"激活")
            dlg.ShowModal()
            code = dlg.GetValue()
            self.OnLicenseCheck(code)
        elif _ == Frame.IdDanXiang and self.status != Frame.IdDanXiang:
            self.sizer.Add(DanXiang(self), proportion=AUTO, flag=UI.EXPAND|UI.ALL)
        elif _ == Frame.IdTaoCan and self.status != Frame.IdTaoCan:
            self.sizer.Add(TaoCan(self), proportion=AUTO, flag=UI.EXPAND|UI.ALL)
        elif _ == Frame.IdHuiYuan and self.status != Frame.IdHuiYuan:
            self.sizer.Add(HuiYuan(self), proportion=AUTO, flag=UI.EXPAND|UI.ALL)
        elif _ == Frame.IdJieZhang and self.status != Frame.IdJieZhang:
            self.sizer.Add(JieZhang(self), proportion=AUTO, flag=UI.EXPAND|UI.ALL)
        elif _ == Frame.IdQingDan:
            # if isinstance(evt, UI.MenuEvent):
            if hasattr(evt, "UserData"):
                self.sizer.Add(QingDan(self, evt.UserData), proportion=AUTO, flag=UI.EXPAND|UI.ALL)
            else:
                dlg = UI.TextEntryDialog(self, u"输入要查询的会员号码", u"清单")
                dlg.ShowModal()
                self.sizer.Add(QingDan(self, dlg.GetValue()), proportion=AUTO, flag=UI.EXPAND|UI.ALL)
        elif _ == Frame.IdTuiChu:
            self.Destroy()
        self.Fit()
        self.PostSizeEvent()
        self.status = _
    def OnLicenseCheck(self, code):
        try:
            i, ii = base64.b64decode(code).split("#")
            i, ii = float(i), float(ii)
            assert MagicAlgorithm(i, ii)
        except (ValueError, TypeError, AssertionError):
            UI.MessageBox(u"非法激活码", u"警告")
        else:
            data = {}
            dlg = JiHuo(self, u"激活", data)
            dlg.ShowModal()
            zxdm = data.get("ZunXingDaMing")
            dsdbs = data.get("DaSiDouBuShuo")
            pn = data.get("PhoneNumber")
            s = data.get("Signboard")
            a = data.get("Address")
            msn = InOut.MainboardSN()
            if dlg.status == JiHuo.IdOK:
                self.database.Execute(u"INSERT INTO GuanLi VALUES ('{zxdm}', '{dsdbs}', '{ed}', '{p}', '{pn}', '{s}', '{a}', '{sn}');"
                                      .format(zxdm=zxdm, dsdbs=dsdbs, ed="2049-10-01 00:00:00", p='ALL', pn=pn, s=s, a=a, sn=msn)) # 插入新管理员
                self.database.Execute("DELETE FROM GuanLi WHERE ZunXingDaMing='nagexiucai.com';")  # 删除试用账户
                UI.MessageBox(u"已经激活（建议重新登入）", u"恭喜")
            else:
                UI.MessageBox(u"未完成激活（请输入全部注册信息并确认）", u"提示")
    def OnAuthenticate(self):
        if InOut.Authenticate():
            zxdm, dsdbs, ed, p, pn, s, a, sn = self.database.Execute("SELECT * FROM GuanLi;")[0]
            if zxdm == "nagexiucai.com":
                now = datetime.datetime.now()
                ed = datetime.datetime.strptime(ed, "%Y-%m-%d %H:%M:%S")
                if now > ed:
                    UI.MessageBox(u"试用期已尽请激活", u"抱歉")
                    self.Destroy()
            else:
                msn = InOut.MainboardSN()
                if msn != sn:
                    UI.MessageBox(u"新设备需要重新激活", u"警告")
                    self.Destroy()
        else:
            self.Destroy()
    def OnTimer(self, evt):
        _ = evt.GetId()
        if _ == Frame.IdZhangHuTimer:
            InOut(self).ShowModal()
            self.OnAuthenticate()

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
