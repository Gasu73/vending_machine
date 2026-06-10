# pantallas/pantalla_conexion.py
# Campo de texto para escribir la IP de la Pico W y botón para conectar.

# Imports
import pygame
import comunicacion


class PantallaConexion:

    def __init__(self, fuente):
        self.fuente          = fuente
        self.ip_escrita      = ""
        self.mensaje_error   = ""
        self.datos_recibidos = None   # Se llena cuando la conexión es exitosa

        # Rectángulos del campo IP y el botón (los definimos fijos)
        self.rect_campo  = pygame.Rect(300, 220, 200, 35) # (x, y, largo, alto)
        self.rect_boton  = pygame.Rect(330, 280, 140, 40)
        self.campo_activo = True


    def manejar_evento(self, evento):
        # Si el evento es un click del mouse
        if evento.type == pygame.MOUSEBUTTONDOWN:
            self.campo_activo = self.rect_campo.collidepoint(evento.pos)
            # Confirma que clicke el campo IP
            # collidepoint() verifica que un punto esté dentro de un rectángulo
            # evento.pos: posición de x, y del mouse en ese momento

            if self.rect_boton.collidepoint(evento.pos):
                self._conectar()
                # Confirma que clicke el botón

        # Si el evento es presionar una tecla
        if evento.type == pygame.KEYDOWN:
            if not self.campo_activo:
                return # Si el campo no está activo no ocurre nada

            if evento.key == pygame.K_RETURN:
                self._conectar() # Conectar al presionar enter

            elif evento.key == pygame.K_BACKSPACE:
                self.ip_escrita = self.ip_escrita[:-1] # Borrar letra en el campo con slicing de strings

            else:
                # Solo aceptamos números y puntos (caracteres válidos de una IP)
                if evento.unicode.isdigit() or evento.unicode == ".":
                    if len(self.ip_escrita) < 15:
                        self.ip_escrita += evento.unicode # Verifica que no sea más largo que 15 dígitos
                # evento.unicode: carácter que genera la tecla al presionarla
                # isdigit(): metodo de stings que evalúa si el texto son solo dígitos


    def _conectar(self):
        if self.ip_escrita.strip() == "":
            self.mensaje_error = "Escribe una IP."
            return
            # Si la IP está vacía actualiza el mensaje de error y no hace nada

        datos = comunicacion.pedir_datos(self.ip_escrita.strip()) # datos es un diccionario

        if datos is None:
            self.mensaje_error = "No se pudo conectar. Verifique la IP." # Esto en caso de error al conectar IP
        else:
            datos["ip"] = self.ip_escrita.strip() # Nueva clave con la ip de la Rasp para usos posteriores
            self.datos_recibidos = datos


    def dibujar(self, ventana):
        ventana.fill((255, 255, 255)) # Pintar ventana de blanco

        ventana.blit(self.fuente.render("CElect Admin", True, (0, 0, 0)), (340, 140))
        ventana.blit(self.fuente.render("IP de la Pico W:", True, (0, 0, 0)), (335, 195))
        # blit lo dibuja en pantalla y render convierte texto a imagen
        # Los parámetros son (texto, suavizado, color negro, xy)

        # Campo de texto: borde azul si está activo, negro si no
        color_borde = (0, 0, 255) if self.campo_activo else (0, 0, 0)

        pygame.draw.rect(ventana, (240, 240, 240), self.rect_campo) # Campo para la ip
        pygame.draw.rect(ventana, color_borde, self.rect_campo, 2) # Último parametro es el borde
        ventana.blit(self.fuente.render(self.ip_escrita, True, (0, 0, 0)), (self.rect_campo.x + 5, self.rect_campo.y + 7)) # Texto dentro del campo

        # Botón conectar
        pygame.draw.rect(ventana, (200, 200, 200), self.rect_boton)
        pygame.draw.rect(ventana, (0, 0, 0), self.rect_boton, 2)
        ventana.blit(self.fuente.render("Conectar", True, (0, 0, 0)), (self.rect_boton.x + 30, self.rect_boton.y + 10))

        if self.mensaje_error != "":
            ventana.blit(self.fuente.render(self.mensaje_error, True, (200, 0, 0)), (250, 340))
            # Si el mensaje de error no es vacío muestra el mensaje de error en pantalla como una imagen del texto
