#coding:utf-8
import multiprocessing
import os
import sys
from src.elements.config_page import ConfigPagr
from src.elements.m_thread import MSocket
from src.elements.monitor import Monitor
from src.elements.translate import TranslateObjcet
import os
import tkinter.messagebox

if __name__=='__main__':
    #判断是否启动
    # for it in os.popen('tasklist').readlines():
    #     print(it)
        # if 'python.exe' in it.split()[0:1]:
        #     tkinter.messagebox.showerror('错误', '请勿重复打开!')
        #     sys.exit(0)
    # Monitor()
    tobs = TranslateObjcet()
    # #配置文件默认路径
    # root_path = tobs.repleceFileSeparator(os.getcwd())
    # root_path = os.path.split(os.path.realpath(__file__))[0]
    # root_path = os.path.dirname(os.path.realpath(__file__))
    root_path = os.path.abspath(sys.argv[0])
    root_path = os.path.dirname(root_path)
    config_path =tobs.repleceFileSeparator(root_path+"/tanslate.config")
    # #读取配置信息
    config = ConfigPagr(config_path)
    infoArr = config.read()
    # # print(infoArr)
    #根据配置信息 1-启动监听线程 2.打开sock服务监听指定端口
    tobs.initValue(infoArr['ffmpeg'],infoArr['dirctory'], infoArr['time'])
    MSocket(infoArr['port'],tobs)