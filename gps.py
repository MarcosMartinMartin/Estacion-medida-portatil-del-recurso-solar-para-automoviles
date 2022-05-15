import RPi.GPIO as GPIO
import cv2, queue, threading, time
import serial
import numpy as np

'''LECTOR DEL MóDULO GPS'''

class GPS:
    
    #GPS
    ser = serial.Serial('/dev/ttyS0',9600)
    ser.flushInput()

    power_key = 4
    rec_buff = ''
    rec_buff2 = ''
    time_count = 0.5
    
    datos = np.array([0,0,0,0])
        
    def __init__(self):
        
        #poner en marcha el modulo
        print('SIM7000X está arrancando:')
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.power_key,GPIO.OUT)
        time.sleep(0.1)
        GPIO.output(self.power_key,GPIO.HIGH)
        time.sleep(2)
        GPIO.output(self.power_key,GPIO.LOW)
        time.sleep(2)
        self.ser.flushInput()
        print('SIM7000X ha sido arrancado')
        
        #conectar a la red GPS
        rec_null = True        
        print('Comenzando sesión GPS')
        self.rec_buff = ''
        self.send_at('AT+CGNSPWR=1','OK',1)
        print('...')
        time.sleep(10)
        #print('PRUEBA DE TODOS LOS DATOS')
        self.send_at('AT+CGNSTST=1', 'OK', 1)
        time.sleep(2)
        self.send_at('AT+CGNSTST=0', 'OK', 1)
        time.sleep(2)
        
        #hilo
        self.q = queue.Queue()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()
    
    def send_at(self, command,back,timeout):
        #función para el envío de comandos AT
        self.rec_buff = ''
        self.ser.write((command+'\r\n').encode())
        time.sleep(timeout)
        if self.ser.inWaiting():
            time.sleep(0.01 )
            self.rec_buff = self.ser.read(self.ser.inWaiting())
        if self.rec_buff != '':
            if back not in self.rec_buff.decode():
                print(command + ' ERROR')
                print(command + ' back:\t' + self.rec_buff.decode())
                print('GPS-send_at: se recibe error')
                return 0
            else:
                return self.rec_buff.decode()
        else:
            print('GPS-send_at: no se recibe respuesta')
            return 0

    def get_gps_data(self):
        answer=0
        
        #Obtener los datos CGNSINF
        answer = self.send_at('AT+CGNSINF','+CGNSINF: ',1)
        if(answer!=0):
            
            datos0 = answer.replace(",", " ")
            datos = datos0.split()
            
            #revisión de este dato, el primero que se es 0 al perder conexión GPS
            if(datos[3]=="0"):
                print("GPS-get_data: se recibe cero. Iniciando bucle para la reconexión")
                while (datos[3]=='0'):
                    self.send_at('AT+CGNSINF','+CGNSINF: ',1)
                    datos0 = answer.replace(",", " ")
                    datos = datos0.split()
                print("GPS-get_data: conexión recuperada. Saliendo del bucle '0'")
                return datos
            else:   
                return datos
            
            #revisión de este dato, ',,,,,' cobertura perdida
            if ',,,,,,' in self.rec_buff:
                print("GPS-get_data: se recibe ,,,,,,. Iniciando bucle para la reconexión")
                while (datos[3]=='0'):
                    self.send_at('AT+CGNSINF','+CGNSINF: ',1)
                    datos0 = answer.replace(",", " ")
                    datos = datos0.split()
                print("GPS-get_data: conexión recuperada. Saliendo del bucle ',,,,'")
                return datos
        else:
            print('error %d'%answer)
            self.rec_buff = ''
            self.send_at('AT+CGPS=0','OK',1)
            return False
        time.sleep(1.5)


    def _reader(self):
        while True:
            datos = self.get_gps_data()
            
            if not self.q.empty():
                try:
                    self.q.get_nowait()   # discard previous (unprocessed) frame
                except queue.Empty:
                  pass
            self.q.put(datos)

    def get_datos(self):
        return self.q.get()

