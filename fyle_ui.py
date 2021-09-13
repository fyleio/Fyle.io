# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 18:04:42 2021

@author: corey
"""

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from os.path import basename, expanduser, isfile, join as joined
from functools import partial
from pathlib import Path
import time
from fyle_backend import Backend

class Application(tk.Frame):
    __name__ = "__main__"
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        master.title('FYLE')
        backend = Backend()
        
        leftConsole = tk.Frame(master)
        leftConsole.grid(row = 1, column = 0, rowspan = 2, sticky = 'NEWS')
        
        self.configureTags = tk.Button(leftConsole, text = 'Define tags',
                                       command = lambda: backend.configureTags())
        self.configureTags.grid(row = 0, sticky = 'NEWS')
        self.loadDirectory = tk.Button(leftConsole, text = 'Load sort folder',
                                       command = lambda: backend.loadDirectory(app = self))
        self.loadDirectory.grid(row = 1, sticky = 'NEWS')
        self.manualTagging = tk.Button(leftConsole, text = 'Manually add tags (Create training dataset)',
                                       command = lambda: backend.manualTagging(app = self))
        self.manualTagging.grid(row = 2, sticky = 'NEWS')
        self.executeModel = tk.Button(leftConsole, text = 'Compile ML Model with sort folder',
                                      command = lambda: backend.modelChain(app = self))
        self.executeModel.grid(row = 3, sticky = 'NEWS')
        self.checkOutput = tk.Button(leftConsole, text = 'Check Model output',
                                     command = lambda: backend.cycleImages(app = self))
        self.checkOutput.grid(row = 4, sticky = 'NEWS')
        
        videoInfo = tk.Frame(master, bg = 'grey32', highlightbackground = '#00CDBC', highlightthickness = 8)
        videoInfo.grid(row = 0, column = 1, sticky = 'NEWS')
        self.filenameLabel = tk.Label(videoInfo, text = 'FILENAME~~~')
        self.filenameLabel.grid(row = 0, column = 0, sticky = 'NEWS')
        self.filenameInfo = tk.Label(videoInfo, text = 'FILE INFO~~~')
        self.filenameInfo.grid(row = 0, column = 1, sticky = 'NEWS')

############################################################################### MEDIA WINDOW
        
        self.videopanel = ttk.Frame(master)
        self.videopanel.grid(row = 1, column = 1)
        self.canvas = tk.Canvas(self.videopanel, bg = 'grey32')
        self.canvas.grid(row = 0, column = 0)

############################################################################### VIDEO CONTROL CONSOLE
        
        videoConsole = tk.Frame(master, bg = 'grey32', highlightbackground = '#00CDBC', highlightthickness = 8)
        videoConsole.grid(row = 2,column = 1, sticky = 'NEWS')
        
        self.play = tk.Button(videoConsole, text = '>',
                              command = lambda: backend.play())        
        self.play.grid(row = 1, column = 0, sticky = 'NEWS')
        self.pause = tk.Button(videoConsole, text = '||',
                               command = lambda: backend.pause())
        self.pause.grid(row = 1, column = 1, sticky = 'NEWS')        
        self.skipAhead = tk.Button(videoConsole, text = '>>',
                                   command = lambda: backend.cycleNext(app = self))
        self.skipAhead.grid(row = 1, column = 2, sticky = 'NEWS')
        self.skipEnd = tk.Button(videoConsole, text = '>|')
        self.skipEnd.grid(row = 1, column = 3, sticky = 'NEWS')
        
        self.volumeVar = tk.IntVar()
        self.volumeSlider = tk.Scale(videoConsole,variable = self.volumeVar, from_ = 0, 
                                     to_ = 100, orient=tk.HORIZONTAL)
        self.volumeSlider.grid(row = 1, column = 4, columnspan = 2, sticky = 'NEWS')
        
        self.mute = tk.Button(videoConsole, text = 'MUTE')
        self.mute.grid(row = 1, column = 6, sticky = 'NEWS')

        self.timeVar = tk.DoubleVar()
        self.timeSliderLast = 0
        self.timeSlider = tk.Scale(videoConsole, variable=self.timeVar,
                                   from_=0, to=1000, orient=tk.HORIZONTAL, length=500,
                                   showvalue=0)                
        self.timeSlider.grid(row = 0, column = 0, columnspan = 7, sticky = 'NEWS')

############################################################################### TAG CONSOLE

        self.tagConsole = tk.Frame(master, bg = 'grey32')
        self.tagConsole.grid(row = 0, column = 2, rowspan = 2, sticky = 'NEWS')
        tagLabel = tk.Label(self.tagConsole, text = 'ADD TAGS:', bg = 'grey32', highlightbackground = '#00CDBC', highlightthickness = 8)
        tagLabel.grid(row = 0, column = 0, columnspan = 2, sticky = 'NEWS')
        
root = tk.Tk()
root.configure(bg = 'black')
app = Application(master=root)
app.master.configure(background = 'gray63', highlightbackground = 'black')
app.mainloop()