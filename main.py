import pandas as pd
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from pymystem3 import Mystem
from rutermextract import TermExtractor

nltk.download("stopwords")
filename1 = 'rest.txt'
filename2 = 'extreme.txt'
filename3 = 'travel.txt'

mystem = Mystem()
russian_stopwords = stopwords.words("russian")

def normolaz_text(filename: str):

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

def get_keywords(filename: str):
  clean_text = normolaz_text(filename)
  words = []
  term_extractor = TermExtractor()

  for term in term_extractor(clean_text):
    if term.count > 3:
      words.append(term.normalized)

  result = " ".join(words)

  with open(f'result {filename[:-4]}.txt', 'w', encoding='utf-8') as f:
      f.write(result.strip())

get_keywords(filename1)
get_keywords(filename2)
get_keywords(filename3)

df = pd.read_excel('analysis.xlsx', header=1, index_col=0)
df = df.drop(columns="Доля трафика %")

concur = pd.read_excel('concur.xlsx', header=1, index_col=0)

dfs = pd.read_excel(io='data.xlsx',
                    engine='openpyxl',
                    sheet_name=None, header=1, index_col=0)


for key in dfs.keys():
    dfs[key].index = dfs[key].index.strftime('%b %Y')
    dfs[key].plot(kind='bar', rot=30)


df.plot(kind='bar', stacked= True , color=['blue','orange','green','red','violet'])
plt.title('Видимость URLов домена sberbank.com в выдаче Яндекс', fontsize= 16 )
plt.ylabel('Запросы')
plt.legend(loc='upper right', title=None)

concur.plot(kind='bar', stacked= True , color=['blue','orange','green','red','violet'])
plt.title('Запросы домена sberbank.com в Яндекс.Директ', fontsize= 16 )
plt.ylabel('Запросы')
plt.legend(loc='upper right', title=None)

plt.show()

