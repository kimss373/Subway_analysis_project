import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
import folium

st.title('2023년 12월 서울 지하철 이용량 분석')
st.sidebar.title('설정')
subway_origin = pd.read_csv('C:\\Users\\User\\dataanalysis\\day10\\subway.csv', encoding='cp949')
#subway12 = subway_origin.query('사용월==202312 and 호선명=="2호선"')
subway12 = subway_origin.query('사용월==202312')
#st.dataframe(subway12)
selected = st.sidebar.selectbox('옵션',
                                    ['선택하세요', '지하철역별','시간대별', '지도'])

# subway12['총 이용객'] = (subway12['00시-01시 승차인원'] + subway12['00시-01시 하차인원'] + subway12['01시-02시 승차인원'] + subway12['01시-02시 하차인원'] +
#                         subway12['02시-03시 승차인원'] + subway12['02시-03시 하차인원'] + subway12['03시-04시 승차인원'] + subway12['03시-04시 하차인원'] +
#                         subway12['04시-05시 승차인원'] + subway12['04시-05시 하차인원'] + subway12['05시-06시 승차인원'] + subway12['05시-06시 하차인원'] +
#                         subway12['06시-07시 승차인원'] + subway12['06시-07시 하차인원'] + subway12['07시-08시 승차인원'] + subway12['07시-08시 하차인원'] +
#                         subway12['08시-09시 승차인원'] + subway12['08시-09시 하차인원'] + subway12['09시-10시 승차인원'] + subway12['09시-10시 하차인원'] +
#                         subway12['10시-11시 승차인원'] + subway12['10시-11시 하차인원'] + subway12['11시-12시 승차인원'] + subway12['11시-12시 하차인원'] +
#                         subway12['12시-13시 승차인원'] + subway12['12시-13시 하차인원'] + subway12['13시-14시 승차인원'] + subway12['13시-14시 하차인원'] +
#                         subway12['14시-15시 승차인원'] + subway12['14시-15시 하차인원'] + subway12['15시-16시 승차인원'] + subway12['15시-16시 하차인원'] +
#                         subway12['16시-17시 승차인원'] + subway12['16시-17시 하차인원'] + subway12['17시-18시 승차인원'] + subway12['17시-18시 하차인원'] +
#                         subway12['18시-19시 승차인원'] + subway12['18시-19시 하차인원'] + subway12['19시-20시 승차인원'] + subway12['19시-20시 하차인원'] +
#                         subway12['20시-21시 승차인원'] + subway12['20시-21시 하차인원'] + subway12['21시-22시 승차인원'] + subway12['21시-22시 하차인원'] +
#                         subway12['22시-23시 승차인원'] + subway12['22시-23시 하차인원'] + subway12['23시-24시 승차인원'] + subway12['23시-24시 하차인원'])
subway12['총 이용객'], subway12['승차'], subway12['하차'] = 0, 0, 0
for i in range(3, 51):
    subway12['총 이용객'] += round(subway12[subway12.columns[i]]/31)

for i in range(3, 51, 2):
    subway12['승차'] += round(subway12[subway12.columns[i]]/31)
    

for i in range(4, 51, 2):
    subway12['하차'] += round(subway12[subway12.columns[i]]/31)



# 그래프 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.figure(figsize=(16, 8))
#############

if selected == '지하철역별':
    line = st.sidebar.selectbox('호선 선택', subway12['호선명'].unique()) # 호선 선택
    sub = subway12.query('호선명==@line')
    st.title('하루평균 - ' + line)
    st.title("")

    st.subheader('전체 - ' + str("{:g}".format(sub['총 이용객'].sum())) + '명')
    fig = plt.figure()
    sns.barplot(data=sub.sort_values('총 이용객', ascending=False).head(10), y='지하철역', x='총 이용객')
    st.pyplot(fig)

    st.subheader('승차 - ' + str("{:g}".format(sub['승차'].sum())) + '명')
    fig = plt.figure()
    sns.barplot(data=sub.sort_values('승차', ascending=False).head(10), y='지하철역', x='승차')
    st.pyplot(fig)

    st.subheader('하차 - ' + str("{:g}".format(sub['하차'].sum())) + '명')
    fig = plt.figure()
    ax = sns.barplot(data=sub.sort_values('하차', ascending=False).head(10), y='지하철역', x='하차')
    
    st.pyplot(fig)

elif selected == '시간대별':
    line = st.sidebar.selectbox('호선 선택', subway12['호선명'].unique()) # 호선 선택
    sub = subway12.query('호선명==@line')
    dict = {'시':[], '이용량':[]}
    for i in range(3, 51):
        dict['시'].append(sub.columns[i][:6])
        dict['이용량'].append(round(sub[sub.columns[i]].sum()/31))

    # dictionary로 데이터프레임 만들기
    df = pd.DataFrame.from_dict(dict)

    st.title('하루평균 - ' + line)
    st.title("")
    st.subheader('전체 - ' + str("{:g}".format(float("{:.9f}".format(df['이용량'].sum())))) + '명')
    fig = plt.figure()
    sns.barplot(data=df, y='시', x='이용량')
    st.pyplot(fig)

elif selected == '지도':
    location_df = pd.read_csv('C:\\Users\\User\\dataanalysis\\day10\\station_coordinate.csv')
    line = st.sidebar.selectbox('호선 선택', subway12['호선명'].unique()) # 호선 선택
    sub = subway12.query('호선명==@line')
    st.title('하루평균 - ' + line)
    st.title("")
    df_INNER_JOIN = pd.merge(subway12, location_df, left_on='지하철역', right_on='name', how='inner')
    df_INNER_JOIN['name'] = df_INNER_JOIN['지하철역']
    df_INNER_JOIN = df_INNER_JOIN.dropna(subset=['lat', 'lng'])
    df_INNER_JOIN = df_INNER_JOIN.drop_duplicates(['지하철역', '호선명'])
    df_INNER_JOIN = df_INNER_JOIN.query('호선명==@line')
    df_INNER_JOIN.reset_index()
    
    st.dataframe(df_INNER_JOIN)
    
    # 표시할 좌표와 값들
    coordinates = [(df_INNER_JOIN['lat'].loc[[i]].values[0], df_INNER_JOIN['lng'].loc[[i]].values[0], df_INNER_JOIN['지하철역'].loc[[i]].values[0]) for i in df_INNER_JOIN.index] ########### 여기 dataframe형식으로 되어있는거 리스트 형태로 바꾸면 돌아갈듯

    
    # 지도의 중심 좌표 설정
    center_coordinates = [sum(x[0] for x in coordinates) / len(coordinates),
                        sum(x[1] for x in coordinates) / len(coordinates)]
    
    # folium 지도 생성
    mymap = folium.Map(location=center_coordinates, zoom_start=13)

    # 좌표에 CircleMarker 추가
    for coord in coordinates:
        folium.CircleMarker(location=(coord[0], coord[1]),
                            radius=(df_INNER_JOIN[df_INNER_JOIN['지하철역'] == coord[2]]['총 이용객'].values[0]+1)/3000,
                            popup=f'Value: {coord[2]}',
                            color='blue',
                            fill=True,
                            fill_color='blue').add_to(mymap)
    st.components.v1.html(mymap._repr_html_(), width=800, height=600)
