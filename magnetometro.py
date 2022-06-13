import RPi.GPIO as GPIO
import smbus
import time
import math
import csv

class HMC5883L:
    address = 0x1e

    #inicializaciones predeterminadas
    scale = 1
    scale_x = 0.7
    scale_y = 0.7
    x_offset = 35
    y_offset = -176.5
    
    def __init__(self):        
        rev = GPIO.RPI_REVISION
        if rev == 2 or rev == 3:
            self.bus = smbus.SMBus(1)
        else:
            self.bus = smbus.SMBus(0)
        self.write_byte(0, 0b01110000) # Set to 8 samples @ 15Hz
        self.write_byte(1, 0b00100000) # 1.3 gain LSb / Gauss 1090 (default)
        self.write_byte(2, 0b00000000) # Continuous sampling
        print('Brujula inicializada')
        
       #leer el archivo donde se guardan los datos para el calibrado del sensor
        with open('ConfiguracioMag.csv', newline='') as File:  
            reader = csv.reader(File)
            for row in reader:
                x_offset=float(row[0])
                y_offset=float(row[1])
                scale_x=float(row[2])
                scale_y=float(row[3])
        print("Calibracion brujula: ", x_offset, ' ', y_offset, ' ', scale_x, ' ', scale_y)

    def read_byte(self, adr):
        return self.bus.read_byte_data(self.address, adr)

    def read_word(self, adr):
        high = self.bus.read_byte_data(self.address, adr)
        low = self.bus.read_byte_data(self.address, adr+1)
        val = (high << 8) + low
        return val

    def read_word_2c(self, adr):
        val = self.read_word(adr)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val

    def write_byte(self, adr, value):
        self.bus.write_byte_data(self.address, adr, value)
    
    def direccion(self):
    
        x_out = (self.read_word_2c(3) - self.x_offset) * self.scale_x
        y_out = (self.read_word_2c(7) - self.y_offset) * self.scale_y
        z_out = (self.read_word_2c(5)) * self.scale

        
        
        bearing  = math.atan2(y_out, x_out) 
        if (bearing < 0):
            bearing += 2 * math.pi
        
        declination =0.3
        bearing = math.degrees(bearing) + declination
        time.sleep(0.1)
        
            
        return bearing