import serial
import time
import os
import requests

SCALELIGHT_ON = "http://scalelight.local/cm?user=admin&password=oijaufdjkvdsui&cmnd=Power%20on"
SCALELIGHT_OFF = "http://scalelight.local/cm?user=admin&password=oijaufdjkvdsui&cmnd=Power%20off"
BAGGERSWITCH_ON = "http://baggerswitch.local/cm?user=admin&password=oijaufdjkvdsui&cmnd=Power%20on"
BAGGERSWITCH_OFF = "http://baggerswitch.local/cm?user=admin&password=oijaufdjkvdsui&cmnd=Power%20off"

class data:
    generalWeight = 0
    unitWeight = 0
    partCount = 0

def parseData(datain):
    returndata = ''
    for letter in datain:
        if(letter.isdigit()):
            returndata += letter
        elif(letter == '-'):
            tmp = '-' + returndata
            returndata = tmp
        elif(returndata[-1:].isdigit() and letter == '.' ):
            returndata += letter
    returndata = returndata.strip()
    try:
        return float(returndata)
    except: 
        return -1
def readdata():
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    ser.flushInput()
    ser.flushOutput()

    x=0
    while (x < 3):
        dataIn = parseData(ser.readline().decode('ascii', 'ignore'))
        if(dataIn == -1):
            print ("crap")
            continue
        elif (x == 0):
            x+=1
            data.generalWeight = dataIn
            data.enitialweight = dataIn
        elif (x == 1):
            x+=1
            data.unitWeight = dataIn
        elif (x == 2):
            x+=1
            data.partCount = dataIn
    ser.close()

#def scaleRead():
requests.post(url = BAGGERSWITCH_OFF)
requests.post(url = SCALELIGHT_OFF)
bagswitchstatus = False
readdata()
previousweight = data.generalWeight
while True:
    readdata()
    sensitivity = 12
    print ("general1: " + str(data.generalWeight)+"\n")
    print ("unit1: " + str(data.unitWeight)+"\n")
    print ("count1: " + str(data.partCount)+"\n")

    if (previousweight + data.unitWeight > data.generalWeight + data.unitWeight/sensitivity or previousweight + data.unitWeight < data.generalWeight - data.unitWeight/sensitivity):
        requests.post(url=SCALELIGHT_ON)
        requests.post(url=BAGGERSWITCH_ON)
        bagswitchstatus = True
        while (bagswitchstatus):
            if(str(requests.get(url="http://scalelight.local/cm?user=admin&password=oijaufdjkvdsui&cmnd=Power%20").json())[11:-2] == "ON"):
                time.sleep(2)
                print ("tripped")
            else:
                bagswitchstatus = False
                requests.post(url=BAGGERSWITCH_OFF)
                readdata()
                previousweight = data.generalWeight
    else:
        print("pass")
        previousweight = data.generalWeight