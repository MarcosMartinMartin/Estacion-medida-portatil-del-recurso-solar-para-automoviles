import cv2
import numpy as np

import math


class procesadoImagen:    

    #obtener el factor de cielo visto 
    def SVF(self, img, img2):
        #centro
        cx=412 
        cy=316
        
        #contadores
        sombra = 0
        sol=0
        contador_pixeles = 0
        contador_sombra = 0
        
        #barrer un cuadrado de 300x300
        for i in range(600): 
            for j in range(600):
                x=cx-300+i
                y=cy-300+j
                
                #limites de imagen
                if(x>799 or y>599 or x<1 or y<1):
                    contador_pixeles=contador_pixeles
                else:
                    
                    #comprobar si el pixel estudiado se encuentra en area definica por la circunferenica con radio 278pixeles y centro en (cx, cy)
                    if(math.sqrt(((x-cx)*(x-cx))+((y-cy)*(y-cy)))<278):
                        contador_pixeles=contador_pixeles+1
                        #test
                        if(math.sqrt(((x-cx)*(x-cx))+((y-cy)*(y-cy)))>277):
                            cv2.circle(img2, (x, y), 1, (0, 255, 0), thickness = 1)
                        #comprobación de luminosidad en pixel estudiado
                        if(img.item(y, x)<253):
                            contador_sombra = contador_sombra + 1
                        
                    
        if(contador_pixeles==0):
            print("no se ha contado ningun pixel")
        else:
            sombra=(contador_sombra/contador_pixeles)
        
        sfv=1-sombra
        
        return sfv
    
    #obtener dato de si se recibe el Sol directo
    def sol(self, img, solarPos, img2):
        #centro
        cx=int(solarPos[0]) 
        cy=int(solarPos[1])
        
        #contadores
        sombra = 0
        sol=0
        contador_pixeles = 0
        contador_sombra = 0
        
        
        #barrer un cuadrado de 36x36
        for i in range(92): 
            for j in range(92):
                x=cx-46+i
                y=cy-46+j
                
                #limites de imagen
                if(x>799 or y>599 or x<1 or y<1):
                    contador_pixeles=contador_pixeles
                else:                    
                    if(math.sqrt(((x-cx)*(x-cx))+((y-cy)*(y-cy)))<46):
                        contador_pixeles=contador_pixeles+1
                        #test
                        if(math.sqrt(((x-cx)*(x-cx))+((y-cy)*(y-cy)))>45):
                            cv2.circle(img2, (x, y), 1, (0, 255, 0), thickness = 1)
                        #comprobación de luminosidad en pixel estudiado
                        if(img.item(y, x)<253):
                            contador_sombra = contador_sombra + 1
                        
                    
        if(contador_pixeles==0):
            print("no se ha contado ningun pixel")
        else:
            sombra=(contador_sombra/contador_pixeles)
        
        if(sombra<0.60):
            sol=1
        
        return sol  
    
    #pintar un HUD con los puntos cardinales y la posición del Sol. Para la 'preview'
    def pintarHUD(self, img, rosa, sol):
        NORTE_x=int(rosa[0][0])
        NORTE_y=int(rosa[0][1])
        ESTE_x=int(rosa[1][0])
        ESTE_y=int(rosa[1][1])
        SUR_x=int(rosa[2][0])
        SUR_y=int(rosa[2][1])
        OESTE_x=int(rosa[3][0])
        OESTE_y=int(rosa[3][1])
        x=int(sol[0])
        y=int(sol[1])
        
        
        cv2.circle(img, (NORTE_x, NORTE_y), 6, (0, 0, 255), thickness = 4)
        cv2.line(img,(412, 316),(NORTE_x, NORTE_y),(0,0,255),2)
        cv2.circle(img, (ESTE_x, ESTE_y), 6, (0, 255, 0), thickness = 4)
        cv2.circle(img, (SUR_x, SUR_y), 6, (255, 0, 0), thickness = 4)
        cv2.circle(img, (OESTE_x, OESTE_y), 6, (0, 255, 255), thickness = 4)
        
        cv2.circle(img, (x, y), 12, (255, 0, 0), thickness = 1)
        return img
        
        
    #para calibrar la cámara: desplegar barras para obtener la relación de delta de angulo zenit por pixel, el centro de la imganen y el radio máximo operativo
    def calibrador(self, img):
        #trackbars
        def empty():
            pass
        
        cv2.namedWindow("TrackBars")
        cv2.resizeWindow("TRackBars", 640, 240)
        cv2.createTrackbar("X", "TrackBars", 0, 800, empty)
        cv2.createTrackbar("Y", "TrackBars", 0, 600, empty)
        cv2.createTrackbar("RADIO", "TrackBars", 0, 600, empty)

        
        x = cv2.getTrackbarPos("X", "TrackBars")
        y = cv2.getTrackbarPos("Y", "TrackBars")
        r = cv2.getTrackbarPos("RADIO", "TrackBars")
        
        cv2.circle(img, (x, y), r, (255, 0, 0), thickness = 2)
        cv2.line(img,(x, y),(x, 0),(0,255,0),1)
        cv2.line(img,(x, y),(x, 599),(0,255,0),1)
        cv2.line(img,(x, y),(0, y),(0,255,0),1)
        cv2.line(img,(x, y),(799, y),(0,255,0),1)
        
        return img
