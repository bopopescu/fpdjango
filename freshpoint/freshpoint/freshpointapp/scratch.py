#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 20:50:22 2018

@author: dar.swift
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import seaborn as sns
import numpy as np
import csv
import pprint as pp
import collections



Saleshist = []

fvt_list = [(19,'GREEN ONIONS ',0,0,0,0,0,1,1,1,1,0,0,0,1017596),(12,'CHERRY TOMATOES',0,0,0,0,0,0,1,1,1,1,0,0,1106274),(50,'SPRITE MELONS',0,0,0,0,0,0,1,1,0,0,0,0,1197281),(7,'BROCCOLI',0,0,0,1,1,0,0,0,0,0,0,0,1201376),(24,'INDIA CORN ',0,0,0,0,0,0,0,0,1,1,1,0,1201958),(49,'SPINACH',1,1,1,1,1,0,0,0,0,1,1,1,1250955),(32,'OKRA',0,0,0,0,0,0,1,1,0,0,0,0,1295483),(54,'SWEET POTATOES',1,1,1,1,1,1,1,1,1,1,1,1,1583974),(45,'ROMAINE',0,0,0,1,1,0,0,0,0,1,1,0,1657272),(10,'CANTALOOPES',0,0,0,0,0,0,1,1,0,0,0,0,1695538),(42,'PUMPKINS',0,0,0,0,0,0,0,0,1,1,0,0,1840745),(31,'NECTARINES',0,0,0,0,0,0,1,1,0,0,0,0,1893549),(26,'LETTUCE',0,0,0,1,1,0,0,0,0,1,1,1,1910007),(16,'EGGPLANT',0,0,0,0,0,1,1,1,0,0,0,0,1921959),(44,'RASPBERRIES',0,0,0,0,0,1,0,0,1,1,0,0,1925689),(23,'HONEYDEW MELONS',0,0,0,0,0,0,1,1,0,0,0,0,2035329),(15,'CUCUMBERS',0,0,0,0,0,1,1,1,1,1,1,0,2125830),(2,'ASPARAGUS',0,0,1,1,0,0,0,0,0,0,0,0,2289502),(39,'PERSIMONS',0,0,0,0,0,0,0,0,1,1,0,0,2361346),(4,'BLACKBERRIES',0,0,0,0,0,1,1,0,1,0,0,0,2497648),(1,'APPLES ',1,1,0,0,0,0,0,1,1,1,1,1,2557119),(21,'GREENS',0,0,1,1,1,1,1,1,1,1,1,1,2621525),(53,'SWEET CORN',0,0,0,0,0,1,1,1,1,0,0,0,2834656),(27,'MUSCADINE GRAPES',0,0,0,0,0,0,0,1,1,1,0,0,2845392),(43,'RADISHES',0,0,0,1,1,1,0,0,0,1,1,0,2946537),(11,'CARROTS',1,0,0,0,0,1,1,0,0,0,0,1,2953655),(29,'MUSTARD GREENS',0,0,0,1,1,1,0,0,1,1,1,1,2971863),(57,'WATERMELON',0,0,0,0,0,0,1,1,0,0,0,0,2979790),(14,'COLLARDS',1,1,1,1,1,1,1,1,1,1,1,1,3002007),(55,'TOMATOES',0,0,0,0,0,1,1,1,1,1,0,0,3013774),(34,'PEACHES',0,0,0,0,0,1,1,1,1,0,0,0,3058103),(20,'GREENS PEAS',0,0,0,0,1,0,0,0,0,0,0,0,3304894),(5,'BLUEBERRIES',0,0,0,0,1,1,1,0,0,0,0,0,3412757),(13,'CHRISTMAS TREES',0,0,0,0,0,0,0,0,0,0,1,1,3442780),(3,'BEETS',0,0,0,0,1,1,0,0,0,1,1,1,3509996),(46,'SNAP BEANS',0,0,0,0,0,1,1,1,1,0,0,0,3555013),(35,'PEANUTS',1,1,1,1,1,1,1,1,1,1,1,1,3658846),(25,'KALE',0,0,0,0,1,1,0,0,0,1,1,1,3676040),(30,'NAPA',0,0,0,0,1,1,0,0,0,1,1,0,3754851),(9,'CABBAGE',0,0,0,0,1,1,1,1,1,1,1,1,3805072),(6,'BOKCHOY',0,0,0,0,1,1,0,0,0,1,1,1,3810851),(56,'TURNIPS',0,0,0,1,1,1,0,0,0,1,1,1,3838576),(51,'SQUASH-YELLOW',0,0,0,0,1,1,1,1,1,0,0,0,3852220),(8,'BUTTERBEANS',0,0,0,0,0,0,1,1,0,0,0,0,3882505),(41,'POTATOES',0,0,0,0,0,1,1,0,0,0,0,0,3898135),(58,'ZUCCHINI',0,0,0,0,1,1,1,1,1,0,0,0,3981754),(59,'TOMATILLO',0,0,0,0,0,1,1,1,1,1,0,0,3981755),(28,'MUSHROOMS',0,0,1,1,1,1,0,0,1,1,1,0,4067311),(37,'PECANS',0,0,0,0,0,0,0,0,0,0,1,1,4127838),(36,'PEARS',0,0,0,0,0,0,0,1,1,1,0,0,4236146),(17,'FIGS',0,0,0,0,0,0,1,1,1,1,1,1,4335992),(40,'PLUMS',0,0,0,0,0,1,1,1,0,0,0,0,4487531),(52,'STRAWBERRIES',0,0,0,1,1,1,0,0,0,0,0,0,4494988),(48,'SNOW PEAS TIPS',0,0,0,1,1,0,0,0,0,1,1,0,4496223),(38,'PEPPERS',0,0,0,0,0,1,1,1,0,0,0,0,4606080),(33,'ONIONS ',0,0,0,0,0,1,1,0,0,0,0,0,4672570),(47,'SNOW PEAS',0,0,0,0,1,1,0,0,0,1,1,0,4852257),(22,'HERBS',1,1,1,1,1,1,1,1,1,1,1,1,4902192),(18,'GARLIC',0,0,0,0,0,0,1,1,0,0,0,0,4921692)]

column_names = ("ID","Food","January","February","March","April","May","June","July","August","September","October","November","December","ProductID")
fvt_dict = {}
combo_dict = {}
def column(fvt_list, colnum):
    return ([row[colnum] for row in fvt_list])

for y in range(len(column_names)):
    fvt_dict[column_names[y]] = column(fvt_list, y)

for y in range(len(column_names)):
    if column_names[y] != "ID" and column_names[y] != "ProductID":
        #print (column_names[y])
        combo_dict[column_names[y]] = column(fvt_list, y)
print (fvt_dict)
#ordered_data = collections.OrderedDict(fvt_dict)
#print (ordered_data)
csvfile = open("""/Users/Dasani/Desktop/Ufoods Csv's/aggiecsvdata utf-8/Complete_WWdata.csv""", 'rt')
#print (csvfile)
reader = csv.DictReader(csvfile)
it = 0
for row in reader:

    it+=1
    #Saleshist.append(row['FPITEM'])
    Saleshist.append(row)
    #if it >= 2: break

Saleshist.append(ordered_data)
#print(sorted(Saleshist, key=lambda x:sorted(x.keys())))
for rowidx, row in enumerate(Saleshist):
#print (rowidx,' / ' , row, '\n')
# still need to get all required fields and correctly process w/ heatmap algorithm.

# how to do fuzzy match algorithm??? or make a matcher for words from data analysis







FVT = pd.DataFrame(combo_dict)

#print (FVT)

transFVT = FVT.set_index('Food').T
#print (transFVT)
for fvtindex, fvtrow in transFVT.iterrows():
    for product in fvtrow.index:
        #print ('fvtindex: ',fvtindex,'|product: ', product,'|fvtrow[product]: ', fvtrow[product])
        fvtProduct = product
        fvtMonth = fvtindex
        fvtAvailability = fvtrow[product]
        #print (fvtProduct, ' / ', fvtMonth, ' / ', fvtAvailability)

csvfile.close
