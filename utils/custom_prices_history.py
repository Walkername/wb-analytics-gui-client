import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt

def build_graph():
    # Подключение к MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["wb-products"]
    collection = db["products"]

    # Загрузка данных из MongoDB
    data = pd.DataFrame(list(collection.find()))

    # Предобработка данных (проверка и извлечение discountPrice и даты)
    if 'sizes' in data.columns:
        data['discountPrice'] = data['sizes'].apply(lambda x: x[0]['discountPrice'] if len(x) > 0 else None)
    if 'priceHistory' in data.columns:
        data['date'] = data['priceHistory'].apply(lambda x: pd.to_datetime(x[0]['time'], unit='s') if len(x) > 0 else None)

    # Фильтрация по категориям entity
    categories = ['Костюмы', 'Пижамы', 'Костюмы спортивные', 'Платья', 'Жилеты', 'Пиджаки', 'Жакеты', 'Болеро', 'Туники',
                'Худи', 'Свитшоты', 'Толстовки', 'Мантии', 'Толстовки спортивные', 'Юбки', 'Брюки', 'Тайтсы', 'Бриджи', 'Бермуды', 'Куртки',
                'Пуховики', 'Пальто', 'Бомберы', 'Ветровки', 'Парки', 'Анораки',  'Косухи', 'Плащи',
                'Полупальто', 'Тренчкоты', 'Водолазки', 'Свитеры', 'Пуловеры', 'Джемперы', 'Кардиганы', 'Кофты',
                'Джинсы']

    # Оставляем данные по этим категориям и корректируем дату и цену
    filtered_data = data[data['entity'].isin(categories)].dropna(subset=['discountPrice', 'date'])
    filtered_data['discountPrice'] = filtered_data['discountPrice'] / 100  # Преобразуем цену в рубли

    # Группировка данных по месяцу и категории
    filtered_data['month'] = filtered_data['date'].dt.to_period('M')  # Перевод даты в месячный период
    grouped_data = filtered_data.groupby(['entity', 'month']).agg({'discountPrice': 'mean'}).reset_index()

    # Функция для построения графика только с историческими данными
    def plot_historical_prices(entity_data, category_name):
        # Преобразуем периоды в даты
        entity_data['month'] = entity_data['month'].dt.to_timestamp()

        # Подготовка данных для графика
        df = entity_data.set_index('month')['discountPrice']

        # Построение графика
        plt.figure(figsize=(10, 6))
        plt.plot(df.index, df, label='Исторические данные', color='blue')
        plt.title(f'Средняя цена для категории: {category_name}')
        plt.xlabel('Дата')
        plt.ylabel('Средняя цена (руб)')
        plt.legend()
        plt.show()

    # Цикл по категориям и построение графиков
    for category in categories:
        entity_data = grouped_data[grouped_data['entity'] == category]
        if not entity_data.empty:
            plot_historical_prices(entity_data, category)

    cv = filtered_data['discountPrice'].std() / filtered_data['discountPrice'].mean() * 100
    print(f"Коэффициент вариации для discountPrice: {cv:.2f}%")

