import pandas as pd
from pymongo import MongoClient
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import kruskal

def build_graph(products):
    # Извлечение данных из коллекции MongoDB в список Python
    data = list(products)

    # Преобразование списка в DataFrame
    df = pd.DataFrame(data)

    # Извлечение нужных столбцов: 'brand' и 'reviewRating'
    df_cleaned = df[['brand', 'reviewRating']].dropna()

    # Удаление строк с нулевым рейтингом
    df_cleaned = df_cleaned[df_cleaned['reviewRating'] > 0]

    # Группировка по брендам и расчет среднего рейтинга и количества отзывов
    df_brand_ratings = df_cleaned.groupby('brand').agg(
        Average_Review_Rating=('reviewRating', 'mean'),
        Review_Count=('reviewRating', 'count')
    ).reset_index()

    # Определение взвешенных средних рейтингов (с учетом количества отзывов)
    df_cleaned['weighted_rating'] = df_cleaned['reviewRating'] * df_cleaned.groupby('brand')['reviewRating'].transform('count')
    weighted_avg = df_cleaned.groupby('brand')['weighted_rating'].sum() / df_cleaned.groupby('brand')['reviewRating'].count()
    df_brand_ratings['Weighted_Average_Rating'] = weighted_avg.values

    # Определяем интервалы с шагом 0.2
    bins = [1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2, 4.4, 4.6, 4.8, 5.0]
    labels = ['1.0-1.2', '1.2-1.4', '1.4-1.6', '1.6-1.8', '1.8-2.0', '2.0-2.2', '2.2-2.4', '2.4-2.6', '2.6-2.8',
            '2.8-3.0', '3.0-3.2', '3.2-3.4', '3.4-3.6', '3.6-3.8', '3.8-4.0', '4.0-4.2', '4.2-4.4',
            '4.4-4.6', '4.6-4.8', '4.8-5.0']

    # Создание новой колонки с категориями среднего рейтинга
    df_brand_ratings['Rating Range'] = pd.cut(df_brand_ratings['Average_Review_Rating'], bins=bins, labels=labels, include_lowest=True)

    # Группировка по диапазонам рейтинга и подсчет количества брендов в каждом диапазоне
    grouped_by_rating_range = df_brand_ratings.groupby('Rating Range').agg({'brand': 'count'}).reset_index()
    grouped_by_rating_range.columns = ['Rating Range', 'Number of Brands']

    # Вывод коэффициента полноты выборки
    fullness_coefficient = len(df_cleaned) / len(data) * 100
    print(f"Коэффициент полноты выборки: {fullness_coefficient:.2f}%")

    # Дисперсионный анализ с использованием критерия Краскела-Уоллиса
    grouped_data = [group['reviewRating'].values for brand, group in df_cleaned.groupby('brand')]
    kruskal_h_val, kruskal_p_val = kruskal(*grouped_data)
    print(f"Критерий Краскела-Уоллиса: H-значение = {kruskal_h_val:.4f}, p-значение = {kruskal_p_val:.4f}")

    # Построение графика
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Rating Range', y='Number of Brands', data=grouped_by_rating_range)
    plt.title('Количество брендов по диапазонам среднего рейтинга товаров (шаг 0.2)')
    plt.xlabel('Диапазон среднего рейтинга')
    plt.ylabel('Количество брендов')
    plt.xticks(rotation=45)
    plt.show()
