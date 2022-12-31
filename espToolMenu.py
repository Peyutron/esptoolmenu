#manera fácil de programar y borrar ESP32 y ESP8266 en Linux
#Fuentes:
#https://www.codigopiton.com/como-hacer-un-menu-de-usuario-en-python/
#https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python

import os   #importa libreria para acceder al sistema de archivos
import serial.tools.list_ports

direccion = "~/.local/bin/" #dirección del archivo esptool.py

comlist = serial.tools.list_ports.comports() #Devuelve una lista de puertos COM
connected = []

nmenu = 0
set_port = ''


def listado_com(): 
    for element in comlist:
        connected.append(element.device)
    return connected
    
def mostrar_menu(opciones):
    global set_port
    print('Seleccione una opción para puerto: ',  set_port)
    for clave in sorted(opciones):
        print(f' {clave}) {opciones[clave][0]}')
        
def leer_opcion(opciones):
    while (a := input('Opción: ')) not in opciones:
        print('Opción ',  a, ' incorrecta, vuelva a intentarlo.')
    return a

def ejecutar_opcion(opcion, opciones):
    if nmenu == 0:
        global set_port
        set_port =  opciones[opcion][0]
        opciones[opcion][1]()
    else:
        opciones[opcion][1]()        
        
def generar_menu(opciones, opcion_salida):
    opcion = None
    while opcion != opcion_salida:
        mostrar_menu(opciones)
        opcion = leer_opcion(opciones)
        ejecutar_opcion(opcion, opciones)
        print()
        
def menu_com(listado):
    opciones = {}
    for index,  com_port in enumerate(listado):
        opciones[str(index)] = (com_port,  accion10)
        opciones['s'] = ('Salir', salir) #añado la opcion de salir al final del diccionario
    generar_menu(opciones, len(listado))

def is_empty(data_structure):
    if data_structure:
        return False
    else:
        print("No hay ningun USB disponible")
        return True


def menu_principal():
    opciones = {
        '1': ('Información', accion1),
        '2': ('Borrar ESP32', accion2),
        '3': ('Borrar ESP8266', accion3),
        '4': ('Subir binario',  accion4),
        's': ('Salir', salir)
    }
    generar_menu(opciones, '5')


def accion1():
    print('Información del chip:')
    os.system(direccion + 'esptool.py chip_id ')
def accion2():
    print('Borrando ESP32...')
    os.system(direccion + 'esptool.py --chip esp32 --port '+ set_port +  'erase_flash')
   # os.system(direccion + 'esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash')
def accion3():
    print('Borrando ESP8266...')
    os.system(direccion + 'esptool.py --chip esp8266 --port ' + set_port + ' erase_flash')
    #os.system(direccion + 'esptool.py --chip esp8266 --port /dev/ttyUSB0 erase_flash')

    print('Borrando finalizado...')
    
def accion4():
    ruta = input('escribe la ruta: ')
    print('Quemando binario ESP8266...')
    os.system(direccion + 'esptool.py --chip esp8266 --port /dev/ttyUSB0 write_flash 0x0 '+ ruta)
    #os.system(direccion + 'esptool.py --chip esp8266 --port /dev/ttyUSB0 erase_flash')
    print('Quemado finalizado...')

def accion10():
    global nmenu
    nmenu = 1
    menu_principal()



def salir():
    print('Saliendo del programa')
    quit()



connected = listado_com()
if __name__ == '__main__':
    if nmenu == 0: 
        if is_empty(connected) == True: quit('La lista estaba vacia :(') 
        else: menu_com(connected)
    else: 
        menu_principal()
#
#
##print("Connected COM ports: " + str(connected))
#

