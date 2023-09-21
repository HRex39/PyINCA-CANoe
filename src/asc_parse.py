import pandas as pd

f = r"C:\Users\llliu\Desktop\HIL\Data\{ES25IV001_2023-08-09_15-55-24}_BUS002.asc"
format=f.split(".")[-1]

framefile = pd.read_csv(f,skiprows=4,encoding="gbk",engine='python',sep=' ',delimiter=None, index_col=False,header=None,skipinitialspace=True)
line=framefile.values[-3]
time=line[0]
t=float(time)
t_int=int(t)

a=1