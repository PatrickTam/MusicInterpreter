import Tkinter as tk
from PIL import ImageTk, Image


def writeGui(notes, noteVal):
    path = "D:\\cap\\Images\\"
    global index
    index=0
    root = tk.Tk()
    img = ImageTk.PhotoImage(Image.open(path+notes[0]+".jpg"))
    panel = tk.Label(root, image = img)
    panel.pack(side = "bottom", fill = "both", expand = "yes")

    
    text1 = tk.Text(root, height=5, width=30)
    text1.tag_configure('bold_italics', font=('Arial', 12, 'bold', 'italic'))
    text1.insert(tk.END, notes[0] + " " + noteVal[0], 'bold_italics')
    text1.pack(side=tk.LEFT)

    def leftPress(e):
        global index
        if index == 0:
            return
        index-=1
        text1.delete('1.0', tk.END)
        text1.insert(tk.END, notes[index] + " " + noteVal[index], 'bold_italics')
        img2 = ImageTk.PhotoImage(Image.open(path+notes[index]+".jpg"))
        panel.configure(image = img2)
        panel.image = img2

    def rightPress(e):
        global index
        if index == len(notes)-1:
            return
        index+=1
        text1.delete('1.0', tk.END)
        text1.insert(tk.END, notes[index] + " " + noteVal[index], 'bold_italics')
        img2 = ImageTk.PhotoImage(Image.open(path+notes[index]+".jpg"))
        panel.configure(image = img2)
        panel.image = img2

    root.bind('<Left>', leftPress)
    root.bind('<Right>', rightPress)
    root.mainloop()


#writeGui(["B5","C6"], ["whole", "half"])
