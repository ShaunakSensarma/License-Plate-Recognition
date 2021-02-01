# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 11:58:29 2021

@author: Shaunak_Sensarma
"""


import preprocess
import plotting
import matplotlib.pyplot as plt
import pickle
import os
import sys
import database

model_pat=os.path.dirname(os.path.realpath(__file__))+"/model.sav"
model= pickle.load(open(model_pat,"rb"))

env=preprocess.Preprocess("test_image/car.jpg")
env.plate_detection()
segmented_characters=env.character_segmentation()
plotting.show()
segmented_characters.sort()

ans=[]
for char in segmented_characters:
    #print(plt.imshow(char[1]))
    ans.append(model.predict(char[1].reshape(1,-1)))


license_plate= []
for val in ans:
    license_plate.append(val[0])


for idx in range(len(license_plate)):
    if(idx==0 or idx==1 or idx==4 or idx==5):
        if(license_plate[idx]=='0'):
            license_plate[idx]=str('O')
        elif(license_plate[idx]=='1'):
            license_plate[idx]=str('I')
        elif(license_plate[idx]=='2'):
            license_plate[idx]='Z'
    else:
        if(license_plate[idx]=='O'):
            license_plate[idx]='0'
        elif(license_plate[idx]=='I'):
            license_plate[idx]='1'
        elif(license_plate[idx]=='Z'):
            license_plate[idx]=str('2')
  
license_plate="".join(license_plate)
print("Recognized License Plate is:")
print(license_plate)


if(license_plate==""):
    print("Cannot detect a valid license plate")
    sys.exit()