# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 02:51:08 2020

@author: NicoS
"""
import numpy as np

def openfile(filename,fileformat):
    '''opens a binary file in desired format and returns it in float'''
    with open((filename), 'rb') as fr:
        data = np.fromfile(fr, dtype=fileformat)
        data = np.array(data, dtype=float)
    return data
    
def savebinaryfile(filename,filedata):
    with open(filename,'wb') as writer:
        writer.write(filedata)
        
def savenumpy(filename,nparray):
    np.savez_compressed(filename,Map=nparray)
    
def readnumpy(name):
    icemap = np.load(name)
    icemap = np.array(icemap['Map'], dtype=float)
    return icemap
            
def csv_columnexport(filename,filedata):
    np.savetxt(filename, np.column_stack((filedata)), delimiter=",", fmt='%s')
    
def csv_rowexport(filename,filedata):
    np.savetxt(filename, np.row_stack((filedata)), delimiter=",", fmt='%s')
    
class CryoDate:
    def __init__  (self,year=2000,month=1,day=1):
        self.year = year
        self.month = month
        self.day = day
        self.strMonth = str(self.month).zfill(2)
        self.strDay = str(self.day).zfill(2)
        self.datestring = f'{self.year}{self.strMonth}{self.strDay}'
    def datecalc(self):
        ''' calculates the day-month for a 366 day year'''
        self.day += 1
        if self.day==32 and (self.month==1 or self.month==3 or self.month==5 or self.month==7 or self.month==8 or self.month==10):
            self.day=1
            self.month += 1
        elif self.day==31 and (self.month==4 or self.month==6 or self.month==9 or self.month==11):
            self.day=1
            self.month += 1
        elif self.day==30 and self.month==2:
            self.day=1
            self.month += 1
        elif  self.day==32 and self.month == 12:
            self.day = 1
            self.month = 1
            self.year +=1
        self.strMonth = str(self.month).zfill(2)
        self.strDay = str(self.day).zfill(2)
        self.datestring = f'{self.year}{self.strMonth}{self.strDay}'