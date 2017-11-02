#coding:utf-8
import os
import sys
from tkinter import *
from wsgiref import validate
import re
from PIL import Image, ImageTk
from tkinter.filedialog import *
import tkinter.messagebox
import socket

class Window():
    def __init__(self,func):
        self.call = func
        self.wnd = Tk()
        self.wnd.protocol("WM_DELETE_WINDOW", self.client_exit)
        self.init_window()
        self.wnd.mainloop()


    def init_window(self):
        width = 280
        height = 200
        screenwidth = self.wnd.winfo_screenwidth()
        screenheight = self.wnd.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2) # 居中对齐
        self.wnd.geometry(alignstr)
        self.wnd.title("颖网科技素材转换专业版")
        # 实例化一个Menu对象，这个在主窗体添加一个菜单
        menu = Menu(self.wnd)
        self.wnd.config(menu=menu)
        # 创建菜单项
        ops = Menu(menu)
        ops.add_command(label='保存',command=self.client_save)
        ops.add_command(label='退出', command=self.client_exit)
        menu.add_cascade(label='选项', menu=ops)

        #监听目录设置
        self.dirctory = StringVar()
        Label(self.wnd, text='监听目录: ').grid(row=0,column=0, stick=W,padx=10, pady=10)
        Entry(self.wnd, textvariable=self.dirctory).grid(row=0, column=1, stick=W, pady=10)
        Button(self.wnd, text='选择', command=self.select_dirctory).grid(row=0, column=2, stick=W, pady=10)

        # 设置ffmpeg位置
        self.ffmpeg = StringVar()
        Label(self.wnd, text='FFmpeg: ').grid(row=1, column=0, stick=W, padx=10, pady=10)
        Entry(self.wnd, textvariable=self.ffmpeg).grid(row=1, column=1, stick=W, pady=10)
        Button(self.wnd, text='选择', command=self.select_ffmpeg).grid(row=1, column=2, stick=W, pady=10)


        CHECK_NUMBER = self.wnd.register(self.check_num_sfun) #包装函数 实时检测数字
        #监听时间设置
        self.time = StringVar()
        Label(self.wnd, text='轮询时间: ').grid(row=2, column=0, stick=W, padx=10, pady=10)
        Entry(self.wnd,
                textvariable=self.time,
                 validate='key',#发生任何变动的时候，就会调用validatecommand
                  validatecommand=(CHECK_NUMBER,'%P') #%P代表输入框的实时内容
                  ).grid(row=2, column=1, stick=W, pady=10)
        Label(self.wnd, text=' 秒').grid(row=2, column=2, stick=W, pady=10)

        #设置对外端口号
        self.port = StringVar()
        Label(self.wnd, text='Sock端口: ').grid(row=3, column=0, stick=W, padx=10, pady=10)
        Entry(self.wnd,
              textvariable=self.port,
              validate='key',  # 发生任何变动的时候，就会调用validatecommand
              validatecommand=(CHECK_NUMBER, '%P')  # %P代表输入框的实时内容
              ).grid(row=3, column=1, stick=W, pady=10)


    #检测是否为数字
    def check_num_sfun(self,content):
        # 如果你不加上==""的话，你就会发现删不完。总会剩下一个数字
        if content.isdigit() or (content == ""):
            return True
        else:
            return False

    #目录路径选择
    def select_dirctory(self):
        path_ = askdirectory()
        self.dirctory.set(path_)
    #ffmpeg文件选择
    def select_ffmpeg(self):
        path_ = askopenfilename(filetypes=[("all files", "*")])
        self.ffmpeg.set(path_)


        #退出
    def client_exit(self):
        sys.exit(0)

    # 退出 保存资料,并关闭自己
    def client_save(self):
        try:
            map = {}
            dirs = str(self.dirctory.get())
            #检测文件夹是否存在
            if os.path.isdir(dirs) :
                map['dirctory'] =  dirs
            else:
                raise Exception('不存在的监听目录 '+dirs+'')

            fpath = str(self.ffmpeg.get())
            if os.path.isfile(fpath) :
                map['ffmpeg'] =  fpath
            else:
                raise Exception('不存在的FFmpeg '+fpath+'')

            #检测时间是否合法
            time = 0
            try:
                time = int(self.time.get())
            except Exception as e:
                raise Exception('请设置时间 ')
            if (time <= 0):
                time = 0
            map["time"] = str(time)

            #检测端口号
            port = 0
            try:
                port = int(self.port.get())
            except Exception as e:
                print(e)
                raise Exception('请设置端口 ')
            if port <= 1023 or port > 65535:
                raise Exception('端口不在可用范围,请输入 1024-65535 任意端口 ')

            if(self.isOpenByLocal(port)):
                raise Exception('端口 '+str(port)+' 被占用.')
            map['port'] = str(port)


            self.call(map)
            self.wnd.destroy()
            self.wnd.quit()
            self.map = map

        except Exception as e:
            tkinter.messagebox.showerror('错误', e)

    def isOpenByLocal(self,port):
        try:
            address = ('127.0.0.1', port)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(address)
            s.shutdown(2)
            return True
        except Exception as e:
            return False

    #返回执行结果
    def getResource(self):
        return self.map

