#!/usr/bin/python
import serial, time, os, requests

SCALELIGHT_ON = "http://scalelight.local/cm?user=admin&password=oijaufdjkvdsui&cmnd=Power%20on"
SCALELIGHT_OFF = "http://scalelight.local/cm?user=admin&password=oijaufdjkvdsui&cmnd=Power%20off"
BAGGERSWITCH_ON = "http://baggerswitch.local/cm?user=admin&password=oijaufdjkvdsui&cmnd=Power%20on"
BAGGERSWITCH_OFF = "http://baggerswitch.local/cm?user=admin&password=oijaufdjkvdsui&cmnd=Power%20off"
LIGHTSTATUS = str(requests.get(url = "http://scalelight.local/cm?user=admin&password=oijaufdjkvdsui&cmnd=Power%20").json())[13:-2]

def parseData(data):
    
    returndata = ""
    for letter in data:
        if letter.isdigit() or letter == '.':
             returndata += letter
    return float(returndata)

run = True
weights = [0.0,0.0,0.0]
previousweight = 0.0
while run:
    ser = serial.Serial('/dev/ttyUSB0', 9600)

    weights[0] = parseData(ser.readline().decode('ascii')[5:]) #general weight 
    weights[1] = parseData(ser.readline().decode('ascii')[5:]) #unit weight 
    weights[2] = parseData(ser.readline().decode('ascii')[4:]) #part count
    sensitivity = 12
    print (weights )
    print (previousweight)
    if (previousweight + weights[1] > weights[0] + weights[1]/sensitivity or  previousweight + weights[1] < weights[0] - weights[1]/sensitivity):
        while (LIGHTSTATUS == "ON"):
            requests.post(url = BAGGERSWITCH_ON)
            print ("tripped")
            time.sleep(1)
        requests.post(url = BAGGERSWITCH_OFF)
        previousweight = weights[0]
        continue
    else:
        previousweight = weights[0]
        continue
        # run = false
        # http://scalelightyellow.local/cm?user=admin&password=password&cmnd=Power%20on
        # http://stopbagger.local/cm?user=admin&password=password&cmnd=Power%20on
    #else if (weights[2] == boxcount)
        # http://scalelightred.local/cm?user=admin&password=password&cmnd=Power%20on
        # http://stopbagger.local/cm?user=admin&password=password&cmnd=Power%20on
    #else     previousweight = weights[0]  continue

    
ser.close()
#return weights
