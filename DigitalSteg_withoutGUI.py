from PIL import Image
import numpy as np
import cv2


def imgData(image):
                                      #this function returns pixel value of image in form of array
    image = Image.open(image)
    image = np.array(image)
    dataSize = image.shape
    data_1d = image.ravel()
    return dataSize, data_1d

def message(textFile):                      #this function is use to convert text message into ascii - binary

    f = open(textFile, 'r')
    mytext = f.read()
    length = str(bin(len(mytext)))
    length = length[2:].zfill(10)                  # $$$$ by changing the value of Zfill, user can input that number of character
                                                   # $$$$ for eg.  zfill(10) --> 2^10 = 1024 character             
    binarytxt = str(bin(int.from_bytes(mytext.encode(), 'big')))    #8bit
    binarytxt = length + binarytxt[2:]
    binarytxt = [int(x) for x in list(binarytxt)]
    return binarytxt

def evenConvt(value):                            #function converts odd number into even in given range

    value = value + 1
    return max(0, min(254, value))

def oddConvt(value):                             #function converts even number into odd in given range

    value = value + 1
    return max(0, min(255, value))

def encode(imgData , messageData, shape):       #encode message in given image and return staganograpy img

    for i in range(len(messageData)):    
        val = imgData[i] % 2
        if messageData[i] == 1:
            if val == 1: pass
            else: imgData[i] = oddConvt(imgData[i])
        else:
            if val == 0: pass
            else: imgData[i] = evenConvt(imgData[i])
    img_3d = imgData.reshape(shape)
    return img_3d

def decode(imgData):

    image = Image.open(imgData)
    image = np.array(image)
    data_1d = image.ravel()
    strData = ""
    length = ""
    for i in range(10):                                       # $$$$ value of range should be equal to vaue of zfill parameter 
        val = data_1d[i] % 2
        length += str(val)
    length = '0b' + length
    length = int(length,2)
    length_1 = length * 8 + 9 
    for i in range(10, length_1):                       #(number of chracter multiply by 8) minus 1    .... let consider (61 character)*8 minus 1 = 487
        val = data_1d[i] % 2
        strData += str(val)
    strData = '0b' + strData
    n = int(strData, 2)
    asciiData = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
    print(asciiData)

if __name__ == '__main__':                               #Run this 5 line to get stegno image
    #data_Length ,img_Data = imgData('sunFlower.png')
    #message_Data = message('message.txt')
    #img_age = encode(img_Data, message_Data, data_Length)
    #img_age = cv2.cvtColor(img_age, cv2.COLOR_BGR2RGB)
    #cv2.imwrite('result.png', img_age)
                                                        #RUn below line to decode image
    #decode('result.png')
