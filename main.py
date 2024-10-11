#imports
from cryptography.fernet import Fernet
import numpy as np
import cv2
import os
 
#key
global key
key = '-' + input() + 'DiALcDU5M-GvUrNBXVyyUaUbpfcgDrBg='
key = Fernet(key) 


#functions
def resize_image(img, target_height=1080):
    # Get original dimensions
    height, width = img.shape[:2]
    
    # Calculate width
    ratio = width / height
    new_width = int(target_height * ratio)
    
    # Resize the image
    img = cv2.resize(img, (new_width, target_height))
    return img

def open_image(list):
    img_amnt = len(list)
    img_number = 0

    img = decrypt("storage/" + list[img_number])

    cv2.namedWindow('ImageViewer', cv2.WINDOW_AUTOSIZE)

    while True:
        cv2.moveWindow("ImageViewer", int(1280-(img.shape[1]/2)), 0)
        cv2.imshow('ImageViewer',img)
    
        k = cv2.waitKey(0)

        if k == 91: #[
            img_number -= 1
            if img_number<0:
                img_number=img_amnt-1
            img = decrypt("storage/" + list[img_number])
        elif k == 93: #]
            img_number += 1
            if img_number > img_amnt-1:
                img_number = img_number - (img_amnt * (img_number // img_amnt))
            img = decrypt("storage/" + list[img_number])
        elif k == 27:  #escape key 
            break
    
    cv2.destroyAllWindows()


def decrypt(image):
    with open (image, "rb") as file:
        f = file.read()
        file.close()

    encrypted = key.decrypt(f)

    nparr = np.fromstring(encrypted, np.uint8)

    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    img = resize_image(img)

    return img

#list of files in folder
templist = os.listdir()

#initialize list
list = []

#remove main.py and storage from list
for i in templist:
    if i!="main.py" and i!="storage":
        list.append(i)

#encrypt new files
for i in list:
    with open (i, "rb") as file:
        f = file.read()
        file.close()
    encrypted = key.encrypt(f)
    j = i.replace(".png", "")
    with open ("storage/" + j, "wb") as file:
        file.write(encrypted)


#newlist
list = os.listdir("storage")

#view image
open_image(list)