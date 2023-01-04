#file này để code các công cụ python support cho các hàm 
import lasio
import pandas as pd
from datetime import datetime

def convert_lasio(path):
     file_las = lasio.read(path)
     df = file_las.df()
     df['WELL'] = file_las.well.WELL.value
     colss = df.columns.tolist()
     colss = colss[-1:] + colss[:-1]
     df = df[colss]
     df.reset_index(inplace= True)
     cur_info = file_las.header['Curves'].__str__()
     well_info = file_las.header['Well'].__str__()
     return cur_info, well_info, df
     
if __name__ == '__main__':
     path = r'C:\Users\clone\OneDrive\javaproject\web\final_git\app\static\files\A10.las'
     x, y, z = convert_lasio(path)
     print(x)
     print(y)
     print(z)
     print(datetime.now())
     print(type(datetime.now()))
