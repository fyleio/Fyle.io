# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 23:48:42 2021

@author: corey
"""

import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import pandas as pd
import os
import csv

class Model(object):
    # __name__ = "__main__"
    def __init__(self):
        super().__init__()
        # self.master = master
        np.set_printoptions(suppress=True)
        
        

    def pipeline(self, file):
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        image = Image.open(file)
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        try:
            data[0] = normalized_image_array

        
            # run the inference
            prediction = self.model.predict(data)
            guesstimate = np.argmax(prediction, axis = None)
            print(file, guesstimate)

            if guesstimate == 0:
                payload = [file, 'True', 'False']
            elif guesstimate == 1:
                payload = [file, 'False', 'True']
            print(payload)
            payload = pd.Series(payload, index = self.df.columns)
            # path = self.directory+file
            # columns = list(self.df)
            # newRow = [path,prediction,self.resultDict[guesstimate]]
            # zipped = zip(columns, newRow)
            # apnd_newRow = dict(zipped)
            # payload = []
            # payload.append(apnd_newRow)
                
            self.df = self.df.append(payload, True)
            return self.resultDict[guesstimate]
        except:
            print(file, 'greyscale?')
            return 'manual'

    def compileData(self, backend, directory, binary_step, binary_0, binary_1):
        modelPath = binary_step + '.h5'
        labelPath = binary_step + '_labels.txt'
        self.model = tensorflow.keras.models.load_model(modelPath)
        self.resultDict = {0: binary_0,
                           1: binary_1
                           }
       
        self.directory =  directory 
        self.testResults = r'test results/'
        self.df = pd.DataFrame(columns = ['file', binary_0, binary_1])
        self.binary_step  = binary_step        
        i = 0
        for file in os.listdir(self.directory):
            print(file)
            if file.endswith('.webp') or file.endswith('.webm') or file.endswith('.mp4'):
                pass
            path = os.path.join(self.directory, file)
            print(path)
            newTag = self.pipeline(self, file = path)
            origin = os.path.join(self.directory, file)
            # try:
            #     os.rename(origin, f"{os.path.join(self.directory, newTag)}{i}.{file.split('.')[-1]}")
            #     i+=1
            # except FileExistsError:
            #     os.rename(origin, f"{os.path.join(self.directory, file)}_{i}.{file.split('.')[-1]}")
            #     i+=1
        backend.df = self.df

        print(backend.df)    
        return backend.df
    
    

