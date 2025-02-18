import cv2
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Assignment (Number)")
        self.defaultbg = self.cget('bg')

    #change 'Assignment1/dop.bmp' to the path to your image. This program only works with bmp files
        self.img1 = cv2.imread(r'Assignment1/dog.bmp', cv2.IMREAD_GRAYSCALE)
        self.img2 = self.img1.copy()

        #organizing the frames on the grid
        for i in range(3):
            self.columnconfigure(i, weight=1, minsize=70)
            if i != 2:
                self.rowconfigure(i, weight=1, minsize=50)
        #build the window
        self.buildWindow()


    #function to create the histogram and image to embed in window
    def buildWindow(self):
        #container for the images frames
        frames = []

        #frames for histograms and pictures
        for i in range(4):
            fr = tk.Frame(self, padx=5, pady=5)
            fr.grid(row=i//2,column=i%2, pady=5, padx=5)
            frames.append(fr)
        

        #container for the image's canvases
        self.canvases = [self.img1, self.img2]

        #adding the images on the canvases
        for i in range(2):
            for j in range(2):
                fig = Figure(figsize=(4,4))
                a = fig.add_subplot(111)
                    #this one for the pictures
                a.imshow(self.canvases[0], cmap= 'gray')
                a.axis(False)
                #creating and embedding the images on the canvases, and the canvases on the frames
                canvas = FigureCanvasTkAgg(fig, frames[(2*i)+j])
                canvas.draw()
                canvas.get_tk_widget().pack()

                #adding the canvases into the canvases list for future use
                self.canvases.append(canvas)
            #removing the images used
            self.canvases.pop(0)

    #updates the image with the modified image
    def update(self, img):
        for i in range(1,4,2):
            fig = self.canvases[i].figure
            fig.clear()
            a = fig.add_subplot(111)

            if i==1:
                a.imshow(img, cmap='gray')
                a.axis('off')
            else:
                a.hist(img.ravel(), bins=256, range=[0, 256])
            self.canvases[i].draw()
        

app = App()
app.mainloop()
