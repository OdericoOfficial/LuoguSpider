import json
import threading
from time import sleep
from tkinter import *
from tkinter import filedialog
import tkinter
from tkinter.ttk import *
from typing import Dict
from ProblemSpider import ProblemSpider, OnSpiderCompleted, OnSpiderCompleting
import tkinter.messagebox
import subprocess as sp
import os

class BaseForm(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.tk_frame__configContainer = self.__tk_frame__configContainer(self)
        self.tk_label__saveLabel = self.__tk_label__saveLabel( self.tk_frame__configContainer) 
        self.tk_input__savePath = self.__tk_input__savePath( self.tk_frame__configContainer) 
        self.tk_label__labalEdge = self.__tk_label__labalEdge( self.tk_frame__configContainer) 
        self.tk_input__edgePath = self.__tk_input__edgePath( self.tk_frame__configContainer) 
        self.tk_button__pathBtn = self.__tk_button__pathBtn( self.tk_frame__configContainer) 
        self.tk_progressbar__loadProcess = self.__tk_progressbar__loadProcess( self.tk_frame__configContainer) 
        self.tk_button__spiderBtn = self.__tk_button__spiderBtn( self.tk_frame__configContainer) 
        self.tk_label___accountLabel = self.__tk_label___accountLabel( self.tk_frame__configContainer) 
        self.tk_input___accountInput = self.__tk_input___accountInput( self.tk_frame__configContainer) 
        self.tk_label___passwordLable = self.__tk_label___passwordLable( self.tk_frame__configContainer) 
        self.tk_input___passwordInput = self.__tk_input___passwordInput( self.tk_frame__configContainer) 
        self.tk_input___threadsInput = self.__tk_input___threadsInput( self.tk_frame__configContainer) 
        self.tk_label___threadsLabel = self.__tk_label___threadsLabel( self.tk_frame__configContainer) 
        self.tk_button___opneServerBtn = self.__tk_button___opneServerBtn( self.tk_frame__configContainer) 
        self.tk_label___serverPathLabel = self.__tk_label___serverPathLabel( self.tk_frame__configContainer) 
        self.tk_input___serverPathInput = self.__tk_input___serverPathInput( self.tk_frame__configContainer) 
        self.tk_button___serverPathBtn = self.__tk_button___serverPathBtn( self.tk_frame__configContainer) 
        self.tk_button___savePathBtn = self.__tk_button___savePathBtn( self.tk_frame__configContainer) 
        self.tk_frame___chartContainer = self.__tk_frame___chartContainer(self)
    def __win(self):
        self.title("洛谷爬虫前50题版")
        # 设置窗口大小、居中
        width = 600
        height = 500
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        self.resizable(width=False, height=False)
        # 自动隐藏滚动条
    def scrollbar_autohide(self,bar,widget):
        self.__scrollbar_hide(bar,widget)
        widget.bind("<Enter>", lambda e: self.__scrollbar_show(bar,widget))
        bar.bind("<Enter>", lambda e: self.__scrollbar_show(bar,widget))
        widget.bind("<Leave>", lambda e: self.__scrollbar_hide(bar,widget))
        bar.bind("<Leave>", lambda e: self.__scrollbar_hide(bar,widget))
    
    def __scrollbar_show(self,bar,widget):
        bar.lift(widget)
    def __scrollbar_hide(self,bar,widget):
        bar.lower(widget)
    
    def vbar(self,ele, x, y, w, h, parent):
        sw = 15 # Scrollbar 宽度
        x = x + w - sw
        vbar = Scrollbar(parent)
        ele.configure(yscrollcommand=vbar.set)
        vbar.config(command=ele.yview)
        vbar.place(x=x, y=y, width=sw, height=h)
        self.scrollbar_autohide(vbar,ele)
    def __tk_frame__configContainer(self,parent):
        frame = Frame(parent,)
        frame.place(x=0, y=0, width=600, height=240)
        return frame
    def __tk_label__saveLabel(self,parent):
        label = Label(parent,text="存放路径",anchor="center", )
        label.place(x=0, y=160, width=60, height=30)
        return label
    def __tk_input__savePath(self,parent):
        ipt = Entry(parent, state=DISABLED)
        ipt.place(x=80, y=160, width=340, height=30)
        return ipt
    def __tk_label__labalEdge(self,parent):
        label = Label(parent,text="Edge路径",anchor="center", )
        label.place(x=0, y=0, width=60, height=30)
        return label
    def __tk_input__edgePath(self,parent):
        ipt = Entry(parent, state=DISABLED)
        ipt.place(x=80, y=0, width=420, height=30)
        return ipt
    def __tk_button__pathBtn(self,parent):
        btn = Button(parent, text="...", takefocus=False,)
        btn.place(x=520, y=0, width=59, height=30)
        return btn
    def __tk_progressbar__loadProcess(self,parent):
        progressbar = Progressbar(parent, orient=HORIZONTAL,)
        progressbar['maximum'] = 100
        progressbar['value'] = 0
        progressbar.place(x=0, y=200, width=500, height=30)
        return progressbar
    def __tk_button__spiderBtn(self,parent):
        btn = Button(parent, text="爬取", takefocus=False,)
        btn.place(x=440, y=160, width=60, height=30)
        return btn
    def __tk_label___accountLabel(self,parent):
        label = Label(parent,text="账号",anchor="center", )
        label.place(x=0, y=80, width=60, height=30)
        return label
    def __tk_input___accountInput(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=80, y=80, width=240, height=30)
        return ipt
    def __tk_label___passwordLable(self,parent):
        label = Label(parent,text="密码",anchor="center", )
        label.place(x=0, y=120, width=60, height=30)
        return label
    def __tk_input___passwordInput(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=80, y=120, width=420, height=30)
        return ipt

    def __tk_input___threadsInput(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=420, y=80, width=160, height=30)
        return ipt
    def __tk_label___threadsLabel(self,parent):
        label = Label(parent,text="线程数",anchor="center", )
        label.place(x=340, y=80, width=60, height=30)
        return label
    def __tk_button___opneServerBtn(self,parent):
        btn = Button(parent, text="打开前端", takefocus=False,)
        btn.place(x=520, y=200, width=60, height=30)
        return btn
    def __tk_label___serverPathLabel(self,parent):
        label = Label(parent,text="前端路径",anchor="center", )
        label.place(x=0, y=40, width=60, height=30)
        return label
    def __tk_input___serverPathInput(self,parent):
        ipt = Entry(parent, state=DISABLED)
        ipt.place(x=80, y=40, width=420, height=30)
        return ipt
    def __tk_button___serverPathBtn(self,parent):
        btn = Button(parent, text="...", takefocus=False,)
        btn.place(x=520, y=40, width=59, height=30)
        return btn
    def __tk_button___savePathBtn(self,parent):
        btn = Button(parent, text="...", takefocus=False,)
        btn.place(x=520, y=160, width=60, height=30)
        return btn
    def __tk_frame___chartContainer(self,parent):
        frame = Frame(parent,)
        frame.place(x=0, y=240, width=600, height=260)
        return frame

class LuoguForm(BaseForm):
    def __init__(self, appsettings):
        super().__init__()
        self.__cookies = appsettings['Cookies']
        self.__port = appsettings['Port']
        self.__inputInit(appsettings)
        self.tk_check_button_lmiva0ho, self.__gpu = self.__tk_check_button_lmiva0ho(self.tk_frame__configContainer, appsettings['GPU']) 
        self.tk_table___logList = self.__tk_table___logList( self.tk_frame___chartContainer) 
        self.__event_bind()

    def __inputInit(self, appsettings):
        self.tk_input__savePath.configure(state=NORMAL)
        self.tk_input__savePath.delete(0, tkinter.END)
        self.tk_input__savePath.insert(tkinter.END, appsettings['SavePath'])
        self.tk_input__savePath.configure(state=DISABLED)
        self.tk_input__edgePath.configure(state=NORMAL)
        self.tk_input__edgePath.delete(0, tkinter.END)
        self.tk_input__edgePath.insert(tkinter.END, appsettings['EdgePath'])
        self.tk_input__edgePath.configure(state=DISABLED)
        self.tk_input___serverPathInput.configure(state=NORMAL)
        self.tk_input___serverPathInput.delete(0, tkinter.END)
        self.tk_input___serverPathInput.insert(tkinter.END, appsettings['ServerPath'])
        self.tk_input___serverPathInput.configure(state=DISABLED)

        self.tk_input___accountInput.delete(0, tkinter.END)
        self.tk_input___accountInput.insert(tkinter.END, appsettings['Account'])

        self.tk_input___passwordInput.delete(0, tkinter.END)
        self.tk_input___passwordInput.insert(tkinter.END, appsettings['Password'])

        self.tk_input___threadsInput.delete(0, tkinter.END)
        self.tk_input___threadsInput.insert(tkinter.END, appsettings['Threads'])
        
    def __onSelectPathClick(self,evt):
        path = filedialog.askopenfilename()
        self.tk_input__edgePath.configure(state=NORMAL)
        self.tk_input__edgePath.delete(0, tkinter.END)
        self.tk_input__edgePath.insert(tkinter.END, path)
        self.tk_input__edgePath.configure(state=DISABLED)
        
    def __onSpiderClick(self,evt):
        edgePath = self.tk_input__edgePath.get()
        savePath = os.path.join(self.tk_input__savePath.get(), 'Problems')
        account = self.tk_input___accountInput.get()
        serverPath = self.tk_input___serverPathInput.get()
        password = self.tk_input___passwordInput.get()
        threads = self.tk_input___threadsInput.get()
        gpu = self.__gpu.get()
        cookies = self.__cookies

        try:        
            if os.path.exists(savePath):
                raise FileExistsError('该文件夹下已经存在一个Problems文件夹')
            os.mkdir(savePath)            

            tkinter.messagebox.showinfo(message='开始爬虫,如果采用Ocr模式\n登录会比较慢,也可能识别失败QAQ')
            threading.Thread(target=lambda: ProblemSpider(account, password, savePath, edgePath, gpu, int(threads), cookies)).start()
        except Exception as e:
            tkinter.messagebox.showerror(message=e.__str__())

    def __onSeletServerPathClick(self,evt):
        path = filedialog.askdirectory()
        self.tk_input___serverPathInput.configure(state=NORMAL)
        self.tk_input___serverPathInput.delete(0, tkinter.END)
        self.tk_input___serverPathInput.insert(tkinter.END, path)
        self.tk_input___serverPathInput.configure(state=DISABLED)

    def __onSavePathBtnClick(self,evt):
        path = filedialog.askdirectory()
        self.tk_input__savePath.configure(state=NORMAL)
        self.tk_input__savePath.delete(0, tkinter.END)
        self.tk_input__savePath.insert(tkinter.END, path)
        self.tk_input__savePath.configure(state=DISABLED)

    def __openServerClick(self,evt):
        try:
            if not os.path.exists(os.path.join(self.tk_input__savePath.get(), 'Problems')):
                raise FileNotFoundError('该文件夹下找不到已保存的Problems文件夹')
            
            # 配置数据库连接字符串
            savePath = os.path.join(self.tk_input__savePath.get(), 'Problems')
            dbPath = os.path.join(savePath, 'luogu.db')
            blazorPath = self.tk_input___serverPathInput.get()
            with open(os.path.join(blazorPath, 'appsettings.json'), 'r', encoding='UTF-8') as fs:
                blazorSettings = json.load(fs)
            blazorSettings['ConnectionStrings']['Sqlite'] = f'Data Source={dbPath}'
            with open(os.path.join(blazorPath, 'appsettings.json'), 'w', encoding='UTF-8') as fs:
                json.dump(blazorSettings, fs)

            args = f"dotnet run --project {blazorPath} --urls http://localhost:{self.__port}"
            sp.Popen(args, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
            tkinter.messagebox.showinfo(message=f'前端已打开在 localhost:{self.__port}')
        except Exception as e:
            tkinter.messagebox.showerror(message=e)
        
    def __disableTriggerTreeview(self,event):
        return "break"

    def __event_bind(self):
        self.tk_button__pathBtn.bind('<Button-1>',self.__onSelectPathClick)
        self.tk_button__spiderBtn.bind('<Button-1>',self.__onSpiderClick)
        self.tk_button___serverPathBtn.bind('<Button-1>',self.__onSeletServerPathClick)
        self.tk_button___opneServerBtn.bind('<Button-1>',self.__openServerClick)
        self.tk_button___savePathBtn.bind('<Button-1>',self.__onSavePathBtnClick)
        self.tk_table___logList.bind("<Button-1>", self.__disableTriggerTreeview)
        OnSpiderCompleting.append(self.__addCompletingLog)
        OnSpiderCompleted.append(self.__addCompletedLog)
        pass

    def __addCompletedLog(self, problemId):
        self.tk_table___logList.insert('', 0, values=(problemId, f'{problemId}爬取完成'))
        self.tk_table___logList.update()
        self.tk_progressbar__loadProcess['value'] += 2
        self.tk_progressbar__loadProcess.update()
        
        if self.tk_progressbar__loadProcess['value'] >= 100:
            tkinter.messagebox.showinfo(message='爬取完成')

    def __addCompletingLog(self, problemId):
        self.tk_table___logList.insert('', 0, values=(problemId, f'{problemId}开始爬取'))
        self.tk_table___logList.update()
        
    def __tk_check_button_lmiva0ho(self,parent, gpu):
        var = tkinter.BooleanVar()
        cb = tkinter.Checkbutton(parent,text="GPU", onvalue=True, offvalue=False, variable=var)
        if gpu:
            cb.select()
        cb.place(x=510, y=120, width=80, height=30)
        return cb, var
    
    def __tk_table___logList(self,parent):
        # 表头字段 表头宽度
        columns = {"题目编号":150,"信息":450}
        tk_table = Treeview(parent, show="headings", columns=list(columns),)
        for text, width in columns.items():  # 批量设置列属性
            tk_table.heading(text, text=text, anchor='center')
            tk_table.column(text, anchor='center', width=width, stretch=False)  # stretch 不自动拉伸
        
        tk_table.place(x=0, y=0, width=600, height=260)
        self.vbar(tk_table, 0, 0, 600, 260,parent)
        return tk_table