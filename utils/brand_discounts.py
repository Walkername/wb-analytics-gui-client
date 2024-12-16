import pandas as pd
from pymongo import MongoClient
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

def build_graph(products):
    # Извлечение данных из коллекции MongoDB в список Python
    data = list(products)

    # Преобразование списка в DataFrame
    df = pd.DataFrame(data)

    #  Извлекаем необходимые столбцы: 'brand' и 'sizes' (для расчета скидки)
    df_cleaned = df[['brand', 'sizes']].dropna()

    #  Рассчитываем процент скидки для каждого товара
    def calculate_discount(row):
        # Если информация о скидке присутствует
        if isinstance(row, list) and len(row) > 0:
            basic_price = row[0].get('basicPrice', 0)
            discount_price = row[0].get('discountPrice', 0)
            if basic_price and discount_price:
                # Рассчитываем процент скидки
                return ((basic_price - discount_price) / basic_price) * 100
        return 0

    # Применяем функцию для расчета скидки
    df_cleaned['discountPercentage'] = df_cleaned['sizes'].apply(lambda x: calculate_discount(x))

    # Удаляем строки с нулевым значением скидки
    df_cleaned = df_cleaned[df_cleaned['discountPercentage'] > 0]

    #  Группировка по бренду и расчет среднего процента скидки
    df_brand_discount = df_cleaned.groupby('brand').agg({'discountPercentage': 'mean'}).reset_index()

    # Переименуем столбцы для удобства
    df_brand_discount.columns = ['Brand', 'Average Discount Percentage']

    # Ensure 'brand' is of type string in both DataFrames
    df['brand'] = df['brand'].astype(str)
    df_brand_discount['Brand'] = df_brand_discount['Brand'].astype(str)

    # Определяем интервалы с шагом 10
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    labels = ['0-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90-100']

    # Создание новой колонки с категориями процента скидки
    df_brand_discount['Discount Range'] = pd.cut(df_brand_discount['Average Discount Percentage'], bins=bins, labels=labels, include_lowest=True)

    # Группировка по диапазонам скидки и подсчет количества брендов в каждом диапазоне
    grouped_by_discount_range = df_brand_discount.groupby('Discount Range').agg({'Brand': 'count'}).reset_index()

    # Переименуем столбцы для удобства
    grouped_by_discount_range.columns = ['Discount Range', 'Number of Brands']

    # Выводим результат
    print(grouped_by_discount_range)

    # Построение графика
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Discount Range', y='Number of Brands', data=grouped_by_discount_range)
    plt.title('Количество брендов по диапазонам среднего процента скидки (интервал 10%)')
    plt.xlabel('Диапазон среднего процента скидки')
    plt.ylabel('Количество брендов')
    plt.xticks(rotation=45)
    plt.show()

    # Проверим количество пропусков в данных
    missing_data = df.isnull().sum()
    print("Количество пропущенных данных по столбцам:")
    print(missing_data)

    # Вычисление стандартной ошибки для среднего процента скидки
    std_error = df_brand_discount['Average Discount Percentage'].std() / (len(df_brand_discount) ** 0.5)
    print(f"Стандартная ошибка: {std_error}")

    # Вычисление 95% доверительного интервала для среднего процента скидки
    confidence_interval = stats.t.interval(0.95, len(df_brand_discount)-1, loc=df_brand_discount['Average Discount Percentage'].mean(), scale=std_error)
    print(f"95% доверительный интервал: {confidence_interval}")
