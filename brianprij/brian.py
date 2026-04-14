import sys
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Your Notebook")
root.geometry("600x450")

style = ttk.Style()
style.layout("Tabless.TNotebook.Tab", [])


# Functions
def quitWindow():
    root.destroy()
    sys.exit(0)

def switch_to_tab1():
    notebook.select(tab1)

def switch_to_tab2():
    notebook.select(tab2)

def make_draggable(widget):
    def on_drag_start(event):
        # Record the mouse position within the widget itself
        widget._drag_start_x = event.x
        widget._drag_start_y = event.y

    def on_drag_motion(event):
        # Calculate where the widget wants to go
        new_x = widget.winfo_x() - widget._drag_start_x + event.x
        new_y = widget.winfo_y() - widget._drag_start_y + event.y
        
        # Get the size of the parent (the tab) and the widget itself
        parent_width = widget.master.winfo_width()
        parent_height = widget.master.winfo_height()
        widget_width = widget.winfo_width()
        widget_height = widget.winfo_height()

        # Constrain X (keep it between 0 and the right edge)
        if new_x < 0:
            new_x = 0
        elif new_x + widget_width > parent_width:
            new_x = parent_width - widget_width

        # Constrain Y (keep it between 0 and the bottom edge)
        if new_y < 0:
            new_y = 0
        elif new_y + widget_height > parent_height:
            new_y = parent_height - widget_height

        widget.place(x=new_x, y=new_y)

    widget.bind("<Button-1>", on_drag_start)
    widget.bind("<B1-Motion>", on_drag_motion)


# NOTEBOOK SETUP
notebook = ttk.Notebook(root, style="Tabless.TNotebook")
notebook.pack(expand=True, fill="both")

# TABS
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
drag_tab = ttk.Frame(notebook)

notebook.add(tab1, text="Home")
notebook.add(tab2, text="Calendar")
notebook.add(drag_tab, text="Draggable Area")

# WIDGETS
# Root widgets
home_button = tk.Button(root, text='Home', command=switch_to_tab1)
home_button.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=10)

calendar_button = tk.Button(root, text='Calendar', command=switch_to_tab2)
calendar_button.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=10)

# tab1 widgets
quit_button = tk.Button(tab1, text='Quit', command=quitWindow)
quit_button.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)

label1 = ttk.Label(tab1, text="Notebook Content")
label1.pack(side=tk.TOP, padx=20, pady=20)

userEntry = tk.Entry(tab1, bd=2)
userEntry.pack(padx=20, pady=20)
make_draggable(userEntry)

# tab2 widgets
label2 = ttk.Label(tab2, text="This is the second tab content.")
label2.pack(padx=20, pady=20)


drag_label = tk.Label(drag_tab, text="Drag Me!", bg="lightblue", width=10, height=2)
drag_label.place(x=50, y=50) # Use place for initial position

# Apply the drag functionality
make_draggable(drag_label)


root.mainloop()
