import pandas as pd
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from pymystem3 import Mystem
from rutermextract import TermExtractor

nltk.download("stopwords")        #загружаем стоп-слова для очистки текстовых файлов перед анализом
filename1 = 'rest.txt'            #названия файлов, которые будем анализировать
filename2 = 'extreme.txt'
filename3 = 'travel.txt'

mystem = Mystem()
russian_stopwords = stopwords.words("russian")

def normolaz_text(filename: str):                #функция для нормализации текста: удаляет стоп-слова и знаки пунктуации

    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()

    tokens = mystem.lemmatize(text.lower())
    clean_tokens = []

    for token in tokens:
        if token.strip().isalpha() == True and token.strip() not in russian_stopwords:
            clean_tokens.append(token)


    result = " ".join(clean_tokens)

    with open('result.txt', 'w', encoding='utf-8') as f:
        f.write(result)

    return result

def get_keywords(filename: str):                #функция проводит анализ текста, сохраняеет слова, которые встречаются в текте боле 3х раз
  clean_text = normolaz_text(filename)
  words = []
  term_extractor = TermExtractor()

  for term in term_extractor(clean_text):
    if term.count > 3:
      words.append(term.normalized)

  result = " ".join(words)

  with open(f'result {filename[:-4]}.txt', 'w', encoding='utf-8') as f:
      f.write(result.strip())

get_keywords(filename1)        #проводим анализ текстов по имени файла
get_keywords(filename2)
get_keywords(filename3)

df = pd.read_excel('analysis.xlsx', header=1, index_col=0)        #создаём датафрейм с анализом поисковых запросов
df = df.drop(columns="Доля трафика %")

concur = pd.read_excel('concur.xlsx', header=1, index_col=0)        #создаём датафрэйм с результатами анализа конкурентов

dfs = pd.read_excel(io='data.xlsx',                                #создаём датафрэйм с анализом запросов у конкурентов по месяцам
                    engine='openpyxl',
                    sheet_name=None, header=1, index_col=0)


for key in dfs.keys():
    dfs[key].index = dfs[key].index.strftime('%b %Y')            #задаём формат вывода даты на графике с поворотом подписей у оси х на 30 градусов
    dfs[key].plot(kind='bar', rot=30)


df.plot(kind='bar', stacked= True , color=['blue','orange','green','red','violet'])        #отображаем остальные датафрэймы
plt.title('Видимость URLов домена sberbank.com в выдаче Яндекс', fontsize= 16 )
plt.ylabel('Запросы')
plt.legend(loc='upper right', title=None)

concur.plot(kind='bar', stacked= True , color=['blue','orange','green','red','violet'])
plt.title('Запросы домена sberbank.com в Яндекс.Директ', fontsize= 16 )
plt.ylabel('Запросы')
plt.legend(loc='upper right', title=None)

plt.show()

