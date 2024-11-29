import os
import pandas as pd
from tabulate import tabulate

class PriceMachine:
    def __init__(self):
        """Инициализация с пустыми данными."""
        self.data = []

    def load_prices(self, folder):
        """Загрузка данных из всех подходящих CSV-файлов в указанной папке."""
        if not os.path.exists(folder) or not os.path.isdir(folder):
            print(f"Папка '{folder}' не существует или не является директорией!")
            return

        for file_name in os.listdir(folder):
            if file_name.endswith('.csv'):
                file_path = os.path.join(folder, file_name)
                try:
                    # Чтение данных
                    df = pd.read_csv(file_path)

                    # Поиск важных столбцов
                    product_col, price_col, weight_col = self._find_columns(df.columns)

                    # Если нашли нужные столбцы, добавляем их в self.data
                    if product_col and price_col and weight_col:
                        for _, row in df.iterrows():
                            product = row[product_col]
                            price = float(row[price_col]) if not pd.isna(row[price_col]) else 0
                            weight = float(row[weight_col]) if not pd.isna(row[weight_col]) else 0
                            price_per_kg = price / weight if weight > 0 else 0

                            self.data.append((file_name, product, price, weight, price_per_kg))

                except Exception as e:
                    print(f"Ошибка чтения файла '{file_name}': {e}")

    def _find_columns(self, headers):
        """Определение ключевых столбцов по их предположительным названиям."""
        product_options = ['название', 'товар', 'наименование', 'продукт']
        price_options = ['цена', 'розничная цена', 'стоимость']
        weight_options = ['вес', 'масса', 'фасовка']

        product_col = next((col for col in headers if col.lower() in product_options), None)
        price_col = next((col for col in headers if col.lower() in price_options), None)
        weight_col = next((col for col in headers if col.lower() in weight_options), None)

        return product_col, price_col, weight_col

    def find_text(self):
        """Поиск по введенному тексту через консоль."""
        if not self.data:
            print("Нет данных для поиска.")
            return

        while True:
            search_text = input("Введите текст для поиска (или 'exit' для выхода): ").strip()
            if search_text.lower() in ['exit', 'выход']:
                print("Выход из программы.")
                break

            # Отфильтровать данные
            filtered_data = [
                (index + 1, item[1], item[2], item[3], item[0], f"{item[4]:.2f}")
                for index, item in enumerate(self.data)
                if search_text.lower() in str(item[1]).lower()
            ]

            # Сортировка по стоимости за килограмм
            filtered_data = sorted(filtered_data, key=lambda x: float(x[5]))

            # Вывод результатов
            if filtered_data:
                headers = ["Номер", "Название", "Цена", "Фасовка", "Файл", "Цена за кг"]
                table = tabulate(filtered_data, headers=headers, tablefmt="grid")
                print("\n**Результаты поиска:**")
                print(table)
            else:
                print(f"\nНе найдено позиций с текстом '{search_text}'.")

# Главная точка входа
if __name__ == "__main__":
    # Создаем объект класса
    machine = PriceMachine()

    # Указываем папку с файлами
    folder_path = './prices'

    # Загружаем данные
    machine.load_prices(folder_path)

    if machine.data:
        print("\nДанные успешно загружены. Вы можете выполнить поиск.")
    else:
        print("\nДанные не найдены. Проверьте папку или содержимое файлов.")

    # Поиск товара через консоль
    machine.find_text()