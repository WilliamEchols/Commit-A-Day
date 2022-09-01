# Goal: a working gui-based text editor in Python 3
# note: flexible text box sizing
import tkinter as tk
from tkinter import filedialog

# window information
window = tk.Tk()
window.title("PTE - Python Text Editor")

text_string = tk.StringVar()
text_string.set("new file")
current_filename = "untitled.txt"

# editable text box
text_box = tk.Text(window)
text_box.pack(expand=True, fill="both")
text_box.insert("end", text_string.get())

# on change update
def status_callback(e): # show document updated
    display_file_info.config(text=current_filename+'*')
text_box.bind("<<Modified>>", status_callback)
text_string.trace("w", lambda name, index, mode, sv=text_string: status_callback(sv))

# controls
top = tk.Frame(window)
top.pack(side=tk.TOP)
def open_file():
    global current_filename, text_string
    file_path = filedialog.askopenfilename()
    if(file_path): current_filename = file_path
    with open(file_path) as f:
        lines = f.readlines()
        text_box.delete(1.0, "end")
        new_text_string = ""
        for l in range(len(lines)):
            new_text_string += lines[l]
            text_box.insert("end", lines[l])
        text_string.set(new_text_string)
def save_file():
    global current_filename, text_string
    text_string.set(text_box.get(1.0, "end"))

    display_file_info.config(text=current_filename) # show document saved

    with open(current_filename, "w") as f:
        f.write(text_string.get())

# file info
display_file_info = tk.Label(text=current_filename)
display_file_info.pack(in_=top, side=tk.RIGHT)

# buttons
tk.Button(window, text="Open", command=open_file).pack(in_=top, side=tk.LEFT)
tk.Button(window, text="Save", command=save_file).pack(in_=top, side=tk.LEFT)

if __name__ == "__main__":
    window.mainloop()
