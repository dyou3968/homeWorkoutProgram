
import tkinter as tk
from tkinter import *

# def getDimensions():
#     width = 800
#     height = 800
#     return (width,height)

# def drawGymSpace():
#     width,height = getDimensions()
#     master = Tk()
#     window = Canvas(master,width= width,height = height)
#     window.pack()

# Use 8 X 10 square feet as minimum

#     window.create_text(width/2, height/4, font = "Arial 32 bold", text = "Workout Space")
#     window.create_rectangle(width/2 - 50 ,height/2 - 50, width/2 + 50, height/2 + 50, fill = None, outline = "black")


#     #Scrolling information taken from 
#     #http://effbot.org/tkinterbook/scrollbar.htm
#     scrollbar = Scrollbar(master)
#     scrollbar.pack(side=RIGHT, fill=Y)

#     text = Text(master, wrap=WORD, yscrollcommand=scrollbar.set)
#     text.pack()

#     scrollbar.config(command=text.yview)

#     window.mainloop()

# drawGymSpace()


def fahrenheit_to_celsius():
    """Convert the value for Fahrenheit to Celsius and insert the
    result into lbl_result.
    """
    fahrenheit = ent_temperature.get()
    celsius = (5/9) * (float(fahrenheit) - 32)
    lbl_result["text"] = f"{round(celsius, 2)} \N{DEGREE CELSIUS}"

# Set-up the window
window = tk.Tk()
window.title("Temperature Converter")
window.resizable(width=False, height=False)

# Create the Fahrenheit entry frame with an Entry
# widget and label in it
frm_entry = tk.Frame(master=window)
ent_temperature = tk.Entry(master=frm_entry, width=10)
lbl_temp = tk.Label(master=frm_entry, text="\N{DEGREE FAHRENHEIT}")

# Layout the temperature Entry and Label in frm_entry
# using the .grid() geometry manager
ent_temperature.grid(row=0, column=0, sticky="e")
lbl_temp.grid(row=0, column=1, sticky="w")

# Create the conversion Button and result display Label
btn_convert = tk.Button(
    master=window,
    text="\N{RIGHTWARDS BLACK ARROW}",
    command=fahrenheit_to_celsius
)
lbl_result = tk.Label(master=window, text="\N{DEGREE CELSIUS}")

# Set-up the layout using the .grid() geometry manager
frm_entry.grid(row=0, column=0, padx=10)
btn_convert.grid(row=0, column=1, pady=10)
lbl_result.grid(row=0, column=2, padx=10)

# Run the application
window.mainloop()

