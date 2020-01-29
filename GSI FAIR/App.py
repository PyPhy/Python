#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import wx
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import xlsxwriter

plt.switch_backend('Agg')

#%% File reader

def File_handle(file):
    
    # First read file
    file = open(file, 'r')
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

def Extract_time(Time_C2, S_ampl_C2, Time_C4, S_ampl_C4, pmnc):
    
    # Newton's difference table
    diff = []
    for i in range(1, len(S_ampl_C4)):
        diff.append(S_ampl_C4[i] - S_ampl_C4[i-1])
        
    # roundoff the values to remove fluctuations
    diff = np.around( np.array(diff) )
    
    # find delta peaks in difference table
    pks, _ = find_peaks( abs(diff), prominence=4.5)
    
    # in real scale peaks are at pks + 1 time
    # peaks were trigger started
    down_peak = pks[::2] + 1
    
    # last edge of trigger
    up_peak = pks[1::2]
    
    # starting edge
    downEdge = np.array( list(Time_C4[i] for i in down_peak ) )
    
    # ending edge
    upEdge = np.array( list(Time_C4[i] for i in up_peak ) )
    
    # Trigger on time
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
        peksmpl2, _ = find_peaks(ssmpl2, prominence = pmnc)
        
        # time when signal detecting in channel C2
        tdect = list(tsmpl2[i] for i in peksmpl2)
        
        dt = []
        if len(tdect):
            dt = tdect - Time_C4[cycle[0]]
    
        ExtTime.append(dt)
    
    return ExtTime, ONTime, f

#%% Median
    
def Stat_time(ext_time):
    
    flat_list = []
    for sublist in ext_time:
        for item in sublist:
            flat_list.append(item)
        
    return min(flat_list), np.mean(flat_list), np.median(flat_list), np.std(flat_list)

#%% write in excel file
 
def Write_in_excel(Data, row, worksheet):

    col = 0    
    for item in (Data):
        worksheet.write(row, col, item)
        col += 1

#%% Raw data plot

def Raw_data_plot(fileC4, fileC2, pmnc, Time_C2, S_ampl_C2, Time_C4, S_ampl_C4):
    
    # Pulse figure
    peak_C2, _ = find_peaks(S_ampl_C2, prominence = pmnc)          # in C2 channel
    peak_C4, _ = find_peaks(5-np.array(S_ampl_C4), prominence=4.5) # in C4 channel
    
    plt.plot(Time_C2, S_ampl_C2)
    plt.plot(Time_C4, S_ampl_C4)
    
    # plot the dot on the peak
    plt.plot( list(Time_C2[i] for i in peak_C2), list(S_ampl_C2[i] for i in peak_C2), 'or' )
    plt.plot( list(Time_C4[i] for i in peak_C4), list(S_ampl_C4[i] for i in peak_C4), 'og' )
    
    plt.savefig('C4Trace' + str(fileC4) + 'C2Trace' + str(fileC2) + '.jpg')
    plt.close()
    
#%% Cycle plot
    
def Cycle_plot(fileC4, fileC2, extraction_time):

    # Dot plot
    fig = plt.figure()

    for i, item in enumerate(extraction_time):
        if len(item) > 0:
            xAxis = [i+1]* len(item)
            plt.scatter(xAxis, item)
    
    plt.grid()
    plt.savefig('C4Trace' + str(fileC4) + 'C2Trace' + str(fileC2) + 'cycle.jpg')
    plt.close()

#%% App

class FRS(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Extraction time calculator', 
                          size=(430, 600), 
                          style = wx.MINIMIZE_BOX | wx.CLOSE_BOX | wx.CAPTION )
        panel = wx.Panel(self, -1)
        
        self.op1 = wx.RadioButton(panel, label = 'Select one file',
                                  pos=(10, 12), style = wx.RB_GROUP)
        
        # first file entry
        wx.StaticText(panel, -1, 'File : ', pos=(10 + 30, 60))
        self.file_op1 = wx.TextCtrl(panel, -1, '00000', pos=(100 + 30, 55))
        
        # Checkbox
        self.cb1 = wx.CheckBox(panel, label = 'Save plot', pos = (10 + 30,140))
        self.cbr1 = wx.CheckBox(panel, label = 'Raw plot', pos = (120 + 30,140))
        
        #%% horizontal line between 1st and 2nd option
        
        ln = wx.StaticLine(panel, -1, pos=(10, 120), style= wx.LI_HORIZONTAL)
        ln.SetSize((410,100))
        
        self.op2 = wx.RadioButton(panel, label = 'Ordered files',
                                  pos = (10,180) )
        
        # first file entry
        wx.StaticText(panel, -1, 'From : ', pos=(10 + 30, 228))
        self.file1_op2 = wx.TextCtrl(panel, -1, '00000', pos=(100 + 30, 223))
        
        # last file entry
        wx.StaticText(panel, -1, 'to : ', pos=(220 + 30, 228))
        self.file2_op2 = wx.TextCtrl(panel, -1, '00000', pos=(260 + 30, 223))
        
        # Checkbox
        self.cb2 = wx.CheckBox(panel, label = 'Save plot', pos = (10 + 30,300))
        self.cbr2 = wx.CheckBox(panel, label = 'Raw plot', pos = (120 + 30,300))

        #%% horizontal line between 2nd and 3rds option
        
        ln = wx.StaticLine(panel, -1, pos=(10, 280), style= wx.LI_HORIZONTAL)
        ln.SetSize((410,100))
        
        self.op3 = wx.RadioButton(panel, label = 'Random files',
                                  pos = (10,340) )
        
        # Checkbox
        self.cb3 = wx.CheckBox(panel, label = 'Save plot', pos = (10 + 30,380))
        self.cbr3 = wx.CheckBox(panel, label = 'Raw plot', pos = (120 + 30,380))
        
        #%% horizontal line
        ln = wx.StaticLine(panel, -1, pos=(10, 360), style= wx.LI_HORIZONTAL)
        ln.SetSize((410,100))
        
        # prominence
        wx.StaticText(panel, -1, 'Prominence : ', pos=(10, 430))
        self.prmnc = wx.TextCtrl(panel, -1, '0.01', pos=(110, 425))
        
        #%% Calculate button
        self.CalBtn = wx.Button(panel, -1, 'Calculate', pos=(150, 500))
        self.CalBtn.Bind(wx.EVT_BUTTON, self.OnClick)
        
    def OnClick(self, event):
        
        option1 = self.op1.GetValue()
        option2 = self.op2.GetValue()
        option3 = self.op3.GetValue()
        pmnc    = float(self.prmnc.GetValue())
        
        # Create a workbook and add a worksheet.
        workbook = xlsxwriter.Workbook('Data.xlsx')
        worksheet = workbook.add_worksheet()
        
        Data_columns = (['File', 'First ion (ms)', 'Mean (ms)', 'Median (ms)', 'Standard deviation (ms)', 'Extraction time (ms)', 'ON time (ms)', 'Detected frequncy (Hz)', 'Edge'])
        Write_in_excel(Data_columns, 0, worksheet)
        
        #%% First option
        
        if (option1 == True):
            
            # get values form all input area
            file = self.file_op1.GetValue()
            
            Time_C2, S_ampl_C2 = File_handle('C2Trace' + file + '.txt')    # Detector signal file
            Time_C4, S_ampl_C4 = File_handle('C4Trace' + file + '.txt')    # Source pulsing file
    
            # calculation of extraction time and on time
            extraction_time, Ton, Freq = Extract_time(Time_C2, S_ampl_C2, Time_C4, S_ampl_C4, pmnc)
            
            # Median of the extration time
            Tmin, Tmean, Tmedian, Tstd = Stat_time(extraction_time)
            
            # Real extrection time
            Textr = Tmedian - np.average(Ton)/2
            
            # write it in a xl file
            Export_data = [file, Tmin* 1000, Tmean* 1000, Tmedian* 1000, Tstd*1000, Textr* 1000, np.average(Ton)*1000, np.average(Freq), 'falling']
            Write_in_excel(Export_data, 1, worksheet)

            if (self.cbr1.GetValue() == True):
                Raw_data_plot(file, file, pmnc, Time_C2, S_ampl_C2, Time_C4, S_ampl_C4)
            
            if (self.cb1.GetValue() == True):
                Cycle_plot(file, file, extraction_time)
        
        #%% Second option
        
        if (option2 == True):
            
            # get values form all input area
            frst_file = self.file1_op2.GetValue()
            last_file = self.file2_op2.GetValue()
                     
            files = [f"{i:05}" for i in range(int(frst_file), int(last_file) + 1)]
            
            NextRow = 1
            for file in files:
                
                Time_C2, S_ampl_C2 = File_handle('C2Trace' + str(file) + '.txt')    # Detector signal file
                Time_C4, S_ampl_C4 = File_handle('C4Trace' + str(file) + '.txt')    # Source pulsing file
        
                # calculation of extraction time and on time
                extraction_time, Ton, Freq = Extract_time(Time_C2, S_ampl_C2, Time_C4, S_ampl_C4, pmnc)
                
                # Median of the extration time
                Tmin, Tmean, Tmedian, Tstd = Stat_time(extraction_time)
                
                # Real extrection time
                Textr = Tmedian - np.average(Ton)/2
                
                # write it in a xl file
                Export_data = [file, Tmin* 1000, Tmean* 1000, Tmedian* 1000, Tstd*1000, Textr* 1000, np.average(Ton)*1000, np.average(Freq), 'falling']
                Write_in_excel(Export_data, NextRow, worksheet)
                NextRow = NextRow  + 1
                
                if (self.cbr2.GetValue() == True):
                    Raw_data_plot(file, file, pmnc, Time_C2, S_ampl_C2, Time_C4, S_ampl_C4)
                
                if (self.cb2.GetValue() == True):
                    Cycle_plot(file, file, extraction_time)
        
        #%% Third option
        
        if (option3 == True):
            
            df = pd.read_csv('ListRandom.txt', delim_whitespace = True )
            
            NextRow = 1
            for fileC2, fileC4 in zip(df.C2, df.C4):
                
                Time_C2, S_ampl_C2 = File_handle('C2Trace' + str(fileC2) + '.txt')    # Detector signal file
                Time_C4, S_ampl_C4 = File_handle('C4Trace' + str(fileC4) + '.txt')    # Source pulsing file
        
                # calculation of extraction time and on time
                extraction_time, Ton, Freq = Extract_time(Time_C2, S_ampl_C2, Time_C4, S_ampl_C4, pmnc)
                
                # Median of the extration time
                Tmin, Tmean, Tmedian, Tstd = Stat_time(extraction_time)
                
                # Real extrection time
                Textr = Tmedian - np.average(Ton)/2
                
                # write it in a xl file
                Export_data = [file, Tmin* 1000, Tmean* 1000, Tmedian* 1000, Tstd*1000, Textr* 1000, np.average(Ton)*1000, np.average(Freq), 'falling']
                Write_in_excel(Export_data, NextRow, worksheet)
                NextRow = NextRow  + 1
                
                if (self.cbr3.GetValue() == True):
                    Raw_data_plot(fileC4, fileC2, pmnc, Time_C2, S_ampl_C2, Time_C4, S_ampl_C4)
                
                if (self.cb3.GetValue() == True):
                    Cycle_plot(fileC4, fileC2, extraction_time)
        
        # Close the excel file now
        workbook.close()
        
        # close the window on the completion of calculation
        self.Close()

#%%

if __name__ == '__main__':
    
    app = wx.App(False)
    frame = FRS()
    frame.Show()
    app.MainLoop()
