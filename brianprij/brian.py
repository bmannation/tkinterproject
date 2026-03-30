#### Cm <-> In Converter Example GUI ####

# imports
import sys
import tkinter as tk
# To enable image support, install Pillow: pip install pillow
try:
    from PIL import ImageTk, Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
PIL_AVAILABLE = True

# Constants
IMAGE_PATH = "images/units_of_measure.gif"
# try:
#     from PIL import ImageTk, Image
#     PIL_AVAILABLE = True
# except ImportError:
#     PIL_AVAILABLE = False


#################### FUNCTIONS ####################

# a function that will convert inches to centimeters.
def convertToCm():
    numInches = float(userEntry.get())
    numCentimeters = numInches * 2.54
    # format numInches to 2 decimal places
    numCentimeters = "{:.2f}".format(numCentimeters)
    # format numCentimeters to 2 decimal places
    msg = str(userEntry.get()) + " in is " + str(numCentimeters) + " cm"
    outputLabel.configure(text=msg)
    status.configure(text="ok")


# a function that will convert centimeters to inches.
def convertToIn():
    try:
        numCentimeters = float(userEntry.get())
        numInches = numCentimeters / 2.54
        numInches = "{:.2f}".format(numInches)
        msg = f"{numCentimeters} cm is {numInches} in"
        outputLabel.configure(text=msg)
        status.configure(text="ok")
    except ValueError:
        outputLabel.configure(text="Enter a valid number")
        status.configure(text="error")


# a function to quit the window
def quitWindow():
    root.destroy()
def quitWindow():
    root.destroy()
    sys.exit(0)
    print("uncomment the destroy method and exit method statements above, then delete this print statement...")





#################### GUI SETUP ####################
# create a GUI window.
root = tk.Tk()
# set the title.
root.title("Centimetres <--> Inches Converter")
# set the size.
root.geometry("450x600")


# add a label for the title
title = tk.Label(root, text="Centimetres <--> Inches Converter", font=('Helvetica', 14))
title.grid(row=0, column=0, columnspan=2)

# add a label for input instruction
inchLabel = tk.Label(root, text="Please enter value to be converted:", font=('Helvetica', 11))
root.grid_rowconfigure(1, minsize=50)
inchLabel.grid(row=1)

# add a entry box for user input
userEntry = tk.Entry(root, bd=2)
userEntry.grid(row=1, column=1)

# add a 'convert to xx' button
convertButton1 = tk.Button(text="Inches --> Centimetres", command=convertToCm)
convertButton1.grid(row=2, column=0)

# add a 'convert to xx' button
convertButton2 = tk.Button(text="Centimetres --> Inches", command=convertToIn)
convertButton2.grid(row=2, column=1, sticky='w')
root.grid_rowconfigure(2, minsize=50)

# add a result text label
outputLabel = tk.Label(root, text="Select conversion button above", font=('Arial', 14))
outputLabel.grid(row=3, column=0, columnspan=2)
root.grid_rowconfigure(3, minsize=50)

if PIL_AVAILABLE:
    try:
        photo = Image.open(IMAGE_PATH)
        if hasattr(Image, "Resampling"):
            resample = Image.Resampling.LANCZOS
        else:
            resample = Image.LANCZOS
        photo = photo.resize((150,150), resample)
        photo = ImageTk.PhotoImage(photo)
        photoLabel = tk.Label(root, image=photo)
        photoLabel.image = photo  # Keep a reference to avoid garbage collection
    except Exception as e:
        photoLabel = tk.Label(
            root,
            text=f"Image not found or could not be loaded.\nExpected at: {IMAGE_PATH}\nError: {e}"
        )
else:
    photoLabel = tk.Label(root, text="Pillow not installed; image disabled.")

photoLabel.grid(row=5, column=0, columnspan=2)
root.grid_rowconfigure(5, minsize=210)

photoLabel.grid(row=5, column=0, columnspan=2)
root.grid_rowconfigure(5, minsize=210)


# add a progress bar
status = tk.Label(root, text="Waiting for user input.", bd=5, relief='sunken', anchor='w')
status.grid(row=6, column=0, sticky='n', columnspan=2, pady=4)
root.grid_rowconfigure(6, minsize=50)


# add quit button
quit_button = tk.Button(root, text='Quit', command=quitWindow).grid(row=8, column=0, rowspan=2, columnspan=2, sticky='n', pady=4)









# start the GUI --> Leave here at the end!
root.mainloop()