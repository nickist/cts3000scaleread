#!/home/pi/scale/bin/python3

import serial
import time
import os
import sys
import requests
import logging
import threading
sensitivity = 12

SCALELIGHT_ON = "http://scalelight.local/cm?user=admin&password=oijaufdjkvdsui&cmnd=Power%20on"
SCALELIGHT_OFF = "http://scalelight.local/cm?user=admin&password=oijaufdjkvdsui&cmnd=Power%20off"
BAGGERSWITCH_ON = "http://baggerswitch.local/cm?user=admin&password=oijaufdjkvdsui&cmnd=Power%20on"
BAGGERSWITCH_OFF = "http://baggerswitch.local/cm?user=admin&password=oijaufdjkvdsui&cmnd=Power%20off"
logging.basicConfig(filename='/home/pi/scale/readScale.log', level=logging.INFO)
class data:
    generalWeight = 0
    unitWeight = 0
    partCount = 0

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
    requests.post(url = SCALELIGHT_OFF)
    requests.post(url = BAGGERSWITCH_OFF)
    writefile("Stopped\n")
    logging.info('Stopped')

def run():
    try:
        #set initial values to off
        logging.info('Begin program set switches off')
        requests.post(url = BAGGERSWITCH_OFF)
        requests.post(url = SCALELIGHT_OFF)
        bagswitchstatus = False
        logging.info('Reading initial data...')
        writefile("Waiting on Initial Reading\n")
        #get first data read
        readdata()
        writefile("Running\n")
        previousweight = data.generalWeight
        while (True):
            try:
                logging.info('Running')
                readdata()
                if(previousweight <= data.generalWeight+.001 and previousweight >= data.generalWeight-.001): 
                    #if data changes less than .00 ignore data and update previous weight
                    previousweight = data.generalWeight
                    continue
                elif(data.generalWeight < 0 or data.partCount == 0):
                    previousweight = data.generalWeight
                    continue
                elif (previousweight + data.unitWeight > data.generalWeight + data.unitWeight/sensitivity or previousweight + data.unitWeight < data.generalWeight - data.unitWeight/sensitivity):
                    #if weight changes by more than 1/sensitivity post switch on
                        requests.post(url=SCALELIGHT_ON)
                        requests.post(url=BAGGERSWITCH_ON)
                        bagswitchstatus = True
                        writefile("Tripped\n")
                        while (bagswitchstatus):
                            
                            if(str(requests.get(url="http://scalelight.local/cm?user=admin&password=oijaufdjkvdsui&cmnd=Power%20").json())[11:-2] == "ON"):
                                #wait for status to change to OFF
                                time.sleep(2)
                            else:
                                #once OFF set switch off and read data again
                                bagswitchstatus = False
                                requests.post(url=BAGGERSWITCH_OFF)
                                writefile("Waiting on reinitialized Reading\n")
                                readdata()
                                previousweight = data.generalWeight
                        writefile("Running\n")
                else:
                    previousweight = data.generalWeight
            except Exception as e:
                writefile("Error")
                logging.error('some exception occurred\n' + str(e))
                requests.post(url=SCALELIGHT_ON)
                requests.post(url=BAGGERSWITCH_ON)
                requests.post(url=SCALELIGHT_OFF)
                requests.post(url=SCALELIGHT_ON)

                    


    except Exception as E:
        writefile("Error\n")
        logging.error('some exception occurred\n' + str(E))
        requests.post(url=SCALELIGHT_ON)
        requests.post(url=BAGGERSWITCH_ON)
        requests.post(url=SCALELIGHT_OFF)
        requests.post(url=SCALELIGHT_ON)

def main():
    if (os.path.isfile('/var/www/html/stop-script')):
        os.remove('/var/www/html/stop-script')
    th = threading.Thread(name='run', target=run)
    th.setDaemon(True)
    th.start()
    while (True):
        #check if stop script file exists and stop if so
        if (os.path.isfile('/var/www/html/stop-script')):
            writefile("Stopped\n")
            logging.info("Stopping program")
            shutdown()
            return 0
    time.sleep(2)

if __name__ == '__main__':
    main()