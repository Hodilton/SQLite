import sqlite3
from datetime import datetime
from .base_table import BaseTable
from .products_table import ProductsTable
from .price_history_table import PriceHistoryTable

class Database:
    def __init__(self, db_name="data1.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.products_table = ProductsTable(self.connection, self.cursor)
        self.price_history_table = PriceHistoryTable(self.connection, self.cursor)
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products'")
        products_table_exists = self.cursor.fetchone()

        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='price_history'")
        price_history_table_exists = self.cursor.fetchone()

        if not products_table_exists:
            self.products_table.create_table()

        if not price_history_table_exists:
            self.price_history_table.create_table()

    def add_product(self, name, shop):
        self.products_table.add_product(name, shop)

    def add_price(self, name, shop, price, date_changed=None):
        if date_changed is None:
            date_changed = datetime.now().strftime('%Y-%m-%d')

        self.cursor.execute('SELECT id FROM products WHERE name = ? AND shop = ?', (name, shop))
        product_id = self.cursor.fetchone()

        if product_id is not None:
            self.price_history_table.add_price_record(product_id[0], shop, price, date_changed)
            self.products_table.update_current_price(name, shop, price)
        else:
            print(f"Product '{name}' in '{shop}' does not exist in the products table.")

    def view_tables(self):
        self.products_table.view_table('products', ['id', 'name', 'shop', 'current_price'])
        self.price_history_table.view_table('price_history', ['id', 'product_id', 'shop', 'price', 'date_changed'])

    def get_price_data(self, product_name, selected_shops, from_date, to_date):
        from_date_str = from_date.strftime("%Y-%m-%d")
        to_date_str = to_date.strftime("%Y-%m-%d")

        data = {}

        for shop in selected_shops:
            self.cursor.execute('''
                SELECT ph.date_changed, ph.price
                FROM price_history ph
                JOIN products p ON ph.product_id = p.id
                WHERE p.name = ? AND p.shop = ? AND ph.date_changed BETWEEN ? AND ?
            ''', (product_name, shop, from_date_str, to_date_str))
            records = self.cursor.fetchall()

            data[shop] = records

        return data

    def close_connection(self):
        self.connection.close()