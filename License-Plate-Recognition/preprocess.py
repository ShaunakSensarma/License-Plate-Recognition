# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 19:48:17 2021

@author: Shaunak_Sensarma
"""

from skimage.io import imread
from skimage.filters import threshold_otsu
from skimage import measure
from skimage.transform import resize
import matplotlib.patches as patches
import plotting
import numpy as np
import matplotlib.pyplot as plt

class Preprocess():
    def __init__(self,image_path):
        self.car_image = imread(image_path, as_gray=True)*255
        threshold_value = threshold_otsu(self.car_image)
        self.binary_car_image = self.car_image > threshold_value
        self.fig,(self.axis,self.axis1)=plotting.gen_plot(2,1)
        
        
        
        
        
        
#LICENSE PLATE DETECTION
    #  heuristics for license plate dimensions
    # height of plate is within [5-20]% of image height and width within [15-60]% of image_width
    # region area >50
    # plate height more than 20% plate_width
    # sum of pixels in plate greater than 60 % of total pixels
    # only 10 cc in actual plate
    


    def plate_detection(self):    
        label_image = measure.label(self.binary_car_image)
        image_height,  image_width=label_image.shape                  
        plate_dim=(0.05*image_height,0.2*image_height,0.15*image_width,0.6*image_width)
        
        plotting.plot_car_image(self.car_image,self.fig,self.axis)

        self.lp_cands=[]
        self.lp_cand_dimension=[]
        for region in measure.regionprops(label_image):
            minRow, minCol, maxRow, maxCol = region.bbox
            (region_height,region_width)=(maxRow-minRow,maxCol-minCol)
            
            if(region.area < 50 or region_height<0.2*region_width ):
                continue
            candidate=np.invert(self.binary_car_image[minRow:maxRow,minCol:maxCol])
            if(region_height>=plate_dim[0] and region_height <=plate_dim[1] and region_width>=plate_dim[2] and region_width<= plate_dim[3]):

                if self.elimininate_candidate(candidate):
                    continue
                
                rectBorder = patches.Rectangle((minCol, minRow), maxCol-minCol, maxRow-minRow, edgecolor="red", linewidth=2, fill=False)
                self.lp_cands.append(candidate)
                self.lp_cand_dimension.append(((minRow,minCol),(maxRow-minRow,maxCol-minCol)))
                plotting.add_borders(rectBorder,self.fig,self.axis) 

    def elimininate_candidate(self,candidate):
        r,c=candidate.shape
        return np.sum(candidate) > 0.3*r*c 







## CHARACTER SEGMENTATION  
##  Heuristics for character
##  character height [35-90]%  and width [2-10]% 

    def character_segmentation(self):
        segmented_characters=[]
        idx=0
        for idx in range(len(self.lp_cands)):
            cand=self.lp_cands[idx]
            plotting.plot_car_image(cand,self.fig,self.axis1)
            char_dim = (0.30*cand.shape[0], 0.90*cand.shape[0], 0.02*cand.shape[1], 0.1*cand.shape[1])
            
            labelled_cand = measure.label(cand)
            cnt=0
            border=[]
            temp_chars=[]
            for region in measure.regionprops(labelled_cand):                         
                minRow, minCol, maxRow, maxCol = region.bbox        
                (region_height,region_width)=(maxRow-minRow,maxCol-minCol)
                if(maxRow==self.lp_cand_dimension[idx][1][0]):
                    continue
                #print(region_height,region_width)
                if(region_height>=char_dim[0] and region_height <=char_dim[1] and region_width>=char_dim[2] and region_width<= char_dim[3]):
                    rectBorder = patches.Rectangle((minCol, minRow), maxCol-minCol, maxRow-minRow, edgecolor="red", linewidth=2, fill=False)
                    border.append(rectBorder)
                    temp_chars.append((minRow,maxRow,minCol,maxCol)) 
                    plotting.add_borders(rectBorder,self.fig,self.axis1)               
            
            
            if(len(border)==10):               
                for borders in border:
                    plotting.add_borders(borders,self.fig,self.axis1)                    
                dim=self.lp_cand_dimension[idx]
                
                for val in temp_chars:
                    r1=dim[0][0]+val[0]
                    r2=dim[0][0]+val[1]
                    c1=dim[0][1]+val[2]
                    c2=dim[0][1]+val[3]
                    segmented_characters.append((val[2],resize(np.invert(self.binary_car_image[r1:r2,c1:c2]),(20,20))))
        return segmented_characters
                    
        
        
    
    
    

if __name__=="__main__":
    env=Preprocess("test_image/car4.jpg")
    env.plate_detection()
    segmented_characters=env.character_segmentation()

   # plotting.show()
   # fig,axis=plt.subplots(1,1)
  #  axis.imshow(segmented_characters[0],cmap="gray")

   # plt.show()