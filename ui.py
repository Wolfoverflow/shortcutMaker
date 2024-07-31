import tkinter as tk
from tkinter import messagebox
import csv
import keyloggerTest as kl
import os

selected = None
homepage = True
editpage = False
shortcuts = kl.csvParser('keylogger.csv')
print(shortcuts)


def contentRenderer(shortcuts):
    canvas = tk.Canvas(frmBody, bg="Black", width=300, height=190, highlightbackground="White", highlightthickness=1)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrlbar = tk.Scrollbar(frmBody, orient='vertical', command=canvas.yview)
    scrlbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrlbar.set)
    frmContent = tk.Frame(canvas, bg="Black", width=290, height=50)
    canvas.create_window((0, 0), window=frmContent, anchor=tk.NW)

    for i, shortcut in enumerate(shortcuts):
        keystrokes = str(list(shortcut[0]))
        commands = shortcut[1]
        date = shortcut[2]
        name = shortcut[3]
        if len(str(keystrokes)) > 25:
            if str(keystrokes)[22] == '.':
                keystrokes = str(keystrokes)[:22] + '..'
            else:
                keystrokes = str(keystrokes)[:22] + '...'
        if len(str(commands)) > 18:
            if str(commands)[15] == '.':
                commands = str(commands)[:15] + '..'
            else:
                commands = str(commands)[:15] + '...'

        frmContentRow = tk.Frame(frmContent, bg="Black", width=290, height=50, highlightbackground="White", highlightthickness=1)
        frmContentRow.pack(side=tk.TOP, pady=2, padx=5, anchor=tk.W)
        lblName = tk.Label(frmContentRow, text=str(i) + ' - ' + name, bg="Black", fg="White", font=("Courier New", 11, 'bold'))
        lblName.place(relx=0.0, rely=0.0)
        lblDate = tk.Label(frmContentRow, text=date, bg="Black", fg="#dddddd", font=("Courier New", 9, 'bold'))
        lblDate.place(relx=0.0, rely=0.5)
        lblKeystrokes = tk.Label(frmContentRow, text=str(keystrokes), bg="Black", fg="White", font=("Courier New", 9))
        lblKeystrokes.place(relx=0.35, rely=0.0)
        lblCommands = tk.Label(frmContentRow, text=commands, bg="Black", fg="White", font=("Courier New", 9))
        lblCommands.place(relx=0.35, rely=0.5)
        bttnSelect = tk.Button(frmContentRow, text="Select", bg="Black", fg="White", font=("Arial", 9), command=lambda i=i, frmContentRow=frmContentRow, frmContent=frmContent: select(i, frmContentRow, frmContent))
        bttnSelect.place(relx=0.84, rely=0.44)

    frmBufferRow = tk.Frame(frmContent, bg="Black", width=290, height=24)
    frmBufferRow.pack(side=tk.TOP, pady=2, padx=5)
    bttnNew = tk.Button(frmBody, width=13, text="New +", bg="Black", fg="White", font=("Arial", 9))
    bttnNew.place(relx=0.005, rely=0.86)

    bttnDelete = tk.Button(frmBody, width=13, text="Delete -", bg="Black", fg="White", font=("Arial", 9))
    bttnDelete.place(relx=0.315, rely=0.86)

    bttnEdit = tk.Button(frmBody, width=13, text="Edit %", bg="Black", fg="White", font=("Arial", 9))
    bttnEdit.configure(command=lambda frmContentRow=frmContentRow, frmContent=frmContent: edit(selected, frmContentRow, frmContent))
    bttnEdit.place(relx=0.626, rely=0.86)

    frmContent.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))


window = tk.Tk()
icon = tk.PhotoImage(file='shortcutmanagericon.ico')
window.title('Shortcut Manager')
window.geometry('400x300')
window.iconphoto(False, icon)
window.config(bg='Black')

frmTitle = tk.Frame(window, bg="Black", width=400, height=80)
frmTitle.grid(column=0, row=0)

lblTitle = tk.Label(frmTitle, text="Shortcut Manager", font=("Arial", 16), fg="White", bg="Black")
lblTitle.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
lblSubtitle = tk.Label(frmTitle, text="v0.0.3 - Alpha", fg="White", bg="Black")
lblSubtitle.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

frmBody = tk.Frame(window, bg="Black", width=300, height=210, highlightbackground="White", highlightthickness=1)
frmBody.grid(column=0, row=1, padx=50)


def select(i, frmContentRow, frmContent):
    global selected
    for widget in frmContentRow.winfo_children():
        widget.configure(bg="White", fg="Black")
    frmContentRow.configure(bg="White")
    for widget in frmContent.winfo_children():
        if widget != frmContentRow:
            widget.configure(bg="Black")
            for child in widget.winfo_children():
                child.configure(bg="Black", fg="White")
    selected = i
    print(i)


def closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()
        os.kill(os.getpid(), 9)

def edit(i, frmContentRow, frmContent):
    global homepage
    global editpage
    global selected
    homepage = False
    editpage = True
    #make new window for editing the shortcut
    new_window = tk.Toplevel(window)
    new_window.title("Edit Shortcut")
    new_window.geometry("400x200")
    new_window.config(bg="Black")

    frmEdit = tk.Frame(new_window, bg="Black", width=400, height=200)
    frmEdit.pack()

    lblEditTitle = tk.Label(frmEdit, text="Edit Shortcut", font=("Arial", 14), fg="White", bg="Black")
    lblEditTitle.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
    lblEditName = tk.Label(frmEdit, text="Name:", font=("Arial", 12), fg="White", bg="Black")
    lblEditName.place(relx=0.1, rely=0.5)
    lblEditKeystrokes = tk.Label(frmEdit, text="Keystrokes:", font=("Arial", 12), fg="White", bg="Black")
    lblEditKeystrokes.place(relx=0.1, rely=0.6)
    lblEditCommands = tk.Label(frmEdit, text="Commands:", font=("Arial", 12), fg="White", bg="Black")
    lblEditCommands.place(relx=0.1, rely=0.7)
    
    entrEditName = tk.Entry(frmEdit, width=20, font=("Arial", 12), bg='Black', fg='White')
    entrEditName.place(relx=0.4, rely=0.5)
    entrEditName.insert(0, shortcuts[selected][3])
    entrEditKeystrokes = tk.Entry(frmEdit, width=20, font=("Arial", 12), bg='Black', fg='White')
    entrEditKeystrokes.place(relx=0.4, rely=0.6)
    entrEditKeystrokes.insert(0, shortcuts[selected][0])
    entrEditCommands = tk.Entry(frmEdit, width=20, font=("Arial", 12), bg='Black', fg='White')
    entrEditCommands.place(relx=0.4, rely=0.7)
    entrEditCommands.insert(0, shortcuts[selected][1])

    bttnEditSave = tk.Button(frmEdit, text="Save", bg="Black", fg="White", font=("Arial", 12))
    bttnEditSave.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
    bttnEditSave.configure(command=lambda i=i, frmContentRow=frmContentRow, frmContent=frmContent: save(i, frmContentRow, frmContent, entrEditName, entrEditKeystrokes, entrEditCommands, new_window))

    bttnEditCancel = tk.Button(frmEdit, text="Cancel", bg="Black", fg="White", font=("Arial", 12))
    bttnEditCancel.place(relx=0.8, rely=0.8, anchor=tk.CENTER)
    bttnEditCancel.configure(command=lambda: cancel(new_window))
    

    

    new_window.mainloop()
    print(i)

def save(i, frmContentRow, frmContent, entrEditName, entrEditKeystrokes, entrEditCommands, new_window):
    global shortcuts
    print("Save")
    print(i)
    print(entrEditName.get())
    print(entrEditKeystrokes.get())
    print(entrEditCommands.get())
    
    #input validation TODO
    
    #update the csv file
    with open('keylogger.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for index, shortcut in enumerate(shortcuts):
            if index == i:
                writer.writerow([index,entrEditKeystrokes.get(), entrEditCommands.get(), shortcut[2], entrEditName.get()])
            else:
                buffer = shortcut
                buffer.insert(0,index)
                writer.writerow(buffer)
    

    shortcuts = kl.csvParser('keylogger.csv')
    refreshcontent()
    cancel(new_window)

def cancel(new_window):
    new_window.destroy()
    global homepage
    global editpage
    homepage = True
    editpage = False

def refreshcontent():
    contentRenderer(shortcuts)


window.protocol("WM_DELETE_WINDOW", closing)

contentRenderer(shortcuts)

window.mainloop()
