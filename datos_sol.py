import matplotlib.pyplot as plt
import pvlib
from pvlib import tracking
from pvlib import pvsystem, location, modelchain
from pvlib import solarposition
import matplotlib.pyplot as plt
import datetime
import math
import numpy as np
import pandas as pd
import json
  
    
class solarPos:  
    
    def solarPos(self, hora, minuto, latitud, longitud):
    
        tod_date = datetime.date.today()
        tod = str(datetime.date.today().year)+'-'+str(datetime.date.today().month)+'-'+str(datetime.date.today().day)
        

    #SALVAR LOS CAMBIOS DE MES
        td = datetime.timedelta(1)
        tom_date = tod_date + td

        tom = str(tom_date.year)+'-'+str(tom_date.month)+'-'+str(tom_date.day)

        tz = 'Etc/GMT+0'
    #lat, lon = 40.5899224, -4.4114131
        loc = location.Location(latitud, longitud)
        times = pd.date_range(tod, tom, closed='left', freq='1min', tz=tz)
        
    #generar la tabla con las posiciones solares de todo un día
        tabla_sol=loc.get_solarposition(times)

    #instante actual
        ahora = (hora*60+minuto)-1 #-1 ¿por que?-> minuto actual

        zenit = tabla_sol['apparent_zenith'][ahora]
        azimut = tabla_sol['azimuth'][ahora]
        
        solarpos = [azimut, zenit]
        
        
        return solarpos
    
    def solares_a_pixel(self, az, ze, direccion):
        deg=(az-direccion)   
        if(deg>360):
            deg=deg-360
        if(deg<0):
            deg=deg+360
        deg=deg+90 #+90 por rotar el elje x y +7 porque son los grados de diferencia entre la cámara y el chasis del dispositivo (cuando el chasis está completamente alineado con el Norte (0º) la camara está en dirección 7º)

        #con el calibrado tenemos que 5pixeles son alrededor de 1º por lo que el sol en Zenit 0º es r=0 y el zenit 90º r= tamaño imagen en y/2
        r=4.6*ze
        if(r>400):
            r=400         
    
        #de polares a cartesianas
        x=math.cos((deg* math.pi)/180)*r
        y=math.sin((deg* math.pi)/180)*r
        
        
        #cartesianas a pixeles
        x_pixel=x+412
        if(x_pixel>799):
            x_pixel=799
        if(x_pixel<1):
            x_pixel=1
            
        y_pixel=316-y
        if(y_pixel>599):
            x_pixel=599
        if(x_pixel<1):
            y_pixel=1

        pixel_sol = (x_pixel, y_pixel)
        
        
        return pixel_sol


#clase para el año meteorológico típico
class tmy:
    DNI=0
    DHI=0
    lat=0
    lon=0
    mes=0
    dia=0
    hora=0
    
    def set_parametros(self, lat, lon, mes, dia, h):
        self.lat=lat
        self.lon=lon
        self.mes=mes
        self.dia=dia
        self.hora=h
    
    def actualizar_tmy(self):
        medidas=pvlib.iotools.get_pvgis_tmy(self.lat, self.lon, outputformat='epw', usehorizon=True, userhorizon=None, url='https://re.jrc.ec.europa.eu/api/', timeout=30)
        
        datos=medidas[0][["ghi","dni","dhi"]]
        
        ##colocar todos los datos en el mismo año para localizarlos sin errores
        nueva_fecha=[]
        for i in range(len(datos)):
            nueva_fecha.append(datos.index[i].replace(year=2000)+datetime.timedelta(minutes=30))
        datos_buenos=datos.reindex(nueva_fecha)
        datos_buenos["ghi"][:]=datos["ghi"][:]
        datos_buenos["dni"][:]=datos["dni"][:]
        datos_buenos["dhi"][:]=datos["dhi"][:]
        
        if(self.mes<10):
            smes="0" + str(self.mes)
        else:
            smes=str(self.mes)
        if(self.dia<10):
            sdia="0" + str(self.dia)
        else:
            sdia=str(self.dia)
        fecha=("2000-" + smes + "-" + sdia + " " + str(self.hora) + ":30:00+01:00")
        
        self.DNI = datos_buenos.loc[fecha, "dni"]
        self.DHI = datos_buenos.loc[fecha, "dhi"]    