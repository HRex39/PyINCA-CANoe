import cantools
import can
#dbc_file = r"C:\Users\master01\Downloads\blf_conf\FS04通用_TBOX(1).dbc"
# dbc = cantools.db.load_file(dbc_file)
f = r"C:\Users\llliu\Desktop\HIL\{ES25IV001_2023-08-09_15-53-20}_BUS001.blf"
log_data = can.BLFReader(f)
file_start=log_data.start_timestamp
file_end=log_data.stop_timestamp

for msg in log_data:
    print(msg)