import cv2
import matplotlib as plt
plt.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import tkinter as tk

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Assignment 1")

        self.img1 = cv2.imread(r'Assignment1/dog.bmp', cv2.IMREAD_GRAYSCALE)
        self.img2 = self.img1.copy()

        self.bri = 0 #brightness deafult
        self.con = 1 ##contrast default

        #organizing the frames on the grid
        for i in range(3):
            self.columnconfigure(i, weight=1, minsize=75)
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
        
        #frame for the scrollbars
        scaleFrame = tk.Frame(self, padx=5, pady=5)
        scaleFrame.grid(row=0,column=2)

        #container for the image's canvases
        self.canvases = [self.img1, self.img2]

        #adding the images on the canvases
        for i in range(2):
            for j in range(2):
                fig = Figure(figsize=(5,5))
                a = fig.add_subplot(111)
                if i==0:
                    #this one for the pictures
                    a.imshow(self.canvases[0], cmap= 'gray')
                    a.axis(False)
                else:
                    #this one for the histograms
                    a.hist(self.canvases[0].ravel(), bins=256, range=[0, 256])

                #creating and embedding the images on the canvases, and the canvases on the frames
                canvas = FigureCanvasTkAgg(fig, frames[(2*i)+j])
                canvas.draw()
                canvas.get_tk_widget().pack()

                #adding the canvases into the canvases list for future use
                self.canvases.append(canvas)
            #removing the images used
            self.canvases.pop(0)
        
        #Creating the button save and giving it a command and placement
        save = tk.Button(self,text= "SAVE",command= lambda: self.save())
        save.grid(row=1, column=2)

        #creating the scrollbars
        br = tk.Scale(scaleFrame, from_=-100, to=100, orient=tk.HORIZONTAL, label= "Brightness", command= self.brightness)
        br.pack()
        con = tk.Scale(scaleFrame, from_=-100, to=100, orient=tk.HORIZONTAL, label= "Contrast", command= self.contrast)
        con.pack()

    #whenever we increase or decrease the brightness
    def brightness(self, var):
        self.bri = ((int(var)-(-100))/(100-(-100)))*(127-(-127))+(-127) #scaling to have a -127 to 127 value
        modified = cv2.convertScaleAbs(self.img2, alpha=self.con, beta=self.bri) #converting the picture
        self.update(modified) #updating with modified value

        

    def contrast(self, var):
        self.con = ((int(var)-(-100))/(100-(-100)))*3 #scaling from -100 to 100 to be 0 to 3
        modified = cv2.convertScaleAbs(self.img2, alpha= self.con, beta= self.bri)
        self.update(modified)

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


    #saving the image, replacing the original one
    def save(self):
        modified = cv2.convertScaleAbs(self.img2, alpha=self.con, beta=self.bri)
        cv2.imwrite(r"Assignment1/dog.bmp", modified)
        

app = App()
app.mainloop()
    
