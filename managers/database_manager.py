from database.database import Database

class DatabaseManager:
    def __init__(self, db_name="database.db"):
        self.database = Database(db_name)

    def close_connection(self):
        self.database.close_connection()

    def get_product_names(self):
        return self.database.products_table.get_product_names()

    def get_shop_names(self):
        return self.database.products_table.get_shop_names()

    def get_price_data(self, product, shops, from_date, to_date):
        return self.database.get_price_data(product, shops, from_date, to_date)

    def get_current_prices(self, product, shops):
        return self.database.products_table.get_current_prices(product, shops)
