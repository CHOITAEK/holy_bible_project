import pandas as pd
import re
import chardet

# 1. 파일 인코딩 확인
file_path = './bible_text/1-4민수기.txt'  # 레위기 파일 경로
with open(file_path, 'rb') as file:
    raw_data = file.read()

encoding = chardet.detect(raw_data)['encoding']  # 인코딩 확인

# 2. 파일 읽기
with open(file_path, 'r', encoding=encoding) as file:
    text = file.readlines()

# 3. 데이터 처리
data = []

for line in text:
    line = line.strip()
    if line:  # 빈 줄 제외
        match = re.match(r"(민\d+:\d+)\s*(<[^>]+>)?\s*(.*)", line)
        if match:
            reference = match.group(1)  # 장과 절 (예: 레1:1)
            title = match.group(2) if match.group(2) else ""  # 제목 (예: <번제>)
            content = match.group(3)  # 구절 내용
            chapter_verse = reference.split(':')
            book = "민수기"  # "레" -> "레위기"
            verse = f"{int(chapter_verse[0][1:])}장 {int(chapter_verse[1])}절"  # "1:1" -> "1장 1절"
            combined_content = f"{title} {content}".strip()  # Title과 Content 합치기
            data.append([book, verse, combined_content])

# 4. 데이터프레임 생성
df = pd.DataFrame(data, columns=['Book', 'Chapter', 'Content'])

# 5. 엑셀 파일로 저장
output_path = './bible_end/1-4민수기.xlsx'
df.to_excel(output_path, index=False)

print("Processing completed. File saved to:", output_path)

