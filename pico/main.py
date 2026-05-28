from machine import ADC, PWM, Pin
from time import sleep

pot = ADC(26)   # GP26 = ADC0
servo = PWM(Pin(16))
servo.freq(50)

# segmentos
a = Pin(0, Pin.OUT)
b = Pin(1, Pin.OUT)
c = Pin(2, Pin.OUT)
d = Pin(3, Pin.OUT)
e = Pin(4, Pin.OUT)
f = Pin(5, Pin.OUT)
g = Pin(6, Pin.OUT)


producto = 0


def leer_potenciometro():        
    Leer = True
    
    while Leer:
        
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
            
        sleep(0.3)
        

segmentos = [a,b,c,d,e,f,g]

numeros = {
    1: [1,0,0,1,1,1,1],
    2: [0,0,1,0,0,1,0],
    3: [0,0,0,0,1,1,0]
}


def cambiar_7segmentos(numero):
    
    if numero in numeros:

        for i in range(7):
            #cada valor de i va hacer un segmento
            segmentos[i].value(numeros[numero][i])


#CONSTANTES
ABRIR = 5000
CERRAR = 2000

def levantar_compuerta():
    
    servo.duty_u16(ABRIR)   # abrir compuerta
    
    sleep(3)

    servo.duty_u16(CERRAR)   # cerrar compuerta


servo.duty_u16(CERRAR) # Cerrar la compuerta al iniciar el código

levantar_compuerta()


    
