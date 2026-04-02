
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
from PIL import Image, ImageTk

class NotebookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Your Notebook")
        self.root.geometry("900x600")
        
        # TABLESS STYLE
        self.style = ttk.Style()
        self.style.layout("Tabless.TNotebook.Tab", [])
        
        try:
            self.df = pd.read_csv('calendar_data.csv')
        except FileNotFoundError:
            print("CSV not found. Ensure 'calendar_data.csv' is in the folder.")
            self.df = pd.DataFrame()

        self.day_map = {'Sunday': 0, 'Monday': 1, 'Tuesday': 2, 'Wednesday': 3,
                        'Thursday': 4, 'Friday': 5, 'Saturday': 6}
        self.open_tabs = {} # Track open day-tabs

        self.setup_main_nav()

    def setup_main_nav(self):
        # root content
        nav_frame = tk.Frame(self.root)
        nav_frame.pack(side=tk.TOP, fill=tk.X)

        tk.Button(nav_frame, text='Home', command=lambda: self.main_nb.select(self.tab1)).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(nav_frame, text='Calendar', command=lambda: self.main_nb.select(self.tab2)).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(nav_frame, text='Quit', command=self.root.destroy).pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)

        self.main_nb = ttk.Notebook(self.root, style="Tabless.TNotebook")
        self.main_nb.pack(expand=True, fill="both")

        self.tab1 = ttk.Frame(self.main_nb)
        self.tab2 = ttk.Frame(self.main_nb)
        self.main_nb.add(self.tab1)
        self.main_nb.add(self.tab2)

        self.setup_home_tab()
        self.setup_calendar_tab()

    def setup_home_tab(self):
        ttk.Label(self.tab1, text="Notebook Home", font=("Arial", 18)).pack(pady=20)
        
        upload_btn = tk.Button(self.tab1, text="Add Image", command=lambda: self.add_image(self.tab1))
        upload_btn.pack(side=tk.LEFT, anchor=tk.NW, pady=20)
        addtextbtn = tk.Button(self.tab1, text="Add Text", command=lambda: self.add_text(self.tab1))
        addtextbtn.pack(side=tk.LEFT,anchor=tk.NW , pady=20)
        
        
        
    def setup_calendar_tab(self):

        self.cal_nb = ttk.Notebook(self.tab2, style="Tabless.TNotebook") 
        self.cal_nb.pack(expand=True, fill='both', padx=10, pady=10)
    
        tk.Button(self.tab2, text='January', command=lambda: self.cal_nb.select(0)).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.tab2, text='February', command=lambda: self.cal_nb.select(1)).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.tab2, text='March', command=lambda: self.cal_nb.select(2)).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.tab2, text='April', command=lambda: self.cal_nb.select(3)).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.tab2, text='May', command=lambda: self.cal_nb.select(4)).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.tab2, text='June', command=lambda: self.cal_nb.select(5)).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.tab2, text='July', command=lambda: self.cal_nb.select(6)).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.tab2, text='August', command=lambda: self.cal_nb.select(7)).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.tab2, text='September', command=lambda: self.cal_nb.select(8)).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.tab2, text='October', command=lambda: self.cal_nb.select(9)).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.tab2, text='November', command=lambda: self.cal_nb.select(10)).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.tab2, text='December', command=lambda: self.cal_nb.select(11)).pack(side=tk.LEFT, padx=5, pady=5)

        # month tabs
        for month_name in self.df['Month'].unique():
            month_frame = ttk.Frame(self.cal_nb)
            self.cal_nb.add(month_frame, text=month_name)

            # weekdays
            for i, day in enumerate(self.day_map.keys()):
                tk.Label(month_frame, text=day[:3], font=('Arial', 9, 'bold')).grid(row=0, column=i, pady=5)

            month_days = self.df[self.df['Month'] == month_name]
            row_idx = 1
            for _, data in month_days.iterrows():
                col_idx = self.day_map[data['Day of Week']]
                day_num = data['Date'].split('-')[-1]
                
                btn = tk.Button(month_frame, text=day_num, width=6, height=3,
                                command=lambda d=data: self.open_day_tab(d))
                btn.grid(row=row_idx, column=col_idx, padx=1, pady=1)
                if col_idx == 6: row_idx += 1

    def open_day_tab(self, data):
        date_str = data['Date']
        if date_str in self.open_tabs:
            self.cal_nb.select(self.open_tabs[date_str])
            return

        day_frame = ttk.Frame(self.cal_nb)
        tab_label = f"{date_str}"
        self.cal_nb.add(day_frame, text=tab_label)
        self.open_tabs[date_str] = day_frame
        
        # day content
        tk.Label(day_frame, text=f"Notes for {date_str}", font=("Arial", 14)).pack(pady=10)
        txt = tk.Text(day_frame, height=15)
        txt.pack(expand=True, fill="both", padx=10, pady=5)
        
        upload_btn = tk.Button(day_frame, text="Add Image", command=lambda: self.add_image(day_frame))
        upload_btn.pack(pady=20)

        
        tk.Button(day_frame, text="Delete Tab", 
                  command=lambda: self.close_day_tab(date_str, day_frame)).pack(pady=5)
        
        self.cal_nb.select(day_frame)

    def close_day_tab(self, date_str, frame):
        self.cal_nb.forget(frame)
        del self.open_tabs[date_str]

    def make_draggable(self, widget):
        def on_drag_start(event):
            widget._drag_start_x = event.x
            widget._drag_start_y = event.y
        def on_drag_motion(event):
            new_x = widget.winfo_x() - widget._drag_start_x + event.x
            new_y = widget.winfo_y() - widget._drag_start_y + event.y
            widget.place(x=new_x, y=new_y)
        widget.bind("<Button-1>", on_drag_start)
        widget.bind("<B1-Motion>", on_drag_motion)
    
    def add_image(self, tab, event=None):
        file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
    )

        image_label = tk.Label(tab, text="No image", bg="lightgrey")
        image_label.pack(expand=True, fill="both", padx=20, pady=20)

        
        if file_path:
            original_img = Image.open(file_path)
            
            # Optional: Resize to fit the widget (e.g., 300x300)
            resized_img = original_img.resize((300, 300), Image.Resampling.LANCZOS)
            tk_img = ImageTk.PhotoImage(resized_img)
            image_label.config(image=tk_img)
            image_label.image = tk_img
            self.make_draggable(image_label)
            
    def add_text(self, tab):
        text_widget = tk.Text(tab, height=5, width=20)
        text_widget.pack(expand=True, fill="both", padx=20, pady=20)
        self.make_draggable(text_widget)

if __name__ == "__main__":
    root = tk.Tk()
    app = NotebookApp(root)
    root.mainloop()