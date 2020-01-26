#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import wx
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
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
    
def Extract_time(t2, s2, t4, s4, f):
    
    epochs = int(round(t4[-1] - t4[0]))

    tex = []
    ton = [] # this is the on time of pulse (or off time)
    
    for epk in range(1, epochs+1):
        
        cycle = np.where( ( (t4[0] + (epk-1)*f) <= t4) & (t4 <= (t4[0] + epk*f) ) )[0]      # first find the cycle in which trigger pulse is given
        
        tsmpl4 = list(t4[i] for i in cycle)        # now we find the time axis of that cycle
        ssmpl4 = list(s4[i] for i in cycle)        # I'm finding trigger signal from C4 here
        
        tsmpl2 = list(t2[i] for i in cycle)        # now we are selecting data of this cycle from C2 channel
        ssmpl2 = list(s2[i] for i in cycle)
        
        peksmpl4, _ = find_peaks( 5 - np.array(ssmpl4), prominence=4.5)        # then all the points having signal magnitude >4.5
        peksmpl2, _ = find_peaks(ssmpl2, prominence=0.02)                      # searching for the peaks having magnitude greater than 0.02

        tdect = list(tsmpl2[i] for i in peksmpl2)                              # find the location of the signal from the peak
        
        dt = []
        if len(tdect):
            dt = tdect - tsmpl4[peksmpl4[0]] 
        
        tex.append(dt)
        ton.append(tsmpl4[peksmpl4[-1]] - tsmpl4[peksmpl4[0]])
    
    return tex, ton

#%% App

class FRS(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Extraction time calculator', size=(430, 600))
        panel = wx.Panel(self, -1)
        
        self.op1 = wx.RadioButton(panel, label = 'Select one file',
                                  pos=(10, 12), style = wx.RB_GROUP)
        
        # first file entry
        wx.StaticText(panel, -1, 'File : ', pos=(10 + 30, 60))
        self.file_op1 = wx.TextCtrl(panel, -1, '', pos=(100 + 30, 55))
        
        # Frequency
        wx.StaticText(panel, -1, 'Frequency : ', pos=(10 + 30, 100))
        self.frqnc_op1 = wx.TextCtrl(panel, -1, '', pos=(100 + 30, 95))
        
        # Checkbox
        self.cb1 = wx.CheckBox(panel, label = 'Save plot', pos = (10 + 30,140))
        
        #%% horizontal line between 1st and 2nd option
        
        ln = wx.StaticLine(panel, -1, pos=(10, 120), style= wx.LI_HORIZONTAL)
        ln.SetSize((410,100))
        
        self.op2 = wx.RadioButton(panel, label = 'Ordered files',
                                  pos = (10,180) )
        
        # first file entry
        wx.StaticText(panel, -1, 'From : ', pos=(10 + 30, 228))
        self.file1_op2 = wx.TextCtrl(panel, -1, '', pos=(100 + 30, 223))
        
        # last file entry
        wx.StaticText(panel, -1, 'to : ', pos=(220 + 30, 228))
        self.file2_op2 = wx.TextCtrl(panel, -1, '', pos=(260 + 30, 223))
        
        # Frequency
        wx.StaticText(panel, -1, 'Frequency : ', pos=(10 + 30, 268))
        self.frqnc_op2 = wx.TextCtrl(panel, -1, '', pos=(100 + 30, 263))
        
        # Checkbox
        self.cb2 = wx.CheckBox(panel, label = 'Save plot', pos = (10 + 30,300))

        #%% horizontal line between 2nd and 3rds option
        
        ln = wx.StaticLine(panel, -1, pos=(10, 280), style= wx.LI_HORIZONTAL)
        ln.SetSize((410,100))
        
        self.op3 = wx.RadioButton(panel, label = 'Random files',
                                  pos = (10,340) )
        
        # Checkbox
        self.cb3 = wx.CheckBox(panel, label = 'Save plot', pos = (10 + 30,380))
        
        #%% Calculate button
        self.CalBtn = wx.Button(panel, -1, 'Calculate', pos=(150, 500))
        self.CalBtn.Bind(wx.EVT_BUTTON, self.OnClick)
        
    def OnClick(self, event):
        
        option1 = self.op1.GetValue()
        option2 = self.op2.GetValue()
        option3 = self.op3.GetValue()
        
        #%% First option
        
        if (option1 == True):
            
            # get values form all input area
            file = self.file_op1.GetValue()
            f    = float(self.frqnc_op1.GetValue())
            
            C2 = 'C2Trace00' + file + '.txt'
            C4 = 'C4Trace00' + file + '.txt'
            
            Time_C2, S_ampl_C2 = File_handle(C2)    # Detector signal file
            Time_C4, S_ampl_C4 = File_handle(C4)    # Source pulsing file
    
            # calculation of extraction time and on time
            extraction_time, _ = Extract_time(Time_C2, S_ampl_C2, Time_C4, S_ampl_C4, f)
            
            # Save the extraction time
            Close_it = open('ExtrTime.txt', 'w+')
            Close_it.write('file is ' + 'C4 and C2 Trace00' + str(file) + '.txt \n')
            for item in extraction_time:
                Close_it.write("%s\n" % item)
            
            Close_it.close()
                
            if (self.cb1.GetValue() == True):
                
                # Pulse figure
                peak_C2, _ = find_peaks(S_ampl_C2, prominence=0.02)            # in C2 channel
                peak_C4, _ = find_peaks(5-np.array(S_ampl_C4), prominence=4.5) # in C4 channel
                
                plt.plot(Time_C2, S_ampl_C2)
                plt.plot(Time_C4, S_ampl_C4)
                
                # plot the dot on the peak
                plt.plot( list(Time_C2[i] for i in peak_C2), list(S_ampl_C2[i] for i in peak_C2), 'or' )
                plt.plot( list(Time_C4[i] for i in peak_C4), list(S_ampl_C4[i] for i in peak_C4), 'og' )
                
                plt.savefig('C4Trace00' + str(file) + 'C2Trace00' + str(file) + '.jpg')
                plt.close()
                
                # Dot plot
                fig = plt.figure()

                for i, item in enumerate(extraction_time):
                    if len(item) > 0:
                        xAxis = [i+1]* len(item)
                        plt.scatter(xAxis, item)
                
                plt.grid()
                plt.savefig('C4Trace00' + str(file) + 'C2Trace00' + str(file) + 'cycle.jpg')
                plt.close()
        
        #%% Second option
        
        if (option2 == True):
            
            # get values form all input area
            frst_file = self.file1_op2.GetValue()
            last_file = self.file2_op2.GetValue()
            f         = float(self.frqnc_op2.GetValue())
                     
            files = np.arange(int(frst_file), int(last_file) + 1)
            
            Close_it = open('ExtrTime.txt', 'w+')
            for file in files:
                
                C2 = 'C2Trace00' + str(file) + '.txt'
                C4 = 'C4Trace00' + str(file) + '.txt'
                
                Time_C2, S_ampl_C2 = File_handle(C2)    # Detector signal file
                Time_C4, S_ampl_C4 = File_handle(C4)    # Source pulsing file
        
                # calculation of extraction time and on time
                extraction_time, _ = Extract_time(Time_C2, S_ampl_C2, Time_C4, S_ampl_C4, f)
                
                # Save the extraction time
                Close_it.write('\nfile is ' + 'C4 and C2 Trace00' + str(file) + '.txt \n')
                for item in extraction_time:
                    Close_it.write("%s\n" % item)
                    
                if (self.cb2.GetValue() == True):
                    
                    # Pulse figure
                    peak_C2, _ = find_peaks(S_ampl_C2, prominence=0.02)            # in C2 channel
                    peak_C4, _ = find_peaks(5-np.array(S_ampl_C4), prominence=4.5) # in C4 channel
                    
                    plt.plot(Time_C2, S_ampl_C2)
                    plt.plot(Time_C4, S_ampl_C4)
                    
                    # plot the dot on the peak
                    plt.plot( list(Time_C2[i] for i in peak_C2), list(S_ampl_C2[i] for i in peak_C2), 'or' )
                    plt.plot( list(Time_C4[i] for i in peak_C4), list(S_ampl_C4[i] for i in peak_C4), 'og' )
                    
                    plt.savefig('C4Trace00' + str(file) + 'C2Trace00' + str(file) + '.jpg')
                    plt.close()
                    
                    # Dot plot
                    fig = plt.figure()
    
                    for i, item in enumerate(extraction_time):
                        if len(item) > 0:
                            xAxis = [i+1]* len(item)
                            plt.scatter(xAxis, item)
                    
                    plt.grid()
                    plt.savefig('C4Trace00' + str(file) + 'C2Trace00' + str(file) + 'cycle.jpg')
                    plt.close()
            
            Close_it.close()
        
        #%% Third option
        
        if (option3 == True):
            
            df = pd.read_csv('ListRandom.txt', delim_whitespace = True )
            
            Close_it = open('ExtrTime.txt', 'w+')
            for fileC2, fileC4, f in zip(df.C2, df.C4, df.frequency):
                
                C2 = 'C2Trace00' + str(fileC2) + '.txt'
                C4 = 'C4Trace00' + str(fileC4) + '.txt'
                
                Time_C2, S_ampl_C2 = File_handle(C2)    # Detector signal file
                Time_C4, S_ampl_C4 = File_handle(C4)    # Source pulsing file
        
                # calculation of extraction time and on time
                extraction_time, _ = Extract_time(Time_C2, S_ampl_C2, Time_C4, S_ampl_C4, f)
                
                # Save the extraction time
                Close_it.write('\nfile is ' + 'C4 Trace00' + str(fileC2) + ' and C2 Trace00' + str(fileC4) + '.txt \n')
                for item in extraction_time:
                    Close_it.write("%s\n" % item)
                
                
                if (self.cb3.GetValue() == True):
                    
                    # Pulse figure
                    peak_C2, _ = find_peaks(S_ampl_C2, prominence=0.02)            # in C2 channel
                    peak_C4, _ = find_peaks(5-np.array(S_ampl_C4), prominence=4.5) # in C4 channel
                    
                    plt.plot(Time_C2, S_ampl_C2)
                    plt.plot(Time_C4, S_ampl_C4)
                    
                    # plot the dot on the peak
                    plt.plot( list(Time_C2[i] for i in peak_C2), list(S_ampl_C2[i] for i in peak_C2), 'or' )
                    plt.plot( list(Time_C4[i] for i in peak_C4), list(S_ampl_C4[i] for i in peak_C4), 'og' )
                    
                    plt.savefig('C4Trace00' + str(fileC4) + 'C2Trace00' + str(fileC2) + '.jpg')
                    plt.close()
                    
                    # Dot plot
                    fig = plt.figure()
    
                    for i, item in enumerate(extraction_time):
                        if len(item) > 0:
                            xAxis = [i+1]* len(item)
                            plt.scatter(xAxis, item)
                    
                    plt.grid()
                    plt.savefig('C4Trace00' + str(fileC4) + 'C2Trace00' + str(fileC2) + 'cycle.jpg')
                    plt.close()
            
            Close_it.close()
        
        # close the window on the completion of calculation
        self.Close()

#%%

if __name__ == '__main__':
    
    app = wx.App(False)
    frame = FRS()
    frame.Show()
    app.MainLoop()
