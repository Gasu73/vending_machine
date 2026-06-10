# pantallas/pantalla_estadísticas.py
# Muestra ventas por producto, ganancias en colones y dólares.

import pygame
import urllib.request
import json
import constantes


def obtener_tipo_de_cambio():
    try:
        with urllib.request.urlopen("https://open.er-api.com/v6/latest/CRC", timeout=5) as respuesta:
            datos = json.loads(respuesta.read().decode())
            # urllib.request.urlopen() abre una URL como si fuera un archivo
            # Se abre y se cierra automáticamente con el with as
            # read () lee los bytes descargados del URL, decode() los decodifica y json.loads lo transforma en diccionario
            
            return datos["rates"]["USD"]
            # devuelve dentro de rates, dentro de USD el tipo de cambio del dollar

    except:
        return 1 / 515.0   #  aproximadamente 515 colones por dólar si no hay internet


class PantallaEstadisticas:

    def __init__(self, fuente, datos):
        self.fuente = fuente

        # datos["ventas"] = {"Coca-Cola": 5, "Pepsi": 3, "Fanta": 2}
        ventas = datos["ventas"]

        self.lista_ventas = []

        for producto, cantidad in ventas.items():
            self.lista_ventas.append({"producto": producto, "cantidad": cantidad})
            # Agrega un diccionario con las claves producto y cantidad por cada producto y cantidad en el diccionario ventas
            # lista_ventas = [{"producto": "Coca-Cola", "cantidad": 5}]

        # Calculamos totales
        self.total_vendido  = sum(ventas["cantidad"] for ventas in self.lista_ventas)

        # La expresión dentro (ventas["cantidad"] for ventas in ...) es un generador:
        # sum() suma todos los valores de un elemento, en este caso el generador de las ventas.
        # Recorre cada venta y saca solo la cantidad, mientras sum() las va sumando.

        self.ganancias_colones = self.total_vendido * constantes.PRECIO

        # Descargamos el tipo de cambio una sola vez al crear la pantalla
        tipo_cambio            = obtener_tipo_de_cambio()
        self.ganancias_dolares = self.ganancias_colones * tipo_cambio

        # Botón de navegación
        self.rect_btn_dashboard = pygame.Rect(650, 10, 130, 35) # Botón arriba a la derecha (x , y, ancho, alto)

    def manejar_evento(self, evento):
        """
        Retorna el nombre de la pantalla a ir, o None.
        """
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect_btn_dashboard.collidepoint(evento.pos):
                return constantes.PANTALLA_DASHBOARD

        # Si se da click sobre el botón de dashboard devuelve la pantalla de dashboard para cambiarla en el bucle principal
        # collidepoint() verifica que un punto esté dentro de un rectángulo
        # evento.pos: posición de x, y del mouse en ese momento

        return None


    def dibujar(self, ventana):
        ventana.fill((255, 255, 255)) # El fondo blanco

        # Barra de navegación
        pygame.draw.rect(ventana, (220, 220, 220), pygame.Rect(0, 0, constantes.ANCHO, 50))
        # Fondo gris de la barra de navegación

        ventana.blit(self.fuente.render("Estadísticas", True, (0, 0, 0)), (10, 15))
        # Texto de esta

        pygame.draw.rect(ventana, (200, 200, 200), self.rect_btn_dashboard) # Botón de dashboard
        pygame.draw.rect(ventana, (0, 0, 0), self.rect_btn_dashboard, 1) # Borde del botón
        ventana.blit(self.fuente.render("Dashboard", True, (0, 0, 0)), (self.rect_btn_dashboard.x + 20, self.rect_btn_dashboard.y + 8)) # Texto de dashboard

        # Ventas por producto
        ventana.blit(self.fuente.render("Ventas por producto:", True, (0, 0, 0)), (50, 70))

        for indice, venta in enumerate(self.lista_ventas): # enumerate() da el indice y en este caso el diccionario de las ventas de cada producto
            pos_y = 110 + indice * 35
            linea = f'{venta["producto"]}:  {venta["cantidad"]} unidades  —  CRC {venta["cantidad"] * constantes.PRECIO:,}'
            ventana.blit(self.fuente.render(linea, True, (0, 0, 0)), (70, pos_y))
            # Dibuja cada línea (texto, suavizado, (color),(x , y))

        # Totales
        pygame.draw.line(ventana, (0, 0, 0), (50, 230), (750, 230), 1) # Dibuja la línea de separación

        ventana.blit(self.fuente.render(f"Total vendido:  {self.total_vendido} unidades", True, (0, 0, 0)), (50, 250))
        ventana.blit(self.fuente.render(f"Ganancias:  CRC {self.ganancias_colones:,}", True, (0, 0, 0)), (50, 290))
        ventana.blit(self.fuente.render(f"Ganancias:  USD {self.ganancias_dolares:.2f}", True, (0, 0, 0)), (50, 330))
        # Sobre la fuente se aplica render para dibujar el texto
        # :, formatea con comas de miles. Python automáticamente separa cada 3 dígitos (estándar internacional)
        # :.2f formatea el número como un float de dos decimales.
        # Después de los dos puntos se coloca el formato que se desea, en el primer caso separar por miles y
        # en el segundo float de dos decimales

