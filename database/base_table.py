class BaseTable:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def create_table(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    def view_table(self, table_name, columns):
        self.cursor.execute(f'SELECT {", ".join(columns)} FROM {table_name}')
        records = self.cursor.fetchall()

        print(f"\n{table_name.capitalize()} Table:")
        for record in records:
            print(", ".join([f"{columns[i]}: {record[i]}" for i in range(len(columns))]))
