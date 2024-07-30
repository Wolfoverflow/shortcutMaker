import tkinter as tk
import csv
import keyloggerTest as kl
import os

homepage=True
editpage=False
shortcuts=kl.csvParser('keylogger.csv')
print((shortcuts))

def contentRenderer(shortcuts): 
    for i, shortcut in enumerate(shortcuts):
        keystrokes=str(list(shortcut[0]))
        commands=shortcut[1]
        date=shortcut[2]
        name=shortcut[3]
        if len(str(keystrokes))>25:
            if str(keystrokes)[22]=='.':
                keystrokes = str(keystrokes)[:22]+'..'
            else:
                keystrokes = str(keystrokes)[:22]+'...'
        if len(str(commands))>23:
            if str(commands)[20]=='.':
                commands = str(commands)[:20]+'..'
            else:
                commands = str(commands)[:20]+'...'
        frmContent = tk.Frame(frmBody, bg="Black", width=290, height=50, highlightbackground="White", highlightthickness=1)
        frmContent.place(relx=0.015, rely=((0.26)*(i))+0.02)
        lblName = tk.Label(frmContent, text=str(i)+' - '+name, bg="Black", fg="White", font=("Courier New", 11))
        lblName.place(relx=0.0, rely=0.0)
        lblDate = tk.Label(frmContent, text=date, bg="Black", fg="White", font=("Courier New", 11))
        lblDate.place(relx=0.0, rely=0.5)
        lblKeystrokes = tk.Label(frmContent, text=str(keystrokes), bg="Black", fg="White", font=("Courier New", 9))
        lblKeystrokes.place(relx=0.35, rely=0.0)
        lblCommands = tk.Label(frmContent, text=commands, bg="Black", fg="White", font=("Courier New", 11))
        lblCommands.place(relx=0.35, rely=0.5)
   
        

window=tk.Tk()
icon=tk.PhotoImage(file='shortcutmanagericon.ico')
window.title('Shortcut Manager')
window.geometry('400x300')
window.iconphoto(False, icon)
window.config(bg='Black')

frmTitle = tk.Frame(window, bg="Black", width=400, height=80)
frmTitle.grid(column=0, row=0)

lblTitle=tk.Label(frmTitle, text="Shortcut Manager", font=("Arial", 16), fg="White", bg="Black")
lblTitle.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
lblSubtitle=tk.Label(frmTitle, text="v0.0.3 - Alpha", fg="White", bg="Black")
lblSubtitle.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

frmBody = tk.Frame(window, bg="Black", width=300, height=210, highlightbackground="White", highlightthickness=1)
frmBody.grid(column=0, row=1, padx=50)

bttnNew = tk.Button(frmBody,width=13, text="New +", bg="Black", fg="White",font=("Arial",9))
bttnNew.place(relx=0.0, rely=0.87)

bttnDelete = tk.Button(frmBody,width=13, text="Delete -", bg="Black", fg="White",font=("Arial",9))
bttnDelete.place(relx=0.333, rely=0.87)

bttnEdit = tk.Button(frmBody,width=13, text="Edit %", bg="Black", fg="White",font=("Arial",9)) #✏️🎬📝🎞️
bttnEdit.place(relx=0.66, rely=0.87)



contentRenderer(shortcuts)

window.mainloop()
