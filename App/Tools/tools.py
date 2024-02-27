import tkinter as tk
from tkinter import ttk

class Tools:
    class Root:
        @staticmethod
        def create_root():
            root = tk.Tk()
            return root

        @staticmethod
        def set_root(root, title="", geometry="800x800"):
            root.title(title)
            root.geometry(geometry)
    class Entry:
        @staticmethod
        def clear_entry(entry):
            entry.delete(0, tk.END)

        @staticmethod
        def set_entry(entry, text):
            entry.insert(tk.END, text)

        @staticmethod
        def get_text(event):
            if isinstance(event, str):
                text = event
            else:
                text = event.widget.cget("text")
            return text
    class Create:
        @staticmethod
        def create_entry(root, row=0, column=0, padx=10, pady=10, columnspan=1, sticky="ew"):
            entry_input = tk.Entry(root, font="Helvetica 24", justify="right")
            entry_input.grid(row=row, column=column,
                             padx=padx, pady=pady, columnspan=columnspan, sticky=sticky)
            return entry_input

        @staticmethod
        def create_combo(root, values, current=0, row=0, column=0, padx=10, pady=10):
            combo_input = ttk.Combobox(root, values=values, state="readonly")
            combo_input.current(current)
            combo_input.grid(row=row, column=column, padx=padx, pady=pady)
            combo_input['font'] = ('Helvetica', 15)
            return combo_input

        @staticmethod
        def create_button(root, command, text="", width=0, row=0, column=0, padx=10, pady=10):
            button = tk.Button(root, text=text, font="Helvetica 18", width=width, height=1, command=command)
            button.grid(row=row, column=column, padx=padx, pady=pady, columnspan=1, sticky="w")
            return button