
import sys
import tkinter as tk
from tkinter import ttk
import pandas as pd

class NotebookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Your Notebook")
        self.root.geometry("600x500")
        
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
        # Top Buttons (Persistent across all tabs)
        nav_frame = tk.Frame(self.root)
        nav_frame.pack(side=tk.TOP, fill=tk.X)

        tk.Button(nav_frame, text='Home', command=lambda: self.main_nb.select(self.tab1)).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(nav_frame, text='Calendar', command=lambda: self.main_nb.select(self.tab2)).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(nav_frame, text='Quit', command=self.root.destroy).pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)

        # MAIN Tabless Notebook
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
        
        # Draggable Entry Example
        drag_entry = tk.Entry(self.tab1, bd=2)
        drag_entry.insert(0, "Drag me!")
        drag_entry.place(x=50, y=100)
        self.make_draggable(drag_entry)
        
    def go_to_january(self):
    # 1. First, make sure the main notebook is showing the Calendar tab (tab2)
        self.main_nb.select(self.tab2)
    
    # 2. Then, tell the month notebook to select the first tab (Index 0)
        self.month_nb.select(0)

    def setup_calendar_tab(self):
        # Inside Tab 2, we create ANOTHER notebook for Months and Days
        self.cal_nb = ttk.Notebook(self.tab2)
        self.cal_nb.pack(expand=True, fill='both', padx=10, pady=10)

        # tk.Button(self.tab2, text='January', command=lambda: self.main_nb.select(self.month_nb.select(0))).pack(side=tk.LEFT, padx=5, pady=5)
        # jan_btn = tk.Button(self.tab2, text="Jump to January", command=lambda: self.go_to_january())
        # jan_btn.pack(side=tk.LEFT, padx=5)

        # Build the Month Grids
        for month_name in self.df['Month'].unique():
            month_frame = ttk.Frame(self.cal_nb)
            self.cal_nb.add(month_frame, text=month_name)

            # Weekday Headers
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
        
        # Content for the day
        tk.Label(day_frame, text=f"Notes for {date_str}", font=("Arial", 14)).pack(pady=10)
        txt = tk.Text(day_frame, height=15)
        txt.pack(expand=True, fill="both", padx=10, pady=5)
        
        tk.Button(day_frame, text="Close Tab", 
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

if __name__ == "__main__":
    root = tk.Tk()
    app = NotebookApp(root)
    root.mainloop()