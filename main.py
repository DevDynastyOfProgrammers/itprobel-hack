from wordcloud import WordCloud
from stop_words import get_stop_words
import re
import numpy as np
from PIL import Image
from parser import result_string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import ngrams, FreqDist
from nltk.util import ngrams
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.collocations import *
import pymorphy3
from collections import Counter
# при первом запуске раскомментить
# nltk.download('punkt_tab')
# nltk.download('omw-1.4')
# nltk.download('wordnet')

import codecs
fileObj = codecs.open( "testText.txt", "r", "utf_8_sig" )
result_string = fileObj.read()
fileObj.close()

result_string = re.sub(r'==.*?==+', '', result_string) # удаляем лишние символы
result_string = result_string.replace('\n', '') # удаляем знаки разделения на абзацы

nltk.download('stopwords')
stop_words = stopwords.words('russian')
stop_words.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', 'к', 'на'])

from nltk.tokenize import RegexpTokenizer
def tokenize_text(text):
  # Удаление стоп слов
  tokenizer = RegexpTokenizer(r'\w+')
  word_tokens = tokenizer.tokenize(text)
  return word_tokens

def delete_stop_words(word_tokens):
  filtered_text = [w for w in word_tokens if not w.lower() in stop_words]

  return filtered_text

morph = pymorphy3.MorphAnalyzer()

def norm_adj_noun(words):

  last_word = words[-1]
  gender = words[1].tag.gender
  if gender == None:
    return (words)

  new_words = []
  last_word = last_word.inflect({'nomn', 'sing'})
  for word in words[:-1]:
    word = word.inflect({gender, 'nomn', 'sing'})
    new_words.append(word.word)
  new_words.append(last_word.word)
  new_words = tuple(new_words)

  return new_words

def __get_pairs_n(all_counts):
  norm_pairs = []

  for seq, freq in list(all_counts.items()):
    first = morph.parse(seq[0])[0]
    second = morph.parse(seq[1])[0]

    words = [morph.parse(word)[0] for word in seq]

    # частные случаи
    # if 'корел' in second.word:
    #   word = second.word.replace('о', 'а', 1)
    #   second = morph.parse(word)[0]

    if second.tag.POS == 'NOUN' and (first.tag.POS == 'ADJF' or first.tag.POS == 'ADJS'):
      norm_pair = norm_adj_noun((first, second))

      pair_exist = [norm_pair == seq for seq, freq in norm_pairs]
      if any(pair_exist):
        old_freq = norm_pairs[pair_exist.index(True)][1]
        norm_pairs[pair_exist.index(True)] = (norm_pair, old_freq+freq)
        continue

      norm_pairs.append((norm_pair, freq))
    else:
      # выбираем оставляем неподходящие словосочетания или пропускаем
      continue
      # norm_pairs.append((pair, freq))
  return norm_pairs

morph = pymorphy3.MorphAnalyzer()

def get_pairs_n(text, n):
    word_tokens = tokenize_text(text)
    filtered_text = delete_stop_words(word_tokens)

    data = filtered_text # stemmed_words, lemmatized_words

    all_counts = dict()
    all_counts[0] = FreqDist(ngrams(data, n))
    norm_pairs = __get_pairs_n(all_counts[0])

    freq_norm_pairs = FreqDist({pair: freq for pair, freq in norm_pairs})

    return freq_norm_pairs

n2 = get_pairs_n(result_string, 2)
# слова до
# print(result_string)
# слова после, выводим 20 самых частых словосочетаний
# print(n2.most_common(20))

def gen_wordsForCloud():
  wordsForCloud = []
  for pair, freq in n2.most_common(100):
    words = ' '.join(pair)
    for i in range(freq):
      wordsForCloud.append(words)
    # wordsForCloud.append(words)
  return wordsForCloud

# Генерируем облако слов
def generate_wordcloud(wordsForCloud):
  # Записываем в переменную стоп-слова русского языка
  STOPWORDS_RU = get_stop_words('russian')
  
  # Превращаем картинку в маску
  mask = np.array(Image.open('bird.jpg'))

  word_cloud_lst = Counter(wordsForCloud)
  print(word_cloud_lst)

  wordcloud = WordCloud(width=2000,
                        height=1500,
                        random_state=1,
                        background_color='white',
                        colormap='Set2',
                        collocation_threshold = 3,
                        # collocations=False,
                        stopwords=STOPWORDS_RU,
                        mask=mask).generate_from_frequencies(word_cloud_lst)
  return wordcloud

if __name__ == '__main__':
  wordsForCloud = gen_wordsForCloud()
  wordcloud = generate_wordcloud(wordsForCloud)

  # Выводим облако слов в картинку
  wordcloud.to_file('hp_cloud_simple.png')
