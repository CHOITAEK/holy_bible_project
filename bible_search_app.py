import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from gensim.models import Word2Vec
from scipy.io import mmread
import pickle
from PyQt5.QtCore import Qt
from konlpy.tag import Okt  # 형태소 분석기

form_window = uic.loadUiType('./bible_search_app.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Tfidf_matrix = mmread('./models/Tfidf_bible_data.mtx').tocsr()
        with open('./models/tfidf.pickle', 'rb') as f:
            self.Tfidf = pickle.load(f)
        self.embedding_model = Word2Vec.load('./models/word2vec_bible_data3.model')

        self.df_Content = pd.read_csv('./bible_end/bible_data3.csv')
        self.okt = Okt()  # 형태소 분석기 초기화

        # 콤보박스 초기화
        self.Chapter = list(self.df_Content.Chapter)
        self.Chapter = self.sort_bible_chapters(self.Chapter)  # 성경 순서로 정렬
        for title in self.Chapter:
            self.cb_title.addItem(title)

        # 버튼 클릭 이벤트 연결
        self.btn_recommend.clicked.connect(self.btn_slot)
        self.cb_title.currentIndexChanged.connect(self.combobox_slot)

        # 레이블 설정
        self.lbl_recommendation.setWordWrap(True)

    def btn_slot(self):
        user_input = self.le_keyword.text()
        recommendation = self.recommendation_by_input(user_input)
        if recommendation:
            self.lbl_recommendation.setText(recommendation)

    def combobox_slot(self):
        title = self.cb_title.currentText()
        recommendation = self.display_only_selected_content(title)
        if recommendation:
            self.lbl_recommendation.setText(recommendation)

    # 사용자가 입력한 고민을 분석하여 추천
    def recommendation_by_input(self, user_input):
        try:
            # 입력 문장을 형태소 분석 후 주요 명사 추출
            keywords = self.okt.nouns(user_input)
            if not keywords:
                return '입력된 문장에서 유의미한 단어를 찾을 수 없습니다.'

            # 추출된 키워드를 하나의 문장으로 결합
            keyword_sentence = ' '.join(keywords)

            # TF-IDF 벡터 변환
            input_vec = self.Tfidf.transform([keyword_sentence])
            cosine_sim_tfidf = linear_kernel(input_vec, self.Tfidf_matrix)

            # TF-IDF 기반 추천 생성
            recommendations = self.getRecommendation_with_content(cosine_sim_tfidf, top_n=3)

            combined_recommendation = f"검색 기반 추천\n\n{recommendations}"
            return combined_recommendation
        except Exception as e:
            return '추천을 생성하는 중 오류가 발생했습니다.'

    # 선택된 제목의 내용만 표시
    def display_only_selected_content(self, title):
        bible_idx = self.df_Content[self.df_Content.Chapter == title].index[0]
        content = self.df_Content.at[bible_idx, 'Content']
        wrapped_content = self.wrap_text(content, 80)  # 줄 바꿈 길이 설정
        return f"{title} \n{wrapped_content}"

    def wrap_text(self, text, width):
        return '\n'.join([text[i:i+width] for i in range(0, len(text), width)])

    def getRecommendation_with_content(self, cosine_sim, top_n=3):
        simScore = list(enumerate(cosine_sim[-1]))
        simScore = sorted(simScore, key=lambda x: x[1], reverse=True)
        simScore = simScore[:top_n]  # 상위 top_n개만 선택
        recommendations = []
        for i in simScore:
            index = i[0]
            chapter = self.df_Content.iloc[index]['Chapter']
            content = self.df_Content.iloc[index]['Content']
            wrapped_content = self.wrap_text(content, 80)  # 줄 바꿈 길이 설정
            recommendations.append(f"{chapter}\n{wrapped_content}\n")
        return '\n'.join(recommendations)

    def sort_bible_chapters(self, chapters):
        # 성경 순서 정렬 정의
        bible_order = [
            "창세기", "출애굽기", "레위기", "민수기", "신명기", "여호수아", "사사기", "룻기", "사무엘상", "사무엘하",
            "열왕기상", "열왕기하", "역대상", "역대하", "에스라", "느헤미야", "에스더", "욥기", "시편", "잠언",
            "전도서", "아가", "이사야", "예레미야", "예레미야애가", "에스겔", "다니엘", "호세아", "요엘", "아모스",
            "오바댜", "요나", "미가", "나훔", "하박국", "스바냐", "학개", "스가랴", "말라기", "마태복음", "마가복음",
            "누가복음", "요한복음", "사도행전", "로마서", "고린도전서", "고린도후서", "갈라디아서", "에베소서", "빌립보서",
            "골로새서", "데살로니가전서", "데살로니가후서", "디모데전서", "디모데후서", "디도서", "빌레몬서", "히브리서",
            "야고보서", "베드로전서", "베드로후서", "요한일서", "요한이서", "요한삼서", "유다서", "요한계시록"
        ]

        # 성경 순서에 따라 정렬
        chapter_dict = {chapter: i for i, chapter in enumerate(bible_order)}
        return sorted(chapters, key=lambda x: chapter_dict.get(x, float('inf')))

if __name__ == '__main__':

    # 노트북 윈도우 배열 문제
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)     # PyQt가 Windows 배율 설정을 감지하고 조절하도록 함
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)        # 아이콘, 그래픽 요소가 흐려지는 문제 해결

    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())



