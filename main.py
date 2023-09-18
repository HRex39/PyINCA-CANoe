'''
Author: Chenrui Huang <chenrui_huang@patac.com.cn>
'''
import multiprocessing

from src.ExternalCall_INCA import Inca

if __name__ == '__main__':
    # Init folder address
    folder_address = '16733'
    exp_address = '167_19519_MY24_ACP3'
    work_address = 'Workspace'
    pathname = 'C:\\Users\\Public\\Documents\\ETAS\\INCA7.3\\Measure\\'
    filename = 'E2LB_Low_Roof'
    increament_flag = 1
    # Init INCA & Set record
    Inca_App = Inca(work_address, exp_address, folder_address)
    Inca_App.set_record(pathname, filename, increament_flag)
    # Init hardware
    init_or_not = int(input("是否需要初始化硬件： "))
    print("\n")
    if init_or_not == 1:
        Inca_App.init_hardware()
    Inca_App.start_measurement()
    Inca_App.Inca_Ready = True
    # Start Measurement
    while Inca_App.Inca_Ready:
        decision = int(input("是否开始记录: "))
        print("\n")
        # 0 不记录并停止测量 1 开始记录
        if decision == 0:
            Inca_App.stop_measurement()
            print("stop measurement!\n")
        elif decision == 1:
            Inca_App.start_record()
            print("start recording\n")
        else:
            print("wrong input, exit\n")
            Inca_App.Inca_Ready = False

