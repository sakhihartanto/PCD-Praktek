from tkinter import *
from tkinter import ttk
import tkinter
from tkinter import simpledialog
from tkinter.messagebox import showinfo
import tkinter.filedialog
from tkinter.simpledialog import askinteger
from PIL import Image, ImageTk
import cv2 as cv
import numpy as np
from numpy.core.fromnumeric import var


root = Tk()

root.title('191524030')


effect = None
label_original = object
panelA = None
panelB = None
currImage = [[]]
current_value = tkinter.DoubleVar()


maxScaleUp = 100
scaleFactor = 20

def nothing(x):
    pass

def select_image():
    global panelA, panelB, path, currImage
    

    path = tkinter.filedialog.askopenfilename(filetypes=[("PNG", "*.png"),("JPG", "*.jpg"), ("JPEG", "*.jpeg"), ("TIFF", "*.tiff"), ("JPEG-2000", ".jpeg-2000"), ("SVG", ".svg"), ("GIF", ".gif"), ("BMP", ".bmp"), ("All files", ".*")])

    # ensure a file path was selected
    if len(path) > 0:
        # load the image from disk, convert it to grayscale
        currImage = cv.imread(path, cv.IMREAD_UNCHANGED)

        # OpenCV represents images in BGR order; however PIL represents
        # images in RGB order, so we need to swap the channels
        currImage = cv.cvtColor(currImage, cv.COLOR_BGR2RGB)

        width = 440
        height = int((currImage.shape[0]/currImage.shape[1])*440)
        dimension = (width, height)

        currImage = cv.resize(currImage, dimension, interpolation= cv.INTER_AREA)
        effect = currImage

        # convert the images to PIL format...
        img = Image.fromarray(currImage)
        effect = Image.fromarray(effect)
        
        # ...and then to ImageTk format
        img = ImageTk.PhotoImage(img)
        effect = ImageTk.PhotoImage(effect)

        # if the panels are None, initialize them
        if panelA is None or panelB is None:
            panelA = Label(image=img)
            panelA.image = img
            panelA.pack(side="left", padx=10, pady=10)

            panelB = Label(image=effect)
            panelB.image = effect
            panelB.pack(side="right", padx=10, pady=10)
            
            clear.pack(side="bottom")

        else :
            panelA.configure(image=img)
            panelB.configure(image=effect)
            panelA.image = img
            panelB.image = effect

def sampling():
    global currImage, my_label

    image = np.array(currImage)
    image = cv.pyrDown(currImage)
    dim   = ((currImage.shape[1]), currImage.shape[0])
    image = cv.resize(image, dim, interpolation = cv.INTER_AREA)
    my_label = Label(root, text = "Sampling Berhasil Di Tambahkan!")
    my_label.pack()
    root.title("Sampling")
    return image

def bw():
    global currImage, my_label

    image = np.array(currImage)
    image= cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    my_label = Label(root, text = "Black and White Berhasil Di Tambahkan!")
    my_label.pack()
    root.title("Black and White")

    return image

def quantize():
    global currImage,my_label

    quantize_value = simpledialog.askinteger("Quantize Input", "Input", minvalue=0, maxvalue=256)
    image = np.array(currImage)
    image = Image.fromarray(currImage) 
    image = image.quantize(quantize_value)
    my_label = Label(root, text = "Quantize Berhasil Di Tambahkan!")
    my_label.pack()
    root.title("Quantization")
    return image
    
    
def negative():
    global currImage,my_label

    image = np.array(currImage) 
    image = 255-currImage
    my_label = Label(root, text = "Negative Berhasil Di Tambahkan!")
    my_label.pack()
    root.title("Negative")
    return image

def intensity():
    global currImage, my_label
    value = simpledialog.askinteger("Intensity Input", "Input", minvalue=0, maxvalue=254)
    image = np.array(currImage)
    for k in range(0,value):
        image[:,:] = np.where(image[:,:]* 1.03 < 255, (image[:,:] * 1.03).astype(np.uint8) , image[:,:])
    my_label = Label(root, text = "Intensitas Berhasil Di Tambahkan!")
    my_label.pack()
    root.title("Intensity")

    return image

def rgb():
    global currImage, my_label

    v = IntVar()
    
    def sel(value):  # pass new scale value
        blue = int(scale1.get())
        value = blue
        return value
    
    scale1 = Scale(root, from_=50, to=255, orient=HORIZONTAL, variable=v, command=sel)
    blue = int(scale1.get())
    scale1.pack()
    scale2 = Scale(root, from_=0, to=255,orient=HORIZONTAL)
    green = int(scale2.get())
    scale2.pack()
    scale3 = Scale(root, from_=0, to=255,orient=HORIZONTAL)
    red = int(scale3.get())
    scale3.pack()
    B,G,R = cv.split(currImage)
    image = np.array(currImage)
    image = cv.merge([B+60,G+30,R+100])

    button = Button(root, text="Submit", command=sel)
    button.pack()
    my_label = Label(root, text = "RGB Berhasil Di Tambahkan!")
    my_label.pack()
    root.title("RGB")
    return image

def applySampling():
    image = np.array(currImage)
    if(effect == 'Sampling'):
        image = sampling(image)
        image = Image.fromarray(image)
    image = sampling()
    image = Image.fromarray(image)  
    image = ImageTk.PhotoImage(image)
    panelB.configure(image=image)
    panelB.image = image

def applyRGB():
    
    image = np.array(currImage)
    if(effect == 'RGB'):
        image = rgb(image)
        image = Image.fromarray(image)
    image = rgb()
    image = Image.fromarray(image)  
    image = ImageTk.PhotoImage(image)
    panelB.configure(image=image)
    panelB.image = image

def applyBW():
    image = np.array(currImage)
    if(effect == 'Black and White'):
        image = bw(image)
        image = Image.fromarray(image)
    image = bw()
    image = Image.fromarray(image)  
    image = ImageTk.PhotoImage(image)
    panelB.configure(image=image)
    panelB.image = image

def applyQuantize():
    image = np.array(currImage)
    if(effect == 'Quantization'):
        image = quantize(image)
        image = Image.fromarray(image)
    image = quantize()
    #image = Image.fromarray(image)  
    image = ImageTk.PhotoImage(image)
    panelB.configure(image=image)
    panelB.image = image


def applyNegative():
    image = np.array(currImage)
    if(effect == 'Negative'):
        image = negative(image)
        image = Image.fromarray(image)
    image = negative()
    image = Image.fromarray(image)  
    image = ImageTk.PhotoImage(image)
    panelB.configure(image=image)
    panelB.image = image

def applyIntensity():
    image = np.array(currImage)
    if(effect == 'Intensity'):
        image = intensity(image)
        image = Image.fromarray(image)
    image = intensity()
    image = Image.fromarray(image)  
    image = ImageTk.PhotoImage(image)
    panelB.configure(image=image)
    panelB.image = image



def menu():
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label='New File')
    filemenu.add_command(label='Open Image', command=select_image)
    filemenu.add_command(label='Save')
    filemenu.add_command(label='Save As')
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label='File', menu=filemenu)

    fileedit = Menu(menubar, tearoff=0)
    fileedit.add_command(label='Sampling', command=applySampling)
    fileedit.add_command(label='Quantization', command = applyQuantize)
    fileedit.add_command(label='Black and White', command = applyBW)
    fileedit.add_command(label='Negative', command=applyNegative)
    fileedit.add_command(label='Intensity', command=applyIntensity)
    fileedit.add_command(label='RGB', command=applyRGB)
    menubar.add_cascade(label='Edit', menu = fileedit)
    root.config(menu=menubar)

    mainloop()

def clearPanel():
    my_label.destroy()
    panelA.image = None
    panelB.image = None

#data = IntVar()
#a = ttk.Entry(root, textvariable=data)
#a.pack()
#b = Button(root, text="Submit", command=quantize)
#b.pack()
clear = Button(root, text="Clear Panel", command=clearPanel)


menu()




