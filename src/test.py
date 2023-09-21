from ExternalCall_CANoe import *
from ExternalCall_INCA import *
import tkinter as tk
from tkinter import filedialog
from pandas import read_csv
from can import BLFReader

if __name__ == '__main__':
    # Get Data Folder and Lists 
    root=tk.Tk()
    root.withdraw()
    Folderpath=filedialog.askdirectory()
    #File = filedialog.askopenfilename()
    FileLists=os.listdir(Folderpath)
    result_path='/'.join(Folderpath.split('/')[:-1])+"/Result"
    if not os.path.isdir(result_path):
        os.mkdir(result_path)

    #Canoe init
    app_Caone = CANoe()
    #app_Caone.open_cfg(r"E:\CANOE_Script\ACP3_HIL_Feedback\ACP3_HIL_Feedback.cfg") #导入某个CANoe config

    #INCA init
    INCA=Inca()
    INCA.get_openExp()
    INCA.set_record_path(result_path)
    INCA.start_measurement()

    for File in FileLists:
        Record_Flag=1
        format=File.split(".")[-1]
        # get file time
        if format=='asc':
            framefile = read_csv(Folderpath+"/"+File,skiprows=4,encoding="gbk",engine='python',sep=' ',delimiter=None, index_col=False,header=None,skipinitialspace=True)
            file_time=framefile.values[-3][0]
            t=int(float(file_time))
        elif format=='blf':
            log_data = BLFReader(Folderpath+"/"+File)
            file_start=log_data.start_timestamp
            file_end=log_data.stop_timestamp
            t=int(float(file_end)-float(file_start)) 
        else:
            Record_Flag=0
            
        if Record_Flag:                       
            print(File+" will record about "+str(t)+"s")                                      
            print(File+" is load...")         
            # set file
            app_Caone.set_ReplayBlock_File(Folderpath+"/"+File)
            INCA.set_record_filename(File)     
            # start 
            app_Caone.start_Measurement()
            #time.sleep(5) # No need to wait Canoe start, it will stay in this line until Canoe start measure
            INCA.start_record()
            print(File+" is replay and recording...")
            time.sleep(t-3) #wait data replay finish
            INCA.stop_record()
            app_Caone.stop_Measurement()        
            print(File+" is done and save...")
        else:
            print(File+" is not correct format, we will skip this file...")
        print("\n")

    print("Done all file replay !!!")
    
    


    
    
    
    
    