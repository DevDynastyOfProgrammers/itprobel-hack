from wordcloud import WordCloud
from stop_words import get_stop_words
import re
import numpy as np
from PIL import Image
from parser import result_string
import nltk
# nltk.download('punkt_tab')
# nltk.download('omw-1.4')
# nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pymorphy3


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
  # word_tokens = word_tokenize(rus_text)
  filtered_text = [w for w in word_tokens if not w.lower() in stop_words]
  # print(len(word_tokens))
  # print(len(filtered_text))

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
  # print(new_words)

  # words[0] = words[0].inflect({gender,'nomn', 'sing'})
  # words[1] = words[1].inflect({'nomn', 'sing'})
  return new_words

def __get_pairs_n(all_counts):
  norm_pairs = []

  for seq, freq in list(all_counts.items()):
    # print(pair, freq)
    first = morph.parse(seq[0])[0]
    second = morph.parse(seq[1])[0]

    words = [morph.parse(word)[0] for word in seq]
    # print(words)

    # частные случаи
    # if 'корел' in second.word:
    #   word = second.word.replace('о', 'а', 1)
    #   second = morph.parse(word)[0]

    if second.tag.POS == 'NOUN' and (first.tag.POS == 'ADJF' or first.tag.POS == 'ADJS'):
      # print(first, second)
      norm_pair = norm_adj_noun((first, second))

      pair_exist = [norm_pair == seq for seq, freq in norm_pairs]
      if any(pair_exist):
        old_freq = norm_pairs[pair_exist.index(True)][1]
        norm_pairs[pair_exist.index(True)] = (norm_pair, old_freq+freq)
        continue

      norm_pairs.append((norm_pair, freq))
    else:
      continue
      # norm_pairs.append((pair, freq))
  return norm_pairs

from nltk import ngrams, FreqDist
from nltk.util import ngrams
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.collocations import *

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
print(result_string)
print(n2.most_common(20))

# wordsForCloud = []
# for pair, freq in n2.most_common(10):
#   wordsForCloud.append(pair)
#   print(freq)

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