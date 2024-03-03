import tkinter as tk

from managers.database_manager import DatabaseManager
from .price_history_gui import PriceHistoryGUI


class MainApp:
    def __init__(self):
        try:
            self.root = tk.Tk()
            self.db_manager = DatabaseManager("data/data3.db")
            self.price_history_gui = PriceHistoryGUI(self.root, self.db_manager)
            self.root.mainloop()
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.db_manager.close_connection()

if __name__ == "__main__":
    main_app = MainApp()