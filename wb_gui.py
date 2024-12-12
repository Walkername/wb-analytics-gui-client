import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import avg_price_history
import pics_rating
import price_rating
import db_service
from collections import defaultdict

def on_closing():
    root.quit()
    root.destroy()

def handle_graph_button(entities):
    selected_option = default_option.get()
    if selected_option == "Average Price History":
        avg_price_history.build_graph(entities)
    elif selected_option == "Pics & Rating":
        pics_rating.build_graph(entities)
    elif selected_option == "Prices & Rating":
        price_rating.build_graph(entities)
    else:
        print("Please select a valid option.")

# Function to toggle entity selection
def toggle_entity(entity, circle_canvas):
    if entity in selected_entities:
        selected_entities.remove(entity)
        circle_canvas.delete("indicator")  # Remove the circle
    else:
        selected_entities.append(entity)
        # Draw a filled circle on the canvas
        circle_canvas.create_oval(5, 5, 25, 25, fill="lightblue", tags="indicator")
    update_selected_list()

# Function to update the display of selected entities
def update_selected_list():
    selected_list_label.config(text=f"Число выбранных категорий: {len(selected_entities)}")

def on_mouse_wheel(canvas, event):
    canvas.yview_scroll(-1 * int(event.delta / 120), "units")

# Function to handle mouse hover
def on_enter(event, frame, label, canvas):
    frame.config(bg="lightgray")
    label.config(bg="lightgray")
    canvas.config(bg="lightgray")

def on_leave(event, frame, label, canvas):
    frame.config(bg="#F0F0F0")
    label.config(bg="#F0F0F0")
    canvas.config(bg="#F0F0F0")

# Function to select or deselect all entities
def toggle_select_all(button):
    if len(selected_entities) == len(entities_dict):  # If all are selected, deselect all
        selected_entities.clear()
        # Clear all circles
        for circle_canvas in entity_to_canvas.values():
            circle_canvas.delete("indicator")
    else:  # Otherwise, select all
        for entity, number in sorted(entities_dict.items(), key=lambda item: item[1], reverse=True):
            if entity not in selected_entities:
                selected_entities.append(entity)
                # Find the corresponding circle canvas and draw the circle
                circle_canvas = entity_to_canvas[entity]
                circle_canvas.create_oval(5, 5, 25, 25, fill="lightblue", tags="indicator")
    
    update_selected_list()

def display_entities():
    # Clear the previous graph from the canvas
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Create a canvas
    canvas = tk.Canvas(frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add a vertical scrollbar to the canvas
    scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the canvas to work with the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Bind the mouse wheel to the canvas for scrolling
    canvas.bind_all("<MouseWheel>", lambda e: on_mouse_wheel(canvas, e))  # Windows and MacOS
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux (scroll up)
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Linux (scroll down)

    # Create another frame inside the canvas to hold the labels
    scrollable_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Define font properties: family, size, and style
    font_properties = ("Arial", 12)  # Set the font size to 16 and the font family to Arial

    right_frame = tk.Frame(frame)
    right_frame.pack(side=tk.RIGHT)

    # Create "Select All" button
    select_all_button = tk.Button(right_frame, text="Выбрать/Отменить все", command=lambda: toggle_select_all(select_all_button))
    select_all_button.pack(pady=10, padx=40)

    for entity, number in sorted(entities_dict.items(), key=lambda item: item[1], reverse=True):
        row_frame = tk.Frame(scrollable_frame)
        row_frame.pack(fill=tk.X, pady=5)
        
        label = f"{entity}: {number}"
        row_label = tk.Label(row_frame, text=label, anchor="w", font=font_properties)
        row_label.pack(side=tk.LEFT, fill=tk.X, pady=5, padx=40)
        
        # Add a canvas for the circle indicator
        circle_canvas = tk.Canvas(row_frame, width=30, height=30, highlightthickness=0)
        circle_canvas.pack(side=tk.RIGHT, padx=5)
        
        # Store the canvas in the dictionary for later reference
        entity_to_canvas[entity] = circle_canvas

        # Bind click event to the row_frame
        row_frame.bind("<Button-1>", lambda e, entity=entity, canvas=circle_canvas: toggle_entity(entity, canvas))
        row_label.bind("<Button-1>", lambda e, entity=entity, canvas=circle_canvas: toggle_entity(entity, canvas))
        circle_canvas.bind("<Button-1>", lambda e, entity=entity, canvas=circle_canvas: toggle_entity(entity, canvas))
        
        # Bind hover events to the row_frame and its components
        row_frame.bind("<Enter>", lambda e, f=row_frame, l=row_label, c=circle_canvas: on_enter(e, f, l, c))
        row_label.bind("<Enter>", lambda e, f=row_frame, l=row_label, c=circle_canvas: on_enter(e, f, l, c))
        circle_canvas.bind("<Enter>", lambda e, f=row_frame, l=row_label, c=circle_canvas: on_enter(e, f, l, c))
        row_frame.bind("<Leave>", lambda e, f=row_frame, l=row_label, c=circle_canvas: on_leave(e, f, l, c))
        row_label.bind("<Leave>", lambda e, f=row_frame, l=row_label, c=circle_canvas: on_leave(e, f, l, c))
        circle_canvas.bind("<Leave>", lambda e, f=row_frame, l=row_label, c=circle_canvas: on_leave(e, f, l, c))
        
        # Add a thinner border line (using canvas)
        border_line = tk.Canvas(scrollable_frame, height=1, width=500, bg="gray", bd=0, highlightthickness=0)
        border_line.pack(fill=tk.X)

def get_categories_from_db():
    url = "mongodb://localhost:27017/"
    db = "wb-products"
    col_name = "products"
    products = db_service.get_all_data(url, db, col_name)
    global num_products
    for product in products:
        num_products += 1
        if "entity" in product:
            entity = product["entity"]
            if (entities_dict.__contains__(entity)):
                current_num = entities_dict[entity]
                entities_dict[entity] = (current_num + 1)
            else:
                entities_dict[entity] = 1
    
    num_products_label.config(text=f"Число данных в БД: {num_products}")
    display_entities()

if __name__ == '__main__':
    # Set up the main window
    root = tk.Tk()
    root.title("Wildberries Analytics GUI")
    root.geometry("800x500")
    #root.resizable(width=False, height=False)
    
    # Bind the window close event to the on_closing function
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    top_frame = tk.Frame(root)
    top_frame.pack(fill=tk.X)
    
    OPTIONS = [
        "Average Price History",
        "Pics & Rating",
        "Prices & Rating"
    ]
    
    default_option = tk.StringVar()
    default_option.set(OPTIONS[0])
    
    # Create a style object
    style = ttk.Style()
    style.theme_use("clam")  # Modern theme
    style.configure(
        "TCombobox",
        background="lightblue",
        foreground="black",
        fieldbackground="white",
        arrowcolor="black",  # Color of the dropdown arrow
        padding=5
    )
    
    combobox = ttk.Combobox(
        top_frame, 
        textvariable=default_option, 
        values=OPTIONS,
        state="readonly",
        style="TCombobox"
    )
    combobox.grid(row=0, column=0, pady=10, padx=10)

    # Categories from DB
    num_products = 0
    entities_dict = defaultdict(int)

    num_products_label = tk.Label(top_frame, text=f"Число данных в БД: {num_products}", font=("Arial", 12))
    num_products_label.grid(row=1, column=1)
    
    selected_entities = []
    # Create a dictionary to map entities to their circle canvases
    entity_to_canvas = {}
    
    show_graph_button = tk.Button(top_frame, text="Построить график", command=lambda: handle_graph_button(selected_entities))
    show_graph_button.grid(row=1, column=0)

    # Get Data Button
    get_data_button = tk.Button(top_frame, text="Получить категории", command=get_categories_from_db)
    get_data_button.grid(row=0, column=1)

    # Create and display selected entities label
    selected_list_label = tk.Label(top_frame, text="Число выбранных категорий: ", font=("Arial", 12))
    selected_list_label.grid(row=2, column=1, pady=10)

    # Create a frame to hold the graph
    frame = tk.Frame(root, bd=2, relief="solid", highlightbackground="blue", highlightcolor="red")
    frame.place(relx=0.15, rely=0.15, relwidth=0.7, relheight=0.7)
    frame.pack(pady=20, expand=True, fill=tk.X)
    
    update_selected_list()
    
    root.mainloop()