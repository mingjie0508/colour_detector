
import tkinter as tk
from tkinter import filedialog
import cpicker2

ROOT_GEOMETRY = "700x300+200+200" # size and position of root windown
ROOT_TITLE = "Colour Detector"
SELECT_IMAGE_TEXT = "Select an Image"
INSTRUCTION = "Select an image and click on it to get colour information"
VIOLET_RED = "#f5387d"
ARIAL28 = "Arial 28 bold"
ARIAL18 = "Arial 18"
MAXHEIGHT_SCALE = 17 / 20
MAXWIDTH_SCALE = 9 / 10


class App:
    def __init__(self):
        # initialize a root window
        self.root = tk.Tk()
        self.root.iconbitmap("cd.ico")
        self._maxheight = self.root.winfo_screenheight()
        self._maxwidth = self.root.winfo_screenwidth()
        self.root.title(ROOT_TITLE)
        self.root.geometry(ROOT_GEOMETRY)
        self._header = tk.Label(self.root, text=ROOT_TITLE, fg="black",
                       font=ARIAL28)
        self._instruct = tk.Label(self.root, text=INSTRUCTION, fg="grey",
                                  font=ARIAL18)
        self._button = tk.Button(self.root, text=SELECT_IMAGE_TEXT,
                       bg=VIOLET_RED,
                       fg="white",
                       font=ARIAL18,
                       command=self.openfile)
        self.top = None

    def on_closing(self):
        self._button.pack()
        self.top.destroy()
        
    def openfile(self):
        self._button.pack_forget()
        self._button.update()
        self.root.filename = filedialog.askopenfilename(title=SELECT_IMAGE_TEXT,
                                filetypes=(("jpg or png files", "*.jpg .*png"),
                                           ("jpg files", "*.jpg"),
                                           ("png files", "*.png")))
        #print(self.root.filename)

        if (self.root.filename != ""): # if dialog box is not cancelled
            # initialize a toplevel window
            self.top = tk.Toplevel()
            d = cpicker2.Detector(self.top,
                                  self.root.filename,
                                  int(self._maxheight * MAXHEIGHT_SCALE),
                                  int(self._maxwidth * MAXWIDTH_SCALE))
            d.run()
            self.top.protocol("WM_DELETE_WINDOW", self.on_closing)

        # if dialog box is cancelled
        else:
            self._button.pack(pady=20)
        
    def run(self):
        self._header.pack(pady=40)
        self._instruct.pack()
        self._button.pack(pady=20)

        tk.mainloop()


a = App()
a.run()

