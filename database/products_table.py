import sqlite3

from .base_table import BaseTable

class ProductsTable(BaseTable):
    def create_table(self):
        query = '''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                shop TEXT NOT NULL,
                current_price REAL,
                UNIQUE(name, shop)
            )
        '''
        super().create_table(query)

    def add_product(self, name, shop):
        try:
            self.cursor.execute('INSERT INTO products (name, shop) VALUES (?, ?)', (name, shop))
            self.connection.commit()
        except sqlite3.IntegrityError:
            print(f"Product '{name}' for shop '{shop}' already exists.")

    def update_current_price(self, name, shop, price):
        self.cursor.execute('''
            UPDATE products
            SET current_price = ?
            WHERE name = ? AND shop = ?;
        ''', (price, name, shop))
        self.connection.commit()

    def get_current_prices(self, product_name, selected_shops):
        current_prices = {}

        for shop in selected_shops:
            self.cursor.execute('''
                SELECT current_price
                FROM products
                WHERE name = ? AND shop = ?
            ''', (product_name, shop))
            price = self.cursor.fetchone()

            current_prices[shop] = price[0] if price is not None else "N/A"

        return current_prices

    def get_product_names(self):
        self.cursor.execute("SELECT DISTINCT name FROM products")
        return [row[0] for row in self.cursor.fetchall()]

    def get_shop_names(self):
        self.cursor.execute("SELECT DISTINCT shop FROM products")
        return [row[0] for row in self.cursor.fetchall()]
