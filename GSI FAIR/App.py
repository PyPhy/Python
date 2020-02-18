#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import wx
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import xlsxwriter
from collections import Counter

plt.switch_backend('Agg')

#%% File reader

def File_handle(FldPth, file):
    
    # First read file
    file = open(FldPth + '/' + file, 'r')
    Data = file.read().split('\n')
    file.close()
    
    # Identify from where the data is starting
    Segments    = int( Data[1].split(',')[1] )
    SegmentSize = int( Data[1].split(',')[3] )
    
    # First and Second part are different now
    # pandas library is required for easy column separation
    Time_Chunk   = pd.DataFrame( [item.split(',') for item in Data[3:Segments+3:]] )
    Signal_Chunk = pd.DataFrame( [item.split(',') for item in Data[Segments+3+1::] ] )
    
    # some setting for time chunk
    Time_Chunk = list(Time_Chunk.loc[:,2])          # first select the correct colomn
    Time_Chunk = list(map(float, Time_Chunk))       # now convert it into the float to do math operations
    Time_Chunk = np.repeat(Time_Chunk, SegmentSize) # repeat it to get real time
    
    # remove last line which is NaN
    Signal_Chunk = Signal_Chunk.drop(len(Signal_Chunk)-1)
    
    # Lets add headers to the signal column
    Signal_Chunk.columns = ['Time', 'Ampl']
    
    # as things were in "str" form, we are converting it to "float" to do numeric operation on data
    Signal_Chunk.Time = pd.to_numeric(Signal_Chunk.Time)
    Signal_Chunk.Ampl = pd.to_numeric(Signal_Chunk.Ampl)
    
    #
    Signal_time = list(Signal_Chunk.Time)
    Signal_ampl = list(Signal_Chunk.Ampl)
    
    # Real time (in sample form)
    time = Time_Chunk + Signal_time
    
    return time, Signal_ampl


#%% Extration time function

def Extract_time(Time_C2, S_ampl_C2, Time_C4, S_ampl_C4, pek_mag, method, Manula_Ton_flag, MnTon_val):

    # Newton's difference table
    diff = []
    for i in range(1, len(S_ampl_C4)):
        diff.append(S_ampl_C4[i] - S_ampl_C4[i-1])
        
    # roundoff the values to remove fluctuations
    diff = np.around( np.array(diff) )
    
    # find delta peaks in difference table
    pks = Detect_Peak(method, abs(diff), 4.5)
    
    # File type
    d1 = pks[1] - pks[0]
    d2 = pks[2] - pks[1]
    
    flag = 'Happy_File'
    
    if (d1 > d2):
        flag = 'Sad_File'
    
    if (flag == 'Happy_File'):
    
        if diff[pks[0]] < 0:
            
            edge = 'fall'
    
            # in real scale peaks are at pks + 1 time
            # peaks were trigger started
            down_peak = pks[::2] + 1
            
            # last edge of trigger
            up_peak = pks[1::2] + 1
            
            # Now check if data ends with fall, if yes ignore the last pulse
            if len(down_peak) > len(up_peak):
                down_peak = down_peak[:-1:]
            
            # starting edge
            downEdge = np.array( list(Time_C4[i] for i in down_peak ) )
            
            # ending edge
            upEdge = np.array( list(Time_C4[i] for i in up_peak ) )
            
            # Trigger on time
            if Manula_Ton_flag:
                ONTime = [MnTon_val]
            else:
                ONTime = upEdge - downEdge
            
            # frequency detected
            f = []
            for i in range(1, len(downEdge)):
                f.append(1/ (downEdge[i] - downEdge[i-1]) )
            
            
            ExtTime = []
            
            for epoch in range(1, len(downEdge) + 1):
                
                # Cycle
                if (epoch == len(downEdge) ):
                    cycle = np.arange(down_peak[epoch - 1], len(Time_C4), 1)
                else:
                    cycle = np.arange(down_peak[epoch - 1], down_peak[epoch] + 1, 1)
                
                
                # Now corresponding cycle in C2 could be found as
                tsmpl2 = list(Time_C2[i] for i in cycle)
                ssmpl2 = list(S_ampl_C2[i] for i in cycle)
                
                # signal detection in C2 channel
                peksmpl2 = Detect_Peak(method, ssmpl2, pek_mag)
                
                # time when signal detecting in channel C2
                tdect = list(tsmpl2[i] for i in peksmpl2)
                
                dt = []
                if len(tdect):
                    dt = tdect - Time_C4[cycle[0]]
                    
                    # negative dt belongs to the previous cycle
                    for index, things in enumerate(dt):
                        
                        if (things - ONTime[0]/2) < 0:
                            if (epoch == 1):
                                dt = np.delete(dt, index)
                            else:
                                # in all the case frequency is going to be almost same
                                things = things + (1/f[0])
                                dt[index] = things
            
                ExtTime.append(dt)
        
        else:
            
            edge = 'up'
            
            # in real scale peaks are at pks + 1 time
            # peaks were trigger started
            up_peak = pks[::2] + 1
            
            # last edge of trigger
            down_peak = pks[1::2] + 1
            
            # Now check if data ends with up pulse, if yes ignore the last pulse
            if len(up_peak) > len(down_peak):
                up_peak = up_peak[:-1:]
            
            # starting edge
            upEdge = np.array( list(Time_C4[i] for i in up_peak ) )
            
            # ending edge
            downEdge = np.array( list(Time_C4[i] for i in down_peak ) )
            
            # Trigger on time
            if Manula_Ton_flag:
                ONTime = [MnTon_val]
            else:
                ONTime = downEdge - upEdge
            
            # frequency detected
            f = []
            for i in range(1, len(upEdge)):
                f.append(1/ (upEdge[i] - upEdge[i-1]) )
                
            
            ExtTime = []
            
            for epoch in range(1, len(upEdge) + 1):
                
                # Cycle
                if (epoch == len(upEdge) ):
                    cycle = np.arange(up_peak[epoch - 1], len(Time_C4), 1)
                else:
                    cycle = np.arange(up_peak[epoch - 1], up_peak[epoch] + 1, 1)
                
                
                # Now corresponding cycle in C2 could be found as
                tsmpl2 = list(Time_C2[i] for i in cycle)
                ssmpl2 = list(S_ampl_C2[i] for i in cycle)
                
                # signal detection in C2 channel
                peksmpl2 = Detect_Peak(method, ssmpl2, pek_mag)
                
                # time when signal detecting in channel C2
                tdect = list(tsmpl2[i] for i in peksmpl2)
                
                dt = []
                if len(tdect):
                    dt = tdect - Time_C4[cycle[0]]
                    
                    # negative dt belongs to the previous cycle
                    for index, things in enumerate(dt):
                        
                        if (things - ONTime[0]/2) < 0:
                            if (epoch == 1):
                                dt = np.delete(dt, index)
                            else:
                                # in all the case frequency is going to be almost same
                                things = things + (1/f[0])
                                dt[index] = things
            
                ExtTime.append(dt)
    
    else:
        
        if diff[pks[0]] < 0:
            
            # if we ignore the first peak then its up
            edge = 'up'
            
            # in real scale peaks are at pks + 1 time
            # peaks were trigger started
            # as its sad file of category 'up', down peak comes first
            down_peak = pks[::2] + 1
            
            # last edge of trigger
            up_peak = pks[1::2] + 1
            
            # now get rid of the devil and make it happy_file
            down_peak = down_peak[1:]
            
            # Now check if data ends with up pulse, if yes ignore the last pulse
            if len(up_peak) > len(down_peak):
                up_peak = up_peak[:-1:]
            
            # starting edge
            upEdge = np.array( list(Time_C4[i] for i in up_peak ) )
            
            # ending edge
            downEdge = np.array( list(Time_C4[i] for i in down_peak ) )
            
            # Trigger on time
            if Manula_Ton_flag:
                ONTime = [MnTon_val]
            else:
                ONTime = downEdge - upEdge
            
            # frequency detected
            f = []
            for i in range(1, len(upEdge)):
                f.append(1/ (upEdge[i] - upEdge[i-1]) )
                
            
            ExtTime = []
            
            for epoch in range(1, len(upEdge) + 1):
                
                # Cycle
                if (epoch == len(upEdge) ):
                    cycle = np.arange(up_peak[epoch - 1], len(Time_C4), 1)
                else:
                    cycle = np.arange(up_peak[epoch - 1], up_peak[epoch] + 1, 1)
                
                
                # Now corresponding cycle in C2 could be found as
                tsmpl2 = list(Time_C2[i] for i in cycle)
                ssmpl2 = list(S_ampl_C2[i] for i in cycle)
                
                # signal detection in C2 channel
                peksmpl2 = Detect_Peak(method, ssmpl2, pek_mag)
                
                # time when signal detecting in channel C2
                tdect = list(tsmpl2[i] for i in peksmpl2)
                
                dt = []
                if len(tdect):
                    dt = tdect - Time_C4[cycle[0]]
                    
                    # negative dt belongs to the previous cycle
                    for index, things in enumerate(dt):
                        
                        if (things - ONTime[0]/2) < 0:
                            if (epoch == 1):
                                dt = np.delete(dt, index)
                            else:
                                # in all the case frequency is going to be almost same
                                things = things + (1/f[0])
                                dt[index] = things
            
                ExtTime.append(dt)

        else:
            
            # if we ignore the first peak then its fall
            edge = 'fall'
            
            # in real scale peaks are at pks + 1 time
            # peaks were trigger started
            # as its sad file of category 'fall', up peak comes first
            up_peak = pks[::2] + 1
            
            # last edge of trigger
            down_peak = pks[1::2] + 1
            
            # now get rid of the devil and make it happy_file
            up_peak = up_peak[1:]
            
            # Now check if data ends with fall, if yes ignore the last pulse
            if len(down_peak) > len(up_peak):
                down_peak = down_peak[:-1:]
            
            # starting edge
            downEdge = np.array( list(Time_C4[i] for i in down_peak ) )
            
            # ending edge
            upEdge = np.array( list(Time_C4[i] for i in up_peak ) )
            
            # Trigger on time
            if Manula_Ton_flag:
                ONTime = [MnTon_val]
            else:
                ONTime = upEdge - downEdge
            
            # frequency detected
            f = []
            for i in range(1, len(downEdge)):
                f.append(1/ (downEdge[i] - downEdge[i-1]) )
            
            
            ExtTime = []
            
            for epoch in range(1, len(downEdge) + 1):
                
                # Cycle
                if (epoch == len(downEdge) ):
                    cycle = np.arange(down_peak[epoch - 1], len(Time_C4), 1)
                else:
                    cycle = np.arange(down_peak[epoch - 1], down_peak[epoch] + 1, 1)
                
                
                # Now corresponding cycle in C2 could be found as
                tsmpl2 = list(Time_C2[i] for i in cycle)
                ssmpl2 = list(S_ampl_C2[i] for i in cycle)
                
                # signal detection in C2 channel
                peksmpl2 = Detect_Peak(method, ssmpl2, pek_mag)
                
                # time when signal detecting in channel C2
                tdect = list(tsmpl2[i] for i in peksmpl2)
                
                dt = []
                if len(tdect):
                    dt = tdect - Time_C4[cycle[0]]
                    
                    # negative dt belongs to the previous cycle
                    for index, things in enumerate(dt):
                        
                        if (things - ONTime[0]/2) < 0:
                            if (epoch == 1):
                                dt = np.delete(dt, index)
                            else:
                                # in all the case frequency is going to be almost same
                                things = things + (1/f[0])
                                dt[index] = things
            
                ExtTime.append(dt)
            
    return ExtTime, ONTime, f, edge

#%% Median

def Stat_time(row_time, Ton):
    
    flat_list = []
    for sublist in row_time:
        for item in sublist:
            flat_list.append(item)
    
    # extraction time
    ext_list = np.array(flat_list) - Ton/2
    
    # for scatter plot
    Text_plot = []
    for i in row_time:
        
        if not(len(i)) == False:
            Text_plot.append( list(np.array(i) - Ton/2) )
        else:
            Text_plot.append([])
    
    return min(ext_list), np.mean(ext_list), np.median(ext_list), np.std(ext_list), Text_plot, ext_list

#%% write in excel file
 
def Write_in_excel(Data, row, worksheet):

    col = 0    
    for item in (Data):
        worksheet.write(row, col, item)
        col += 1

#%% Raw data plot

def Raw_data_plot(FldPth, fileC4, fileC2, pek_mag, method, edge, Time_C2, S_ampl_C2, Time_C4, S_ampl_C4):
    
    plt.figure(figsize=(20, 10))
    
    # Pulse figure
    peak_C2 = Detect_Peak(method, S_ampl_C2, pek_mag)          # in C2 channel
    
    if edge == 'fall':
        peak_C4 = Detect_Peak(method, 5-np.array(S_ampl_C4), 4.5) # in C4 channel
    else:
        peak_C4 = Detect_Peak(method, np.array(S_ampl_C4), 4.5)
    
    plt.plot(Time_C2, S_ampl_C2, label = 'C2 channel')
    plt.plot(Time_C4, S_ampl_C4, label = 'C4 channel')

    # plot the dot on the peak
    plt.plot( list(Time_C2[i] for i in peak_C2), list(S_ampl_C2[i] for i in peak_C2), 'or' )
    plt.plot( list(Time_C4[i] for i in peak_C4), list(S_ampl_C4[i] for i in peak_C4), 'og' )
    plt.xlabel('Time (s)', fontsize = 14)
    plt.ylabel('Voltage (V)', fontsize = 14)
    plt.legend()
    
    plt.savefig(r'' + FldPth + '/C4Trace' + str(fileC4) + 'C2Trace' + str(fileC2) + '.jpg')
    plt.close()
    
#%% Cycle plot
    
def Cycle_plot(FldPth, fileC4, fileC2, Text_plot, Tmedian, Tstd, Ton):

    # Dot plot
    plt.figure(figsize=(20, 10))

    for i, item in enumerate(Text_plot):
        if len(item) > 0:
            xAxis = [i+1]* len(item)
            # things are in milli seconds now
            plt.scatter(xAxis, np.array(item)* 1000, alpha = 0.4, color = 'k')
    
    plt.plot([1, xAxis[0]], [Tmedian*1000]*2, 'r', label = 'median(Text) = ' + str( round(Tmedian*1000) ) )
    plt.plot([1, xAxis[0]], [(Tmedian + Tstd)*1000]*2, 'g', label = 'STD(Text) (up) = ' + str( round((Tmedian + Tstd)*1000) ) )
    plt.plot([1, xAxis[0]], [(Tmedian - Tstd)*1000]*2, 'k', label = 'STD(Text) (down) = ' + str( round((Tmedian - Tstd)*1000) ) )
    
    plt.legend(prop={'size':20})
    
    if (xAxis[0] < 20):
        plt.xticks( np.arange(1, xAxis[0] + 1, 1), fontsize = 16 )
    else:
        h = myround( xAxis[0]/ 20, 5)
        plt.xticks( np.arange(1, xAxis[0] + h, h), fontsize = 16)
    
    plt.yticks(fontsize = 16)
    plt.xlabel('Cycles', fontsize = 18)
    plt.ylabel('Textraction (ms)', fontsize = 18)
    plt.grid()
    plt.savefig(r'' + FldPth + '/C4Trace' + str(fileC4) + 'C2Trace' + str(fileC2) + 'cycle.jpg')
    plt.close()

#%% Histogram plot
    
def Histogram_Plot(FldPth, fileC4, fileC2, Flat_formula_list, Tmedian, Tstd, Tmin):
    
    # in Text_plot, Ton is subtracted. which is according to the formulae
    
    plt.figure(figsize=(20, 10))
    
    Data = np.array(Flat_formula_list)* 1000
    plt.hist(Data, bins=np.arange(min(Data), max(Data) + 20, 20)) # 20 ms is the width of bin
    
    # things for ticks
    flat_ext_time = np.sort( np.around( np.array(Flat_formula_list)* 1000 ) )
    rep = Counter(flat_ext_time)
    plt.xticks( list(rep.keys()), fontsize = 16 )
    
    if max(rep.values()) < 25:
        plt.yticks( np.arange(0, max(rep.values()) + 2, 2 ), fontsize = 16 )
    else:
        try:
            h = myround(max(rep.values())/ 25, 5)
            plt.yticks( np.arange(0, max(rep.values()) + h, h), fontsize = 16 )
        except ZeroDivisionError:
            plt.yticks(fontsize = 16)
        
    plt.title('First ion = ' + str( round(Tmin*1000, 2)) + ' (ms), median(Text) = ' + str( round(Tmedian*1000, 2)) + ' (ms), STD(Text) = ' + str( round(Tstd*1000, 2)) + ' (ms)', fontweight = 'bold', fontsize = 20)
    plt.xlabel('Textaction (ms)', fontsize = 18)
    plt.ylabel('Counts', fontsize = 18)
    plt.grid()
    plt.savefig(r'' + FldPth + '/C4Trace' + str(fileC4) + 'C2Trace' + str(fileC2) + 'hist.jpg')
    plt.close()

#%% Round off the number with different base
    
def myround(x, base):
    return base * round(x/base)

#%% Detect peak

def Detect_Peak(method, var, var_val):
    
    if (method == 'height'):
        peaks, _ = find_peaks(var, height = var_val)
    elif (method == 'prominence'):
        peaks, _ = find_peaks(var, prominence = var_val)
    elif (method == 'threshold'):
        peaks, _ = find_peaks(var, threshold = var_val)
    
    return peaks

#%% App

class FRS(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Extraction Time Analyzer', 
                          size=(400,720), 
                          style = wx.MINIMIZE_BOX | wx.CLOSE_BOX | wx.CAPTION )
        panel  = wx.Panel(self, -1)
        
        self.FoldPath = os.getcwd()
        
        wx.StaticText(panel, -1, 'Browse Folder : ', pos=(10,21))
        self.BrowsFile = wx.Button(panel, -1, 'Browse', pos=(130,16))
        self.BrowsFile.Bind(wx.EVT_BUTTON, self.onOpenFolder)
        
        ln = wx.StaticLine(panel, -1, pos=(10, 10), style= wx.LI_HORIZONTAL)
        ln.SetSize((410,100))
        
        #
        self.op1 = wx.RadioButton(panel, label = 'Select file',
                                  pos=(10, 69), style = wx.RB_GROUP)
        
        # manually add Ton
        self.MnTon_1 = wx.CheckBox(panel, label = 'Manual Ton', pos = (150,69))
        self.MnTon_val_1 = wx.TextCtrl(panel, -1, '(ms)', pos=(270,67))
        
        # first file entry
        wx.StaticText(panel, -1, 'File : ', pos=(40, 117))
        self.file_op1 = wx.TextCtrl(panel, -1, '00000', pos=(110, 112))
        
        # Checkbox
        self.cb1 = wx.CheckBox(panel, label = 'Cycle plot', pos = (40,157))
        self.cbr1 = wx.CheckBox(panel, label = 'Raw plot', pos = (150,157))
        self.cbh1 = wx.CheckBox(panel, label = 'Hist plot', pos = (260,157))
        
        # horizontal line between 1st and 2nd option
        ln = wx.StaticLine(panel, -1, pos=(10,136), style= wx.LI_HORIZONTAL)
        ln.SetSize((410,100))
        
        self.op2 = wx.RadioButton(panel, label = 'Ordered files',
                                  pos = (10,196) )
        
        # manually add Ton
        self.MnTon_2 = wx.CheckBox(panel, label = 'Manual Ton', pos = (150,196))
        self.MnTon_val_2 = wx.TextCtrl(panel, -1, 'all/sep (ms)', pos=(270,194))
        
        # first file entry
        wx.StaticText(panel, -1, 'From : ', pos=(40, 244))
        self.file1_op2 = wx.TextCtrl(panel, -1, '00000', pos=(110,239))
        
        # last file entry
        wx.StaticText(panel, -1, 'to : ', pos=(230,244))
        self.file2_op2 = wx.TextCtrl(panel, -1, '00000', pos=(270,239))
        
        # Checkbox
        self.cb2 = wx.CheckBox(panel, label = 'Cycle plot', pos = (40,284))
        self.cbr2 = wx.CheckBox(panel, label = 'Raw plot', pos = (150,284))
        self.cbh2 = wx.CheckBox(panel, label = 'Hist plot', pos = (260,284))

        # horizontal line between 2nd and 3rds option
        ln = wx.StaticLine(panel, -1, pos=(10,264), style= wx.LI_HORIZONTAL)
        ln.SetSize((410,100))
        
        self.op3 = wx.RadioButton(panel, label = 'Random files',
                                  pos = (10,324) )
        
        # manually add Ton
        self.MnTon_3 = wx.CheckBox(panel, label = 'Manual Ton', pos = (150,324))
        
        # Checkbox
        self.cb3 = wx.CheckBox(panel, label = 'Cycle plot', pos = (40,364))
        self.cbr3 = wx.CheckBox(panel, label = 'Raw plot', pos = (150,364))
        self.cbh3 = wx.CheckBox(panel, label = 'Hist plot', pos = (260,364))
        
        # horizontal line
        ln = wx.StaticLine(panel, -1, pos=(10,344), style= wx.LI_HORIZONTAL)
        ln.SetSize((410,100))
        
        # Peak detection method
        wx.StaticText(panel, -1, 'Select the peak detection method...', pos=(10,405))
        
        # height method
        self.Peak_op1 = wx.RadioButton(panel, label = 'Height',
                                       pos=(10, 435), style = wx.RB_GROUP)
        self.hght = wx.TextCtrl(panel, -1, '10', pos=(120,430))
        wx.StaticText(panel, -1, '(mV)', pos=(235,435))
        
        # Prominence method
        self.Peak_op2 = wx.RadioButton(panel, label = 'Prominence',
                                       pos=(10, 467))
        self.pmnc = wx.TextCtrl(panel, -1, '10', pos=(120,465))
        wx.StaticText(panel, -1, '(mV)', pos=(235,470))
        
        # Threshold method
        self.Peak_op3 = wx.RadioButton(panel, label = 'Threshold',
                                       pos=(10, 500))
        self.thrsld = wx.TextCtrl(panel, -1, '10', pos=(120,500))
        wx.StaticText(panel, -1, '(mV)', pos=(235,505))
        
        
        ln = wx.StaticLine(panel, -1, pos=(10,490), style= wx.LI_HORIZONTAL)
        ln.SetSize((410,100))
        
        # Master merger
        self.MasterMerge = wx.CheckBox(panel, label = 'Master Merger Tool \nHelpful when statistics are low', pos = (10,550))

        ln = wx.StaticLine(panel, -1, pos=(10,545), style= wx.LI_HORIZONTAL)
        ln.SetSize((410,100))
        
        # Calculate button
        self.CalBtn = wx.Button(panel, -1, 'Calculate', pos=(30,610))
        self.CalBtn.Bind(wx.EVT_BUTTON, self.OnClick)
        
        # About button
        self.AboutBtn = wx.Button(panel, -1, 'About', pos=(210,610))
        self.AboutBtn.Bind(wx.EVT_BUTTON, self.AboutApp)
        
        # Close button
        self.CloseBtn = wx.Button(panel, -1, 'Close', pos=(300,610))
        self.CloseBtn.Bind(wx.EVT_BUTTON, self.CloseApp)
        
        ln = wx.StaticLine(panel, -1, pos=(10,605), style= wx.LI_HORIZONTAL)
        ln.SetSize((410,100))
        
        # warning
        wx.StaticText(panel, -1, 'CAUTION: Duty cycle must be less than 50%', pos=(10, 665))
        
        # Setup
        Icon_Path = os.path.abspath('divsys.png')
        icon = wx.Icon(Icon_Path, wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)
        
    #%% Close the app
    
    def CloseApp(self, event):
        
        self.Close()
        
    #%% About an app
    
    def AboutApp(self, event):
        
        Document = 'Extraction Time Analyzer\n\n\
By: Divyang R. Prajapati\n\
email: divyangprajapati72@gmail.com\n\
First release: February 15, 2020\n \n\
Extraction Time Analyser is designed to simplify the analysis of extraction time \
for FRS-IC. Three selections Select file, Ordered files, and Random files help \
the user to analyze single or multiple files. The signal detection is the heart\
 of the analysis, that is the reason that three different peak detection methods\
 are provided.\n\n\
For a scientific app, the logo is scientific as well. The logo is the contour map\
 of the magnetic field of the ADITYA-U tokamak. The layout of an app is simple and\
 userfriendly.\n\n\
For the detailed explanation of each section, please refer to my report of the \
Get Involved program. If some bug or error is detected, feel free to contact me \
on the given email-id on the personal info.'
        
        dlg = wx.MessageDialog(None, Document, 'About')
        dlg.ShowModal()

    #%%
    
    def onOpenFolder(self, event):
        
        dlg = wx.DirDialog (None, 'Choose input directory', '',
                            wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        
        if dlg.ShowModal() == wx.ID_OK:
            self.FoldPath = dlg.GetPath()
        
        dlg.Destroy()
    
    #%%
    
    def OnClick(self, event):
        
        option1 = self.op1.GetValue()
        option2 = self.op2.GetValue()
        option3 = self.op3.GetValue()
        FldPth  = self.FoldPath
        MasterMerger = self.MasterMerge.GetValue()

        # peak detection method
        if (self.Peak_op1.GetValue() == True):
            method  = 'height'
            pek_mag = float(self.hght.GetValue())* 1e-3
            
        elif (self.Peak_op2.GetValue() == True):
            method  = 'prominence'
            pek_mag = float(self.pmnc.GetValue())* 1e-3
            
        elif (self.Peak_op3.GetValue() == True):
            method  = 'threshold'
            pek_mag = float(self.thrsld.GetValue())* 1e-3
            
        
        # Create a workbook and add a worksheet.
        workbook = xlsxwriter.Workbook(FldPth + '/Data.xlsx')
        worksheet = workbook.add_worksheet()
        
        Data_columns = (['File C2', 'File C4', 'First ion (ms)', 'Mean (ms)', 'Median (ms)', \
                         'Standard deviation (ms)', 'ON time (ms)', \
                         'Detected frequncy (Hz)', 'Edge', \
                         'Push Volt (mV)', 'Focus Volt (mV)', 'Temperature (K)', 'Pressure (mbar)'])
        Write_in_excel(Data_columns, 0, worksheet)
        
        #%% First option
        
        if (option1 == True):
            
            # Manual Ton
            MnTon_1 = self.MnTon_1.GetValue()
            MnTon_val_1 = ['junk var']
            
            if (MnTon_1 == True): 
                try:
                    # this should be in second as we are calculating things in second not in milli second
                    MnTon_val_1 = float(self.MnTon_val_1.GetValue())* 1e-3
                except ValueError:
                    wx.MessageBox('Ton can not be a string')
                
            try:      
                # get values form all input area
                file = self.file_op1.GetValue()
    
                Time_C2, S_ampl_C2 = File_handle(FldPth, 'C2Trace' + file + '.txt')    # Detector signal file
                Time_C4, S_ampl_C4 = File_handle(FldPth, 'C4Trace' + file + '.txt')    # Source pulsing file
        
                # calculation of extraction time and on time
                Row_time, Ton, Freq, edge = Extract_time(Time_C2, S_ampl_C2, Time_C4, S_ampl_C4, pek_mag, method, MnTon_1, MnTon_val_1)
                
                Ton = np.average(Ton)
                
                # Median of the extration time
                Tmin, Tmean, Tmedian, Tstd, Text_plot, Flat_formula_list = Stat_time(Row_time, Ton)
                
                # write it in a excel file
                Export_data = [file, file, Tmin* 1000, Tmean* 1000, \
                               Tmedian* 1000, Tstd*1000, \
                               Ton*1000, np.average(Freq), edge]
                Write_in_excel(Export_data, 1, worksheet)
    
                if (self.cbr1.GetValue() == True):
                    Raw_data_plot(FldPth, file, file, pek_mag, method, edge, Time_C2, S_ampl_C2, Time_C4, S_ampl_C4)
                
                if (self.cb1.GetValue() == True):
                    Cycle_plot(FldPth, file, file, Text_plot, Tmedian, Tstd, Ton)
                    
                if (self.cbh1.GetValue() == True):
                    Histogram_Plot(FldPth, file, file, Flat_formula_list, Tmedian, Tstd, Tmin)
                
                # Close the excel file now
                workbook.close()
                
                # close the window on the completion of calculation
                self.Close()
            
            except FileNotFoundError:
                
                wx.MessageBox('No file named C2Trace' + file + '.txt or ' + \
                              'C4Trace' + file + '.txt in a given path... \n \n' \
                              + FldPth, 'File Not Found')
                
        #%% Second option
        
        if (option2 == True):
            
            # get values form all input area
            frst_file = self.file1_op2.GetValue()
            last_file = self.file2_op2.GetValue()
            
            files = [f'{i:05}' for i in range(int(frst_file), int(last_file) + 1)]
            
            # Manual Ton
            MnTon_2 = self.MnTon_2.GetValue()
            MnTon_val_2 = ['junk var']* len(files)
            
            if (MnTon_2 == True):
                MnTon_val_2 = self.MnTon_val_2.GetValue().split()
                if MnTon_val_2[0] == 'all':
                    MnTon_val_2 = [ float(MnTon_val_2[1])* 1e-3 ]* len(files)
                elif MnTon_val_2[0] == 'sep':
                    MnTon_val_2 = MnTon_val_2[1].split(',')
                    MnTon_val_2 = [float(itime)* 1e-3 for itime in MnTon_val_2]
            
            try:
                progressMax = len(files)
                
                dialog = wx.ProgressDialog('A progress box', 'Processing file...', progressMax,
                                           style = wx.PD_ELAPSED_TIME)
                
                Master_Extr_List = []
                
                NextRow = 1
                for file in files:
                    
                    Time_C2, S_ampl_C2 = File_handle(FldPth, 'C2Trace' + str(file) + '.txt')    # Detector signal file
                    Time_C4, S_ampl_C4 = File_handle(FldPth, 'C4Trace' + str(file) + '.txt')    # Source pulsing file
            
                    # calculation of extraction time and on time
                    Row_time, Ton, Freq, edge = Extract_time(Time_C2, S_ampl_C2, Time_C4, S_ampl_C4, pek_mag, method, MnTon_2, MnTon_val_2[NextRow-1])
                    
                    Ton = np.average(Ton)
                    
                    if (MasterMerger != True):
                        
                        # Median of the extration time
                        Tmin, Tmean, Tmedian, Tstd, Text_plot, Flat_formula_list = Stat_time(Row_time, Ton)
                                                
                        # write it in a xl file
                        Export_data = [file, file, Tmin* 1000, Tmean* 1000, \
                                       Tmedian* 1000, Tstd*1000, \
                                       Ton*1000, np.average(Freq), edge]
                        Write_in_excel(Export_data, NextRow, worksheet)
                        
                        if (self.cbr2.GetValue() == True):
                            Raw_data_plot(FldPth, file, file, pek_mag, method, edge, Time_C2, S_ampl_C2, Time_C4, S_ampl_C4)
                        
                        if (self.cb2.GetValue() == True):
                            Cycle_plot(FldPth, file, file, Text_plot, Tmedian, Tstd, Ton)
    
                        if (self.cbh2.GetValue() == True):
                            Histogram_Plot(FldPth, file, file, Flat_formula_list, Tmedian, Tstd, Tmin)
                    
                    else:
                        
                        for timings in Row_time:
                            Master_Extr_List.append(timings)
                    
                    dialog.Update(NextRow, 'Processing: C2Trace' + str(file) + ' and C4Trace' + str(file) )
                    NextRow = NextRow  + 1
                
                # Master Merger part finishing
                if (MasterMerger == True):
                    
                    NextRow = 1
                    
                    # Median of the extration time
                    Tmin, Tmean, Tmedian, Tstd, Text_plot, Flat_formula_list = Stat_time(Master_Extr_List, Ton)
                                        
                    file = str(files[0]) + 'to' + str(files[-1])
                    
                    # write it in a xl file
                    Export_data = [file, file, Tmin* 1000, Tmean* 1000, \
                                   Tmedian* 1000, Tstd*1000, \
                                   Ton*1000, np.average(Freq), edge]
                    Write_in_excel(Export_data, NextRow, worksheet)
                    
                    if (self.cb2.GetValue() == True):
                        Cycle_plot(FldPth, file, file, Text_plot, Tmedian, Tstd, Ton)

                    if (self.cbh2.GetValue() == True):
                        Histogram_Plot(FldPth, file, file, Flat_formula_list, Tmedian, Tstd, Tmin)

                # Close the progress bar
                dialog.Destroy()
                
                # Close the excel file now
                workbook.close()
                
                # close the window on the completion of calculation
                self.Close()
            
            except FileNotFoundError:
                
                wx.MessageBox('No file named C2Trace' + file + '.txt or ' + \
                              'C4Trace' + file + '.txt in a given path... \n \n' \
                              + FldPth, 'File Not Found')

            
        #%% Third option
        
        if (option3 == True):
            
            df = pd.read_csv(FldPth + '/ListRandom.txt', delim_whitespace = True )
            
            # Manual Ton
            MnTon_3 = self.MnTon_3.GetValue()
            MnTon_val_3 = ['junk']* len(df.C2)
            
            if (MnTon_3 == True):
                MnTon_val_3 = np.array(df.ManualTon)*1e-3
            
            try:
                
                progressMax = len(df.C2)
                
                dialog = wx.ProgressDialog('A progress box', 'Processing file...', progressMax,
                                           style = wx.PD_ELAPSED_TIME)
                
                Master_Extr_List = []
                
                NextRow = 1
                for fileC2, fileC4 in zip(df.C2, df.C4):
                    
                    fileC2 = f'{fileC2:05}'
                    fileC4 = f'{fileC4:05}'
                    
                    Time_C2, S_ampl_C2 = File_handle(FldPth, 'C2Trace' + str(fileC2) + '.txt')    # Detector signal file
                    Time_C4, S_ampl_C4 = File_handle(FldPth, 'C4Trace' + str(fileC4) + '.txt')    # Source pulsing file
            
                    # calculation of extraction time and on time
                    Row_time, Ton, Freq, edge = Extract_time(Time_C2, S_ampl_C2, Time_C4, S_ampl_C4, pek_mag, method, MnTon_3, MnTon_val_3[NextRow -1])
                    
                    Ton = np.average(Ton)
                    
                    if (MasterMerger != True):
                        
                        # Median of the extration time
                        Tmin, Tmean, Tmedian, Tstd, Text_plot, Flat_formula_list = Stat_time(Row_time, Ton)
                        
                        # write it in a xl file
                        Export_data = [fileC2, fileC4, Tmin* 1000, Tmean* 1000, \
                                       Tmedian* 1000, Tstd*1000, \
                                       Ton*1000, np.average(Freq), edge]
                        Write_in_excel(Export_data, NextRow, worksheet)
                        
                        if (self.cbr3.GetValue() == True):
                            Raw_data_plot(FldPth, fileC4, fileC2, pek_mag, method, edge, Time_C2, S_ampl_C2, Time_C4, S_ampl_C4)
                        
                        if (self.cb3.GetValue() == True):
                            Cycle_plot(FldPth, fileC4, fileC2, Text_plot, Tmedian, Tstd, Ton)
    
                        if (self.cbh3.GetValue() == True):
                            Histogram_Plot(FldPth, fileC4, fileC2, Flat_formula_list, Tmedian, Tstd, Tmin)

                    else:
                        
                        for timings in Row_time:
                            Master_Extr_List.append(timings)

                    dialog.Update(NextRow, 'Processing: C2Trace' + str(fileC2) + ' and C4Trace' + str(fileC4) )
                    NextRow = NextRow  + 1

                # Master Merger part finishing
                if (MasterMerger == True):
                    
                    NextRow = 1
                    
                    # Median of the extration time
                    Tmin, Tmean, Tmedian, Tstd, Text_plot, Flat_formula_list = Stat_time(Master_Extr_List, Ton)
                    
                    file = 'Random'
                    
                    # write it in a xl file
                    Export_data = [file, file, Tmin* 1000, Tmean* 1000, \
                                   Tmedian* 1000, Tstd*1000, \
                                   Ton*1000, np.average(Freq), edge]
                    Write_in_excel(Export_data, NextRow, worksheet)
                    
                    if (self.cb3.GetValue() == True):
                        Cycle_plot(FldPth, file, file, Text_plot, Tmedian, Tstd, Ton)
                    
                    if (self.cbh3.GetValue() == True):
                        Histogram_Plot(FldPth, file, file, Flat_formula_list, Tmedian, Tstd, Tmin)

                # Close the progress bar
                dialog.Destroy()

                # Close the excel file now
                workbook.close()
                
                # close the window on the completion of calculation
                self.Close()

            except FileNotFoundError:
                
                wx.MessageBox('No file named C2Trace' + str(fileC2) + '.txt or ' \
                              + 'C4Trace' + str(fileC4) + '.txt in a given path... \n \n'\
                              + FldPth, 'File Not Found')

#%%

if __name__ == '__main__':
    
    app = wx.App(False)
    frame = FRS()
    frame.Show()
    app.MainLoop()
