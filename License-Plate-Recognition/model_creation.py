# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 10:32:20 2021

@author: Shaunak_Sensarma
"""


import os
import numpy as np
from sklearn.svm import SVC                                     #for Support Vector Classifier. 
from sklearn.model_selection import cross_val_score             #cross validation for seperating data into train and validation sets.
import joblib
from skimage.io import imread
from skimage.filters import threshold_otsu

#array to store all possible characters of number plate.

letters=['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F',
         'G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V',
         'W','X','Y','Z'
    ]

def read_training_data(training_directory):
    image_data=[]
    target_data=[]
    for each_letter in letters:
        for each in range(10):                              #10 denotes maximum no. of characters of a particular type in training data
            image_path = os.path.join(training_directory, each_letter, each_letter + '_' + str(each) + '.jpg')
            
            #checks for grayscale
            
            img_details = imread(image_path, as_gray=True)
            
            
            # converts each character image to binary image.
            
            binary_image = img_details < threshold_otsu(img_details)      #approximately take a value in the middle of those peaks as threshold value.
            flat_bin_image = binary_image.reshape(-1)
            image_data.append(flat_bin_image)
            target_data.append(each_letter)
            
    return (np.array(image_data), np.array(target_data))


#Performing Cross Validation for dividing data subsets




current_dir = os.path.dirname(os.path.realpath(__file__))
   
print('reading data....')
training_dataset_dir = os.path.dirname(os.path.realpath(__file__))        #getting current path.
training_dataset_dir =training_dataset_dir+"/train20X20"                  #forming training data path.
print(training_dataset_dir)
image_data, target_data = read_training_data(training_dataset_dir)        #directing to method.
print('reading of data is completed')

#performing linear vector classification to find the optimal hyperplane.

svc_model = SVC(kernel='linear', probability=True)              #Linear model.

cross_validation(svc_model, 8, image_data, target_data)         #Number of folds= 8 (optimal=5-10).

print('training model is in progress...')

svc_model.fit(image_data, target_data)


#Saving the trained model in the directory.

import pickle
print("model trained.saving model..")
filename = os.path.dirname(os.path.realpath(__file__))+"/model.sav"
pickle.dump(svc_model, open(filename, 'wb'))
print("model saved")
