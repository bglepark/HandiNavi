import pandas as pd
from datetime import datetime
import numpy as np

## 이전 모든 csv를 한번에 합치는 코드
## os 라이브러리를 사용해서 해당 경로에 있는 파일을 전부 불러와서 concat

# data_list = os.listdir('C:/PythonStudy/taxi/')
# data_all = pd.DataFrame()
#
# % cd
# C: / PythonStudy / taxi /
#
# for files in data_list:
#     df = pd.read_csv(files, encoding='cp949')
#     data_all = pd.concat([data_all, df], ignore_index=True)

## datetime으로 바꾸기 위해서 각각의 누락된 값 합치기

# df['운행시작1'] = ''
# for i in range(len(drive_start)):
#     if len(drive_start[i]) == 13:
#         df['운행시작1'][i] = '2021' + drive_start[i][:6] + ' ' + drive_start[i][7:] + '00'
#     elif len(drive_start[i]) == 15:
#         df['운행시작1'][i] = '20' + drive_start[i][:8] + ' ' + drive_start[i][9:] + '00'
#     elif len(drive_start[i]) == 19:
#         df['운행시작1'][i] = drive_start[i][:10] + ' ' + drive_start[i][11:]
#


data = pd.read_csv('calltaxi.csv')
drive_start = data['운행시작']

drive_date =[] #날짜
for i in drive_start:
    drive_date.append(datetime.strptime(i[0:10], '%Y-%m-%d')) #문자열->datetime으로 변환

# datetime이 각 요일에 맞춰서 숫자로 나오기 때문에 미리 dateDict을 설정
dateDict = {0:'월요일' , 1:'화요일' , 2:'수요일' , 3:'목요일' , 4:'금요일' , 5:'토요일' ,6:'일요일'}
dayday = [] #요일
for i in drive_date:
    dayday.append(dateDict[i.weekday()])
# 바로 dateDict에서 value값 찾아서 요일로 변환


data['운행시작'].replace('24:00','0:00', inplace=True) #중복 방지
data['운행시작'] = pd.to_datetime(data['운행시작'] , errors='coerce') #오류 방지


data['운행시작_시간']=data['운행시작'].dt.time

data = data.drop(columns=['시동ON 시각'])
data['요일'] = dayday

data = data.set_index('운행시작') #index로 datetime을 설정해야 between_time 사용 가능 / 이후 시계열 분석

morning = data.between_time('06:00:01', '12:00:00') #between_time 사용해서 시간대별로 구분
afternoon = data.between_time('12:00:01', '18:00:00')
evening = data.between_time('18:00:01', '00:00:00')
midnight = data.between_time('00:00:01', '06:00:00')

data['구분']= 'N/A'
data.loc[morning.index, '구분'] = '아침'
data.loc[afternoon.index, '구분'] = '점심'
data.loc[evening.index, '구분'] = '저녁'
data.loc[midnight.index, '구분'] = '심야'

data.to_csv('calltaxi_전처리완료.csv' ,  encoding='utf-8-sig')

