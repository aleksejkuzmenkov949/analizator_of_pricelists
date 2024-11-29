import pandas as pd
import os

class PriceMachine:
    def __init__(self):
        self.data = []
        self.result = ''
        self.name_length = 0

    def load_prices(self, file_path='./prices'):  # Указываем путь к папке со списком прайсов
        # Поиск и обработка файлов с "price" в имени
        if not os.path.exists(file_path):
            print(f"Папка {file_path} не существует!")
            return
        for filename in os.listdir(file_path):
            if 'price' in filename and filename.endswith('.csv'):  # Проверяем шаблон имени
                file_path_full = os.path.join(file_path, filename)
                file = pd.read_csv(file_path_full)
                product_col, price_col, weight_col = self._search_product_price_weight(file.columns)
                # Проверка, что столбцы найдены
                if product_col and price_col and weight_col:
                    for _, row in file.iterrows():
                        product_name = row[product_col]
                        price = row[price_col]
                        weight = row[weight_col]
                        price_per_kg = price / weight if weight else 0  # Цена за кг
                        self.data.append((filename, product_name, price, weight, price_per_kg))

    def _search_product_price_weight(self, headers):
        # Определение подходящих заголовков для названия, цены и веса
        product_options = ['товар', 'название', 'наименование', 'продукт']
        price_options = ['розница', 'цена']
        weight_options = ['вес', 'масса', 'фасовка']
        product_col = next((header for header in headers if header.lower() in product_options), None)
        price_col = next((header for header in headers if header.lower() in price_options), None)
        weight_col = next((header for header in headers if header.lower() in weight_options), None)
        return product_col, price_col, weight_col

    def export_to_html(self, fname='output.html'):
        # Сортировка данных по `price_per_kg` от наименьшего к наибольшему
        self.data.sort(key=lambda x: x[4])  # x[4] - это price_per_kg
        # Генерация HTML-таблицы
        result = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Позиции продуктов</title>
        </head>
        <body>
            <table border="1" style="border-collapse: collapse;">
                <tr>
                    <th>Номер</th>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Фасовка</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>'''
        for number, item in enumerate(self.data):
            file_name, product_name, price, weight, price_per_kg = item
            result += f'<tr>'
            result += f'<td>{number + 1}</td>'
            result += f'<td>{product_name}</td>'
            result += f'<td>{price}</td>'
            result += f'<td>{weight}</td>'
            result += f'<td>{file_name}</td>'
            result += f'<td>{price_per_kg:.2f}</td>'
            result += f'</tr>'
        result += '''
            </table>
        </body>
        </html>'''
        with open(fname, 'w', encoding='windows-1251') as f:
            f.write(result)
        print(f'HTML-файл {fname} успешно создан!')

if __name__ == '__main__':
    pm = PriceMachine()
    pm.load_prices()  # Путь по умолчанию теперь "./prices"
    pm.export_to_html()
    print('The end')