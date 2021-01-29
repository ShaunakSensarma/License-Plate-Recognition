# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 10:32:20 2021

@author: Shaunak_Sensarma
"""


import os
import numpy as py
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
import joblib
from skimage.io import imread
from skimage.filters import threshold_otsu

letters=['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F',
         'G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V',
         'W','X','Y','Z'
    ]
