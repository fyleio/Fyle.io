# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 20:43:02 2021

@author: corey
"""

import tkinter as tk
from tkinter.filedialog import askdirectory
from os.path import basename, expanduser, isfile, join as joined
from pathlib import Path
import pickle
import os
import pandas as pd
from PIL import Image,ImageTk
from fyle_popups import ConfigureTags
# from fyle_models import fyle_models
from fyle_models import Model
import math
import vlc
import time


class Backend(object):
    __name__ = "__main__"
    def __init__(self, master=None):
        super().__init__()
        self.master = master
        self.loadMasterTable()
        
    def loadMasterTable(self):
        try:
            print('Attempting to unpickle tag DF...')
            self.tags = pd.read_pickle("tags.p")
        except:
            print('Creating new tag DF...')
            configTagsWindow = ConfigureTags()
        # columns = self.tags['tag']    
        try:
            print('Attempting to upickle Database...')
            self.master_table = pd.read_pickle("master_table.p")
            print(self.master_table)
        except:
            print('Creating new Database...')
            self.master_table = pd.DataFrame()
            print(self.master_table)
        
    def loadDirectory(self, app):
        self.sortDir = askdirectory(title='Select Folder to Sort')
        app.filenameLabel.config(text = self.sortDir)
        
        print(self.sortDir)
        for file in os.listdir(self.sortDir):
            self.master_table = self.master_table.append(pd.Series(os.path.join(self.sortDir, file), name = 'file'), ignore_index = True)
        self.master_table.columns = ['file']
        print(self.master_table)
        pickle.dump(self.master_table, open("master_table.p", "wb"))

############################################################################### COMPILE DATASET WITH MACHINELEARNING MODELS

    def modelChain(self, app):
        tagModels = [('toon_bin', 'toon', 'photo'),                     
                     ('toonp_bin', 'toon penis', 'toon no_penis'),
                     ('p_bin', 'penis (1)', 'no_penis (1)'),
                     ('p2_bin', 'penis (2)', 'no_penis (2)'),
                     ('p3_bin', 'penis(3)', 'no_penis (3)'),
                     ('cum_bin', 'cum', 'no_cum')]
        for model in tagModels:
            print(model[0], model[1], model[2])
            newTag = Model.compileData(
                Model, backend = self, directory = self.sortDir,
                binary_step = model[0], 
                binary_0 = model[1], 
                binary_1 = model[2]
                )
            
            self.master_table = self.master_table.merge(newTag, how = 'left', on = 'file')
            print(self.master_table)
            with open('results.csv', 'w') as f:
                self.master_table.to_csv(f, mode = 'a',header = f.tell()==0)
            pickle.dump(self.master_table, open("master_table.p", "wb"))


############################################################################### VLC WINDOW OPERATIONS            


############################################################################### ITERATE THROUGH IMAGES TAGGED BY MACHINE

    def cycleImages(self, app):
        self.master_iter = self.master_table.iterrows()
        self.i, self. row = next(self.master_iter)
        global img
        file = Image.open(self.row[0])
        [imageSizeWidth, imageSizeHeight] = file.size
        newImageSizeWidth = min(int(imageSizeWidth*0.25), 600)
        newImageSizeHeight = min(int(imageSizeHeight*0.25), 600)
        resized = file.resize((newImageSizeWidth, newImageSizeHeight), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(resized)
        app.canvas.create_image(0,0, anchor = 'nw', image = img)
        app.canvas.config(width=newImageSizeWidth, height=newImageSizeHeight)
        app.filenameInfo.config(text = self.row)
        self.addTagButtons(app = app, file = self.row[0])


    def cycleNext(self, app):
        self.i, self.row = next(self.master_iter)                            
        global img                                                                                       
        file = Image.open(self.row[0])                                                            
        [imageSizeWidth, imageSizeHeight] = file.size
        newImageSizeWidth = min(int(imageSizeWidth*0.25), 600)
        newImageSizeHeight = min(int(imageSizeHeight*0.25), 600)
        resized = file.resize((newImageSizeWidth, newImageSizeHeight), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(resized)                                                  
        app.canvas.create_image(0,0, anchor = 'nw', image = img)
        app.canvas.config(width=newImageSizeWidth, height=newImageSizeHeight)
        app.filenameInfo.config(text = self.row)
        self.addTagButtons(app = app, file = self.row[0])
                   
    def addTagButtons(self, app, file):
        index = self.master_table.index[self.master_table['file'] == file]
        row = self.master_table.iloc[index]
        i=0
        for column in row.columns:
            if row[column].item() == 'True':
                print(column)
                app.tagRemove = tk.Button(app.tagConsole, text = column)
                app.tagRemove.grid(column = 0, row = i, sticky = 'NEWS') 
                i+=1
            
        
    def configureTags(self):
        configTagsWindow = ConfigureTags()
        
    def manualTagging(self, app):
        self.tags = pd.read_pickle("tags.p")
        print(self.tags)
        i = 0
        for tag in self.tags['tag']:
            tagBtn = tk.Button(app.tagConsole, name = tag, text = tag.upper(), command = lambda: self.applyTag(tag))
            if (i%2) == 0:
                x = 0
            else:
                x = 1
            tagBtn.grid(column = x, row = math.floor(i/2), sticky = 'NEWS')
            i = i + 1