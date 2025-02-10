import os
import pandas as pd

# 변환된 엑셀 파일이 있는 폴더 경로
input_folder = './converted_files/'  # 변환된 엑셀 파일이 저장된 폴더
output_file = 'bible_end/bible_data.csv'  # 최종 저장될 CSV 파일 이름

# 파일명에서 숫자를 추출하는 함수
def extract_number(filename):
    return int(''.join(filter(str.isdigit, filename.split('-')[0])))

# 모든 엑셀 파일 읽어와 합치기
dataframes = []

for filename in sorted(os.listdir(input_folder), key=extract_number):  # 숫자 순으로 정렬
    if filename.endswith('.xlsx'):  # 엑셀 파일만 처리
        file_path = os.path.join(input_folder, filename)
        df = pd.read_excel(file_path)  # 엑셀 파일 읽기
        dataframes.append(df)  # 데이터프레임 리스트에 추가

# 모든 데이터프레임을 하나로 합치기
combined_df = pd.concat(dataframes, ignore_index=True)

# 합친 데이터를 CSV로 저장
combined_df.to_csv(output_file, index=False, encoding='utf-8-sig')  # UTF-8-SIG로 저장 (Excel 호환)

print(f"Combined CSV file created: {output_file}")
