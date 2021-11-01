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
from matplotlib import pyplot as plt



root = Tk()

root.title('191524030 - Muhammad Sakhi Hartanto')


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
    histogram(currImage, image)
    my_label = Label(root, text = "Sampling Berhasil Di Tambahkan!")
    my_label.pack()
    root.title("Sampling")
    return image

def bw():
    global currImage, my_label

    image = np.array(currImage)
    image= cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    #histogram(currImage, image)
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
   # histogram(currImage, image)
    my_label = Label(root, text = "Quantize Berhasil Di Tambahkan!")
    my_label.pack()
    root.title("Quantization")
    return image
    
    
def negative():
    global currImage,my_label

    image = np.array(currImage) 
    image = 255-currImage
    histogram(currImage, image)
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
    
    histogram(currImage, image)
    my_label = Label(root, text = "Intensitas Berhasil Di Tambahkan!")
    my_label.pack()
    root.title("Intensity")

    return image

def rgb():
    global currImage, my_label
    B,G,R = cv.split(currImage)
    red = cv.equalizeHist(R)
    green = cv.equalizeHist(G)
    blue = cv.equalizeHist(B)
    image = np.array(currImage)
    image = cv.merge([blue,green,red])
    histogram(currImage,image)
    my_label = Label(root, text = "RGB Berhasil Di Tambahkan!")
    my_label.pack()
    root.title("RGB")
    return image

def filterLowPass():
    global currImage, my_label
    image = np.array(currImage)
    kernel = np.ones((5,5),np.float32)/25
    image = cv.filter2D(image,-1,kernel)
    histogram(currImage, image)
    my_label = Label(root, text = "Filter Low Pass Berhasil Di Tambahkan!")
    my_label.pack()
    root.title("Low Pass Filter")
    return image

def filterHighPass():
    global currImage, my_label
    image = np.array(currImage)
    kernel = np.array([[0.0, -1.0, 0.0], 
                   [-1.0, 4.0, -1.0],
                   [0.0, -1.0, 0.0]])
    kernel = kernel/(np.sum(kernel) if np.sum(kernel)!=0 else 1)
    image = cv.filter2D(image,-1,kernel)
    histogram(currImage, image)
    my_label = Label(root, text = "Filter High Pass Berhasil Di Tambahkan!")
    my_label.pack()
    root.title("High Pass Filter")
    return image

def filterBandPass():
    global currImage, my_label
    image = np.array(currImage)
    kernel = np.array([[1.0, -2.0, 1.0], 
                   [-2.0, 5.0, -2.0],
                   [1.0, -2.0, 1.0]])
    kernel = kernel/(np.sum(kernel) if np.sum(kernel)!=0 else 1)
    image = cv.filter2D(image,-1,kernel)
    histogram(currImage, image)
    my_label = Label(root, text = "Filter Band Pass Berhasil Di Tambahkan!")
    my_label.pack()
    root.title("Band Pass Filter")
    return image

def histogram(bfr,aft):
    color = ('b','g','r')
    fig,ax = plt.subplots(2,1)
    for i,col in enumerate(color):
        histr = cv.calcHist([bfr],[i],None,[256],[0,256])
        histrAft= cv.calcHist([aft],[i],None,[256],[0,256])
        ax[0].plot(histr, color=col)
        ax[1].plot(histrAft, color=col)
        plt.xlim([0,256])
    plt.show()

    

def fig2img(fig):
    """Convert a Matplotlib figure to a PIL Image and return it"""
    import io
    global edited_image
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    temp = Image.open(buf)
    return temp

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
    if(effect == 'RGB Equalization'):
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

def applyLowPass():
    image = np.array(currImage)
    if(effect == 'Low Pass Filter'):
        image = filterLowPass(image)
        image = Image.fromarray(image)
    image = filterLowPass()
    image = Image.fromarray(image)  
    image = ImageTk.PhotoImage(image)
    panelB.configure(image=image)
    panelB.image = image

def applyHighPass():
    image = np.array(currImage)
    if(effect == 'High Pass Filter'):
        image = filterHighPass(image)
        image = Image.fromarray(image)
    image = filterHighPass()
    image = Image.fromarray(image)  
    image = ImageTk.PhotoImage(image)
    panelB.configure(image=image)
    panelB.image = image


def applyBandPass():
    image = np.array(currImage)
    if(effect == 'Band Pass Filter'):
        image = filterBandPass(image)
        image = Image.fromarray(image)
    image = filterBandPass()
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
    submenu = Menu(fileedit)
    fileedit.add_command(label='Sampling', command=applySampling)
    fileedit.add_command(label='Quantization', command = applyQuantize)
    fileedit.add_command(label='Black and White', command = applyBW)
    fileedit.add_command(label='Negative', command=applyNegative)
    fileedit.add_command(label='Intensity', command=applyIntensity)
    fileedit.add_command(label='RGB Equalization', command=applyRGB)
    submenu.add_command(label = 'Low Pass Filter', command=applyLowPass)
    submenu.add_command(label = 'High Pass Filter', command=applyHighPass)
    submenu.add_command(label = 'Band Pass Filter', command=applyBandPass)
    fileedit.add_cascade(label='Filter', menu = submenu)
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




