from ExternalCall_INCA import *
import time

FileLists=["test1.blf","test2.blf","test3.blf"]
result_path=r"C:\Users\llliu\Desktop"
INCA=Inca()
INCA.get_openExp()
INCA.set_record_path(result_path)
INCA.is_measurement()
INCA.start_measurement()

for File in FileLists:
    INCA.set_record_filename(File)  
    INCA.start_record()
    print(File+" is replay and recording...")
    time.sleep(6) #wait data replay finish
    INCA.stop_record()