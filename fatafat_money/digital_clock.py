import tkinter as tk
from time import strftime

def update_time():
  current_time = strftime("%H:%M:%S:%p" )  # Get current time in HH:MM:SS format
  digital_clock_lbl.config(text=current_time)  # Update label text
  window.after(1000, update_time)  # Schedule next update after 1 second

# Window and label creation
window = tk.Tk()
digital_clock_lbl = tk.Label(window, text="00:00:00" , font="Helvetica 72 bold")
digital_clock_lbl.pack()

# Schedule the first update
update_time()

# Main loop
window.mainloop()