from .base_table import BaseTable

class PriceHistoryTable(BaseTable):
    def create_table(self):
        query = '''
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY,
                product_id INTEGER,
                shop TEXT NOT NULL,
                price REAL NOT NULL,
                date_changed TEXT NOT NULL,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        '''
        super().create_table(query)

    def add_price_record(self, product_id, shop, price, date_changed):
        self.cursor.execute('''
            INSERT INTO price_history (product_id, shop, price, date_changed)
            VALUES (?, ?, ?, ?)
        ''', (product_id, shop, price, date_changed))
        self.connection.commit()

    def get_average_prices(self, product_name, selected_shops):
        average_prices = {}

        for shop in selected_shops:
            self.cursor.execute('''
                SELECT AVG(ph.price) as average_price
                FROM price_history ph
                JOIN products p ON ph.product_id = p.id
                WHERE p.name = ? AND p.shop = ?
            ''', (product_name, shop))
            average_price = self.cursor.fetchone()

            average_prices[shop] = average_price[0] if average_price[0] is not None else 0.0

        return average_prices
