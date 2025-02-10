import os
import pandas as pd
import re
import chardet

# 텍스트 파일이 있는 폴더 경로
folder_path = 'bible_text/'  # 여기에 폴더 경로를 설정하세요
output_folder = 'converted_files/'  # 변환된 파일을 저장할 폴더

# 출력 폴더 생성 (없으면 생성)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


# 엑셀에서 허용되지 않는 문자 제거 함수
def clean_text(text):
    # 제어 문자를 제거
    return ''.join(c for c in text if ord(c) >= 32 and ord(c) != 127)


# 폴더 내 모든 파일 처리
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):  # .txt 파일만 처리
        file_path = os.path.join(folder_path, filename)

        # 파일 인코딩 확인
        with open(file_path, 'rb') as file:
            raw_data = file.read()
        encoding = chardet.detect(raw_data)['encoding']

        # 파일 읽기
        with open(file_path, 'r', encoding=encoding) as file:
            text = file.readlines()

        # 데이터 처리
        data = []
        full_name = filename.split('.')[0]  # 파일 이름 전체 (숫자 포함)
        book_name = re.sub(r'[\d-]', '', full_name).strip()  # 숫자와 '-' 제거한 성경 제목
        for line in text:
            line = line.strip()
            if line:  # 빈 줄 제외
                match = re.match(r"(\D+\d+:\d+)\s*(<[^>]+>)?\s*(.*)", line)
                if match:
                    reference = match.group(1)  # 장과 절 (예: 민1:1)
                    title = match.group(2) if match.group(2) else ""  # 제목
                    content = match.group(3)  # 구절 내용
                    chapter_verse = reference.split(':')
                    chapter = int(re.search(r'\d+', chapter_verse[0]).group())  # "민1" -> 1
                    verse = int(chapter_verse[1])  # 절
                    combined_content = f"{title} {content}".strip()
                    combined_content = clean_text(combined_content)  # 비정상 문자 제거
                    data.append([book_name, chapter, verse, combined_content])

        # 데이터프레임 생성
        df = pd.DataFrame(data, columns=['Book', 'Chapter', 'Verse', 'Content'])

        # Chapter와 Verse를 기준으로 정렬
        df.sort_values(by=['Chapter', 'Verse'], inplace=True)

        # Chapter와 Verse를 문자열로 변환 (예: "1장 1절")

        df = df[['Book', 'Chapter','Verse', 'Content']]  # 필요한 열만 유지

        # 엑셀 파일 저장
        output_file = os.path.join(output_folder, f"{full_name}.xlsx")  # 숫자를 유지한 파일명
        df.to_excel(output_file, index=False)
        print(f"Converted {filename} to {output_file}")


