import pandas as pd
from pymongo import MongoClient
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.stats import shapiro
import numpy as np

def build_graph(products):
    data = list(products)
    df = pd.DataFrame(data)

    # Извлечение нужных столбцов и очистка данных
    df_cleaned = df[['brand', 'reviewRating']].dropna()
    df_cleaned = df_cleaned[df_cleaned['reviewRating'] > 0]

    # Группировка по брендам и расчет среднего рейтинга
    df_brand_ratings = df_cleaned.groupby('brand').agg({'reviewRating': 'mean'}).reset_index()
    df_brand_ratings.columns = ['Brand', 'Average Review Rating']

    # Определение диапазонов рейтинга
    bins = [1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2, 4.4, 4.6, 4.8, 5.0]
    labels = ['1.0-1.2', '1.2-1.4', '1.4-1.6', '1.6-1.8', '1.8-2.0', '2.0-2.2', '2.2-2.4', '2.4-2.6', '2.6-2.8',
            '2.8-3.0', '3.0-3.2', '3.2-3.4', '3.4-3.6', '3.6-3.8', '3.8-4.0', '4.0-4.2', '4.2-4.4', '4.4-4.6',
            '4.6-4.8', '4.8-5.0']

    df_brand_ratings['Rating Range'] = pd.cut(df_brand_ratings['Average Review Rating'], bins=bins, labels=labels, include_lowest=True)
    grouped_by_rating_range = df_brand_ratings.groupby('Rating Range').agg({'Brand': 'count'}).reset_index()
    grouped_by_rating_range.columns = ['Rating Range', 'Number of Brands']

    # Оценка полноты
    missing_values = df.isnull().sum()
    print("Количество пропущенных значений по столбцам:\n", missing_values)

    # Оценка однородности
    cv = df_cleaned['reviewRating'].std() / df_cleaned['reviewRating'].mean() * 100
    print(f"Коэффициент вариации для рейтингов: {cv:.2f}%")

    # Тест на нормальность
    stat, p_value = shapiro(df_cleaned['reviewRating'])
    print(f"Статистика Shapiro-Wilk: {stat:.4f}, p-value: {p_value:.4f}")

    # 95% доверительный интервал
    mean_rating = df_cleaned['reviewRating'].mean()
    std_rating = df_cleaned['reviewRating'].std()
    n = df_cleaned.shape[0]
    confidence_interval = stats.norm.interval(0.95, loc=mean_rating, scale=std_rating / np.sqrt(n))
    print(f"Доверительный интервал для среднего рейтинга: {confidence_interval}")

    # Построение графика количества брендов по диапазонам рейтинга
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Rating Range', y='Number of Brands', data=grouped_by_rating_range)
    plt.title('Количество брендов по диапазонам среднего рейтинга товаров (шаг 0.2)')
    plt.xlabel('Диапазон среднего рейтинга')
    plt.ylabel('Количество брендов')
    plt.xticks(rotation=45)
    plt.show()
