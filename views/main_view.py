import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from controllers.main_controller import MainController


class MainWindow:
    def __init__(self, root):
        self.root = root

        # Setup the main frame
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(fill=tk.X, pady=5)
        
        self.error_frame = tk.Frame(self.root)
        self.error_frame.pack(fill=tk.X)
        
        self.main_frame = tk.Frame(self.root, bd=2, relief="solid", highlightbackground="blue", highlightcolor="red")
        self.main_frame.place(relx=0.15, rely=0.15, relwidth=0.7, relheight=0.7)
        self.main_frame.pack(pady=5, expand=True, fill=tk.BOTH)
        
        self.left_frame = tk.Frame(self.main_frame, bd=2, relief="solid", highlightbackground="blue", highlightcolor="red")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=40)

        self.right_frame = tk.Frame(self.main_frame, bd=2, relief="solid", highlightbackground="blue", highlightcolor="red")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, pady=40, padx=10)

        # Add widgets to the main frame
        self.create_widgets()

    def create_widgets(self):
        """Create and layout widgets."""
        # Task List
        self.create_task_list()
        
        # Build graph button
        self.show_graph_button = ttk.Button(self.top_frame, text="Построить график", command=lambda: self.controller.handle_graph_button(self.default_task))
        self.show_graph_button.grid(row=1, column=0)
        
        # Get Data Button
        self.get_data_button = ttk.Button(self.top_frame, text="Получить категории")
        self.get_data_button.grid(row=0, column=1)
        
        # Num of data from DB Label
        self.num_products_label = ttk.Label(self.top_frame, text=f"Число данных в БД: 0", font=("Arial", 12))
        self.num_products_label.grid(row=1, column=1, padx=20)
        
        # Export data from DB
        self.export_data_button = ttk.Button(self.top_frame, text="Экспорт")
        self.export_data_button.grid(row=0, column=2, padx=20)
        
        # Import data to DB
        self.import_data_button = ttk.Button(self.top_frame, text="Импорт")
        self.import_data_button.grid(row=0, column=3, padx=20)
        
        # Error Label
        self.error_label = ttk.Label(self.error_frame, font=("Arial", 12), foreground="red")
        self.error_label.pack(padx=30, pady=10)
        
        # Create "Select All" button
        self.select_all_button = ttk.Button(self.right_frame, text="Выбрать/Отменить все")
        self.select_all_button.pack(pady=10, padx=40)
       
       # Selected categories Label
        self.selected_list_label = ttk.Label(self.right_frame, text="Число выбранных категорий: 0", font=("Arial", 12))
        self.selected_list_label.pack(pady=10)
        
        # Num of selected data
        self.selected_data = ttk.Label(self.right_frame, text="Число выбранных данных: 0", font=("Arial", 12))
        self.selected_data.pack()
       
        self.controller = MainController(
            self.num_products_label, 
            self.selected_list_label,
            self.selected_data,
            self.error_label,
            self.left_frame
            )
        
        self.get_data_button.config(command=self.controller.display_entities)
        
        self.select_all_button.config(command=self.controller.toggle_select_all)
        
        self.export_data_button.config(command=self.controller.export_data)
        
        self.import_data_button.config(command=self.controller.import_data)

    def create_task_list(self):
        OPTIONS = [
            "История цены",
            "Рейтинг от числа картинок",
            "Размеры одежды",
            "Рейтинг и стоимость",
            "Рейтинг брендов 1",
            "Рейтинг брендов 2",
            "Скидки брендов",
            "История цены (37 категорий)"
        ]
        self.default_task = tk.StringVar()
        self.default_task.set(OPTIONS[0])
        # Create a style object
        style = ttk.Style()
        #style.theme_use("clam")  # Modern theme
        style.configure(
            "TCombobox",
            background="lightblue",
            foreground="black",
            fieldbackground="white",
            arrowcolor="black",  # Color of the dropdown arrow
            padding=5
        )
        self.task_list = ttk.Combobox(
            self.top_frame,
            textvariable=self.default_task, 
            values=OPTIONS,
            state="readonly",
            style="TCombobox",
            width=25
        )
        self.task_list.grid(row=0, column=0, pady=10, padx=20)
