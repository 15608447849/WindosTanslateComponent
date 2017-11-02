#coding:utf-8
import configparser
import os

from src.elements.windwos import Window
import tkinter.messagebox

class ConfigPagr(object):
    def __init__(self,path):
        self.path = path
        self.conf = configparser.ConfigParser()
        self.conf.read(self.path)

    def read(self):
        if os.path.exists(self.path) :
            result = self.getConfig()
            if(result is not None):
                return result
        return self.openConfigWindow()


#获取配置信息
    def getConfig(self):
        try:
            sections = self.conf.sections()
            items = self.conf.items('configuration')
            map = {}
            map['dirctory'] = items[0][1]
            map['ffmpeg'] = items[1][1]
            map['time'] = items[2][1]
            map['port'] = items[3][1]
            return map
        except Exception as e:
            print(e)
            #删除配置文件
            os.remove(self.path)
            return None

    def callback(self,map):
        #保存信息
        try:
            self.conf.add_section('configuration')
        except Exception as e:
            print(e)
        try:
            self.conf.set("configuration", "dirctory", map['dirctory'])
        except Exception as e:
            print(e)
        try:
            self.conf.set("configuration", "ffmpeg", map['ffmpeg'])
        except Exception as e:
            print(e)
        try:
            self.conf.set("configuration", "time", map['time'])
        except Exception as e:
            print(e)
        try:
            self.conf.set("configuration", "port", map['port'])
        except Exception as e:
            print(e)
        try:
            self.conf.write(open(self.path, "w"))
        except Exception as e:
            print(e)
        tkinter.messagebox.showinfo('提示', '配置成功,配置文件保存路径: ' + self.path)


    #打开配置界面
    def openConfigWindow(self):
       resp = Window(self.callback).getResource()
       return resp
