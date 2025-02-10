import pandas as pd
import re

# 주요 키워드 정의
keywords = {
    "사랑": ["사랑", "은혜", "구원", "자비"],
    "믿음": ["믿음", "신뢰", "의지", "확신"],
    "평안": ["평안", "안식", "위로", "쉼"],
    "용기": ["용기", "힘", "능력", "강함"],
    "감사": ["감사", "찬양", "기쁨", "영광"],
}

# 기존 성경 데이터 파일 로드
input_file = "./bible_end/bible_data.csv"  # 기존 CSV 파일 경로
df = pd.read_csv(input_file)

# 데이터 클린업
df["Content"] = df["Content"].fillna("").str.strip()  # 공백 및 NULL 값 처리

# 분류 결과를 저장할 열 추가
df["Topic"] = ""

# 키워드 기반으로 주제를 분류하는 함수
def classify_content(content):
    matched_topics = []
    for topic, words in keywords.items():
        for word in words:
            if word in str(content):  # 단어 포함 여부 확인
                matched_topics.append(topic)
                break  # 해당 주제에 매칭되면 나머지 키워드는 확인하지 않음
    return ", ".join(matched_topics)

# 데이터프레임에 주제 할당
df["Topic"] = df["Content"].apply(classify_content)

# 열 이름 변경 및 순서 조정
df = df[["Book", "Chapter", "Verse", "Content", "Topic"]]  # 열 순서 변경

# 결과를 저장
output_file = "./bible_end/classified_bible_data.csv"
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print(f"분류된 데이터를 '{output_file}'에 저장했습니다!")
