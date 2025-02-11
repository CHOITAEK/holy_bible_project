import pandas as pd
from gensim.models import Word2Vec

# 데이터 로드
df_Content = pd.read_csv('./bible_end/cleaned_bible_data3.csv')
df_Content.info()

# 결측값 처리
df_Content['Content'] = df_Content['Content'].fillna("")

# Content 열의 데이터를 리스트로 변환
content = list(df_Content['Content'])
print("첫 번째 문장:", content[0])

# 문장 단위 토큰화
tokens = []
for sentence in content:
    token = sentence.split()
    tokens.append(token)
print("첫 번째 문장의 토큰:", tokens[0])

# Word2Vec 학습
embedding_model = Word2Vec(
    tokens,
    vector_size=100,
    window=4,
    min_count=20,
    workers=4,
    epochs=100,
    sg=1
)

# 모델 저장
embedding_model.save('./models/word2vec_bible_data3.model')

# 학습된 단어 확인
print("학습된 단어 목록:", list(embedding_model.wv.index_to_key))
print("학습된 단어 수:", len(embedding_model.wv.index_to_key))



