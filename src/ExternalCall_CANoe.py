'''
Author: Fuqiang Liu <fuqiang_liu@patac.com.cn>
'''
import os
import time
import shutil
import win32com
from win32com.client import *
from win32com.client.connect import *
from win32com.client import Dispatch, constants

class CANoe:
    def __init__(self):
        self.application = None
        self.application = DispatchEx("CANoe.Application")
        self.ver = self.application.Version
        print('Loaded CANoe version ',
            self.ver.major, '.',
            self.ver.minor, '.',
            self.ver.Build, '...')
        self.Measurement = self.application.Measurement.Running

    def open_cfg(self, cfgname):
        # open CANoe simulation
        if (self.application != None):
            # check for valid file and it is *.cfg file
            if os.path.isfile(cfgname) and (os.path.splitext(cfgname)[1] == ".cfg"):
                self.application.Open(cfgname)
                print("opening..."+cfgname)
            else:
                raise RuntimeError("Can't find CANoe cfg file")
        else:
            raise RuntimeError("CANoe Application is missing,unable to open simulation")

    def close_cfg(self):
        # close CANoe simulation
        if (self.application != None):
            print("close cfg ...")
            # self.stop_Measurement()
            self.application.Quit()
            self.application = None

    def start_Measurement(self):
        retry = 0
        retry_counter = 5
        # try to establish measurement within 5s timeout
        while not self.application.Measurement.Running and (retry < retry_counter):
            self.application.Measurement.Start()
            time.sleep(1)
            retry += 1
        if (retry == retry_counter):
            raise RuntimeWarning("CANoe start measuremet failed, Please Check Connection!")
        
    def stop_Measurement(self):
        if self.application.Measurement.Running:
            self.application.Measurement.Stop()
        else:
            pass
    
    def Running(self):
        if self.application.Measurement.Running:
            return True
        else:
            return False
    
    def set_ReplayBlock_File(self,file):
        ReplayBlocks=self.application.Bus.ReplayCollection     
        # if false,delete false cache in C:\Users\<my username>\AppData\Local\Temp\gen_py
        # C:\Users\llliu\AppData\Local\Temp\gen_py
        n=ReplayBlocks.Count
        Flag=1
        while Flag:
            try:
                for i in range(1,n+1):
                    ReplayBlock_i=ReplayBlocks.Item(i)
                    ReplayBlock_CastTo=CastTo(ReplayBlock_i,"IReplayBlock2")
                    ReplayBlock_CastTo.Path=file
                Flag=0
            except Exception:
                genpy=win32com.__gen_path__
                FolderLists=os.listdir(genpy)
                print("ReplayBlock Issue")
                for i in FolderLists:
                    if os.path.isdir(genpy+"\\"+i):
                        shutil.rmtree(genpy+"\\"+i)
                        print("delete temp gen_py") 
        