from wordcloud import WordCloud
from stop_words import get_stop_words
import re
import numpy as np
from PIL import Image
from parser import result_string


result_string = re.sub(r'==.*?==+', '', result_string) # удаляем лишние символы
result_string = result_string.replace('\n', '') # удаляем знаки разделения на абзацы


# Записываем в переменную стоп-слова русского языка
STOPWORDS_RU = get_stop_words('russian')

# Превращаем картинку в маску
mask = np.array(Image.open('bird.jpg'))

# Генерируем облако слов
wordcloud = WordCloud(width=2000,
                      height=1500,
                      random_state=1,
                      background_color='white',
                      colormap='Set2',
                      collocations=False,
                      stopwords=STOPWORDS_RU,
                      mask=mask).generate(result_string)


# Выводим облако слов в картинку
wordcloud.to_file('hp_cloud_simple.png')