import sys
import tkinter as tk
from tkinter import ttk
import pandas as pd

class NotebookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Your Notebook")
        self.root.geometry("1100x800")
        
        self.style = ttk.Style()
        self.style.layout("Tabless.TNotebook.Tab", []) 
        
        try:
            self.df = pd.read_csv('calendar_data.csv')
        except FileNotFoundError:
            print("CSV not found.")
            self.df = pd.DataFrame()

        self.day_map = {'Sunday': 0, 'Monday': 1, 'Tuesday': 2, 'Wednesday': 3,
                        'Thursday': 4, 'Friday': 5, 'Saturday': 6}
        self.open_tabs = {} 

        self.setup_main_nav()

    def setup_main_nav(self):
        nav_frame = tk.Frame(self.root)
        nav_frame.pack(side=tk.TOP, fill=tk.X)

        tk.Button(nav_frame, text='Home', command=lambda: self.main_nb.select(self.tab1)).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(nav_frame, text='Calendar', command=lambda: self.main_nb.select(self.tab2)).pack(side=tk.LEFT, padx=5, pady=5)

        self.main_nb = ttk.Notebook(self.root, style="Tabless.TNotebook")
        self.main_nb.pack(expand=True, fill="both")

        self.tab1 = ttk.Frame(self.main_nb)
        self.tab2 = ttk.Frame(self.main_nb)
        self.main_nb.add(self.tab1)
        self.main_nb.add(self.tab2)

        self.setup_home_tab()
        self.setup_calendar_tab()

    def setup_calendar_tab(self):
        # --- SPLIT SCREEN SETUP ---
        # We use a PanedWindow so you can resize the divider between Calendar and Notes
        paned = ttk.PanedWindow(self.tab2, orient=tk.HORIZONTAL)
        paned.pack(expand=True, fill='both')

        # Left Side: Month/Grid Notebook
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)
        
        self.month_nb = ttk.Notebook(left_frame)
        self.month_nb.pack(expand=True, fill='both', padx=5, pady=5)

        # Right Side: Day Content Notebook (Where day tabs appear)
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=1)
        
        # Label to indicate this area is for notes
        tk.Label(right_frame, text="Daily Notes", font=("Arial", 10, "bold")).pack(pady=2)
        
        self.day_nb = ttk.Notebook(right_frame)
        self.day_nb.pack(expand=True, fill='both', padx=5, pady=5)

        # Build Month Grids inside self.month_nb
        for month_name in self.df['Month'].unique():
            m_frame = ttk.Frame(self.month_nb)
            self.month_nb.add(m_frame, text=month_name)

            for i, day in enumerate(self.day_map.keys()):
                tk.Label(m_frame, text=day[:3], font=('Arial', 8, 'bold')).grid(row=0, column=i)

            month_days = self.df[self.df['Month'] == month_name]
            row_idx = 1
            for _, data in month_days.iterrows():
                col_idx = self.day_map[data['Day of Week']]
                day_num = data['Date'].split('-')[-1]
                
                # Button targets the NEW day_nb
                btn = tk.Button(m_frame, text=day_num, width=5, height=2,
                                command=lambda d=data: self.open_day_tab(d))
                btn.grid(row=row_idx, column=col_idx, padx=1, pady=1)
                if col_idx == 6: row_idx += 1

    def open_day_tab(self, data):
        date_str = data['Date']
        
        # If already open in the SECOND notebook, just select it
        if date_str in self.open_tabs:
            self.day_nb.select(self.open_tabs[date_str])
            return

        # Add tab to day_nb (the right-side notebook)
        day_frame = ttk.Frame(self.day_nb)
        self.day_nb.add(day_frame, text=date_str)
        self.open_tabs[date_str] = day_frame
        
        # UI inside the Day Tab
        tk.Label(day_frame, text=f"Notes: {date_str}").pack(pady=5)
        txt = tk.Text(day_frame, height=10, width=30)
        txt.pack(expand=True, fill="both", padx=5, pady=5)
        
        tk.Button(day_frame, text="Close Day", 
                  command=lambda: self.close_day_tab(date_str, day_frame)).pack(pady=2)
        
        self.day_nb.select(day_frame)

    def close_day_tab(self, date_str, frame):
        self.day_nb.forget(frame)
        del self.open_tabs[date_str]

    def setup_home_tab(self):
        ttk.Label(self.tab1, text="Notebook Home").pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = NotebookApp(root)
    root.mainloop()