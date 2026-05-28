from machine import ADC, PWM, Pin
from time import sleep

pot = ADC(26)   # GP26 = ADC0
servo = PWM(Pin(16))
servo.freq(50)

producto = 0

while False:
    
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
    
    
    
def cambiar_7segmentos(numero):
    





#CONSTANTE
ABRIR = 5000
CERRAR = 2000

def levantar_compuerta():
    
    servo.duty_u16(ABRIR)   # abrir compuerta
    
    sleep(3)

    servo.duty_u16(CERRAR)   # cerrar compuerta


servo.duty_u16(CERRAR) # Cerrar la compuerta al iniciar el código

levantar_compuerta()


    
