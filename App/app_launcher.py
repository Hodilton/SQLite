import tkinter as tk
from tkinter import ttk

class WidgetParams:
    def __init__(self, row=0, column=0, padx=10, pady=10, width=0, height=1, columnspan=1, sticky="w", font="Helvetica 18"):
        self.row = row
        self.column = column
        self.padx = padx
        self.pady = pady
        self.width = width
        self.height = height
        self.columnspan = columnspan
        self.sticky = sticky
        self.font = font

class App:
    def __init__(self):
        self.root = Tools.create_root()
        MainApplication(self.root).create_widgets()

    def run(self):
        self.root.mainloop()

class MainApplication:
    def __init__(self, master):
        self.root = master
        Tools.set_root(self.root, "MyApplication", "650x500+500+80")
        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)

        self.calculator_tab = FrameWithCalculator(self.notebook)
        self.converter_tab = FrameWithConverter(self.notebook, self.calculator_tab)

        self.notebook.add(self.calculator_tab, text="Calculator")
        self.notebook.add(self.converter_tab, text="Converter")

        self.notebook.pack(expand=1, fill="both")

class FrameWithCalculator(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.calculator_app = CalculatorApp(self)

        self.frameparams = self._initialize_widget_params()

    def _initialize_widget_params(self):
        entry_1 = WidgetParams(row=1, column=2, padx=5, pady=5, width=20)
        button_1 = WidgetParams(row=2, column=2, padx=5, pady=5, width=10)

        return entry_1, button_1

    def get_widget_params(self):
        return self.frameparams

class FrameWithConverter(tk.Frame):
    def __init__(self, master, calculator_frame):
        super().__init__(master)
        self.converter_app = NumberConverterApp(self, calculator_frame)

        self.frameparams = self._initialize_widget_params()

    def _initialize_widget_params(self):
        entry_1 = WidgetParams(row=1, column=2, padx=5, pady=5, width=20)
        button_1 = WidgetParams(row=2, column=2, padx=5, pady=5, width=10)

        return entry_1, button_1

    def get_widget_params(self):
        return self.frameparams

class NumberConverterApp:
    def __init__(self, master, calculator_frame):
        self.master = master
        self.create_widgets()

        self.calculator_frame = calculator_frame

    def create_widgets(self):
        frame_params = self.master.get_widget_params()

class CalculatorApp:
    def __init__(self, master):
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        frame_params = self.master.get_widget_params()