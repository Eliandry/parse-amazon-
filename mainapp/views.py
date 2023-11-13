import os

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
import re
import string
import random
import base64
from io import BytesIO
from .forms import ScraperForm
import subprocess
import shlex

def file_list(request):
    # Получаем список всех файлов в папке 'res'
    files = os.listdir('res')
    csv_files = [file for file in files if file.endswith('.csv')]
    return render(request, 'file_list.html', {'files': csv_files})

def main(request):
    return render(request,"main.html")
def run_spider(request):
    if request.method == 'POST':
        form = ScraperForm(request.POST)
        if form.is_valid():
            my_base_url = form.cleaned_data['my_base_url']
            k = my_base_url.split(sep='/')
            name = k[3]
            # Запуск скрипта Scrapy с параметром
            command = f'scrapy runspider amazon_reviews_scraping/spiders/amazon_review.py -o res/{name}.csv -a my_base_url="{my_base_url}"'
            subprocess.run(shlex.split(command))
    else:
        form = ScraperForm()
    return render(request, 'run_spider.html', {'form': form})

def plot_view(request,filename):
    nltk.download('stopwords')

    # Загрузка данных
    df = pd.read_csv(f'res/{filename}')

    # Предобработка данных
    def preprocess_text(text):
        # Приведение текста к нижнему регистру
        text = text.lower()
        # Удаление знаков пунктуации
        text = re.sub(f"[{string.punctuation}]", " ", text)
        # Удаление стоп-слов
        stop_words = set(stopwords.words('english'))
        text = ' '.join([word for word in text.split() if word not in stop_words])
        return text

    df['comment'] = df['comment'].apply(preprocess_text)

    # Извлечение ключевых слов с использованием TF-IDF
    vectorizer = TfidfVectorizer(max_features=100, max_df=0.85, min_df=2)
    tfidf_matrix = vectorizer.fit_transform(df['comment'])
    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.sum(axis=0).tolist()[0]
    sorted_words = sorted(zip(feature_names, scores), key=lambda x: x[1], reverse=True)
    keywords, values = zip(*sorted_words)

    word_scores = {word: score for word, score in zip(keywords, values)}

    # Сортируем слова по убыванию важности
    data = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)

    fig = plt.figure(figsize=(15, 12))

    # Добавление облака слов
    ax = plt.subplot2grid((5, 4), (0, 0), rowspan=4, colspan=4)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    positions = []

    for word, freq in data:
        x, y = random.uniform(1, 9), random.uniform(1, 9)
        text = plt.text(x, y, word, ha='center', va='center', size=freq * 10, alpha=0.75,
                        color=np.random.rand(3, ))
        bbox = text.get_window_extent(renderer=fig.canvas.get_renderer())
        bbox = bbox.transformed(ax.transData.inverted())

        overlap = True
        iteration = 0

        while overlap and iteration < 100:
            overlap = False
            for pos in positions:
                if bbox.overlaps(pos):
                    x, y = random.uniform(1, 9), random.uniform(1, 9)
                    text.set_position((x, y))
                    bbox = text.get_window_extent(renderer=fig.canvas.get_renderer())
                    bbox = bbox.transformed(ax.transData.inverted())
                    overlap = True
                    break
            iteration += 1

        positions.append(bbox)

    # Добавление гистограммы
    ax2 = plt.subplot2grid((5, 4), (4, 0), rowspan=1, colspan=4)
    frequencies = [freq for word, freq in data]
    labels = [word for word, freq in data]
    ax2.bar(labels, frequencies, edgecolor='black')
    ax2.set_title('Распределение частоты слов')
    ax2.set_xlabel('Слова')
    ax2.set_ylabel('Частота')
    ax2.tick_params(axis='x', rotation=60)  # Поворот подписей

    # Настройка отступов
    plt.subplots_adjust(hspace=0.5)
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    plt.close()
    return render(request, 'plot.html', {'image_base64': image_base64})