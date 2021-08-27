#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import glob
import openpyxl
import pandas as pd
import datetime
from datetime import datetime
import matplotlib.pyplot as plt
plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False
import seaborn as sns
import matplotlib.font_manager as fm
import warnings 
warnings.filterwarnings('ignore')


# In[1]:


def data():
    for i in [2019,2020]:
        input_file = r'C:\Users\vxpko\202105_lab\HakerTon\data\{}'.format(i)
        output_file = r'C:\Users\vxpko\202105_lab\HakerTon\data\{}_dong.csv'.format(i)

        allFile_list = glob.glob(os.path.join(input_file, '*.csv'))

        allData = [] 
        for file in allFile_list:
            try:
                df = pd.read_csv(file,encoding='utf-8',index_col=False) 
                print(file)
                df=pd.DataFrame(df)        
                allData.append(df) 
            except:
                df = pd.read_csv(file,encoding='euc-kr',index_col=False) 
                print(file)
                df=pd.DataFrame(df)        
                allData.append(df) 
        dataCombine = pd.concat(allData, axis=0)
        dataCombine=dataCombine.iloc[:,[0,1,2,3,6,7,8,9,10,20,21,22,23,24]]
        dataCombine=dataCombine.astype('int')

        code=pd.read_excel('./code.xlsx', engine='openpyxl')
        code=code[code['시도명']=='서울특별시'].iloc[:,:6]
        for j in range(769):
            code['행정동코드'][j]=int(str(code['행정동코드'][j])[:8])
            code['법정동코드'][j]=int(str(code['법정동코드'][j])[:8])
        total=pd.merge(dataCombine,code,on='행정동코드')
        total['10대_남']=total.iloc[:,4]
        total['20대_남']=total.iloc[:,5]+total.iloc[:,6]
        total['30대_남']=total.iloc[:,7]+total.iloc[:,8]
        total['10대_합']=total.iloc[:,4]+total.iloc[:,9]
        total['20대_합']=total.iloc[:,5]+total.iloc[:,6]+total.iloc[:,10]+total.iloc[:,11]
        total['30대_합']=total.iloc[:,7]+total.iloc[:,8]+total.iloc[:,12]+total.iloc[:,13]
        total['10_30남']=total.iloc[:,4]+total.iloc[:,5]+total.iloc[:,6]+total.iloc[:,7]+total.iloc[:,8]
        total['10_30합']=total.iloc[:,4]+total.iloc[:,5]+total.iloc[:,6]+total.iloc[:,7]+total.iloc[:,8]+total.iloc[:,9]+total.iloc[:,10]+total.iloc[:,11]+total.iloc[:,12]+total.iloc[:,13]

        total.drop(total.iloc[:,4:14],axis=1,inplace=True)
        total.to_csv('./data/{}_dong.csv'.format(i),index=False)


# In[3]:


# 자치구별 생활인구 변화 그래프
def total(age):
    data_2020 = pd.read_csv('./data/2020_dong.csv')
    data_2019 = pd.read_csv('./data/2019_dong.csv')
    data_total=pd.concat([data_2019,data_2020],axis=0)
    data_total=pd.DataFrame(data_total.groupby(['기준일ID','법정동코드','시간대구분','시군구명','동리명'],as_index=False).sum())
    data_total['기준일ID']=data_total['기준일ID'].astype('str')
    data_total['기준일ID']=pd.to_datetime(data_total['기준일ID'])
    data_total.set_index('기준일ID',inplace=True)
    data_total['year']=data_total.index.year
    data_total['month']=data_total.index.month
    total_=pd.DataFrame(data_total[['총생활인구수','10대_남','20대_남','30대_남','10대_합','20대_합','30대_합','10_30남','10_30합']].groupby([data_total['법정동코드'],data_total['시군구명'],data_total['동리명'],data_total['month'],data_total['year']]).resample('Y').mean()).reset_index()
    city_total=total_[['동리명','총생활인구수','10대_남','20대_남','30대_남','10대_합','20대_합','30대_합','10_30남','10_30합']].groupby([total_['시군구명'],total_['동리명'],total_['year']]).mean().reset_index()
    plt.figure(figsize=(20,10))
    sns.set(font='NanumGothic',rc={"axes.unicode_minus":False},style="darkgrid")
    sns.barplot(x='시군구명',y=age,hue='year',data=city_total,ci=None,palette='OrRd')


# In[ ]:


def year_change(age):
    data_2020 = pd.read_csv('./data/2020_dong.csv')
    data_2019 = pd.read_csv('./data/2019_dong.csv')
    data_total=pd.concat([data_2019,data_2020],axis=0)
    data_total=pd.DataFrame(data_total.groupby(['기준일ID','법정동코드','시간대구분','시군구명','동리명'],as_index=False).sum())
    data_total['기준일ID']=data_total['기준일ID'].astype('str')
    data_total['기준일ID']=pd.to_datetime(data_total['기준일ID'])
    data_total.set_index('기준일ID',inplace=True)
    data_total['year']=data_total.index.year
    data_total['month']=data_total.index.month
    total_m=pd.DataFrame(data_total[['총생활인구수','10대_남','20대_남','30대_남','10대_합','20대_합','30대_합','10_30남','10_30합']].groupby([data_total['법정동코드'],data_total['시군구명'],data_total['동리명'],data_total['month'],data_total['year']]).resample('Y').mean()).reset_index()
    plt.figure(figsize=(20,10))
    sns.set(font='NanumGothic',rc={"axes.unicode_minus":False},style="darkgrid")
    sns.barplot(x='month',y=age,hue='year',data=total_m,ci=None,palette='OrRd')


# In[ ]:


# 구 생활인구  시간
def time_gu(gu,age):
    data_2020 = pd.read_csv('./data/2020_dong.csv')
    data_2019 = pd.read_csv('./data/2019_dong.csv')
    data_total=pd.concat([data_2019,data_2020],axis=0)
    data_total=pd.DataFrame(data_total.groupby(['기준일ID','법정동코드','시간대구분','시군구명','동리명'],as_index=False).mean())
    data_total['기준일ID']=data_total['기준일ID'].astype('str')
    data_total['기준일ID']=pd.to_datetime(data_total['기준일ID'])
    data_total.set_index('기준일ID',inplace=True)
    data_total['year']=data_total.index.year
    data_total['month']=data_total.index.month
    plt.figure(figsize=(20,10))
    sns.set(font='NanumGothic',rc={"axes.unicode_minus":False},style="darkgrid")
    sns.barplot(x='시간대구분',y=age,hue='year',data=data_total[data_total['시군구명']==gu],ci=None,palette='OrRd')


# In[ ]:


# 송파구 이륜 + 생활인구 + 월별

def acc_pop(gu,age):
    
    
    data_2020 = pd.read_csv('./data/2020_dong.csv')
    data_2019 = pd.read_csv('./data/2019_dong.csv')
    data_total=pd.concat([data_2019,data_2020],axis=0)
    data_total=pd.DataFrame(data_total.groupby(['기준일ID','법정동코드','시간대구분','시군구명','동리명'],as_index=False).mean())
    data_total['기준일ID']=data_total['기준일ID'].astype('str')
    data_total['기준일ID']=pd.to_datetime(data_total['기준일ID'])
    data_total.set_index('기준일ID',inplace=True)
    data_total['year']=data_total.index.year
    data_total['month']=data_total.index.month
    total_m=pd.DataFrame(data_total[['총생활인구수','10대_남','20대_남','30대_남','10대_합','20대_합','30대_합','10_30남','10_30합']].groupby([data_total['법정동코드'],data_total['시군구명'],data_total['동리명'],data_total['month'],data_total['year']]).resample('M').mean()).reset_index()   

    acc=pd.read_excel('./accidentInfoList.xlsx',engine='openpyxl')
    acc['사고']=1
    acc['년']=[0]*len(acc)
    acc['월']=[0]*len(acc)
    acc['시']=[0]*len(acc)
    acc['구']=[0]*len(acc)
    acc['동']=[0]*len(acc)

    for i in range(len(acc)):
        acc['년'][i]=int(acc['사고일시'][i].split()[0][:-1])
        acc['월'][i]=int(acc['사고일시'][i].split()[1][:-1])
        acc['시'][i]=int(acc['사고일시'][i].split()[3][:-1])
        acc['구'][i]=acc['시군구'][i].split()[1]
        acc['동'][i]=acc['시군구'][i].split()[2]

    acc=acc[acc['구']=='송파구'][['사고']].groupby(acc['월']).sum().reset_index() 


    colors = sns.color_palette('OrRd', 12)
    fig, ax1 = plt.subplots(figsize=(12,6))
    ax2 = ax1.twinx()
    ax1.bar(total_m[(total_m['시군구명']=='송파구')&(total_m['year']==2020)]['month'], total_m[(total_m['시군구명']=='송파구')&(total_m['year']==2020)]['총생활인구수'], color=colors, alpha=0.7)
    ax2.plot(acc['월'], acc['사고'])
    plt.show()


# In[ ]:


# 송파구 이륜 + 생활인구 + 시간대별
def acc_time_gu(gu,age):
    data_2020 = pd.read_csv('./data/2020_dong.csv')
    data_2019 = pd.read_csv('./data/2019_dong.csv')
    data_total=pd.concat([data_2019,data_2020],axis=0)
    data_total=pd.DataFrame(data_total.groupby(['기준일ID','법정동코드','시간대구분','시군구명','동리명'],as_index=False).mean())
    data_total['기준일ID']=data_total['기준일ID'].astype('str')
    data_total['기준일ID']=pd.to_datetime(data_total['기준일ID'])
    data_total.set_index('기준일ID',inplace=True)
    data_total['year']=data_total.index.year
    data_total['month']=data_total.index.month
    plt.figure(figsize=(20,10))
    
    acc=pd.read_excel('./accidentInfoList.xlsx',engine='openpyxl')
    acc['사고']=1
    acc['년']=[0]*len(acc)
    acc['월']=[0]*len(acc)
    acc['시']=[0]*len(acc)
    acc['구']=[0]*len(acc)
    acc['동']=[0]*len(acc)

    for i in range(len(acc)):
        acc['년'][i]=int(acc['사고일시'][i].split()[0][:-1])
        acc['월'][i]=int(acc['사고일시'][i].split()[1][:-1])
        acc['시'][i]=int(acc['사고일시'][i].split()[3][:-1])
        acc['구'][i]=acc['시군구'][i].split()[1]
        acc['동'][i]=acc['시군구'][i].split()[2]

    acc=acc[acc['구']==gu][['사고']].groupby(acc['시']).sum().reset_index()   


    
    ax1 = sns.set_style(style=None, rc=None )
    fig, ax1 = plt.subplots(figsize=(12,6))
    sns.lineplot(x='시',y='사고',data=acc,palette='RdBu')
    ax2 = ax1.twinx()
    
    
    sns.barplot(x='시간대구분',y=age,data=data_total[(data_total['시군구명']==gu)&(data_total['year']==2020)],ci=None,palette='OrRd',alpha=0.5)


# In[ ]:


#법정동별 생활인구 + 사고
def acc_dong(gu,age):
    data_2020 = pd.read_csv('./data/2020_dong.csv')
    data_2019 = pd.read_csv('./data/2019_dong.csv')
    data_total=pd.concat([data_2019,data_2020],axis=0)
    data_total=pd.DataFrame(data_total.groupby(['기준일ID','법정동코드','시간대구분','시군구명','동리명'],as_index=False).sum())
    data_total['기준일ID']=data_total['기준일ID'].astype('str')
    data_total['기준일ID']=pd.to_datetime(data_total['기준일ID'])
    data_total.set_index('기준일ID',inplace=True)
    data_total['year']=data_total.index.year
    data_total['month']=data_total.index.month
    total_=pd.DataFrame(data_total[['총생활인구수','10대_남','20대_남','30대_남','10대_합','20대_합','30대_합','10_30남','10_30합']].groupby([data_total['법정동코드'],data_total['시군구명'],data_total['동리명'],data_total['month'],data_total['year']]).resample('Y').mean()).reset_index()
    city_total=total_[['동리명','총생활인구수','10대_남','20대_남','30대_남','10대_합','20대_합','30대_합','10_30남','10_30합']].groupby([total_['시군구명'],total_['동리명'],total_['year']]).mean().reset_index()
    
    acc=pd.read_excel('./accidentInfoList.xlsx',engine='openpyxl')
    acc['사고']=1
    acc['년']=[0]*len(acc)
    acc['월']=[0]*len(acc)
    acc['시']=[0]*len(acc)
    acc['구']=[0]*len(acc)
    acc['동']=[0]*len(acc)

    for i in range(len(acc)):
        acc['년'][i]=int(acc['사고일시'][i].split()[0][:-1])
        acc['월'][i]=int(acc['사고일시'][i].split()[1][:-1])
        acc['시'][i]=int(acc['사고일시'][i].split()[3][:-1])
        acc['구'][i]=acc['시군구'][i].split()[1]
        acc['동'][i]=acc['시군구'][i].split()[2]

    acc=acc[acc['구']==gu][['사고']].groupby(acc['동']).sum().reset_index()    
    plt.figure(figsize=(20,20))
    
    ax1 = sns.set_style(style=None, rc=None )

    fig, ax1 = plt.subplots(figsize=(12,6))
    sns.lineplot(x='동',y='사고',data=acc,palette='RdBu',ci=False)
    ax2 = ax1.twinx()
    sns.barplot(x='동리명',y=age,data=city_total[(city_total['시군구명']==gu)&(city_total['year']==2020)],ci=None,palette='OrRd',alpha=0.5)

    
    

