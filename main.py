import tkinter as tk
from tkinter import filedialog
import serial
import serial.tools.list_ports
import time
import threading

#todo Comic Sans MS mode

ports = []
ser = serial.Serial()

prevTime = 0 #todo find a better way to do this
running = False #todo

#todo figure out where to actually put these variables
s0 = 0
s1 = 0
s2 = 0
s3 = 0
s4 = 0
s5 = 0
s6 = 0
s10 = 0
s11 = 0.0
s12 = 0.0
s13 = 0
s20 = 0
s21 = 0
s22 = 0
s23 = 0
s24 = 0.0
s25 = 0.0
s26 = 0.0
s27 = 0.0
s30 = 0
s31 = 0
s32 = 0
s100 = 0.0
s101 = 0.0
s102 = 0.0
s110 = 0.0
s111 = 0.0
s112 = 0.0
s120 = 0.0
s121 = 0.0
s122 = 0.0
s130 = 0.0
s131 = 0.0
s132 = 0.0

def waitForOk():
    ser.timeout = 0.01
    response = str(ser.readline())
    while response.find("ok") == -1:
        if response.find("error") != -1:
            print("Grbl response: " + response)
            return
        else:
            response = str(ser.readline())

def getGrblResponse():
    ser.timeout = 0.01
    response = str(ser.read(10))
    if response.find("ok") == -1:
        print(response) #todo add error handling function

def getConfig(): #todo get rid of grbl intro message
    #todo fix this. I don't think these should all be global
    global s0,s1,s2,s3,s4,s5,s6,s10,s11,s12,s13,s20,s21,s22,s23,s24,s25,s26,s27,s30,s31,s32,s100,s101,s102,s110,s111,s112,s120,s121,s122,s130,s131,s132
    def getSetting(myList, substring, type):
        for i,s in enumerate(myList): #todo figure out why i is needed here
            if substring in s:
                if type == "int":
                    test = (int(s[(s.index("=") +1 ):]))
                elif type == "float":
                    test = (float(s[(s.index("=") +1 ):]))
                return test
        return -1

    try:
        ser.timeout = 0.5
        ser.write(b'$$\r')
        settings = str(ser.read(1000))
        settings = settings.split("\\r\\n")
        s0 = getSetting(settings, '$0', "int")
        s1 = getSetting(settings, '$1', "int")
        s2 = getSetting(settings, '$2', "int")
        s3 = getSetting(settings, '$3', "int")
        s4 = getSetting(settings, '$4', "int")
        s5 = getSetting(settings, '$5', "int")
        s6 = getSetting(settings, '$6', "int")
        s10 = getSetting(settings, '$10', "int")
        s11 = getSetting(settings, '$11', "float")
        s12 = getSetting(settings, '$12', "float")
        s13 = getSetting(settings, '$13', "int")
        s20 = getSetting(settings, '$20', "int")
        s21 = getSetting(settings, '$21', "int")
        s22 = getSetting(settings, '$22', "int")
        s23 = getSetting(settings, '$23', "int")
        s24 = getSetting(settings, '$24', "float")
        s25 = getSetting(settings, '$25', "float")
        s26 = getSetting(settings, '$26', "int")
        s27 = getSetting(settings, '$27', "float")
        s30 = getSetting(settings, '$30', "int")
        s31 = getSetting(settings, '$31', "int")
        s32 = getSetting(settings, '$32', "int")
        s100 = getSetting(settings, '$100', "float")
        s101 = getSetting(settings, '$101', "float")
        s102 = getSetting(settings, '$102', "float")
        s110 = getSetting(settings, '$110', "float")
        s111 = getSetting(settings, '$111', "float")
        s112 = getSetting(settings, '$112', "float")
        s120 = getSetting(settings, '$120', "float")
        s121 = getSetting(settings, '$121', "float")
        s122 = getSetting(settings, '$122', "float")
        s130 = getSetting(settings, '$130', "float")
        s131 = getSetting(settings, '$131', "float")
        s132 = getSetting(settings, '$132', "float")
    except:
        print("fail")

def openSettings():
    def saveSettings(): #todo add validity checks for variables
        ser.write(b"$0=" + str(stepPulseMicro.get()).encode() + b"\r")
        getGrblResponse()
        ser.write(b"$1=" + str(stepIdleDelay.get()).encode() + b"\r")
        getGrblResponse()

        stepMask = stepInvertX.get()
        stepMask = stepMask | (stepInvertY.get() << 1)
        stepMask = stepMask | (stepInvertZ.get() << 2)
        ser.write(b"$2=" + str(stepMask).encode() + b"\r")
        getGrblResponse()

        dirMask = directionInvertX.get()
        dirMask = dirMask | (directionInvertY.get() << 1)
        dirMask = dirMask | (directionInvertZ.get() << 2)
        ser.write(b"$3=" + str(dirMask).encode() + b"\r")
        getGrblResponse()

        ser.write(b"$4=" + str(stepEnableInvert.get()).encode() + b"\r")
        getGrblResponse()
        ser.write(b"$5=" + str(limitPinsInvert.get()).encode() + b"\r")
        getGrblResponse()
        ser.write(b"$6=" + str(probePinInvert.get()).encode() + b"\r")
        getGrblResponse()

        if str(statusMask.get()) == "Wpos":
            ser.write(b"$10=0\r")
        elif str(statusMask.get()) == "Mpos":
            ser.write(b"$10=1\r")
        else:
            ser.write(b"$10=2\r")

        ser.write(b"$11=" + str(junctionDeviation.get()).encode() + b"\r")
        getGrblResponse()
        ser.write(b"$12=" + str(arcTolerance.get()).encode() + b"\r")
        getGrblResponse()
        ser.write(b"$13=" + str(reportInches.get()).encode() + b"\r")
        getGrblResponse()
        ser.write(b"$20=" + str(softLimits.get()).encode() + b"\r")
        getGrblResponse()
        ser.write(b"$21=" + str(hardLimits.get()).encode() + b"\r")
        getGrblResponse()
        ser.write(b"$22=" + str(homingCycle.get()).encode() + b"\r")
        getGrblResponse()

        homingInvertMask = homingInvertX.get()
        homingInvertMask = homingInvertMask | (homingInvertY.get() << 1)
        homingInvertMask = homingInvertMask | (homingInvertZ.get() << 2)
        ser.write(b"$23=" + str(homingInvertMask).encode() + b"\r")
        getGrblResponse()

        ser.write(b"$24=" + str(homingFeed.get()).encode() + b"\r")
        getGrblResponse()
        ser.write(b"$25=" + str(homingSeek.get()).encode() + b"\r")
        getGrblResponse()
        ser.write(b"$26=" + str(homingDebounce.get()).encode() + b"\r")
        getGrblResponse()
        ser.write(b"$27=" + str(homingPulloff.get()).encode() + b"\r")
        getGrblResponse()
        ser.write(b"$30=" + str(maxSpindleSpeed.get()).encode() + b"\r")
        getGrblResponse()
        ser.write(b"$31=" + str(minSpindleSpeed.get()).encode() + b"\r")
        getGrblResponse()
        ser.write(b"$32=" + str(laserMode.get()).encode() + b"\r")
        getGrblResponse()

        ser.write(b"$100=" + str(xStepsMm.get()).encode() + b"\r")
        getGrblResponse()
        ser.write(b"$101=" + str(yStepsMm.get()).encode() + b"\r")
        getGrblResponse()
        ser.write(b"$102=" + str(zStepsMm.get()).encode() + b"\r")
        getGrblResponse()

        ser.write(b"$110=" + str(xMaxRate.get()).encode() + b"\r")
        getGrblResponse()
        ser.write(b"$111=" + str(yMaxRate.get()).encode() + b"\r")
        getGrblResponse()
        ser.write(b"$112=" + str(zMaxRate.get()).encode() + b"\r")
        getGrblResponse()

        ser.write(b"$120=" + str(xAccl.get()).encode() + b"\r")
        getGrblResponse()
        ser.write(b"$121=" + str(yAccl.get()).encode() + b"\r")
        getGrblResponse()
        ser.write(b"$122=" + str(zAccl.get()).encode() + b"\r")
        getGrblResponse()

        ser.write(b"$130=" + str(xMaxTravel.get()).encode() + b"\r")
        getGrblResponse()
        ser.write(b"$131=" + str(yMaxTravel.get()).encode() + b"\r")
        getGrblResponse()
        ser.write(b"$132=" + str(zMaxTravel.get()).encode() + b"\r")
        getGrblResponse()

        settingsWindow.destroy()

    settingsWindow = tk.Toplevel(window)
    settingsWindow.grab_set()
    getConfig()

    #Step pulse microseconds
    stepPulseMicro = tk.StringVar()
    stepPulseMicro.set(str(s0))
    stepPulseMicroLabel = tk.Label(settingsWindow, text="Step pulse Microseconds: ")
    stepPulseMicroLabel.grid(row=0, column=0)
    stepPulseMicroEntry = tk.Entry(settingsWindow, textvariable=stepPulseMicro)
    stepPulseMicroEntry.grid(row=0,column=1)

    #step idle delay
    stepIdleDelay = tk.StringVar()
    stepIdleDelay.set(str(s1))
    stepIdleDelayLabel = tk.Label(settingsWindow, text="Step idle delay Milliseconds: ")
    stepIdleDelayLabel.grid(row=1, column=0)
    stepIdleDelayEntry = tk.Entry(settingsWindow, textvariable=stepIdleDelay)
    stepIdleDelayEntry.grid(row=1,column=1)

    #step invert port
    stepInvertX = tk.BooleanVar() 
    stepInvertY = tk.BooleanVar()
    stepInvertZ = tk.BooleanVar()
    stepInvertX.set(s2 & 1)
    stepInvertY.set(s2 & 2)
    stepInvertZ.set(s2 & 4)
    tk.Label(settingsWindow, text="Step port invert:").grid(row=2, column=0)
    tk.Checkbutton(settingsWindow, text="X", variable=stepInvertX).grid(row=2, column=1)
    tk.Checkbutton(settingsWindow, text="Y", variable=stepInvertY).grid(row=2, column=2)
    tk.Checkbutton(settingsWindow, text="Z", variable=stepInvertZ).grid(row=2, column=3)

    #direction invert port
    directionInvertX = tk.BooleanVar()
    directionInvertY = tk.BooleanVar()
    directionInvertZ = tk.BooleanVar()
    directionInvertX.set(s3 & 1)
    directionInvertY.set(s3 & 2)
    directionInvertZ.set(s3 & 4)
    tk.Label(settingsWindow, text="Direction port invert:").grid(row=3, column=0)
    tk.Checkbutton(settingsWindow, text="X", variable=directionInvertX).grid(row=3, column=1)
    tk.Checkbutton(settingsWindow, text="Y", variable=directionInvertY).grid(row=3, column=2)
    tk.Checkbutton(settingsWindow, text="Z", variable=directionInvertZ).grid(row=3, column=3)

    #step enable invert
    stepEnableInvert = tk.IntVar()
    stepEnableInvert.set(s4 & 1)
    tk.Label(settingsWindow, text="Step enable invert:").grid(row=4, column=0)
    tk.Checkbutton(settingsWindow, variable=stepEnableInvert).grid(row=4, column=1)

    #limit pins invert
    limitPinsInvert = tk.IntVar()
    limitPinsInvert.set(s5 & 1)
    tk.Label(settingsWindow, text="Limit pins invert:").grid(row=5, column=0)
    tk.Checkbutton(settingsWindow, variable=limitPinsInvert).grid(row=5, column=1)
    
    #probe pin invert
    probePinInvert = tk.IntVar()
    probePinInvert.set(s6 & 1)
    tk.Label(settingsWindow, text="Probe pin invert:").grid(row=6, column=0)
    tk.Checkbutton(settingsWindow, variable=probePinInvert).grid(row=6, column=1)

    #status report mask
    statusOpts = ["Wpos","Mpos","Buf"]
    statusMask = tk.StringVar()
    statusMask.set(statusOpts[s10])
    tk.OptionMenu(settingsWindow, statusMask, *statusOpts).grid(row=7,column=0)

    #junction deviation mm
    junctionDeviation = tk.StringVar()
    junctionDeviation.set(str(s11))
    junctionDeviationLabel = tk.Label(settingsWindow, text="Juntion deviation mm: ")
    junctionDeviationLabel.grid(row=8, column=0)
    junctionDeviationEntry = tk.Entry(settingsWindow, textvariable=junctionDeviation)
    junctionDeviationEntry.grid(row=8,column=1)

    #arc tolerance mm
    arcTolerance = tk.StringVar()
    arcTolerance.set(str(s12))
    arcToleranceLabel = tk.Label(settingsWindow, text="Arc tolerance mm: ")
    arcToleranceLabel.grid(row=9, column=0)
    arcToleranceEntry = tk.Entry(settingsWindow, textvariable=arcTolerance)
    arcToleranceEntry.grid(row=9,column=1)

    #report inches
    reportInches = tk.IntVar()
    reportInches.set(s13 & 1)
    tk.Label(settingsWindow, text="Report inches:").grid(row=10, column=0)
    tk.Checkbutton(settingsWindow, variable=reportInches).grid(row=10, column=1)

    #soft limits
    softLimits = tk.IntVar()
    softLimits.set(s20 & 1)
    tk.Label(settingsWindow, text="Soft limits:").grid(row=11, column=0)
    tk.Checkbutton(settingsWindow, variable=softLimits).grid(row=11, column=1)

    #hard limits
    hardLimits = tk.IntVar()
    hardLimits.set(s21 & 1)
    tk.Label(settingsWindow, text="Hard limits:").grid(row=12, column=0)
    tk.Checkbutton(settingsWindow, variable=hardLimits).grid(row=12, column=1)

    #homing cycle
    homingCycle = tk.IntVar()
    homingCycle.set(s22 & 1)
    tk.Label(settingsWindow, text="Homing cycle:").grid(row=13, column=0)
    tk.Checkbutton(settingsWindow, variable=homingCycle).grid(row=13, column=1)

    #Homing dir invert
    homingInvertX = tk.BooleanVar()
    homingInvertY = tk.BooleanVar()
    homingInvertZ = tk.BooleanVar()
    homingInvertX.set(s23 & 1)
    homingInvertY.set(s23 & 2)
    homingInvertZ.set(s23 & 4)
    tk.Label(settingsWindow, text="Homing direction invert:").grid(row=14, column=0)
    tk.Checkbutton(settingsWindow, text="X", variable=homingInvertX).grid(row=14, column=1)
    tk.Checkbutton(settingsWindow, text="Y", variable=homingInvertY).grid(row=14, column=2)
    tk.Checkbutton(settingsWindow, text="Z", variable=homingInvertZ).grid(row=14, column=3)

    #homing feed mm
    homingFeed = tk.StringVar()
    homingFeed.set(str(s24))
    homingFeedLabel = tk.Label(settingsWindow, text="Homing feed mm/min: ")
    homingFeedLabel.grid(row=15, column=0)
    homingFeedEntry = tk.Entry(settingsWindow, textvariable=homingFeed)
    homingFeedEntry.grid(row=15,column=1)

    #homing seek mm
    homingSeek = tk.StringVar()
    homingSeek.set(str(s25))
    homingSeekLabel = tk.Label(settingsWindow, text="Homing seek mm/min: ")
    homingSeekLabel.grid(row=16, column=0)
    homingSeekEntry = tk.Entry(settingsWindow, textvariable=homingSeek)
    homingSeekEntry.grid(row=16,column=1)

    #homing debounce milli
    homingDebounce = tk.StringVar()
    homingDebounce.set(str(s26))
    homingDebounceLabel = tk.Label(settingsWindow, text="Homing debounce milliseconds: ")
    homingDebounceLabel.grid(row=17, column=0)
    homingDebounceEntry = tk.Entry(settingsWindow, textvariable=homingDebounce)
    homingDebounceEntry.grid(row=17,column=1)

    #homing pulloff mm
    homingPulloff = tk.StringVar()
    homingPulloff.set(str(s27))
    homingPulloffLabel = tk.Label(settingsWindow, text="Homing pulloff mm: ")
    homingPulloffLabel.grid(row=18, column=0)
    homingPulloffEntry = tk.Entry(settingsWindow, textvariable=homingPulloff)
    homingPulloffEntry.grid(row=18,column=1)

    #max spindle speed RPM
    maxSpindleSpeed = tk.StringVar()
    maxSpindleSpeed.set(str(s30))
    maxSpindleSpeedLabel = tk.Label(settingsWindow, text="Max spindle speed RPM: ")
    maxSpindleSpeedLabel.grid(row=19, column=0)
    maxSpindleSpeedEntry = tk.Entry(settingsWindow, textvariable=maxSpindleSpeed)
    maxSpindleSpeedEntry.grid(row=19,column=1)

    #min spindle speed RPM
    minSpindleSpeed = tk.StringVar()
    minSpindleSpeed.set(str(s31))
    minSpindleSpeedLabel = tk.Label(settingsWindow, text="Min spindle speed RPM: ")
    minSpindleSpeedLabel.grid(row=0, column=5)
    minSpindleSpeedEntry = tk.Entry(settingsWindow, textvariable=minSpindleSpeed)
    minSpindleSpeedEntry.grid(row=0,column=6)

    #laser mode
    laserMode = tk.IntVar()
    laserMode.set(s32 & 1)
    tk.Label(settingsWindow, text="Laser mode:").grid(row=13, column=5)
    tk.Checkbutton(settingsWindow, variable=laserMode).grid(row=13, column=6)

    #x steps per mm
    xStepsMm = tk.StringVar()
    xStepsMm.set(str(s100))
    xStepsMmLabel = tk.Label(settingsWindow, text="X steps per mm: ")
    xStepsMmLabel.grid(row=1, column=5)
    xStepsMmEntry = tk.Entry(settingsWindow, textvariable=xStepsMm)
    xStepsMmEntry.grid(row=1,column=6)

    #y steps per mm
    yStepsMm = tk.StringVar()
    yStepsMm.set(str(s101))
    yStepsMmLabel = tk.Label(settingsWindow, text="Y steps per mm: ")
    yStepsMmLabel.grid(row=2, column=5)
    yStepsMmEntry = tk.Entry(settingsWindow, textvariable=yStepsMm)
    yStepsMmEntry.grid(row=2,column=6)

    #z steps per mm
    zStepsMm = tk.StringVar()
    zStepsMm.set(str(s102))
    zStepsMmLabel = tk.Label(settingsWindow, text="Z steps per mm: ")
    zStepsMmLabel.grid(row=3, column=5)
    zStepsMmEntry = tk.Entry(settingsWindow, textvariable=zStepsMm)
    zStepsMmEntry.grid(row=3,column=6)

    #x max rate mm/min
    xMaxRate = tk.StringVar()
    xMaxRate.set(str(s110))
    xMaxRateLabel = tk.Label(settingsWindow, text="X max rate mm/min: ")
    xMaxRateLabel.grid(row=4, column=5)
    xMaxRateEntry = tk.Entry(settingsWindow, textvariable=xMaxRate)
    xMaxRateEntry.grid(row=4,column=6)

    #y max rate
    yMaxRate = tk.StringVar()
    yMaxRate.set(str(s111))
    yMaxRateLabel = tk.Label(settingsWindow, text="Y max rate mm/min: ")
    yMaxRateLabel.grid(row=5, column=5)
    yMaxRateEntry = tk.Entry(settingsWindow, textvariable=yMaxRate)
    yMaxRateEntry.grid(row=5,column=6)

    #z max rate
    zMaxRate = tk.StringVar()
    zMaxRate.set(str(s112))
    zMaxRateLabel = tk.Label(settingsWindow, text="Z max rate mm/min: ")
    zMaxRateLabel.grid(row=6, column=5)
    zMaxRateEntry = tk.Entry(settingsWindow, textvariable=zMaxRate)
    zMaxRateEntry.grid(row=6,column=6)

    #x accl mm/sec2
    xAccl = tk.StringVar()
    xAccl.set(str(s120))
    xAcclLabel = tk.Label(settingsWindow, text="X acceleration mm/sec^2: ")
    xAcclLabel.grid(row=7, column=5)
    xAcclEntry = tk.Entry(settingsWindow, textvariable=xAccl)
    xAcclEntry.grid(row=7,column=6)

    #y accl mm/sec2
    yAccl = tk.StringVar()
    yAccl.set(str(s121))
    yAcclLabel = tk.Label(settingsWindow, text="Y acceleration mm/sec^2: ")
    yAcclLabel.grid(row=8, column=5)
    yAcclEntry= tk.Entry(settingsWindow, textvariable=yAccl)
    yAcclEntry.grid(row=8,column=6)

    #z accl mm/sec2
    zAccl = tk.StringVar()
    zAccl.set(str(s122))
    zAcclLabel = tk.Label(settingsWindow, text="Z acceleration mm/sec^2: ")
    zAcclLabel.grid(row=9, column=5)
    zAcclEntry = tk.Entry(settingsWindow, textvariable=zAccl)
    zAcclEntry.grid(row=9,column=6)

    #x max travel
    xMaxTravel = tk.StringVar()
    xMaxTravel.set(str(s130))
    xMaxTravelLabel = tk.Label(settingsWindow, text="X max travel mm: ")
    xMaxTravelLabel.grid(row=10, column=5)
    xMaxTravelEntry = tk.Entry(settingsWindow, textvariable=xMaxTravel)
    xMaxTravelEntry.grid(row=10,column=6)

    #y max travel
    yMaxTravel = tk.StringVar()
    yMaxTravel.set(str(s131))
    yMaxTravelLabel = tk.Label(settingsWindow, text="Y max travel mm: ")
    yMaxTravelLabel.grid(row=11, column=5)
    yMaxTravelEntry = tk.Entry(settingsWindow, textvariable=yMaxTravel)
    yMaxTravelEntry.grid(row=11,column=6)

    #z max travel
    zMaxTravel = tk.StringVar()
    zMaxTravel.set(str(s132))
    zMaxTravelLabel = tk.Label(settingsWindow, text="Z max travel mm: ")
    zMaxTravelLabel.grid(row=12, column=5)
    zMaxTravelEntry = tk.Entry(settingsWindow, textvariable=zMaxTravel)
    zMaxTravelEntry.grid(row=12,column=6)

    tk.Button(settingsWindow, text="Save settings", command=saveSettings).grid(row=50,column=1)


def scanForComms():
    portScan = serial.tools.list_ports.comports()

    for x in portScan:
        ports.append(x.device)

def setupSerial(): 
    if serialConnected.get() == True:
        ser.close()
        connectButton.configure(text="Connect", bg="SystemButtonFace") #default color
        g0Button.configure(state=tk.DISABLED)
        settingsButton.configure(state=tk.DISABLED)
        runButton.configure(state=tk.DISABLED)
        serialConnected.set(False)
    else:
        try:
            ser.port = selectedCOM.get()
            ser.baudrate = selectedBaud.get()
            ser.open()
            ser.read(10) #todo do this in a better way
            connectButton.configure(text="Connected", bg="#0be044")
            g0Button.configure(state=tk.ACTIVE)
            settingsButton.configure(state=tk.ACTIVE)
            upArrowButton.configure(state=tk.ACTIVE)
            rightArrowButton.configure(state=tk.ACTIVE)
            leftArrowButton.configure(state=tk.ACTIVE)
            downArrowButton.configure(state=tk.ACTIVE)
            if gCodeFileName.get():
                runButton.configure(state=tk.ACTIVE)
            serialConnected.set(True)
        except:
            connectButton.configure(text="Failed", bg="red")
            print("Failed to connect to com port")

def uploadGCode():
    gCodeFileName.set(filedialog.askopenfilename(initialdir = "/home",title = "Select file", filetypes=[("gCode files","*.gcode")]))
    fileName = gCodeFileName.get()[gCodeFileName.get().rfind("/") + 1:]
    fileNameLabel.configure(text=fileName)
    if serialConnected.get() == True:
        runButton.configure(state=tk.ACTIVE)

def testThread():
    gFile = open(gCodeFileName.get())    
    for line in gFile:
        if(line.find('\n') == -1):
            line = line + "\n"
        if line[0] == "G":
            ser.write(line.encode())
            waitForOk()           
    print("done")

def runGCode(): #todo thread this so it can be canceled
    runThread = threading.Thread(target=testThread)
    runThread.start()
    #todo
    """ gFile = open(gCodeFileName.get())    
    for line in gFile:
        if(line.find('\n') == -1):
            line = line + "\n"
        if line[0] == "G":
            ser.write(line.encode())
            waitForOk()           
    print("done") """

def g0Command():
    try:
        command = "g0 "
        if str(xPos.get()):
            command += ("x" + str(xPos.get()) + " ")
        if str(yPos.get()):
            command += ("y" + str(yPos.get()) + " ")
        if str(zPos.get()):
            command += ("z" + str(zPos.get()))
        command += "\r\n"
        ser.write(command.encode())
        #getGrblResponse()
    except:
        print("didn't work")

scanForComms()

#window setup stuff
window = tk.Tk()

window.title("GRBL configuration")
window.geometry('550x400')

#ports dropdown
selectedCOM = tk.StringVar(window)
if len(ports) > 0:
    selectedCOM.set("Select COM port")
    #selectedCOM.set("COM3") #todo just for test
else:
    selectedCOM.set("No COM ports available")
    ports.append(":(")

comPorts = tk.OptionMenu(window, selectedCOM, "----", *ports)
comPorts.grid(row=0,column=0)

#baud drop down
selectedBaud = tk.StringVar(window)
selectedBaud.set("115200")

baud = tk.OptionMenu(window, selectedBaud, *["9600", "115200", "921600"])
baud.grid(row=1,column=0)

#connect button
serialConnected = tk.BooleanVar()
connectButton = tk.Button(window, text="Connect", command=setupSerial)
connectButton.grid(row=0,column=1)

#settings button
settingsButton = tk.Button(window, text="Settings", command=openSettings, state=tk.DISABLED)
settingsButton.grid(row=0,column=2)

#x pos
xPosLabel = tk.Label(window, text="X position")
xPosLabel.grid(row=3, column=0)
xPos = tk.DoubleVar() 
tk.Entry(window, textvariable=xPos).grid(row=3,column=1)

#y pos
yPosLabel = tk.Label(window, text="Y position")
yPosLabel.grid(row=4, column=0)
yPos = tk.DoubleVar() 
tk.Entry(window, textvariable=yPos).grid(row=4,column=1)

#z pos
tk.Label(window, text="Z position").grid(row=5, column=0)
zPos = tk.DoubleVar()
tk.Entry(window, textvariable=zPos).grid(row=5,column=1)

#go button
g0Button = tk.Button(window, text="G0", command=g0Command, state=tk.DISABLED)
g0Button.grid(row=5, column=2)

#upload button
gCodeFileName = tk.StringVar()
uploadButton = tk.Button(window, text="Upload gCode", command=uploadGCode)
uploadButton.grid(row=6, column=0)
fileNameLabel = tk.Label(window, text=gCodeFileName.get())
fileNameLabel.grid(row=6, column=1)

#run button
runButton = tk.Button(window, text="Run gCode", command=runGCode, state=tk.DISABLED)
runButton.grid(row=7, column=0)

def moveXPlus():
    currentX = xPos.get()
    currentX = round((currentX + stepSize.get()), 2)
    if currentX < 100: #todo set an actual max
        xPos.set(currentX)
    else:
        xPos.set("100")
    g0Command()
    waitForOk()

def moveXMinus():
    currentX = xPos.get()
    currentX = round((currentX - stepSize.get()), 2)
    if (currentX > 0) or (enableNegX.get()):
        xPos.set(currentX)
    else:
        xPos.set(0)
    g0Command()
    waitForOk()

def moveYPlus():
    currentY = yPos.get()
    currentY = round((currentY + stepSize.get()), 2)
    if currentY < 100: #todo set an actual max
        yPos.set(currentY)
    else:
        yPos.set(100)
    g0Command()
    waitForOk()

def moveYMinus():
    currentY = yPos.get()
    currentY = round((currentY - stepSize.get()), 2)
    if currentY > 0 or (enableNegY.get()):
        yPos.set(currentY)
    else:
        yPos.set(0)
    g0Command()
    waitForOk()

def keyDownEvent(event):
    global prevTime
    if (time.monotonic() * 1000) > (prevTime + 40): #slow down key events to stop motors from spinning after key is released
        if event.keycode == 38:
            upArrowButton.invoke()
            upArrowButton.configure(relief=tk.SUNKEN)
        elif event.keycode == 39:
            rightArrowButton.invoke()
            rightArrowButton.configure(relief=tk.SUNKEN)
        elif event.keycode == 40:
            downArrowButton.invoke()
            downArrowButton.configure(relief=tk.SUNKEN)
        elif event.keycode == 37:
            leftArrowButton.invoke()
            leftArrowButton.configure(relief=tk.SUNKEN)
        prevTime = time.monotonic()*1000

def keyUpEvent(event):
    if event.keycode == 38:
        upArrowButton.configure(relief=tk.RAISED)
    elif event.keycode == 39:
        rightArrowButton.configure(relief=tk.RAISED)
    elif event.keycode == 40:
        downArrowButton.configure(relief=tk.RAISED)
    elif event.keycode == 37:
        leftArrowButton.configure(relief=tk.RAISED)

#arrow buttons
upArrow = tk.PhotoImage(file="upArrow.png")
rightArrow = tk.PhotoImage(file="rightArrow.png")
downArrow = tk.PhotoImage(file="downArrow.png")
leftArrow = tk.PhotoImage(file="leftArrow.png")
arrowsContainer = tk.Frame(window)
arrowsContainer.grid(row=8,column=0)

""" zUpButton = tk.Button(arrowsContainer, text="Z up")
zUpButton.grid(row=0,column=2)
zDownButton = tk.Button(arrowsContainer, text="Z\ndown", font=("Comic Sans MS", 12))
zDownButton.grid(row=0,column=0) """


upArrowButton = tk.Button(arrowsContainer, image=upArrow, command=moveYPlus, repeatdelay= 1, repeatinterval=50, state=tk.DISABLED)
upArrowButton.grid(row=0, column=1)
rightArrowButton = tk.Button(arrowsContainer, image=rightArrow, command=moveXPlus, repeatdelay= 1, repeatinterval=50, state=tk.DISABLED)
rightArrowButton.grid(row=1, column=2)
downArrowButton = tk.Button(arrowsContainer, image=downArrow, command=moveYMinus, repeatdelay= 1, repeatinterval=50, state=tk.DISABLED)
downArrowButton.grid(row=1, column=1)
leftArrowButton = tk.Button(arrowsContainer, image=leftArrow, command=moveXMinus, repeatdelay= 1, repeatinterval=50, state=tk.DISABLED)
leftArrowButton.grid(row=1, column=0)

#keyboard support for movement
arrowsContainer.bind("<Up>", keyDownEvent) #todo diable multiple keys being pressed
arrowsContainer.bind("<KeyRelease-Up>", keyUpEvent)
arrowsContainer.bind("<Right>", keyDownEvent)
arrowsContainer.bind("<KeyRelease-Right>", keyUpEvent)
arrowsContainer.bind("<Down>", keyDownEvent)
arrowsContainer.bind("<KeyRelease-Down>", keyUpEvent)
arrowsContainer.bind("<Left>", keyDownEvent)
arrowsContainer.bind("<KeyRelease-Left>", keyUpEvent)
arrowsContainer.focus_set() #todo buttons lose focus after typing in entry

#step size option menu
tk.Label(window, text="Step size: ").grid(row=8,column=1)
stepSize = tk.DoubleVar()
stepSize.set(1)
stepSizeOption = tk.OptionMenu(window, stepSize, *[0.01, 0.1, 1, 10])
stepSizeOption.grid(row=8,column=2)

#enable negative X and Y 
tk.Label(window, text="Enable negative X and/or Y position: ").grid(row=9,column=1)
enableNegX = tk.BooleanVar()
enableNegY = tk.BooleanVar()

enableNegXCheck = tk.Checkbutton(window, text="X", variable=enableNegX)
enableNegXCheck.grid(row=9,column=2)
enableNegYCheck = tk.Checkbutton(window, text="Y", variable=enableNegY)
enableNegYCheck.grid(row=9,column=3)


#todo test kill button
killButton = tk.Button(window, text="kill", command=runGCode, state=tk.DISABLED)
killButton.grid(row=999,column=0) #todo

window.mainloop()
