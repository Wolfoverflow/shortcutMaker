import tkinter as tk

def deleteShortcut(i, element):
    pass

root = tk.Tk()
root.title("Element Display")

elements = [[{'Key.ctrl', 'm'}, "batchCommand"], [{'Key.cmd', ';'}, "batchCommand"]]

for i, element in enumerate(elements):
    keystokes = element[0]
    command = element[1]
    keystrokesLabel = tk.Label(root, text=f"Keystokes: {keystokes}")
    keystrokesLabel.pack()

    commandLabel = tk.Label(root, text=f"Command: {command}")
    commandLabel.pack()

    button = tk.Button(root, text="Delete", command=lambda i=i, element=element: deleteShortcut(i, element))
    button.pack()

root.mainloop()