from machine import ADC, PWM, Pin
from time import sleep
import ujson

pot = ADC(26)   # GP26 = ADC0
servo = PWM(Pin(16))
servo.freq(50)
boton  = Pin(9, Pin.IN, Pin.PULL_UP)

led_verde = Pin(14, Pin.OUT)
led_rojo = Pin(15, Pin.OUT)


# segmentos
a = Pin(0, Pin.OUT)
b = Pin(1, Pin.OUT)
c = Pin(2, Pin.OUT)
d = Pin(3, Pin.OUT)
e = Pin(4, Pin.OUT)
f = Pin(5, Pin.OUT)
g = Pin(6, Pin.OUT)


segmentos = [a,b,c,d,e,f,g]
numeros = {
    0: [0,0,0,0,0,0,1],
    1: [1,0,0,1,1,1,1],
    2: [0,0,1,0,0,1,0],
    3: [0,0,0,0,1,1,0],
    4: [1,0,0,1,1,0,0],
    5: [0,1,0,0,1,0,0],
    6: [0,1,0,0,0,0,0],
    7: [0,0,0,1,1,1,1],
    8: [0,0,0,0,0,0,0],
    9: [0,0,0,0,1,0,0],
    -1: [1,1,1,1,1,1,1]
}



producto = 1


#Funciones JSON
def cargar_productos():
    with open("productos.json", "r") as archivo:
        return ujson.load(archivo)

def guardar_productos(productos):
    with open("productos.json", "w") as archivo:
        ujson.dump(productos, archivo)

def cargar_ventas():
    with open("ventas.json", "r") as archivo:
        return ujson.load(archivo)

def guardar_ventas(ventas):
    with open("ventas.json", "w") as archivo:
        ujson.dump(ventas, archivo)
        
        


def leer_potenciometro():
    global producto
    
    valor = pot.read_u16()

    print("Valor:", valor)

    if valor < 20000:
        print("1")   # izquierda
        producto = 1

    elif valor < 45000:
        print("2")   # centro
        producto = 2
        
    else:
        print("3")   # derecha
        producto = 3
    


def cambiar_7segmentos(numero):
    
    if numero in numeros:

        for i in range(7):
            #cada valor de i va hacer un segmento
            segmentos[i].value(numeros[numero][i])
            
            
def cambiar_leds(stock):

    if stock > 0:
        led_verde.value(1)
        led_rojo.value(0)

    else:
        led_verde.value(0)
        led_rojo.value(1)
            


#CONSTANTES
ABRIR = 5000
CERRAR = 2000

def levantar_compuerta():
    
    servo.duty_u16(ABRIR)   # abrir compuerta
    
    sleep(3)

    servo.duty_u16(CERRAR)   # cerrar compuerta
    
    
def vender_producto():
    productos = cargar_productos()
    ventas = cargar_ventas()

    id_producto = str(producto)

    nombre = productos[id_producto]["nombre"]

    if productos[id_producto]["stock"] > 0:

        productos[id_producto]["stock"] -= 1
        ventas[nombre] += 1

        guardar_productos(productos)
        guardar_ventas(ventas)
        
        levantar_compuerta()

        print("Venta realizada")

    else:
        print("Sin stock")



servo.duty_u16(CERRAR) # Cerrar la compuerta al iniciar el código
cambiar_7segmentos(-1) # Apagar 7 segmentos

productos = cargar_productos()

while True:

    leer_potenciometro()

    stock = productos[str(producto)]["stock"]

    cambiar_7segmentos(stock)
    cambiar_leds(stock)
    

    if boton.value() == 0 and stock > 0:

        vender_producto()

        productos = cargar_productos()  # recargar después de vender
        
        stock = productos[str(producto)]["stock"]

        cambiar_7segmentos(stock)
        cambiar_leds(stock)

        while boton.value() == 0:
            sleep(0.01)

    sleep(0.1)


    
