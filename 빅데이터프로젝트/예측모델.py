import pandas as pd
import scipy.stats
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, roc_auc_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix, classification_report
import warnings
warnings.filterwarnings('ignore')

import os
import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier

os.chdir("/home/piai/문서/빅데이터프로젝트")
os.getcwd()
df = pd.read_csv("./df.csv", encoding='euc-kr')

대분류_입력 = st.sidebar.selectbox("대분류", ["식품", "의류"])



# 중분류 입력

if 대분류_입력 == "식품":

    중분류_입력 = st.sidebar.selectbox("중분류", ["가공식품", "건강식품", "김치", "농산물", "수산물", "차/음료", "축산물"])

else:

    중분류_입력 = st.sidebar.selectbox("중분류", ["UNISEX류", "남성의류", "애견의류", "여성의류", "유아의류"])



# 계절 입력

계절_입력 = st.sidebar.selectbox("계절", ["봄", "여름", "가을", "겨울"])



# 월 입력

월_입력 = st.sidebar.number_input("월", min_value=1, max_value=12, value=1)



# 요일 입력

요일_입력 = st.sidebar.selectbox("요일", ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"])



# 시간대 입력

시간대_입력 = st.sidebar.selectbox("시간대", ["새벽", "오전", "점심", "오후", "저녁", "심야", "야간"])


# 시간 입력

시간_입력 = st.sidebar.number_input("시간", min_value=0, max_value=23, value=0)


# 열 생성
if 대분류_입력 == '식품':
    user_input = pd.DataFrame(columns=['월', '시간', '중분류_가공식품', '중분류_건강식품', '중분류_김치', '중분류_농산물', '중분류_수산물','중분류_차/음료', '중분류_축산물', '요일_금요일', '요일_목요일', '요일_수요일', '요일_월요일','요일_일요일', '요일_토요일', '요일_화요일', '계절_가을', '계절_겨울', '계절_봄', '계절_여름','시간대_새벽', '시간대_심야', '시간대_아침', '시간대_야간', '시간대_오전', '시간대_오후','시간대_저녁', '시간대_점심'])

    user_input.loc[0] = 0  # 모든 값을 0으로 초기화
    # 입력값에 해당하는 열에 1 할당
    user_input.loc[0, '중분류_' + 중분류_입력] = 1
    user_input.loc[0, '계절_' + 계절_입력] = 1
    user_input.loc[0, '월'] = 월_입력
    user_input.loc[0, '요일_' + 요일_입력] = 1
    user_input.loc[0, '시간대_' + 시간대_입력] = 1
    user_input.loc[0, '시간'] = 시간_입력
    df = df[['목표달성여부', '대분류', '중분류', '월', '요일', '시간', '계절', '시간대']]
    df = df[df['대분류'] == '식품']
    df['목표달성여부'] = df['목표달성여부'].astype(int)
    df_dummy = pd.get_dummies(df[['중분류', '요일', '계절', '시간대']])
    df_new = pd.concat([df, df_dummy], axis=1)
    df_new = df_new.drop(['중분류', '요일', '계절', '시간대', '대분류'], axis=1)
    df_raw_y = df_new["목표달성여부"]
    df_raw_x = df_new.drop("목표달성여부", axis=1, inplace=False)
    df_train_x, df_test_x, df_train_y, df_test_y = train_test_split(df_raw_x, df_raw_y, test_size=0.4,random_state=1234)
    gb_final = GradientBoostingClassifier(min_samples_leaf=11,max_depth=19, n_estimators=187,learning_rate=0.01, random_state=1234)
    gb_final.fit(df_train_x, df_train_y)
    y_pred = gb_final.predict(user_input)
    
    
    if y_pred == 0:
        print('실패할 확률이 높습니다')
    else:
        print('성공할 확률이 높습니다')

if 대분류_입력 == '의류':
    user_input = pd.DataFrame(columns=['월', '시간', '중분류_UNISEX류', '중분류_남성의류', '중분류_애견의류', '중분류_여성의류','중분류_유아의류', '요일_금요일', '요일_목요일', '요일_수요일', '요일_월요일', '요일_일요일','요일_토요일', '요일_화요일', '계절_가을', '계절_겨울', '계절_봄', '계절_여름','시간대_새벽', '시간대_심야', '시간대_아침', '시간대_야간', '시간대_오전', '시간대_오후','시간대_저녁', '시간대_점심'])
    user_input.loc[0] = 0  # 모든 값을 0으로 초기화
    # 입력값에 해당하는 열에 1 할당
    user_input.loc[0, '중분류_' + 중분류_입력] = 1
    user_input.loc[0, '계절_' + 계절_입력] = 1
    user_input.loc[0, '월'] = 월_입력
    user_input.loc[0, '요일_' + 요일_입력] = 1
    user_input.loc[0, '시간대_' + 시간대_입력] = 1
    user_input.loc[0, '시간'] = 시간_입력
    
    df = df[['목표달성여부', '대분류', '중분류', '월', '요일', '시간', '계절', '시간대']]
    df = df[df['대분류'] == '의류']
    df['목표달성여부'] = df['목표달성여부'].astype(int)
    df_dummy = pd.get_dummies(df[['중분류', '요일', '계절', '시간대']])
    df_new = pd.concat([df, df_dummy], axis=1)
    df_new = df_new.drop(['중분류', '요일', '계절', '시간대', '대분류'], axis=1)
    df_raw_x = df_new.drop("목표달성여부", axis=1, inplace=False)
    df_raw_y = df_new["목표달성여부"]
    df_train_x, df_test_x, df_train_y, df_test_y = train_test_split(df_raw_x, df_raw_y, test_size=0.4,random_state=1234)
    rf_final = RandomForestClassifier(min_samples_leaf=19,min_samples_split=12,max_depth=7, random_state=1234,)
    rf_final.fit(df_train_x, df_train_y)
    y_pred = rf_final.predict(user_input)
    if y_pred == 0:
        print('실패할 확률이 높습니다')
    else:
        print('성공할 확률이 높습니다')

# 의류 여성의류 봄 3 화요일 오후 15 ==> 성공
# 식품 건강식품 여름 7 화요일 저녁 19 ==> 실패
