import pandas as pd
import json

with open('seoulparking.json' , 'r' , encoding='UTF-8') as f:
    contents = json.load(f)


# print(contents)
# print(len(contents))
name = []
capacity = []
addr = []
lng = []
lat = []

content = contents.get('total')


for i in range(len(content)):
    for j in range(len(content[i])):
        name.append(content[i][j].get('name'))
        addr.append(content[i][j].get('addr'))
        capacity.append(content[i][j].get('capacity'))
        lat.append(content[i][j].get('lat'))
        lng.append(content[i][j].get('lng'))

gu_list = ["강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구", "노원구", "도봉구",
           "동대문구", "동작구", "마포구", "서대문구", "서초구", "성동구", "성북구", "송파구", "양천구",
           "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구"]

gu = []
detail = []
detail2 = []

for i in range(len(content)):
    for _ in range(len(content[i])):
        gu.append(gu_list[i])
        detail.append('주차장')
        detail2.append('공영주차장')


for i in range(len(name)):
    if(name[i].find('(민영)'))>0:
        detail2[i]='민영주차장'
    else:
        continue




df = pd.DataFrame({'시설명':name , '담당구':gu, '주차가능면' : capacity , '주소':addr , '위도' : lat , '경도':lng ,
                   '시설분류' : detail , '세부분류':detail2})
print(df)
df.to_csv('(final)seoulparking.csv' , encoding='utf-8-sig' , index=False)