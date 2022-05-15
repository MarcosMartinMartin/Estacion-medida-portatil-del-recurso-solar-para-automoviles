'''
Alumno / Programador : ÁLVARO MUÑOZ RUIZ
Grado : DOBLE GRADO EN INGENIERÍA ELÉCTRICA Y EN INGENIERÍA 
        ELECTRÓNICA Y AUTOMÁTICA
Univerisidad : UNIVERISDAD POLITÉCNICA DE MADRID
Escuela : ESCUELA TÉCNICA SUPERIOR DE INGENIERÍA Y DISEÑO INDUSTRIAL
'''

# PROYECTO

'''
---------------------------------------------------------------
--- LIBRERÍA - EVALUACIÓN DEL RECURSO SOLAR DEL COCHE SOLAR ---
---       MÓDULO DE TRATAMIENTO MÁSCARAS DE IMAGENES        ---
---------------------------------------------------------------

modificado MARCOS MARTíN MARTÍN 20/02/2022

Uso de la máscara rápida junto con la programada anteriormente con los filtros de color
'''
# Importa las librerias


import numpy as np
import cv2

class mascaras:
    def mask(self, image):
        #trackbars
        def empty():
            pass
        
        imgHSV = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        lower = np.array([0, 0, 40])   #h_min, s_min, v_min 0,0,118
        upper = np.array([179, 255, 255])   #h_max, s_max, v_max 130l,
        mask = cv2.inRange(imgHSV, lower, upper)
        
        # Umbral del procesado
        thresh = cv2.threshold(
            mask, 0, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C + cv2.THRESH_OTSU)[1]

        # Filtrado usando área de contornos y elimninando el ruido
        cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            area = cv2.contourArea(c)
            if area < 0.0005: #0.0005
                cv2.drawContours(thresh, [c], -1, (0, 0, 0), -1)

        # Cierre morfológico e inversión de la imagen
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        close = 255 - cv2.morphologyEx(thresh,
                                       cv2.MORPH_CLOSE, kernel, iterations=5)
        return close


    
    #misma máscara pero generando barras para obtener los parámetros correctos
    def mask_test(self, image):
        #trackbars
        def empty():
            pass
        
        cv2.namedWindow("TrackBars")
        cv2.resizeWindow("TRackBars", 640, 240)
        cv2.createTrackbar("Hue min", "TrackBars", 0, 179, empty)
        cv2.createTrackbar("Hue Max", "TrackBars", 179, 179, empty)
        cv2.createTrackbar("Sat min", "TrackBars", 0, 255, empty)
        cv2.createTrackbar("Sat Max", "TrackBars", 255, 255, empty)
        cv2.createTrackbar("Val min", "TrackBars", 0, 255, empty)
        cv2.createTrackbar("Val Max", "TrackBars", 255, 255, empty)
        h_min = cv2.getTrackbarPos("Hue min", "TrackBars") #15
        h_max = cv2.getTrackbarPos("Hue Max", "TrackBars") #179
        s_min = cv2.getTrackbarPos("Sat min", "TrackBars") #0
        s_max = cv2.getTrackbarPos("Sat Max", "TrackBars") #255
        v_min = cv2.getTrackbarPos("Val min", "TrackBars") #70
        v_max = cv2.getTrackbarPos("Val Max", "TrackBars") #255
        
        
        
        imgHSV = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        lower = np.array([0, 0, 40])   #h_min, s_min, v_min 0,0,118
        upper = np.array([179, 255, 255])   #h_max, s_max, v_max 130l,
        mask = cv2.inRange(imgHSV, lower, upper)
        # Umbral del procesado
        thresh = cv2.threshold(
            mask, 0, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C + cv2.THRESH_OTSU)[1]

        # Filtrado usando área de contornos y elimninando el ruido
        cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            area = cv2.contourArea(c)
            if area < 0.0005: #0.0005
                cv2.drawContours(thresh, [c], -1, (0, 0, 0), -1)

        # Cierre morfológico e inversión de la imagen
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        close = 255 - cv2.morphologyEx(thresh,
                                       cv2.MORPH_CLOSE, kernel, iterations=5)
        return close
