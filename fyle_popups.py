# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 23:37:18 2021

@author: corey
"""

import tkinter as tk
import pickle
import pandas as pd
# import partial

class ConfigureTags(object):
    __name__ = "__main__"
    def __init__(self, master=None):
        super().__init__()
        self.master = master
        
        configTags= tk.Toplevel()
        directions = tk.Label(configTags, text = 'Enter a new sortable tag')
        directions.grid(row = 0, column = 0, columnspan = 2)
        self.newTagEntry = tk.Entry(configTags)
        self.newTagEntry.grid(row = 1, column = 0)
        addNew = tk.Button(configTags, text = '+', command = lambda: self.addNew())
        addNew.grid(row = 1, column = 1)
        acceptTags = tk.Button(configTags, text = "Accept and save", command = lambda: self.acceptTags())
        acceptTags.grid(row = 2, column = 0, columnspan = 2, sticky = "NEWS")
        
        self.tagListFrame = tk.Frame(configTags, bg = 'grey32')
        self.tagListFrame.grid(row = 2, column = 0, columnspan = 2, sticky = 'NEWS')
        tagListLabel = tk.Label(self.tagListFrame, text = 'Current sort tags:')
        tagListLabel.grid(row = 0, column = 0, columnspan = 2, sticky = 'NEWS')
        
        try:
            print('Attempting to unpickle tag DF...')
            self.tags = pd.read_pickle("tags.p")
        except:
            print('Creating new tag DF...')
            self.tags = pd.DataFrame(columns = ['tag'])
            print(self.tags)
        index = 1    
        for tag in self.tags['tag']:
            print(index)
            self.addToList(tag, index)
            index+= 1
            
    def addToList(self, tag, index):
        print(tag)
        tagLabel = tk.Label(self.tagListFrame, name = tag, text = (str(index) + '   ' + str(tag)))
        tagLabel.grid(row = index, column = 0, sticky = 'NEWS')
        btnName = str(tag) + 'Button'
        removeTag = tk.Button(self.tagListFrame, text = '-', name = btnName, command = lambda: self.removeTag(tag, self.tagListFrame.nametowidget(tag),self.tagListFrame.nametowidget(btnName)))
        removeTag.grid(row = index, column = 1, sticky = 'NEWS')
        
    def addNew(self):
        # self.tags = self.tags.append(pd.Series([tag]), ignore_index=True)
        tag = self.newTagEntry.get()
        print(tag)
        self.tags.loc[len(self.tags.index)] = tag 
        print(self.tags)
        self.tags.to_pickle("tags.p")
        self.addToList(tag, index = len(self.tags))
        self.newTagEntry.delete(0, 'end')
        
    def removeTag(self, tag, lWidget, bWidget):
        dropped = self.tags[self.tags['tag']== tag].index
        self.tags = self.tags.drop(dropped)
        lWidget.destroy()
        bWidget.destroy()
        self.tags.to_pickle("tags.p")
        
        
        