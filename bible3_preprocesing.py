import pandas as pd
from konlpy.tag import Okt
from tqdm import tqdm
import re

df = pd.read_csv('./bible_end/bible_data3.csv')
df.info()

df_stopwords = pd.read_csv('./bible_end/stopwords.csv')
stopwords = list(df_stopwords['stopword'])

okt = Okt()
print(df.Chapter[0])
print(df.Content[0])
cleaned_sentences = []
#for Content in df.Content:
for Content in tqdm(df.Content):
    Content = re.sub('[^가-힣]', ' ', Content)
    print(Content)
    tokened_Content = okt.pos(Content, stem=True)
    print(tokened_Content)
    df_token = pd.DataFrame(tokened_Content, columns=['word', 'class'])
    df_token = df_token[(df_token['class'] == 'Noun') |
                        (df_token['class'] == 'Verb') |
                        (df_token['class'] == 'Adjective')]
    print(df_token)
    words = []
    for word in df_token.word:
        if 1 < len(word):
            if word not in stopwords:
                words.append(word)
    cleaned_sentence = ' '.join(words)
    cleaned_sentences.append(cleaned_sentence)
df.Content = cleaned_sentences
df.dropna(inplace=True)
df.info()
df.to_csv('./bible_end/cleaned_bible_data3.csv', index=False)