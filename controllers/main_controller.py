import pymongo.errors
from database.db_service import DBService
from collections import defaultdict
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from database.db_service import DBService
from utils import avg_price_history, pics_rating, product_sizes, rating_price
from utils import brand_ratings_1, brand_ratings_2, brand_discounts, custom_prices_history
import json
import threading

class MainController:
    def __init__(
        self,
        num_products_label, 
        selected_list_label,
        selected_data,
        error_label,
        left_frame
        ):
        
        self.db_service = DBService()
        
        # Dynamic elements
        self.num_products_label = num_products_label
        self.selected_list_label = selected_list_label
        self.selected_data = selected_data
        self.error_label = error_label
        self.left_frame = left_frame
        
        self.selected_entities = []
        self.num_selected_data = 0
        self.entity_to_canvas = {}
        self.entities_dict = defaultdict(list)
        self.num_products = 0

    def on_mouse_wheel(self, canvas, event):
        canvas.yview_scroll(-1 * int(event.delta / 120), "units")
    
    def toggle_select_all(self):
        if len(self.entities_dict) != 0:
            self.error_label.config(text=f"")
            if len(self.selected_entities) == len(self.entities_dict):  # If all are selected, deselect all
                self.selected_entities.clear()
                self.num_selected_data = 0
                # Clear all circles
                for circle_canvas in self.entity_to_canvas.values():
                    circle_canvas.delete("indicator")
            else:  # Otherwise, select all
                for entity, number in sorted(self.entities_dict.items(), key=lambda item: item[1], reverse=True):
                    if entity not in self.selected_entities:
                        self.selected_entities.append(entity)
                        self.num_selected_data += number
                        # Find the corresponding circle canvas and draw the circle
                        circle_canvas = self.entity_to_canvas[entity]
                        circle_canvas.create_oval(5, 5, 25, 25, fill="lightblue", tags="indicator")
            
            self.update_selected_list()
        else:
            self.error_label.config(text=f"Невозможно выбрать: данные не извлечены из БД")
    
    def update_selected_list(self):
        self.selected_list_label.config(text=f"Число выбранных категорий: {len(self.selected_entities)}")
        self.selected_data.config(text=f"Число выбранных данных: {self.num_selected_data}")
    
    def display_entities(self):
        # Clear the previous data from the canvas
        for widget in self.left_frame.winfo_children():
            widget.destroy()
        self.get_categories_from_db()
        
        # Canvas
        self.canvas = tk.Canvas(self.left_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create another frame inside the canvas to hold the labels
        self.scrollable_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Add a vertical scrollbar to the canvas
        self.scrollbar = ttk.Scrollbar(self.canvas, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the canvas to work with the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.canvas.bind_all("<MouseWheel>", lambda e: self.on_mouse_wheel(self.canvas, e))  # Windows and MacOS
        self.canvas.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))  # Linux (scroll up)
        self.canvas.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))   # Linux (scroll down)
        
        for entity, number in sorted(self.entities_dict.items(), key=lambda item: item[1], reverse=True):
            row_frame = tk.Frame(self.scrollable_frame)
            row_frame.pack(fill=tk.X, pady=5)
            
            label = f"{entity}: {number}"
            row_label = tk.Label(row_frame, text=label, anchor="w", font=("Arial", 12))
            row_label.pack(side=tk.LEFT, fill=tk.X, pady=5, padx=40)
            
            # Add a canvas for the circle indicator
            circle_canvas = tk.Canvas(row_frame, width=30, height=30, highlightthickness=0)
            circle_canvas.pack(side=tk.RIGHT, padx=5)
            
            # Store the canvas in the dictionary for later reference
            self.entity_to_canvas[entity] = circle_canvas

            # Bind click event to the row_frame
            row_frame.bind("<Button-1>", lambda e, entity=entity, canvas=circle_canvas: self.toggle_entity(entity, canvas))
            row_label.bind("<Button-1>", lambda e, entity=entity, canvas=circle_canvas: self.toggle_entity(entity, canvas))
            circle_canvas.bind("<Button-1>", lambda e, entity=entity, canvas=circle_canvas: self.toggle_entity(entity, canvas))
            
            # Bind hover events to the row_frame and its components
            row_frame.bind("<Enter>", lambda e, f=row_frame, l=row_label, c=circle_canvas: self.on_enter(e, f, l, c))
            row_label.bind("<Enter>", lambda e, f=row_frame, l=row_label, c=circle_canvas: self.on_enter(e, f, l, c))
            circle_canvas.bind("<Enter>", lambda e, f=row_frame, l=row_label, c=circle_canvas: self.on_enter(e, f, l, c))
            row_frame.bind("<Leave>", lambda e, f=row_frame, l=row_label, c=circle_canvas: self.on_leave(e, f, l, c))
            row_label.bind("<Leave>", lambda e, f=row_frame, l=row_label, c=circle_canvas: self.on_leave(e, f, l, c))
            circle_canvas.bind("<Leave>", lambda e, f=row_frame, l=row_label, c=circle_canvas: self.on_leave(e, f, l, c))
            
            # Add a thinner border line (using canvas)
            border_line = tk.Canvas(self.scrollable_frame, height=1, width=500, bg="gray", bd=0, highlightthickness=0)
            border_line.pack(fill=tk.X)
    
    def get_categories_from_db(self):
        if self.db_service.is_connected():
            self.error_label.config(text=f"")
            products = self.db_service.get_all_data()
        else:
            self.error_label.config(text=f"Ошибка: не удалось извлечь данные из БД")
            return
        self.entities_dict.clear()
        self.num_selected_data = 0
        self.selected_entities.clear()
        self.num_products = 0
        self.update_selected_list()
        for product in products:
            self.num_products += 1
            if "entity" in product:
                entity = product["entity"]
                if (self.entities_dict.__contains__(entity)):
                    current_num = self.entities_dict[entity]
                    self.entities_dict[entity] = (current_num + 1)
                else:
                    self.entities_dict[entity] = 1
        
        self.num_products_label.config(text=f"Число данных в БД: {self.num_products}")
        
    def toggle_entity(self, entity, circle_canvas):
        if entity in self.selected_entities:
            self.selected_entities.remove(entity)
            self.num_selected_data -= self.entities_dict[entity]
            circle_canvas.delete("indicator")  # Remove the circle
        else:
            self.selected_entities.append(entity)
            self.num_selected_data += self.entities_dict[entity]
            # Draw a filled circle on the canvas
            circle_canvas.create_oval(5, 5, 25, 25, fill="lightblue", tags="indicator")
        self.update_selected_list()
    
    def on_enter(self, event, row_frame, row_label, circle_canvas):
        row_frame.config(bg="lightgray")
        row_label.config(bg="lightgray")
        circle_canvas.config(bg="lightgray")

    def on_leave(self, event, row_frame, row_label, circle_canvas):
        row_frame.config(bg="#F0F0F0")
        row_label.config(bg="#F0F0F0")
        circle_canvas.config(bg="#F0F0F0")
        
    def handle_graph_button(self, default_option):
        products = self.db_service.get_by_entities(self.selected_entities)
        
        selected_option = default_option.get()
        if len(self.selected_entities) != 0:
            self.error_label.config(text=f"")
            if selected_option == "История цены":
                avg_price_history.build_graph(products)
            elif selected_option == "Рейтинг от числа картинок":
                pics_rating.build_graph(products)
            elif selected_option == "Размеры одежды":
                product_sizes.build_graph(products)
            elif selected_option == "Зависимость между рейтингом и стоимостью":
                rating_price.build_graph(products)
            elif selected_option == "Рейтинг брендов 1":
                brand_ratings_1.build_graph(products)
            elif selected_option == "Рейтинг брендов 2":
                brand_ratings_2.build_graph(products)
            elif selected_option == "Скидки брендов":
                brand_discounts.build_graph(products)
            elif selected_option == "История цены (37 категорий)":
                custom_prices_history.build_graph()
            else:
                self.error_label.config(text=f"Этот вариант недопустим для построения графика.")
        else:
            self.error_label.config(text=f"Необходимо выбрать хотя бы одну категорию.")

    def export_data(self):
        # Start the export thread
        thread_export = threading.Thread(target=self.export_thread, daemon=True)
        thread_export.start()

    def export_thread(self):
        # File selection dialog
        file_path = filedialog.askdirectory(title="Выберите папку для сохранения")
        self.error_label.config(text=f"")  # Clear any previous messages

        if file_path:  # If a directory is selected
            print(f"Selected directory: {file_path}")
            if self.db_service.is_connected():
                documents = list(self.db_service.get_all_data())

                # Remove the MongoDB "_id" field if needed (optional)
                for doc in documents:
                    doc.pop("_id", None)

                # Export to a JSON file
                try:
                    with open(f"{file_path}/exported_data.json", "w", encoding="utf-8") as file:
                        json.dump(documents, file, indent=4, ensure_ascii=False)
                    self.error_label.after(0, lambda: self.error_label.config(text="Данные успешно экспортированы"))
                except Exception as e:
                    self.error_label.after(0, lambda: self.error_label.config(text=f"Ошибка экспорта: {e}"))
            else:
                self.error_label.after(0, lambda: self.error_label.config(text="Ошибка: не удалось подключиться к БД"))
        else:
            self.error_label.after(0, lambda: self.error_label.config(text="Директория не выбрана"))
    
    def import_data(self):
        file_path = filedialog.askopenfilename(title="Выберите файл")
        self.error_label.config(text=f"")
        
        self.elapsed_time = 0
        self.cur_import_num = 0
        self.total_import_num = 0
        # Start the export thread
        thread_import = threading.Thread(target=lambda: self.import_thread(file_path), daemon=True)
        self.thread_import_running = True
        thread_import.start()
        self.update_timer()
    
    def import_thread(self, file_path):
        if file_path:
            print(f"Selected file: {file_path}")
            if self.db_service.is_connected():
                with open(file_path, "r", encoding="utf-8") as file:
                    documents = json.load(file)
                
                # Insert the documents into the collection
                if isinstance(documents, list):
                    try:
                        result = self.db_service.insert_many(documents)
                        #result = self.collection.insert_many(documents, ordered=False)
                    except pymongo.errors.BulkWriteError as bwe:
                        pass
                    
                    self.error_label.after(0, lambda: self.stop_timer(text=f"Выполняется импорт, время: {self.elapsed_time} сек"))        
            else:
                self.error_label.after(0, lambda: self.stop_timer(text=f"Ошибка: не удалось подключиться к БД"))
        else:
            self.error_label.after(0, lambda: self.stop_timer(text=f"Файл не выбран."))
    
    def update_timer(self):
        if self.thread_import_running:
            self.error_label.config(text=f"Выполняется импорт, время: {self.elapsed_time} сек")
            self.elapsed_time += 1
            self.error_label.after(1000, self.update_timer)
    
    def stop_timer(self, text):
        self.thread_import_running = False
        self.error_label.config(text=text)