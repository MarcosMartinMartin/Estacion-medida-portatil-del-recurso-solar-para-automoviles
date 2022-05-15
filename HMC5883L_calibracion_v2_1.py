#https://gist.github.com/ViennaMike/d8b8f9636694c7edf4f115b28c9378c0
#https://www.instructables.com/Configure-read-data-calibrate-the-HMC5883L-digital/

#CALIBRADO DEL SENSOR -> GENERA ARCHIVO CON OFFSET Y GANANCIA

import RPi.GPIO as GPIO
import smbus
import time
import math
import csv



rev = GPIO.RPI_REVISION
if rev == 2 or rev == 3:
    bus = smbus.SMBus(1)
else:
    bus = smbus.SMBus(0)

address = 0x1e

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def write_byte(adr, value):
    bus.write_byte_data(address, adr, value)
       
def calibrar2():
    write_byte(0, 0b01110000) # Set to 8 samples @ 15Hz
    write_byte(1, 0b00100000) # 1.3 gain LSb / Gauss 1090 (default)
    write_byte(2, 0b00000000) # Continuous sampling
    mag=[0,0,0]
    
    running_mmin = (32767, 32767, 32767)
    running_mmax = (-32768, -32768, -32768)
    
    for i in range(500):
        # Read the X, Y, Z axis magnetometer
        mag_x = read_word_2c(3)
        mag_y = read_word_2c(7)
        mag_z = read_word_2c(5)
        
        # Grab the X, Y, Z components from the reading for printing.
        mag = (mag_x, mag_y, mag_z)
        # set lowest and highest values seen so far
        running_mmin = tuple(map(lambda x, y: min(x,y), running_mmin, mag))
        running_mmax = tuple(map(lambda x, y: max(x,y), running_mmax, mag))
        
        print('Mag ', mag_x, mag_y, mag_z)
        print('mag minimums: ',running_mmin)
        print('mag maximums: ',running_mmax)
        # Wait 1/10th of a second and repeat.
        time.sleep(0.1)
    # Compute Magnetometer Corrections
    # Corrects for "soft iron" errors (bias) and approximate correction for "hard iron" through scaling along 3 axes
    print('computing, printing, and saving calibration factors')
    # Magnetometer Corrections
    moffset = tuple(map(lambda x1, x2: (x1+x2) / 2., running_mmin, running_mmax))
    avg_mdelta = tuple(map(lambda x1, x2: (x2-x1)/2., running_mmin, running_mmax))
    combined_avg_mdelta = (avg_mdelta[0] + avg_mdelta[1] + avg_mdelta[2])/3.
    scale_mx = combined_avg_mdelta / avg_mdelta[0]
    scale_my = combined_avg_mdelta / avg_mdelta[1]
    scale_mz = combined_avg_mdelta / avg_mdelta[2]
    print('magnetometer offsets: ',moffset)
    print('magentometer scaling: ',scale_mx, scale_my, scale_mz)
    
    
    moffset[0]
    moffset[1]
    scale_mx
    scale_my
    
    #outputFilename = "ConfiguracioMag_{0}.csv".format( int( time.time() ) )
    outputFilename = "ConfiguracioMag.csv"
    with open(outputFilename, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([moffset[0], moffset[1], scale_mx, scale_my])
    
    
calibrar2()


    