# pantallas/pantalla_dashboard.py
# Muestra el stock de los 3 productos y el botón de mantenimiento.

import pygame
import constantes
import comunicacion


class PantallaDashboard:

    def __init__(self, fuente, datos, ip):
        self.fuente = fuente
        self.ip     = ip

        # datos["stock"] diccionario con diccionarios = {"Coca-Cola": {"nombre": "Coca-Cola", "stock": 5}, ...}
        self.lista_stock = list(datos["stock"].values()) # Saca solo los valores y los ingresa a una lista. En este caso son los subdiccionarios

        
        self.mantenimiento_activo = False

        # Botones de navegación y mantenimiento
        self.rect_btn_stats = pygame.Rect(650, 10, 130, 35) # Botón para regresar a la pantalla de estadísticas
        self.rect_btn_mant  = pygame.Rect(290, 400, 220, 40) # Botón para hacer mantenimiento

    def manejar_evento(self, evento):
        """
        Retorna el nombre de la pantalla a la que hay que ir,
        o None si no hay cambio.
        """
        if evento.type == pygame.MOUSEBUTTONDOWN:

            if self.rect_btn_stats.collidepoint(evento.pos):
                return constantes.PANTALLA_ESTADISTICAS
            #Verifica que se clickeara el botón de estadísticas para devolver la pantalla de estadísticas para cambiarla en el bucle principal

            if self.rect_btn_mant.collidepoint(evento.pos):
                self.mantenimiento_activo = not self.mantenimiento_activo # not invierte el valor, en este caso de False a True
                comunicacion.enviar_mantenimiento(self.ip)
            # Llama a enviar el mantenimiento si se clickea el botón del mantenimiento

        return None


    def dibujar(self, ventana):
        ventana.fill((255, 255, 255)) #Color blanco del fondo

        # Barra de navegación
        pygame.draw.rect(ventana, (220, 220, 220), pygame.Rect(0, 0, constantes.ANCHO, 50)) # Barra gris de arriba
        ventana.blit(self.fuente.render("Dashboard", True, (0, 0, 0)), (10, 15)) # Texto de dashboard

        pygame.draw.rect(ventana, (200, 200, 200), self.rect_btn_stats) # Botón de estadísticas
        pygame.draw.rect(ventana, (0, 0, 0), self.rect_btn_stats, 1) # Borde del botón de color negro

        ventana.blit(self.fuente.render("Estadísticas", True, (0, 0, 0)), (self.rect_btn_stats.x + 5, self.rect_btn_stats.y + 8)) # Texto de estadísticas dentro del botón

        # Aviso de mantenimiento
        if self.mantenimiento_activo:
            ventana.blit(self.fuente.render("** MAQUINA EN MANTENIMIENTO **", True, (200, 100, 0)), (230, 60)) #Muestra un texto de aviso si el mantenimiento está activo

        # Tarjetas de stock (una por producto)
        for indice, producto in enumerate(self.lista_stock):
            # enumerate() da el índice (0,1,2) y el elemento al mismo tiempo

            pos_x = 60 + indice * 240
            pos_y = 100

            pygame.draw.rect(ventana, (240, 240, 240), pygame.Rect(pos_x, pos_y, 200, 150)) # Dibuja los rectangulos grises donde aparece el stock
            pygame.draw.rect(ventana, (0, 0, 0),       pygame.Rect(pos_x, pos_y, 200, 150), 2) # Dibuja sus bordes

            ventana.blit(self.fuente.render(producto["nombre"],          True, (0, 0, 0)),   (pos_x + 10, pos_y + 15)) # Dibuja el nombre del producto
            ventana.blit(self.fuente.render(f'Stock: {producto["stock"]}', True, (0, 0, 0)), (pos_x + 10, pos_y + 55)) # Dibuja su stock

            if producto["stock"] == 0:
                color_estado = (200, 0, 0) # Rojo si no hay stock
                texto_estado = "Sin stock"
            else:
                color_estado = (0, 150, 0) # Verde si sí hay stock
                texto_estado = "Disponible"

            ventana.blit(self.fuente.render(texto_estado, True, color_estado), (pos_x + 10, pos_y + 95)) # Dibuja los estados para cada producto

        # Botón mantenimiento
        texto_mant = "Desactivar Mant." if self.mantenimiento_activo else "Activar Mant."  # Si el mantenimiento está desactivado el texto del botón es Activar Mant. por el contrario, es Desactivar Mant.
        pygame.draw.rect(ventana, (200, 200, 200), self.rect_btn_mant) # Dibuja el rectangulo gris para el botón
        pygame.draw.rect(ventana, (0, 0, 0),       self.rect_btn_mant, 2) # Dibuja su borde
        ventana.blit(self.fuente.render(texto_mant, True, (0, 0, 0)), (self.rect_btn_mant.x + 20, self.rect_btn_mant.y + 10)) # Dibuja el texto dependiendo del estado del mantenimiento.
