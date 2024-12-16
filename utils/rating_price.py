from pymongo import MongoClient

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

import numpy as np
from scipy.stats import kruskal, shapiro

def build_graph(products):
    # Извлечение данных из коллекции MongoDB в список Python
    data = list(products)

    # Преобразование списка в DataFrame
    df = pd.DataFrame(data)

    # Извлекаем нужные столбцы: reviewRating и sizes
    df_cleaned = df[['reviewRating', 'sizes']].dropna()

    # Получение discountPrice из 'sizes' (это список словарей) и перевод в рубли
    df_cleaned['discountPrice'] = df_cleaned['sizes'].apply(lambda x: x[0]['discountPrice'] / 100 if x else None)

    # Удаляем записи с отсутствующими или нулевыми значениями рейтинга и цены
    df_cleaned = df_cleaned[(df_cleaned['reviewRating'] > 0) & (df_cleaned['discountPrice'] > 0)]

    # Фильтрация товаров с ценой меньше 20,000 рублей
    df_filtered = df_cleaned[df_cleaned['discountPrice'] < 20000]

    # Визуализация данных (диаграмма рассеяния)
    sns.scatterplot(x='discountPrice', y='reviewRating', data=df_filtered)
    plt.title('Зависимость между оценкой и ценой товара (цена < 20000 руб.)')
    plt.xlabel('Цена со скидкой (рубли)')
    plt.ylabel('Оценка товара')
    plt.show()

    # Вычисляем коэффициент корреляции Пирсона
    corr, p_value = pearsonr(df_filtered['discountPrice'], df_filtered['reviewRating'])
    print(f'Корреляция Пирсона для товаров с ценой ниже 20000 руб: {corr}, p-value: {p_value}')

    # Оценка полноты выборки через распределение цен
    df_filtered['price_category'] = pd.cut(df_filtered['discountPrice'], bins=[0, 1000, 5000, 10000, 20000], labels=['<1000', '1000-5000', '5000-10000', '>10000'])

    # Посмотрим распределение по ценовым категориям
    price_distribution = df_filtered['price_category'].value_counts()
    print('Распределение товаров по ценовым категориям:')
    print(price_distribution)

    # Проверка нормальности распределения цен и рейтингов
    stat, p_price = shapiro(df_filtered['discountPrice'])
    stat, p_rating = shapiro(df_filtered['reviewRating'])

    print(f'Нормальность распределения цен: p-value = {p_price}')
    print(f'Нормальность распределения рейтингов: p-value = {p_rating}')

    # Если p-value < 0.05, данные не нормальны

    # Оценка однородности через критерий Крускала-Уоллиса (для ценовых категорий)
    kruskal_result = kruskal(
        df_filtered[df_filtered['price_category'] == '<1000']['reviewRating'],
        df_filtered[df_filtered['price_category'] == '1000-5000']['reviewRating'],
        df_filtered[df_filtered['price_category'] == '5000-10000']['reviewRating'],
        df_filtered[df_filtered['price_category'] == '>10000']['reviewRating']
    )

    print(f'Критерий Крускала-Уоллиса для рейтингов по ценовым категориям: p-value = {kruskal_result.pvalue}')

    # Если p-value < 0.05, различия значимы

    # Оценка погрешности (стандартная ошибка) для средней цены и рейтинга
    mean_price = df_filtered['discountPrice'].mean()
    mean_rating = df_filtered['reviewRating'].mean()

    std_err_price = np.std(df_filtered['discountPrice']) / np.sqrt(len(df_filtered))
    std_err_rating = np.std(df_filtered['reviewRating']) / np.sqrt(len(df_filtered))

    print(f'Средняя цена: {mean_price}, Стандартная ошибка цены: {std_err_price}')
    print(f'Средний рейтинг: {mean_rating}, Стандартная ошибка рейтинга: {std_err_rating}')


