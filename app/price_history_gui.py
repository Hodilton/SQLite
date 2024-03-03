import tkinter as tk
import matplotlib.pyplot as plt

from tkinter import ttk
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import DateFormatter


class PriceHistoryGUI:
    def __init__(self, master, database_manager):
        self.canvas_widget = None
        self.canvas = None
        self.ax = None
        self.fig = None
        self.plot_button = None
        self.to_date_entry = None
        self.to_date_label = None
        self.from_date_entry = None
        self.from_date_label = None
        self.shop_listbox = None
        self.shop_label = None
        self.product_combobox = None
        self.product_label = None

        self.master = master
        self.master.title("Price History App")
        self.database_manager = database_manager

        self.create_widgets()
        self.setup_plot()

    def create_widgets(self):
        self.product_label = ttk.Label(self.master, text="Select Product:")
        self.product_combobox = ttk.Combobox(self.master, values=self.database_manager.get_product_names())
        self.product_combobox.bind("<<ComboboxSelected>>", self.update_price_history)

        self.shop_label = ttk.Label(self.master, text="Select Shop(s):")
        self.shop_listbox = tk.Listbox(self.master, selectmode=tk.MULTIPLE, exportselection=0)
        for shop in self.database_manager.get_shop_names():
            self.shop_listbox.insert(tk.END, shop)

        self.from_date_label = ttk.Label(self.master, text="From Date:")
        self.from_date_entry = ttk.Entry(self.master)
        self.from_date_entry.insert(0, "YYYY-MM-DD")

        self.to_date_label = ttk.Label(self.master, text="To Date:")
        self.to_date_entry = ttk.Entry(self.master)
        self.to_date_entry.insert(0, "YYYY-MM-DD")

        self.plot_button = ttk.Button(self.master, text="Plot Graph", command=self.update_price_history)

        self.product_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.product_combobox.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

        self.shop_label.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        self.shop_listbox.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

        self.from_date_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.from_date_entry.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

        self.to_date_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.to_date_entry.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)

        self.plot_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.fig, self.ax = plt.subplots(figsize=(15, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def setup_plot(self):
        self.ax.set_xlabel("Date")
        self.ax.set_ylabel("Price")
        self.ax.legend()
        self.canvas.draw()

    def update_price_history(self):
        selected_product = self.product_combobox.get()
        selected_shops = [self.shop_listbox.get(idx) for idx in self.shop_listbox.curselection()]
        from_date_str = self.from_date_entry.get()
        to_date_str = self.to_date_entry.get()

        try:
            from_date = datetime.strptime(from_date_str, "%Y-%m-%d")
            to_date = datetime.strptime(to_date_str, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

        price_data = self.database_manager.get_price_data(selected_product, selected_shops, from_date, to_date)

        # Clear previous plot
        self.ax.clear()

        # Plot price history
        for shop, records in price_data.items():
            dates, prices = zip(*[(datetime.strptime(record[0], "%Y-%m-%d"), record[1]) for record in records])
            self.ax.plot(dates, prices, label=shop)

        # Format x-axis as dates
        date_format = DateFormatter("%Y-%m-%d")
        self.ax.xaxis.set_major_formatter(date_format)
        self.fig.autofmt_xdate()

        # Set labels and legend
        self.ax.set_xlabel("Date")
        self.ax.set_ylabel("Price")
        self.ax.legend()

        current_prices = self.database_manager.get_current_prices(selected_product, selected_shops)

        # # Clear the current prices label
        # for widget in self.master.winfo_children():
        #     if isinstance(widget, ttk.Label) and widget.cget("text") == "Current Prices:":
        #         widget.destroy()
        #
        # # Display current prices
        # current_prices_label = ttk.Label(self.master, text="Current Prices:")
        # current_prices_label.grid(row=0, column=3, padx=10, pady=5, sticky=tk.W)
        #
        # for i, (shop, price) in enumerate(current_prices.items(), start=1):
        #     current_prices_display = ttk.Label(self.master, text=f"{shop}: {price}")
        #     current_prices_display.grid(row=0 + i, column=3, padx=10, pady=5, sticky=tk.W)

        for shop, price in current_prices.items():
            self.ax.axhline(y=price, color='r', linestyle='--', label=f"{shop} Current Price - {price}")
            self.ax.annotate(f"Current Price: {price}", xy=(0, price), xytext=(10, 0), textcoords='offset points',
                             color='r')

        self.canvas.draw()
