import cv2
import numpy as np
import tkinter as tk
from PIL import Image
from PIL import ImageTk

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Assignment 2")
        self.defaultbg = self.cget('bg')

    #change 'Assignment1/dop.bmp' to the path to your image. This program only works with bmp files
        self.img1 = cv2.imread(r'Assignment2/dog.bmp', cv2.IMREAD_GRAYSCALE)
        self.length, self.width = self.img1.shape[:2]

        #organizing the frames on the grid
        # for i in range(7):
        #     self.columnconfigure(i, weight=1, minsize=70)
        #     if i != 2:
        #         self.rowconfigure(i, weight=1, minsize=50)
        #build the window
        self.buildWindow()


    #function to create the histogram and image to embed in window
    def buildWindow(self):
        #container for the images frames
        frames = []

        #frames for histograms and pictures
        for i in range(4):
            fr = tk.Frame(self, padx=5, pady=5)
            fr.grid(row=i%2,column=i//2, pady=5, padx=5)
            frames.append(fr)
        
        filters = [self.boxNoCV(k=3), self.boxNoCV(k=5), self.box(k=3), self.box(k=5)]


        for i in range(len(filters)):
            img= Image.fromarray(filters[i])
            img= ImageTk.PhotoImage(img)
            label = tk.Label(frames[i], image = img)
            label.image = img
            label.pack()


    def boxNoCV(self, k):
        mask = np.ones((k,k),np.float32)/k**2

        pad = k // 2
        padded_image = np.zeros((self.length + 2 * pad, self.width + 2 * pad))
        padded_image[pad:self.length + pad, pad:self.width + pad] = self.img1

        blurred = np.zeros((self.length,self.width), np.uint8)

        for row in range(self.length):
            for col in range(self.width):
                region = padded_image[row:row + k, col:col + k]
                value = np.sum(region * mask)
                blurred[row, col] = value
        return blurred
    
    def box(self, k):
        mask = np.ones((k,k),np.float32)/k**2

        pad = k // 2
        padded_image = np.zeros((self.length + 2 * pad, self.width + 2 * pad))
        padded_image[pad:self.length + pad, pad:self.width + pad] = self.img1

        blurred = np.zeros((self.length,self.width), np.uint8)
        cv2.boxFilter(self.img1, -1, (k,k), blurred)

        return blurred

if __name__ == "__main__":
    app = App()
    app.mainloop()