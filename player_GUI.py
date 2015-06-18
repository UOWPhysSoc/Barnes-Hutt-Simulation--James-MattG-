from Tkinter import *
import threading
import os
from barnesplayer import *
import threading

FILES = []
print('word')

for f in os.listdir("./"):
    if f.endswith(".barnes"):
        g = f[:-7]
        while True:
            try:
                if isinstance(int(g[-1]),int):
                    g = g[:-1]
            except:
                break
        if not g in FILES:
            FILES.append(g)
           
root = Tk()

selectedFile = StringVar(root)
rate = StringVar()
rate.set(30)

fileMenu = apply(OptionMenu, (root, selectedFile) + tuple(FILES))
fileMenu.config(width = 20)
fileMenu.pack()

rateLabel = Label(root, text='Playback rate')
rateLabel.pack()
rateEntry = Entry(root, width = 8, textvariable = rate)
rateEntry.pack()

runButton = Button(root, text='Play', width=10,command=lambda:runPlayer(selectedFile.get(), int(rate.get())))
runButton.pack()

def runPlayer(fName, rate):
    root.destroy()
    from visual import *
    secondaryThread = threading.Thread(target = player(fName, rate))
    secondaryThread.start()

mainloop()

print('finish')
