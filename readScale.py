#!/home/pi/scale/bin/python3

import serial
import time
import os
import sys
import requests
import logging
import threading

logging.basicConfig(filename='/home/pi/scale/readScale.log', level=logging.INFO)
class data:
    generalWeight = 0
    unitWeight = 0
    partCount = 0
    SCALELIGHT_ON = "http://scalelight.local/cm?user=admin&password=oijaufdjkvdsui&cmnd=Power%20on"
    SCALELIGHT_OFF = "http://scalelight.local/cm?user=admin&password=oijaufdjkvdsui&cmnd=Power%20off"
    BAGGERSWITCH_ON = "http://baggerswitch.local/cm?user=admin&password=oijaufdjkvdsui&cmnd=Power%20on"
    BAGGERSWITCH_OFF = "http://baggerswitch.local/cm?user=admin&password=oijaufdjkvdsui&cmnd=Power%20off"

def writefile(filedata):
    path = '/home/pi/scale/status'
    if (os.path.isfile(path)):
        os.remove(path)
    status_file = open(path, "w")
    status_file.write("%s" % filedata)

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
    x=0
    while (x < 3):
        dataIn = parseData(ser.readline().decode('ascii', 'ignore'))
        if(dataIn == -1):
            continue
        elif (x == 0):
            x+=1
            data.generalWeight = dataIn
        elif (x == 1):
            x+=1
            data.unitWeight = dataIn
        elif (x == 2):
            x+=1
            data.partCount = dataIn
    ser.close()

def shutdown():
    os.remove('/var/www/html/stop-script')
    requests.post(url = data.SCALELIGHT_OFF)
    requests.post(url = data.BAGGERSWITCH_OFF)
    writefile("Stopped\n")

def run(sensitivity = 10):
    try:
        #set initial values to off
        requests.post(url = data.BAGGERSWITCH_OFF)
        requests.post(url = data.SCALELIGHT_OFF)
        bagswitchstatus = False
        logging.info('Reading initial data...')
        writefile("Waiting on Initial Reading\n")
        #get first data read
        readdata()
        writefile("Running\n")
        previousweight = data.generalWeight
        while (True):
                readdata()
                if (previousweight + data.unitWeight > data.generalWeight + data.unitWeight/sensitivity or previousweight + data.unitWeight < data.generalWeight - data.unitWeight/sensitivity):
                    #if weight changes by more than 1/sensitivity post switch on
                        requests.post(url=data.SCALELIGHT_ON)
                        requests.post(url=data.BAGGERSWITCH_ON)
                        bagswitchstatus = True
                        writefile("Tripped\n")
                        while (bagswitchstatus):
                            
                            if(str(requests.get(url="http://scalelight.local/cm?user=admin&password=oijaufdjkvdsui&cmnd=Power%20").json())[11:-2] == "ON"):
                                #wait for status to change to OFF
                                time.sleep(2)
                            else:
                                #once OFF set switch off and read data again
                                bagswitchstatus = False
                                requests.post(url=data.BAGGERSWITCH_OFF)
                                writefile("Waiting on reinitialized Reading\n")
                                readdata()
                                previousweight = data.generalWeight
                        writefile("Running\n")
                else:
                    previousweight = data.generalWeight
    except Exception as E:
        handleError(E)

def main():
    try:
        if (os.path.isfile('/var/www/html/stop-script')):
            os.remove('/var/www/html/stop-script')
        th = threading.Thread(name='run', target=run)
        th.setDaemon(True)
        th.start()
        while (True):
            #check if stop script file exists and stop if so
            if (os.path.isfile('/var/www/html/stop-script')):
                writefile("Stopped\n")
                shutdown()
                return 0
        time.sleep(2)
    except Exception as E:
        writefile("Error\n")
        logging.error('some exception occurred\n' + str(E))
        requests.post(url=data.SCALELIGHT_ON)
        requests.post(url=data.BAGGERSWITCH_ON)
        sleep(1)
        requests.post(url=data.SCALELIGHT_OFF)
        sleep(1)
        requests.post(url=data.SCALELIGHT_ON)


if __name__ == '__main__':
    main()