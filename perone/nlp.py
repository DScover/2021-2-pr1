import numpy as np
import pandas as pd
import plotly
import plotly.graph_objs as go
import json
import io
import re
import matplotlib.pyplot as plt
from gensim.models import Word2Vec

company_name = ["삼성전자","SK하이닉스","네이버","삼성바이오로직스",
                "삼성전자우","카카오","LG화학","삼성SDI","현대차",
                "기아","카카오뱅크","셀트리온","카카오페이","포스코",
                "KB금융","크래프톤","현대모비스","삼성물산","LG전자",
                "SK이노베이션","신한지주","SK바이오사이언스","SK","LG생활건강",
                "엔씨소프트","하이브","한국전력","삼성생명","HMM"]

def nlp1():
    data = pd.read_excel("Valuation_corpus.xlsx",engine = "openpyxl")
    corpus = data[['Corpus']]
    k = 0

    for i in corpus["Corpus"]:
        text = re.compile("[ㄱ-ㅎ|\d\ㅏ-ㅣ|가-힣]+").findall(str(i))
        corpus.loc[k,"Corpus"] = " ".join(text).strip()
        k+=1
    #print(len(corpus))
    drop_index = corpus[corpus['Corpus'] == ""].index
    corpus = corpus.drop(drop_index)
    #print(len(corpus))
    #! pip install konlpy
    from konlpy.tag import Hannanum, Kkma, Komoran, Mecab, Okt
    hannanum = Hannanum()
    kkma = Kkma()
    komoran = Komoran()
    okt = Okt()
    def tokenizer(row):
        return hannanum.morphs(row)
    corpus["rev_token"] = corpus["Corpus"].apply(tokenizer)
    model = Word2Vec(sentences = corpus['rev_token'], size=32, window = 7, min_count = 0, workers = 20, sg =1)
    word_vectors = model.wv
    vocabs = word_vectors.vocab.keys()
    word_vectors_list = [word_vectors[v] for v in vocabs]
    company_similarity = []

    for i in ["삼성전자","하이닉스","네이버","삼성바이오로직스","삼성전자우","카카오","화학","006400","현대차","기아","카카오뱅크","셀트리온","카카오페이","포스코","105560","크래프톤","현대모비스","삼성물산","066570","096770","055550","바이오사이언스","에스케이","생활건강", "엔씨소프트","하이브","한국전력","삼성생명","에이치엠엠"]:
        for k in ["삼성전자","하이닉스","네이버","삼성바이오로직스","삼성전자우","카카오","화학","006400","현대차","기아","카카오뱅크","셀트리온","카카오페이","포스코","105560","크래프톤","현대모비스","삼성물산","066570","096770","055550","바이오사이언스","에스케이","생활건강", "엔씨소프트","하이브","한국전력","삼성생명","에이치엠엠"]:
            #print(i+"와",k+"의 유사도: ",word_vectors.similarity(w1=i,w2=k))
            company_similarity.append(word_vectors.similarity(w1=i,w2=k))
        
    company_similar_frame = []
    company_similar_frame = pd.DataFrame(company_similar_frame)

    k = 0
    for i in range(0,841,29):
        company_similar_frame.insert(k,company_name[k],company_similarity[i:i+29],True)
        k = k + 1
    company_similar_frame.insert(0,"회사명",company_name,True)

    #print(company_similar_frame["삼성전자"][1])
    company_similar_frame2 = company_similar_frame
    for i in company_name:
        for k in range(0,29):
            if company_similar_frame2[i][k] < 0.7:
                company_similar_frame2[i][k] = 0
            if company_similar_frame2[i][k] > 0.99:
                company_similar_frame2[i][k] = 2.0
    
    cs_sum = company_similar_frame2.sum(axis=1)
    company_similar_frame4 = company_similar_frame.set_index("회사명")
    
def visual():
    data1 = pd.read_excel("PER_df_final.xlsx",engine = "openpyxl")
    data1 = data1.loc[(data1['차이']>=10) | (data1['차이']<=-10)]
    data = [
        go.Bar(
            x = data1["티커"],
            y = data1["차이"]
        )
    ]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
    
    


