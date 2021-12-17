import streamlit as st
import pandas as pd
import plotly.express as px



# 회사 데이터 들고 오기
@st.cache
def load_data():
    df = pd.read_excel('df3.xlsx')
    return df
def load_per_data():
    per_df = pd.read_excel('PER_df.xlsx')
    return per_df

df = load_data()
per_df = load_per_data()

df2 = df.set_index("종목명")
#제목 설정
st.title('주가 데이터  Web app')
#포트폴리오 들어갈 목록 적기
st.subheader('포트폴리오 설정')
multi_select = st.multiselect('당신의 포트폴리오를 적어주세요',
                              df.종목명)
#회사 정보 담아두기
stock_info = df2.loc[multi_select]

#포트폴리오 들어갈 수량 적기

quantity = []
for i in range(len(multi_select)):
    a = st.number_input(f'{multi_select[i]}의 수량을 입력해주세요')
    b = int(stock_info.iloc[i]['종가'])
    quantity.append(a*b)

fig = px.pie(values= quantity, names= multi_select)



# 산업별 자산 비중 알아보기 1
stock_info['종목별 금액'] = quantity

#예상 주가 정보 들고 오기
df_pred = pd.merge(left = stock_info, right = per_df, how="left", on="종목명")
df_pred['계산'] = df_pred['차이']*df_pred['종목별 금액']
predict = df_pred['계산'].sum() / df_pred['종목별 금액'].sum()



#산업별 자산비중 알아보기 2

stock_info_summ = stock_info.groupby('업종명')['종목별 금액'].sum().reset_index()

fig1 = px.treemap(stock_info_summ,
                  path=['업종명'],
                  values= '종목별 금액'
                  )


analysis = st.sidebar.selectbox('옵션을 선택하세요',['포트폴리오 분석','산업별 자산 비중','포트폴리오 위험도 분석'])
if analysis == '포트폴리오 위험도 분석':
    st.subheader('적정 PER을 이용한 위험도 분석')
    st.write('종목별 실제 PER - 적정 PER')
    fig2 = px.bar(df_pred, x='종목명', y='차이')
    st.plotly_chart(fig2)
    st.write(f'PER 차이의 가중 평균치: {predict}')
    if predict <= 20:
        st.write('안전한 포트폴리오입니다.')
    elif predict < 60:
        st.write('공격적인 포트폴리오입니다.')
    else:
        st.write('위험한 포트폴리오입니다.')
elif analysis == '포트폴리오 분석':
    st.subheader('포트폴리오 자산 비중')
    st.write('포트폴리오의 자산 비중은 다음과 같습니다.')
    st.plotly_chart(fig)
    st.write(f'총액: {sum(quantity)} 원입니다.')
elif analysis == '산업별 자산 비중':
    st.subheader('산업별 자산 비중')
    st.write('산업별 자산 비중은 다음과 같습니다.')
    st.plotly_chart(fig1)




