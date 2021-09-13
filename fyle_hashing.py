# -*- coding: utf-8 -*-
"""
Created on Thu May 13 17:28:59 2021

@author: corey
"""

from imutils import paths
import numpy as np
import argparse
import cv2
import os


dataset = r'G:\jpg'

def dhash(image, hashSize=8):
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (hashSize + 1, hashSize))
        diff = resized[:, 1:] > resized[:, :-1]
        return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])
    except:
        pass

hashes = {}
for imagePath in os.listdir(dataset):
    print('HASHING:     ', imagePath)
    image = cv2.imread(imagePath)
    h = dhash(image)
    p = hashes.get(h, [])
    p.append(imagePath)
    hashes[h] = p
    
for (h, hashedPaths) in hashes.items():
    print('COLLECTING:        ',hashedPaths)
    print('H TYPE:', type(h))
    print('HASHEDPATH TYPE:', type(hashedPaths))
    if len(hashedPaths) > 1:

        montage = None
        for p in (hashedPaths):
            print(p)
            image = cv2.imread(p)
            image = cv2.resize(image, (150, 150))
            if montage is None:
                montage = image
            else:
                montage = np.hstack([montage, image])
        print("[INFO] hash: {}".format(h))
        cv2.imshow("Montage", montage)
        cv2.waitKey(0)
            
            