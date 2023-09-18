'''
Author: Fuqiang Liu <fuqiang_liu@patac.com.cn>
'''
import os
import time
from win32com.client import *
from win32com.client.connect import *

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
    
    def replay_Block(self,filelists):
        ReplayBlocks=self.application.Bus.ReplayCollection
        #print(ReplayBlocks.Count)
        
        ReplayBlock1=ReplayBlocks.Item(1)
        ReplayBlock11=CastTo(ReplayBlock1,"IReplayBlock2")
        
        ReplayBlock2=ReplayBlocks.Item(2)
        ReplayBlock22=CastTo(ReplayBlock2,"IReplayBlock2")
        
        ReplayBlock3=ReplayBlocks.Item(3)
        ReplayBlock33=CastTo(ReplayBlock3,"IReplayBlock2")
        
        ReplayBlock4=ReplayBlocks.Item(4)
        ReplayBlock44=CastTo(ReplayBlock4,"IReplayBlock2")
        
        for file in filelists:
            a=1
            ReplayBlock11.Path=file
            ReplayBlock22.Path=file
            ReplayBlock33.Path=file
            ReplayBlock44.Path=file
            print(ReplayBlock11.Path)
            print(ReplayBlock22.Path)
            print(ReplayBlock33.Path)
            print(ReplayBlock44.Path)
            time.sleep(1)

app = CANoe()
app.open_cfg(r"E:\CANOE_Script\ACP3_HIL_Feedback\ACP3_HIL_Feedback.cfg") #导入某个CANoe config