from tkinter import *

root = Tk()
c0 = Canvas(root, width=150, height=150)
c0.create_text(75, 75, text='hello, world!', font=('FixedSys', 14))
c0.pack()
root.mainloop()
