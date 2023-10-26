'''
Author: Chenrui Huang <chenrui_huang@patac.com.cn>
'''

import win32com
from win32com.client import Dispatch, constants


class Inca(object):

    def __init__(self):
        self.w = win32com.client.Dispatch('inca.inca')
        self.DB = self.w.GetCurrentDataBase()       
        # Vars
        self.Inca_Ready = 0
        self.Inca_Measure = 0
        self.Inca_Record = 0
        self.Inca_Exit = 0
        self.filename="default"
    
    def open_INCA(self, workspace_address, exp_address, folder_address):
        WS = self.DB.BrowseItemInFolder(workspace_address, folder_address)
        # get Hardware
        self.HwApp = WS[0]
        # get exp
        Exp = self.DB.BrowseItemInFolder(exp_address, folder_address)
        ExpApp = Exp[0]
        ExpView = ExpApp.OpenExperiment()
        self.WorkExp = ExpView.GetExperiment()
        
    def init_hardware(self):
        return self.WorkExp.InitializeHardware()

    def set_record_path(self, pathname):
        # don't change the state of measurement
        # if measurement is running, the path setting function is invalid
        if self.is_measurement():
            self.stop_measurement()
            self.WorkExp.SetRecordingPathName(pathname)
            self.start_measurement()
        else:
            self.WorkExp.SetRecordingPathName(pathname)
        
    def set_record_filename(self,filename,increament_flag=1):
        # self.WorkExp.SetRecordingFileName seems not work, because when Debug cannot find var_FileName
        self.filename='.'.join(filename.split(".")[:-1])  #remove the format in name like ".blf"
        #self.WorkExp.SetRecordingFileName(filename)
        #self.WorkExp.SetRecordingFileAutoincrementFlag(increament_flag)
        
    def get_measure_value(self, ValueName):
        return self.WorkExp.GetMeasureElement(ValueName)

    def start_measurement(self):
        result = self.WorkExp.StartMeasurement()
        if result:
            self.Inca_Measure = 1
        return result
    
    def is_measurement(self):
        if self.WorkExp.IsMeasurementRunning():
            return 1
        else:
            return 0
    
    def get_openExp(self):
        self.WorkExp =self.w.GetOpenedExperiment()
        
    def start_record(self):
        result = self.WorkExp.StartRecording()
        if result:
            self.Inca_Measure = 1
            self.Inca_Record = 1
        return result

    def stop_record(self):
        result = self.WorkExp.StopRecording(self.filename, self.WorkExp.GetRecordingFileFormat())
        if result:
            self.Inca_Measure = 0
            self.Inca_Record = 0
        return result

    def stop_measurement(self):
        result = self.WorkExp.StopMeasurement()
        if result:
            self.Inca_Measure = 0
        return result

    def close_inca(self):
        result = self.w.CloseTool()
        if result:
            self.Inca_Exit = 1
        return result