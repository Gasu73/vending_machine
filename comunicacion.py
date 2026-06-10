# Imports
import socket
import json


def pedir_datos(ip):

    try:
        canal = socket.socket() # Crea un canal de comunicación TCP
        canal.settimeout(10) # Espera 10 segundos para la respuesta, si no lanza error
        canal.connect((ip, 8080)) # Conectar a la IP de la Pico en el puerto 8080

        print("Enviando a Raspberry:", repr("GET_DATA\n")) # repr es para imprimir el \n
        canal.send("GET_DATA\n".encode()) # \n es para decirle a la Rasp que el mensaje finaliza ahí
                                          # encode, convierte el texto en bytes, códifica para el socket

        respuesta = canal.recv(4096).decode() # decode decodifica los bytes a texto, recv() tiene como parametro
                                              # el máximo de bytes que se reciben en una única llamada

        canal.close()

        print(f"Datos recibidos: {respuesta}")
        return json.loads(respuesta) # Devuelve la respuesta como diccionario, json.loads convierte texto a dic

    except Exception as error: # Guarda cualquier error que ocurra
        print(f"Error al conectar: {error}")
        return None


def enviar_mantenimiento(ip, activar):
    try:
        canal = socket.socket() # Crea el canal TCP
        canal.settimeout(5) # Tiempo de espera para la respuesta
        canal.connect((ip, 8080)) # Conexión con la rasp en el puerto 8080

        comando = json.dumps({"accion": "mantenimiento", "estado": activar}) # Se convierte el diccionario a str json
        canal.sendall((comando + "\n").encode()) # Envía el comando en bytes a la rasp
        canal.close()

        return True

    except Exception as error:
        print(f"Error al enviar mantenimiento: {error}") # Si no responde después del contador
        return False