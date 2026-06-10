# main.py
# Inicia Pygame y corre el bucle principal.
# Ejecute este archivo para abrir la app.

import pygame
import sys
import constantes
from pantallas.pantalla_conexion     import PantallaConexion
from pantallas.pantalla_dashboard    import PantallaDashboard
from pantallas.pantalla_estadisticas import PantallaEstadisticas


def main():
    pygame.init() # Se inician los modulos de pygame

    ventana = pygame.display.set_mode((constantes.ANCHO, constantes.ALTO)) #Dimenciones de la ventana

    pygame.display.set_caption("CElect Admin") #Título de la ventana

    reloj = pygame.time.Clock()

    # Una sola fuente para toda la app
    fuente = pygame.font.SysFont(None, 26)

    # Empezamos en la pantalla de conexión
    pantalla_activa   = constantes.PANTALLA_CONEXION
    pantalla_conexion = PantallaConexion(fuente)

    # Estas se crean después de conectarse
    pantalla_dashboard    = None
    pantalla_estadisticas = None

    corriendo = True

    while corriendo:

        # Eventos
        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                corriendo = False

            if pantalla_activa == constantes.PANTALLA_CONEXION:
                pantalla_conexion.manejar_evento(evento) # Pasa eventos a la pantalla de conexión

            elif pantalla_activa == constantes.PANTALLA_DASHBOARD:
                cambio = pantalla_dashboard.manejar_evento(evento)
                if cambio is not None:
                    pantalla_activa = cambio
                # Se realiza el cambio a la pantalla de estadistica, si se devuelve None no ocurre cambio, si devuelve otra cosa ocurre cambio

            elif pantalla_activa == constantes.PANTALLA_ESTADISTICAS:
                cambio = pantalla_estadisticas.manejar_evento(evento)
                if cambio is not None:
                    pantalla_activa = cambio
                    # Se realiza el cambio a la pantalla de dashboard, si se devuelve None no ocurre cambio, si devuelve otra cosa ocurre cambio

        #Revisar si la conexión terminó
        if pantalla_activa == constantes.PANTALLA_CONEXION:
            if pantalla_conexion.datos_recibidos is not None:
                datos = pantalla_conexion.datos_recibidos
                ip    = datos["ip"]

                pantalla_dashboard    = PantallaDashboard(fuente, datos, ip)
                pantalla_estadisticas = PantallaEstadisticas(fuente, datos)
                pantalla_activa       = constantes.PANTALLA_DASHBOARD
        # Si se logra conectar se rellenan los datos, es decir no está vacío, se crean las otras dos pantallas y se pasa a la pantalla del dashboard.


        # Dibujar la pantalla activa
        if pantalla_activa == constantes.PANTALLA_CONEXION:
            pantalla_conexion.dibujar(ventana)

        elif pantalla_activa == constantes.PANTALLA_DASHBOARD:
            pantalla_dashboard.dibujar(ventana)

        elif pantalla_activa == constantes.PANTALLA_ESTADISTICAS:
            pantalla_estadisticas.dibujar(ventana)

        # Verifica cual pantalla es la activa, para dibujarla con el metodo dibujar.

        pygame.display.flip() # Muestra en pantalla lo dibujado en el frame
        reloj.tick(constantes.FPS) # Espera lo necesario para no correr a más de 60 FPS

    pygame.quit() # Cierra modulos de pygame
    sys.exit() # Cierra el programa


if __name__ == "__main__":
    main()
# Esto hace que solo se pueda ejecutar desde este archivo, no desde otros que lo importen