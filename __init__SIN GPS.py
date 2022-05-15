from camara import VideoCapture
#from gps import GPS
from magnetometro import HMC5883L
from mascaras import mascaras
from datos_sol import solarPos
from datos_sol import tmy
from procesado_img import procesadoImagen
from IoT import ThingSpeak


import time
import cv2
from datetime import datetime

tmy=tmy()

iot = ThingSpeak()

#gps = GPS()
brujula = HMC5883L()
mask = mascaras()
solPos = solarPos()
img_procesado = procesadoImagen()

cap = VideoCapture(0)

frame = cap.read()

delay=delay()

SOL=0
SFV=0
DNI=0
DHI=0

segundos = 0
bdt=0

while True:
    
    frame = cap.read()
    
    #gps_data = gps.get_datos()
    brujula_data = brujula.direccion()
    
    ##DATOS GPS SUSTITUIDOS
    hora = datetime.now().hour-2  #-2POSICION DEL SOL CALCULADA CON GMT 0
    minuto = datetime.now().minute
    latitud = 40.3100000  #40.4053673 #40.3100000
    longitud = -3.4856012 #-3.700096 #-3.4856012
        
    ##posicion solar
    solares = solPos.solarPos(hora, minuto, latitud, longitud)
    #pixel donde virtualmente se encuentra el Sol
    pixelSolar = solPos.solares_a_pixel(solares[0], solares[1], brujula_data)

    #prueba de brujula: las orientaciones magnéticas cada una pintada para un ángulo zenit diferente (test)
    pixelRosaN = solPos.solares_a_pixel(0, 80, brujula_data)
    pixelRosaE = solPos.solares_a_pixel(90, 60, brujula_data)
    pixelRosaS = solPos.solares_a_pixel(180, 45, brujula_data)
    pixelRosaO = solPos.solares_a_pixel(270, 30, brujula_data)
    pixel_rosa = (pixelRosaN, pixelRosaE, pixelRosaS, pixelRosaO)  
    
    ###pintar brujula
    frame_pintado = frame.copy()
    frame_pintado = img_procesado.pintarHUD(frame_pintado, pixel_rosa, pixelSolar)
    
    frame_previo=frame_pintado.copy()
    
    cv2.imshow("previo", frame_previo )
    
    ####if chr(cv2.waitKey(1)&255) == 'e':
    if(segundos>30 or bdt==0):
        bdt=1
        segundos=0
        instanteInicial=datetime.now()
        print('Procesando frame...')
        #procesado de imagen completa
        frame_mascara = frame.copy()
        frame_mascara = mask.mask(frame)
        
        #obtención del parametro sombra y el factor SVF
        SOL = img_procesado.sol(frame_mascara, pixelSolar, frame_pintado)
        SVF = img_procesado.SVF(frame_mascara, frame_pintado)
        
        
        ##obtención del DNI y el DHI sobre el año tipico meteorológico
        tmy.set_parametros(latitud, longitud, datetime.today().month, datetime.today().day, hora)
        tmy.actualizar_tmy()
        ##obtención del DNI y DHI sobre el dispositivo
        DNI=tmy.DNI*SOL
        DHI=tmy.DHI*SVF
        
        ##imprimir datos (descomentar para test)
        print('DNI TMY: ', tmy.DNI, ' - DHI TMY: ',tmy.DHI, '   -DNI calculado: ', DNI ,'...sombra...',SOL, '  DHI calculado: ', DHI, '...SVF...', SVF)
        
        #enviar datos a plataforma IoT
        iot.enviar(latitud, longitud, DNI, DHI)
        
        #mostrar frame capturado y proesado de imagen (descomentar para test)
        cv2.imshow("mascara", frame_mascara) 
        cv2.imshow("frame_pintado", frame_pintado )
        
        print('...frame procesado')
    instanteFinal=datetime.now()
    tiempo = instanteFinal - instanteInicial
    segundos = tiempo.seconds
        
    
            
    
    
    if chr(cv2.waitKey(1)&255) == 'q':
        break        
    
    