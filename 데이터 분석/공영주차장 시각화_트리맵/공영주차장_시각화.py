import pandas as pd
import matplotlib.font_manager as fm
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import plotly.express as px

font_list = [font.name for font in fm.fontManager.ttflist]

plt.rcParams['font.family'] = 'HYGothic-Medium'

# 최종 csv
# 서울특별시 주차정보안내시스템에서 민영주차장은 제거
# 노상주차장 : 20대 이상 -> 장애인 주차가능
# 노외주차장 : 50대 이상 -> 장애인 주차가능
# 부설주차장 : 10대 이상 -> 장애인 주차가능

data = pd.read_csv('(final_장애인주차가능여부)seoulparking.csv')
public = data['세부분류'] == '공영주차장'
data_public = data[public]

# 불필요한 컬럼 제거
data_public = data_public.drop(columns=['주차가능면'])
data_public = data_public.drop(columns=['시설분류'])
data_public = data_public.drop(columns=['세부분류'])
data_public = data_public.drop(columns=['주소'])
data_public = data_public.drop(columns=['위도'])
data_public = data_public.drop(columns=['경도'])
# print(data_public)


data_group = data_public.groupby(['담당구' , '장애인 주차칸 여부'] , as_index=False).count()



gu = [] #지역구

# 각 구마다가 주차가능/주차불가능 으로 나열되기 때문에 구이름 추출만을 위해서는 간격을 두개씩 해서 추출
for i in range(0, len(data_group.values), 2):
    gu.append(data_group.values[i][0])


# 컬럼명 재설정
data_group.rename(columns={'시설명':'주차장 수'} , inplace= True)
data_group['장애인 주차칸 여부'] = data_group['장애인 주차칸 여부'].replace('가능' , '주차 가능')
data_group['장애인 주차칸 여부'] = data_group['장애인 주차칸 여부'].replace('불가능' , '주차 불가능')

# print(data_group)
# print(data_group.values)

value = data_group.values.copy()
data_group['장애인 주차칸 비율(%)']=""
ratio = data_group['장애인 주차칸 비율(%)'].copy()

# 주차가능/주차불가능 비율 계산
for i in range(len(value)):
    if i == 0:
        ratio[i] = round(value[i][2]/(value[i][2]+value[i+1][2]),2)*100
    elif i%2 ==0:
        ratio[i] = round(
            value[i][2] / (value[i][2] + value[i + 1][2]), 2) * 100

    elif i%2 == 1:
        ratio[i] = round(
            value[i][2] / (value[i][2] + value[i - 1][2]), 2) * 100

data_group['장애인 주차칸 비율(%)'] = ratio
# print(data_group)
data_group['장애인 주차칸 비율(%)'] = data_group['장애인 주차칸 비율(%)'].astype(int)
# print(data_group)
# # print(round(data_group.values[0][2]/(data_group.values[0][2]+data_group.values[1][2])))
# # print(data_group.values[0][2])
# # print(data_group.values[1][2])
# # print(round((data_group.values[0][2] / (data_group.values[0][2]+data_group.values[1][2])) , 2))

# plotyly.express의 treemap 사용
fig = px.treemap(data_group,
                 path=['담당구', '장애인 주차칸 여부'],
                 values='주차장 수', # 각 구에 대한 면적은 주차장 수에 비례
                 color='장애인 주차칸 비율(%)', #color-bar는 주차장 비율에 비례
color_continuous_scale='RdBu'

                  )

fig.update_layout(title="각 구별 공영 주차장 수/장애인 주차칸 여부",
                margin = dict(t=50, l=25, r=25, b=25),
                  width=1000, height=600,)

fig.show()

