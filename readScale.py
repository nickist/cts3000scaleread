#!/home/pi/scale/bin/python3

import serial
import time
import os
import requests
import logging

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
    if (os.path.isfile('/home/pi/scale/status')):
        os.remove('/home/pi/scale/status')
    status_file = open("/home/pi/scale/status", "w")
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
    ser.flushInput()
    ser.flushOutput()

    x=0
    while (x < 3):
        dataIn = parseData(ser.readline().decode('ascii', 'ignore'))
        if(dataIn == -1):
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
logging.info('Begin program set switches off')
requests.post(url = BAGGERSWITCH_OFF)
requests.post(url = SCALELIGHT_OFF)
bagswitchstatus = False
if (os.path.isfile('/var/www/html/stop-script')):
    os.remove("/var/www/html/stop-script")
logging.info('Reading initial data...')
readdata()
writefile("Running")
previousweight = data.generalWeight
try:
    while True:
        try:
            if (os.path.isfile('/var/www/html/stop-script')):
                requests.post(url = BAGGERSWITCH_OFF)
                os.remove('/var/www/html/stop-script')
                requests.post(url = SCALELIGHT_OFF)
                bagswitchstatus = False
                writefile("Stopped")
                logging.info('Stopped')
                break 
        except IOError as e:
            logging.error('I/O error occurred' + str(e))
            writefile("Error")
            break
        readdata()
        sensitivity = 12

        if (previousweight + data.unitWeight > data.generalWeight + data.unitWeight/sensitivity or previousweight + data.unitWeight < data.generalWeight - data.unitWeight/sensitivity):
                requests.post(url=SCALELIGHT_ON)
                requests.post(url=BAGGERSWITCH_ON)
                bagswitchstatus = True
                writefile("Tripped")
                while (bagswitchstatus):
                    if(str(requests.get(url="http://scalelight.local/cm?user=admin&password=oijaufdjkvdsui&cmnd=Power%20").json())[11:-2] == "ON"):
                        time.sleep(2)
                    else:
                        bagswitchstatus = False
                        requests.post(url=BAGGERSWITCH_OFF)
                        readdata()
                        previousweight = data.generalWeight
                writefile("Running")
        else:
            previousweight = data.generalWeight
except IOError as e:
    writefile("Error")
    logging.error('Some I/O error occurred ' + str(e))
except ValueError as ve:
    writefile("Error")
    logging.error('some value error occurred ' + str(e)) 
except Exception as E:
    writefile("Error")
    logging.error('some exception occurred ' + str(E))