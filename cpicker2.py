
import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import rgbname

TOPLEVEL_TITLE = "Colour Detector - Image"
INITIAL_MESSAGE = "Click on a point to see colour"
HEIGHT_MIN = 200
WIDTH_MIN = 500
RGB_MAX = 255
INITIAL_ID = 1
ARIAL18 = "Arial 18"
ARIAL14 = "Arial 14"


def cv2_imread(path):
        return cv2.imdecode(np.fromfile(path, dtype=np.uint8), 1)


class Detector:
    def __init__(self, window, file, max_height, max_width):
        self.img = cv2_imread(file)
        self.h, self.w, self.d = self.img.shape

        # maximum size of the display window
        self.HEIGHT_MAX = max_height
        self.WIDTH_MAX = max_width
        
        self.adjust_window()
        
        # initial widgets
        self.root = window
        self.root.title(TOPLEVEL_TITLE)
        self.root.iconbitmap("cd.ico")
        self.canvas = tk.Canvas(self.root,
                                width=self.w+3,
                                height=self.h+3)
        self.colour_label = tk.Label(self.root,
                                     text=INITIAL_MESSAGE,
                                     bg="white",
                                     font=ARIAL18)
        self.r_label = tk.Label(self.root, text="R: ", font=ARIAL14)
        self.r_input = tk.Entry(self.root, width=5, font=ARIAL14)
        self.g_label = tk.Label(self.root, text="G: ", font=ARIAL14)
        self.g_input = tk.Entry(self.root, width=5, font=ARIAL14)
        self.b_label = tk.Label(self.root, text="B: ", font=ARIAL14)
        self.b_input = tk.Entry(self.root, width=5, font=ARIAL14)
        self.hex_label = tk.Label(self.root, text="Hex: ", font=ARIAL14)
        self.hex_input = tk.Entry(self.root, width=10, font=ARIAL14)

        self._circleid = INITIAL_ID

    def adjust_window(self):
        #print("h = %d, w = %d" % (self.h, self.w))
        if (self.h > self.HEIGHT_MAX):
            self.w = int(self.w * self.HEIGHT_MAX / self.h)
            self.h = self.HEIGHT_MAX
        if (self.w < WIDTH_MIN):
            self.h = int(self.h * WIDTH_MIN / self.w)
            self.w = WIDTH_MIN
        elif (self.w > self.WIDTH_MAX):
            self.h = int(self.h * self.WIDTH_MAX / self.w)
            self.w = self.WIDTH_MAX
        if (self.h > self.HEIGHT_MAX):
            self.h = self.HEIGHT_MAX
        elif (self.h < HEIGHT_MIN):
            self.h = HEIGHT_MIN
        #print("h = %d, w = %d" % (self.h, self.w))
        self.img = cv2.resize(self.img, (self.w, self.h))

    def set_image_label(self):
        # rearrang the color channel
        b, g, r = cv2.split(self.img)
        self.img = cv2.merge((r, g, b))

        # convert the Image object into a TkPhoto object
        im = Image.fromarray(self.img)
        imgtk = ImageTk.PhotoImage(image=im)

        return imgtk

    def label_fg_colour(self, r, g, b):
        total = r + g + b
        if (total > 2 * RGB_MAX):
            return "black"
        else:
            return "white"
        
    def update_window(self, x, y):
        # retrieve pixel and convert numpy tuple to tuple
        rgb = tuple(map(int, self.img[y, x]))
        r, g, b = rgb

        # self.colour_label fg colour
        colour = self.label_fg_colour(r, g, b)
        # hex string
        hex_str = "#%02X%02X%02X" % rgb
        name = rgbname.get_name(r, g, b)
        
        # delete curser circle from canvas
        if (self._circleid > INITIAL_ID):
            self.canvas.delete(self._circleid)
        
        # update labels
        self._circleid = self.canvas.create_oval(x-5, y-5, x+5, y+5,
                         outline=colour, width=2)
        self.r_input.delete(0, "end")
        self.r_input.insert(0, str(r))
        self.g_input.delete(0, "end")
        self.g_input.insert(0, str(g))
        self.b_input.delete(0, "end")
        self.b_input.insert(0, str(b))
        self.hex_input.delete(0, "end")
        self.hex_input.insert(0, hex_str)
        self.colour_label = tk.Label(self.root, text=name,
                                     fg=colour,
                                     bg=hex_str,
                                     font=ARIAL18)
        self.colour_label.grid(row=1, column=0, sticky="ew",
                               columnspan=9)
            
    def motion(self, event):
        abs_x = (self.root.winfo_pointerx() -
                 self.root.winfo_rootx())
        abs_y = (self.root.winfo_pointery() -
                 self.root.winfo_rooty())
        
        if (abs_x < self.w and abs_x >= 0 and
            abs_y < self.h and abs_y >= 0):
            print("x: {}, y: {}".format(abs_x, abs_y))
            self.update_window(abs_x, abs_y)

    def run(self):
        global imgtk
        self.adjust_window()
        imgtk = self.set_image_label() 
        
        # put widgets in the display window
        self.canvas.grid(row=0, column=0, columnspan=9)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
        self.colour_label.grid(row=1, column=0, sticky="ew",
                               columnspan=9)
        self.r_label.grid(row=2, column=0)
        self.r_input.grid(row=2, column=1)
        self.g_label.grid(row=2, column=2)
        self.g_input.grid(row=2, column=3)
        self.b_label.grid(row=2, column=4)
        self.b_input.grid(row=2, column=5)
        self.hex_label.grid(row=2, column=7)
        self.hex_input.grid(row=2, column=8)
        
        self.root.bind('<Button 1>', self.motion)

        #tk.mainloop()

        
# test
"""
d = Detector("0513_1.jpg", 750, 1400)
d.run()
"""
