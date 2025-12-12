from konlpy.tag import Okt
import re
import joblib
import random  # 랜덤 추천용

okt = Okt()




def okt_tokenize_to_str(text: str) -> str:
    # 형태소 분석 후 공백으로 이어서 하나의 문자열로 변환
    morphs = okt.morphs(text)
    return " ".join(morphs)

# 2. 학습된 TF-IDF 벡터라이저 & 감성 모델 로드
tfidf = joblib.load('models/movie_tfidf_vectorizer.joblib')
sentiment_model = joblib.load('models/movie_sentiment_model.joblib')


def ai_run(text: str):
    """
    한 문장을 입력받아 감성 분석 결과를 반환
    """
    # 1) 특수문자 제거 (한글/공백만 남기기)
    clean = re.sub(r'[^ ㄱ-ㅎ가-힣]+', " ", text)

    # 2) 학습 때와 똑같이: 먼저 Okt로 형태소 분석 → 문자열로 변환
    tokenized_str = okt_tokenize_to_str(clean)

    # 3) TF-IDF 변환
    X = tfidf.transform([tokenized_str])

    # 4) 감성 예측 (배열 → 스칼라)
    pred = int(sentiment_model.predict(X)[0])

    if pred == 0:
        label = "부정"
      
    else:
        label = "긍정"
       

    print(clean, "->>", label)
    return label


# 단독 테스트용
if __name__ == "__main__":
    st = "완전 ^o^ 짜증 잔뜩. 재미없어100%! ^^*"
    print(ai_run(st))