#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import wx
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import xlsxwriter

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

def Extract_time(Time_C2, S_ampl_C2, Time_C4, S_ampl_C4, pmnc):

    # Newton's difference table
    diff = []
    for i in range(1, len(S_ampl_C4)):
        diff.append(S_ampl_C4[i] - S_ampl_C4[i-1])
        
    # roundoff the values to remove fluctuations
    diff = np.around( np.array(diff) )
    
    # find delta peaks in difference table
    pks, _ = find_peaks( abs(diff), prominence=4.5)
    
    if diff[pks[0]] < 0:
        
        edge = 'fall'

        # in real scale peaks are at pks + 1 time
        # peaks were trigger started
        down_peak = pks[::2] + 1
        
        # last edge of trigger
        up_peak = pks[1::2]
        
        # Now check if data ends with fall, if yes ignore the last pulse
        if len(down_peak) > len(up_peak):
            down_peak = down_peak[:-1:]
        
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
    
    else:
        
        edge = 'up'
        
        # in real scale peaks are at pks + 1 time
        # peaks were trigger started
        up_peak = pks[::2] + 1
        
        # last edge of trigger
        down_peak = pks[1::2]
        
        # Now check if data ends with up pulse, if yes ignore the last pulse
        if len(up_peak) > len(down_peak):
            up_peak = up_peak[:-1:]
        
        # starting edge
        upEdge = np.array( list(Time_C4[i] for i in up_peak ) )
        
        # ending edge
        downEdge = np.array( list(Time_C4[i] for i in down_peak ) )
        
        # Trigger on time
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
            peksmpl2, _ = find_peaks(ssmpl2, prominence = pmnc)
            
            # time when signal detecting in channel C2
            tdect = list(tsmpl2[i] for i in peksmpl2)
            
            dt = []
            if len(tdect):
                dt = tdect - Time_C4[cycle[0]]
        
            ExtTime.append(dt)
    
    return ExtTime, ONTime, f, edge

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

def Raw_data_plot(FldPth, fileC4, fileC2, pmnc, edge, Time_C2, S_ampl_C2, Time_C4, S_ampl_C4):
    
    # Pulse figure
    peak_C2, _ = find_peaks(S_ampl_C2, prominence = pmnc)          # in C2 channel
    
    if edge == 'fall':
        peak_C4, _ = find_peaks(5-np.array(S_ampl_C4), prominence=4.5) # in C4 channel
    else:
        peak_C4, _ = find_peaks(np.array(S_ampl_C4), prominence=4.5)
    
    plt.plot(Time_C2, S_ampl_C2)
    plt.plot(Time_C4, S_ampl_C4)
    
    # plot the dot on the peak
    plt.plot( list(Time_C2[i] for i in peak_C2), list(S_ampl_C2[i] for i in peak_C2), 'or' )
    plt.plot( list(Time_C4[i] for i in peak_C4), list(S_ampl_C4[i] for i in peak_C4), 'og' )
    
    plt.savefig(r'' + FldPth + '/C4Trace' + str(fileC4) + 'C2Trace' + str(fileC2) + '.jpg')
    plt.close()
    
#%% Cycle plot
    
def Cycle_plot(FldPth, fileC4, fileC2, extraction_time):

    # Dot plot
    fig = plt.figure()

    for i, item in enumerate(extraction_time):
        if len(item) > 0:
            xAxis = [i+1]* len(item)
            plt.scatter(xAxis, item)
    
    plt.grid()
    plt.savefig(r'' + FldPth + '/C4Trace' + str(fileC4) + 'C2Trace' + str(fileC2) + 'cycle.jpg')
    plt.close()

#%% App

class FRS(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Extraction time calculator', 
                          size=(400,568), 
                          style = wx.MINIMIZE_BOX | wx.CLOSE_BOX | wx.CAPTION )
        panel = wx.Panel(self, -1)
        
        self.FoldPath = os.getcwd()
        
        wx.StaticText(panel, -1, 'Browse Folder : ', pos=(10,21))
        self.BrowsFile = wx.Button(panel, -1, 'Browse', pos=(130,16))
        self.BrowsFile.Bind(wx.EVT_BUTTON, self.onOpenFolder)
        
        ln = wx.StaticLine(panel, -1, pos=(10, 10), style= wx.LI_HORIZONTAL)
        ln.SetSize((410,100))
        
        #
        self.op1 = wx.RadioButton(panel, label = 'Select one file',
                                  pos=(10, 69), style = wx.RB_GROUP)
        
        # first file entry
        wx.StaticText(panel, -1, 'File : ', pos=(40, 117))
        self.file_op1 = wx.TextCtrl(panel, -1, '00000', pos=(110, 112))
        
        # Checkbox
        self.cb1 = wx.CheckBox(panel, label = 'Save plot', pos = (40,157))
        self.cbr1 = wx.CheckBox(panel, label = 'Raw plot', pos = (150,157))
        
        # horizontal line between 1st and 2nd option
        ln = wx.StaticLine(panel, -1, pos=(10,136), style= wx.LI_HORIZONTAL)
        ln.SetSize((410,100))
        
        self.op2 = wx.RadioButton(panel, label = 'Ordered files',
                                  pos = (10,196) )
        
        # first file entry
        wx.StaticText(panel, -1, 'From : ', pos=(40, 244))
        self.file1_op2 = wx.TextCtrl(panel, -1, '00000', pos=(110,239))
        
        # last file entry
        wx.StaticText(panel, -1, 'to : ', pos=(230,244))
        self.file2_op2 = wx.TextCtrl(panel, -1, '00000', pos=(270,239))
        
        # Checkbox
        self.cb2 = wx.CheckBox(panel, label = 'Save plot', pos = (40,284))
        self.cbr2 = wx.CheckBox(panel, label = 'Raw plot', pos = (150,284))

        # horizontal line between 2nd and 3rds option
        ln = wx.StaticLine(panel, -1, pos=(10,264), style= wx.LI_HORIZONTAL)
        ln.SetSize((410,100))
        
        self.op3 = wx.RadioButton(panel, label = 'Random files',
                                  pos = (10,324) )
        
        # Checkbox
        self.cb3 = wx.CheckBox(panel, label = 'Save plot', pos = (40,364))
        self.cbr3 = wx.CheckBox(panel, label = 'Raw plot', pos = (150,364))
        
        # horizontal line
        ln = wx.StaticLine(panel, -1, pos=(10,344), style= wx.LI_HORIZONTAL)
        ln.SetSize((410,100))
        
        # prominence
        wx.StaticText(panel, -1, 'Prominence : ', pos=(10,419))
        self.prmnc = wx.TextCtrl(panel, -1, '0.02', pos=(110,414))
        
        ln = wx.StaticLine(panel, -1, pos=(10,410), style= wx.LI_HORIZONTAL)
        ln.SetSize((410,100))
        
        # Calculate button
        self.CalBtn = wx.Button(panel, -1, 'Calculate', pos=(150,484))
        self.CalBtn.Bind(wx.EVT_BUTTON, self.OnClick)

        # Setup
        Icon_Path = os.path.abspath('divsys.png')
        icon = wx.Icon(Icon_Path, wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)

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
        pmnc    = float(self.prmnc.GetValue())
        FldPth  = self.FoldPath
        
        # Create a workbook and add a worksheet.
        workbook = xlsxwriter.Workbook(FldPth + '/Data.xlsx')
        worksheet = workbook.add_worksheet()
        
        Data_columns = (['File C2', 'File C4', 'First ion (ms)', 'Mean (ms)', 'Median (ms)', \
                         'Standard deviation (ms)', 'Extraction time (ms)', \
                         'ON time (ms)', 'Detected frequncy (Hz)', 'Edge', \
                         'Voltage (volt)', 'Temperature (K)', 'Pressure (units)'])
        Write_in_excel(Data_columns, 0, worksheet)
        
        #%% First option
        
        if (option1 == True):
            
            try:      
                # get values form all input area
                file = self.file_op1.GetValue()
    
                Time_C2, S_ampl_C2 = File_handle(FldPth, 'C2Trace' + file + '.txt')    # Detector signal file
                Time_C4, S_ampl_C4 = File_handle(FldPth, 'C4Trace' + file + '.txt')    # Source pulsing file
        
                # calculation of extraction time and on time
                extraction_time, Ton, Freq, edge = Extract_time(Time_C2, S_ampl_C2, Time_C4, S_ampl_C4, pmnc)
                
                # Median of the extration time
                Tmin, Tmean, Tmedian, Tstd = Stat_time(extraction_time)
                
                # Real extrection time
                Textr = Tmedian - np.average(Ton)/2
                
                # write it in a xl file
                Export_data = [file, file, Tmin* 1000, Tmean* 1000, \
                               Tmedian* 1000, Tstd*1000, Textr* 1000, \
                               np.average(Ton)*1000, np.average(Freq), edge]
                Write_in_excel(Export_data, 1, worksheet)
    
                if (self.cbr1.GetValue() == True):
                    Raw_data_plot(FldPth, file, file, pmnc, edge, Time_C2, S_ampl_C2, Time_C4, S_ampl_C4)
                
                if (self.cb1.GetValue() == True):
                    Cycle_plot(FldPth, file, file, extraction_time)
                    
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
            
            try:
                progressMax = len(files)
                
                dialog = wx.ProgressDialog('A progress box', 'Processing file...', progressMax,
                                           style = wx.PD_ELAPSED_TIME)
                
                NextRow = 1
                for file in files:
                    
                    Time_C2, S_ampl_C2 = File_handle(FldPth, 'C2Trace' + str(file) + '.txt')    # Detector signal file
                    Time_C4, S_ampl_C4 = File_handle(FldPth, 'C4Trace' + str(file) + '.txt')    # Source pulsing file
            
                    # calculation of extraction time and on time
                    extraction_time, Ton, Freq, edge = Extract_time(Time_C2, S_ampl_C2, Time_C4, S_ampl_C4, pmnc)
                    
                    # Median of the extration time
                    Tmin, Tmean, Tmedian, Tstd = Stat_time(extraction_time)
                    
                    # Real extrection time
                    Textr = Tmedian - np.average(Ton)/2
                    
                    # write it in a xl file
                    Export_data = [file, file, Tmin* 1000, Tmean* 1000, \
                                   Tmedian* 1000, Tstd*1000, Textr* 1000, \
                                   np.average(Ton)*1000, np.average(Freq), edge]
                    Write_in_excel(Export_data, NextRow, worksheet)
                    
                    if (self.cbr2.GetValue() == True):
                        Raw_data_plot(FldPth, file, file, pmnc, edge, Time_C2, S_ampl_C2, Time_C4, S_ampl_C4)
                    
                    if (self.cb2.GetValue() == True):
                        Cycle_plot(FldPth, file, file, extraction_time)
                    
                    dialog.Update(NextRow, 'Processing: C2Trace' + str(file) + ' and C4Trace' + str(file) )
                    NextRow = NextRow  + 1
                
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
            
            try:
                
                progressMax = len(df.C2)
                
                dialog = wx.ProgressDialog('A progress box', 'Processing file...', progressMax,
                                           style = wx.PD_ELAPSED_TIME)
                
                NextRow = 1
                for fileC2, fileC4 in zip(df.C2, df.C4):
                    
                    fileC2 = f'{fileC2:05}'
                    fileC4 = f'{fileC4:05}'
                    
                    Time_C2, S_ampl_C2 = File_handle(FldPth, 'C2Trace' + str(fileC2) + '.txt')    # Detector signal file
                    Time_C4, S_ampl_C4 = File_handle(FldPth, 'C4Trace' + str(fileC4) + '.txt')    # Source pulsing file
            
                    # calculation of extraction time and on time
                    extraction_time, Ton, Freq, edge = Extract_time(Time_C2, S_ampl_C2, Time_C4, S_ampl_C4, pmnc)
                    
                    # Median of the extration time
                    Tmin, Tmean, Tmedian, Tstd = Stat_time(extraction_time)
                    
                    # Real extrection time
                    Textr = Tmedian - np.average(Ton)/2
                    
                    # write it in a xl file
                    Export_data = [fileC2, fileC4, Tmin* 1000, Tmean* 1000, \
                                   Tmedian* 1000, Tstd*1000, Textr* 1000, \
                                   np.average(Ton)*1000, np.average(Freq), edge]
                    Write_in_excel(Export_data, NextRow, worksheet)
                    
                    if (self.cbr3.GetValue() == True):
                        Raw_data_plot(FldPth, fileC4, fileC2, pmnc, edge, Time_C2, S_ampl_C2, Time_C4, S_ampl_C4)
                    
                    if (self.cb3.GetValue() == True):
                        Cycle_plot(FldPth, fileC4, fileC2, extraction_time)

                    dialog.Update(NextRow, 'Processing: C2Trace' + str(fileC2) + ' and C4Trace' + str(fileC4) )
                    NextRow = NextRow  + 1

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
