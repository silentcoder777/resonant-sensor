"""
This python script is used to read the temperature from the tag without using a temperature probe. We first read
the data from VNA. We have used R60 VNA and the python script needs the RVNA software opened and running before running this
script. 
"""

# PyVisa is used for UI
import pyvisa as visa    #PyVisa is required along with NIVisa
from time import sleep
import os 
from tkinter import *
import pandas as pd
import matlab.engine

#counter to keep track of files
buttonClickedCounter = 0

def getTemperature(filePath, fileCounter):
    csvDataPath = filePath + "\Scat_data_" + '{}'.format(fileCounter) + ".csv"
    freqVectorPath = filePath + "\FreqVector.csv"

    ############ Matlab Engine Code ############
   
    eng = matlab.engine.start_matlab()
    c = eng.R60VNAdataplot(freqVectorPath, csvDataPath)
    print(c)


# This function will read the frequency from the reader. Much of this code has been inherited from the code provided by Copper Mountain
def readDataFromRVNA():
    global buttonClickedCounter
    buttonClickedCounter += 1
    rm = visa.ResourceManager('@py')
    #Connect to a Socket on the local machine at 5025
    #Use the IP address of a remote machine to connect to it instead
    try:
        CMT = rm.open_resource('TCPIP0::localhost::5025::SOCKET')
    except:
        print("Failure to connect to VNA!")
        print("Check network settings")
        label2.configure(text="RVNA Software is not Opened")
    #The VNA ends each line with this. Reads will time out without this
    CMT.read_termination='\n'
    #Set a really long timeout period for slow sweeps
    CMT.timeout = 10000
    CMT.write("TRIG:SOUR BUS\n")
    CMT.query("*OPC?\n")

    
    # get the directory where this python script is located, the csv file will be saved in the same folder
    
    file_path = os.path.dirname("C:\\Users\\reuelgroup\\Desktop\\R60\\")
    
    CMT.write("TRIG:SING\n")
    CMT.write("SENS:FREQ:STAR 100 MHZ;STOP 200MHZ")
    CMT.write("SENS:SWE:POIN 10000")
    CMT.query("*OPC?\n")
    command = 'MMEM:STOR:FDAT ' + '"' + file_path + '/Scat_data_' + '{}'.format(buttonClickedCounter) + '.csv"' + '\n'
    CMT.write(command)
    #print(command)
    label2.configure(text="Data " + str(buttonClickedCounter) + " Saved Succesfully ...")
    sleep(2)   # seconds

    CMT.write("TRIG:SOUR INT\n")
    getTemperature(file_path, buttonClickedCounter)
    



window = Tk()
window.title("Pig Healthcare Application")

lbl = Label(window, text="Please press the \"Take Reading\" button to monitor Pig's Health", font=("Arial", 20))
label2 = Label(fg='#f00', font=("Arial", 10))


lbl.grid(column=0, row=0)
label2.place(relx=0.5, rely=0.65, anchor=CENTER)

window_height = 200
window_width = 850

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))


btn = Button(window, text="Take Reading", command=readDataFromRVNA)

btn.place(relx=0.5, rely=0.5, anchor=CENTER)

window.mainloop()



