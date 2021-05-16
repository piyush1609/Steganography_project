from tkinter import *
from PIL import Image
import numpy as np
from cv2 import cv2
# from matplotlib import pyplot as plt
import os

d_path = ""
s_path = ""
dec_path = "" 


def selection():
    p=int(q.get())
    
    if p==1:
        print("You have selected Image")

    elif p==2:
        print("You have selected Video")
        print("Feature not currently available") 

    else :
        print("Invalid Input, run again")
def img_ConvToPNG():

    global s_path,d_path
    s_path=str(l.get())
    d_path=str(m.get()+c.get())
    print(s_path)
    print(d_path)
    
    im=Image.open(s_path)
    im.save(d_path)
def img_details():
    print(d_path)
    im=Image.open(d_path)
    print((im.size))
    w, h = im.size
    print('width: ', w)
    print('height:', h)
def imgData():                         #this function returns pixel value of image in form of array
    a=d_path                         
    global dataSize, data_1d
    image = Image.open(a)

    image = np.array(image)
    dataSize = image.shape
    #data = np.asarray(image)             #3d array into 1d
    data_1d = image.ravel()
    #print(data_1d)
def message():                      #this function is use to convert text message into ascii - binary
    inp=inputtxt.get("1.0","end-1c")
    mytext= inp
    global binarytxt
    length = str(bin(len(mytext)))
    length = length[2:].zfill(10)                  # $$$$ by changing the value of Zfill, user can input that number of character
                                                   # $$$$ for eg.  zfill(10) --> 2^10 = 1024 character             
    binarytxt = str(bin(int.from_bytes(mytext.encode(), 'big')))    #8bit
    binarytxt = length + binarytxt[2:]
    binarytxt = [int(x) for x in list(binarytxt)]
    print(binarytxt)
def evenConvt(value):                            #function converts odd number into even in given range
    value = value + 1
    return max(0, min(254, value))
def oddConvt(value):                             #function converts even number into odd in given range
    value = value + 1
    return max(0, min(255, value))
def encode():                                    #encode message in given image and return staganograpy img

    for i in range(len(binarytxt)):              #need to add error wala function if message value increase the size of img and diffrent encryotion tecnique
        #print(imgData[i])
        val = data_1d[i] % 2
        if binarytxt[i] == 1:
            if val == 1: pass
            else: data_1d[i] = oddConvt(data_1d[i])
        else:
            if val == 0: pass
            else: data_1d[i] = evenConvt(data_1d[i])
    #    print(imgData[i])
    #print(imgData)
    global img_3d
    img_3d = data_1d.reshape(dataSize)

    #img_3d = Image.fromarray(img_3d, 'RGB')
    #print(img_3d)
def decode():
    global dec_path
    dec_path=str(ds.get())
    image = Image.open(dec_path)
    image = np.array(image)
    data_1d = image.ravel()
    strData = ""
    length = ""
    for i in range(10):
        val = data_1d[i] % 2
        length += str(val)
    length = '0b' + length
    length = int(length,2)
    length_1 = length * 8 + 9 
    #print(length_1)
    for i in range(10, length_1):
        val = data_1d[i] % 2
        strData += str(val)

    strData = '0b' + strData
    global asciiData
    #print(strData)
    n = int(strData, 2)
    asciiData = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
    print(asciiData)
    global Decoded_message
    Decoded_message=str(asciiData)
    head_tail = os.path.split(dec_path)
    nice=head_tail[0]+"/DecMessage.txt"
    f11=open(nice,"w")
    f11.write(str(asciiData))
    f11.close()
def save():
    sa= cv2.cvtColor(img_3d,cv2.COLOR_BGR2RGB)
    #cv2.imwrite(c.get(),sa)
    cv2.imwrite(d_path,sa)
def p1():
    selection()
    img_ConvToPNG()
    img_details()
    imgData()
    message()
    encode()
    save()
def p2():
    decode()
    decMessage()    
def encWin():

    
    root=Toplevel(parent)
    root.grab_set() # when you show the popup
    root.geometry("600x500")
    
    global q,l,si_path,di_path,c,m,inp
    
    label1=Label(root,text="Select file format",font=(None,18)).pack()
    q=IntVar()
    Radiobutton(root,text="Image",variable=q,value=1,indicatoron = 0).pack()
    Radiobutton(root,text="Video",variable=q,value=2,indicatoron = 0,state=DISABLED).pack()

    
    label2=Label(root,text="Enter path of source",font=(None,18)).pack()
    l=StringVar()
    si_path=Entry(root,width=80,justify="center",textvariable=l).pack()

    label3=Label(root,text="Enter destination folder path\\",font=(None,18)).pack()
    m=StringVar()
    di_path=Entry(root,width=80,justify="center",textvariable=m).pack()

    label4=Label(root,text="Enter File name of result",font=(None,18)).pack()
    c=StringVar()
    name=Entry(root,width=80,justify="center",textvariable=c).pack()

    label5=Label(root,text="Enter Message",font=(None,18)).pack()
    global inputtxt
    inputtxt =Text(root,height = 10,width = 50)
    inputtxt.pack() 
    
    inp=(inputtxt.get(1.0,"end-1c"))

    Fin_button=Button(root,text="Run",bg='green',width=10,command=p1).place(relx=0.75,rely=0.9)
    #Rs_button=Button(root,text="Clear Input",bg = 'yellow',width=10).place(relx=0.15,rely=0.9)


    root.mainloop()
def decWin():
    root2=Toplevel(parent)
    root2.grab_set() # when you show the popup
    root2.geometry("600x500")

    global dec_path,ds

    label6=Label(root2,text="Enter file image path").pack()
    ds=StringVar()
    dec_source=Entry(root2,width=80,justify="center",textvariable=ds).pack()

    label7=Label(root2,text="The decoded message will be opened in next window and is also saved in same directory as source").pack()
    """ outputtxt =Text(root2,height= 10,width=50).insert(END,asciiData) """
    

    Fin_button2=Button(root2,text="Run",bg='green',width=10,command=p2).place(relx=0.75,rely=0.9)
    #Rs_button2=Button(root2,text="Clear Input",bg = 'yellow',width=10).place(relx=0.15,rely=0.9)
def decMessage():
    root3=Toplevel(parent)
    root3.grab_set()
    root3.geometry("600x500") 
    label8=Label(root3,text="The message",fg='red').pack()
    label9=Label(root3,text=Decoded_message).pack()


parent=Tk()
parent.geometry("300x300")
parent.title("STEGANOGRAPHY")

enc_button=Button(parent,text="Encode",width=10,command=encWin).place(relx=0.5, rely=0.25, anchor=CENTER)
dec_button=Button(parent,text="Decode",width=10,command=decWin).place(relx=0.5, rely=0.75, anchor=CENTER)


parent.mainloop()

