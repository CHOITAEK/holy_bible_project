import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.io import mmwrite
import pickle
import os

# 데이터 로드
df_Content = pd.read_csv('./bible_end/cleaned_bible_data3.csv')
print("데이터프레임 정보:")
df_Content.info()

# 결측값 처리
df_Content['Content'] = df_Content['Content'].fillna("")

# TF-IDF 벡터화
Tfidf = TfidfVectorizer(sublinear_tf=True, stop_words='english', min_df=2, max_features=10000)
Tfidf_matrix = Tfidf.fit_transform(df_Content['Content'])
print(f"TF-IDF 행렬 크기: {Tfidf_matrix.shape}")

# 저장 디렉토리 생성
os.makedirs('./models', exist_ok=True)

# TF-IDF 모델 저장
with open('./models/tfidf.pickle', 'wb') as f:
    pickle.dump(Tfidf, f)

# TF-IDF 행렬 저장
mmwrite('./models/Tfidf_bible_data3.mtx', Tfidf_matrix)

print("TF-IDF 모델과 행렬이 성공적으로 저장되었습니다!")

