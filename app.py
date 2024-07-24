import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openai
import time

# 타이틀과 설명
st.title("MBTI 심리검사 앱")
st.write("업로드한 파일을 분석해서 MBTI 16개 유형에 해당하는지 여부를 알 수 있는 30문제를 작성합니다.")

# OpenAI API 키 입력
st.sidebar.header("OpenAI API 설정")
api_key = st.sidebar.text_input("API Key", type="password")

# 30문제 예시 (MBTI 질문)
questions = [
    "나는 파티에서 새로운 사람들과 쉽게 어울린다.",
    "나는 계획을 세우고 따르는 것을 좋아한다.",
    "나는 감정에 따라 결정을 내리는 경향이 있다.",
    "나는 미래에 대해 많은 걱정을 한다.",
    "나는 팀 작업보다 개인 작업을 선호한다.",
    "나는 사실과 세부 사항에 집중하는 편이다.",
    "나는 직관과 영감을 많이 활용한다.",
    "나는 논리와 분석을 통해 결정을 내린다.",
    "나는 다른 사람들의 감정에 민감하다.",
    "나는 예측 가능하고 체계적인 것을 좋아한다.",
    "나는 변화와 다양성을 좋아한다.",
    "나는 사교적이고 외향적이다.",
    "나는 시간을 정리하고 체계적으로 사용하는 편이다.",
    "나는 창의적이고 독창적인 아이디어를 내는 것을 즐긴다.",
    "나는 사실을 기반으로 한 현실적인 결정을 내린다.",
    "나는 다른 사람들과 쉽게 감정을 나눈다.",
    "나는 계획보다는 유연성을 더 중요하게 생각한다.",
    "나는 내면의 생각과 감정에 집중하는 편이다.",
    "나는 현실보다 가능성에 더 집중한다.",
    "나는 감정보다 논리를 우선시한다.",
    "나는 직관보다는 감각에 의존한다.",
    "나는 사람들과의 상호작용에서 에너지를 얻는다.",
    "나는 규칙과 절차를 따르는 것을 선호한다.",
    "나는 즉흥적으로 행동하는 것을 좋아한다.",
    "나는 세부적인 것보다 전체적인 그림을 더 중시한다.",
    "나는 다른 사람들과 잘 협력한다.",
    "나는 일관성과 체계가 중요하다고 생각한다.",
    "나는 자발적이고 유연한 태도를 취한다.",
    "나는 새로운 아이디어를 탐구하는 것을 즐긴다.",
    "나는 감정적인 결정보다 객관적인 결정을 내린다."
]

# 질문과 답변을 위한 라디오 버튼 생성
answers = []
for i, question in enumerate(questions):
    st.write(f"Q{i+1}. {question}")
    answer = st.radio(
        f"Q{i+1}", 
        ("매우 그렇다", "그렇다", "전혀 그렇지 않다"),
        key=f"question_{i+1}"
    )
    answers.append(answer)

# MBTI 유형 분석 함수
def analyze_mbti(answers):
    # 각 질문에 대한 점수 매기기
    score_mapping = {
        "매우 그렇다": 2,
        "그렇다": 1,
        "전혀 그렇지 않다": 0
    }
    scores = [score_mapping[answer] for answer in answers]
    
    # MBTI 지표 계산
    EI = sum(scores[0:30:4]) - sum(scores[1:30:4])  # 외향/내향
    SN = sum(scores[2:30:4]) - sum(scores[3:30:4])  # 감각/직관
    TF = sum(scores[4:30:4]) - sum(scores[5:30:4])  # 사고/감정
    JP = sum(scores[6:30:4]) - sum(scores[7:30:4])  # 판단/인식
    
    # 각 지표에 따른 MBTI 유형 결정
    mbti = ""
    mbti += "E" if EI > 0 else "I"
    mbti += "S" if SN > 0 else "N"
    mbti += "T" if TF > 0 else "F"
    mbti += "J" if JP > 0 else "P"
    
    return mbti, EI, SN, TF, JP

# 결과 분석 및 시각화
if st.button("결과 분석"):
    with st.spinner("MBTI 유형을 분석중입니다. 잠시만 기다리세요..."):
        mbti, EI, SN, TF, JP = analyze_mbti(answers)
        time.sleep(3)  # 결과를 기다리는 시간 시뮬레이션
        
        # 결과 시각화
        labels = ['E/I', 'S/N', 'T/F', 'J/P']
        scores = [EI, SN, TF, JP]
        fig, ax = plt.subplots()
        ax.bar(labels, scores, color=['blue', 'orange', 'green', 'red'])
        ax.set_ylim([-15, 15])
        st.pyplot(fig)
        
        # MBTI 결과 설명
        st.subheader("당신의 MBTI 유형: " + mbti)
        
        # OpenAI API를 사용하여 자세한 설명 생성
        if api_key:
            openai.api_key = api_key
            prompt = f"MBTI 유형 {mbti}에 대한 상세 설명과 직업 적성, 그리고 앞으로의 조언을 제공해주세요."
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=5000
                )
                st.write(response['choices'][0]['message']['content'])
            except Exception as e:
                st.error(f"OpenAI API 요청 중 오류가 발생했습니다: {e}")
        else:
            st.warning("OpenAI API 키를 입력해주세요.")

# 다시 시작하기 버튼
if st.button("다시 시작하기"):
    st.experimental_rerun()

# 업로드한 파일을 불러오기
st.sidebar.header("업로드한 파일")
uploaded_file = st.sidebar.file_uploader("파일 업로드", type=["md"])
if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
    st.sidebar.write(content)
