import pandas as pd
from wordcloud import WordCloud
import collections
import matplotlib.pyplot as plt
from matplotlib import font_manager

font_path = '../holy_bible_project/malgun.ttf'
font_name = font_manager.FontProperties(fname=font_path).get_name()

df = pd.read_csv('./bible_end/cleaned_bible_data3.csv')
words = df.iloc[400, 1].split()
print(df.iloc[400, 1])

worddict = collections.Counter(words)
worddict = dict(worddict)
print(worddict)

wordcloud_img = WordCloud(
    background_color='white', font_path=font_path).generate_from_frequencies(worddict)
plt.figure(figsize=(12, 12))
plt.imshow(wordcloud_img, interpolation='bilinear')
plt.axis('off')
plt.show()

