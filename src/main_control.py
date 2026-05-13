import os
import pygame
from pydub import AudioSegment
from logic.logic_stack import EffectStack 

class DJProController:
    def __init__(self, carpeta_musica):
        pygame.mixer.init()
        self.ruta_musica = carpeta_musica
        self.biblioteca = [f for f in os.listdir(carpeta_musica) if f.endswith(('.wav', '.mp3'))]
        self.indice_actual = 0
        self.pilas_por_cancion = {cancion: EffectStack() for cancion in self.biblioteca}
        self.temp_file = os.path.abspath("assets/temp/playback.wav")
        
        self.tiempo_inicio_ms = 0
        self.duracion_total_ms = 0
        
        self.cargar_cancion_actual()

    def cambiar_cancion(self, direccion):
        self.indice_actual = (self.indice_actual + direccion) % len(self.biblioteca)
        self.cargar_cancion_actual()

    def seleccionar_por_indice(self, num):
        if 0 <= num < len(self.biblioteca):
            self.indice_actual = num
            self.cargar_cancion_actual()
            
    def cargar_cancion_actual(self):
        cancion = self.biblioteca[self.indice_actual]
        pila = self.pilas_por_cancion[cancion]
        if pila.is_empty():
            ruta = os.path.join(self.ruta_musica, cancion)
            audio = AudioSegment.from_file(ruta)
            pila.push(audio, label="base")  # label base para el audio original
        
        self.duracion_total_ms = len(pila.top())
        self.tiempo_inicio_ms = 0
        self.play_current(desde_ms=0)

    def get_posicion_actual_ms(self):
        if not pygame.mixer.music.get_busy():
            return self.tiempo_inicio_ms
        return self.tiempo_inicio_ms + pygame.mixer.music.get_pos()

    def play_current(self, desde_ms=None):
        import time
        try:
            pos_actual = desde_ms if desde_ms is not None else self.get_posicion_actual_ms()
            
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            time.sleep(0.1)  # damos tiempo a Windows para liberar el archivo

            cancion = self.biblioteca[self.indice_actual]
            audio_pt = self.pilas_por_cancion[cancion].top()
            audio_pt.export(self.temp_file, format="wav")
            
            pygame.mixer.music.load(self.temp_file)
            
            self.tiempo_inicio_ms = pos_actual
            pygame.mixer.music.play(start=pos_actual / 1000.0)
        except Exception as e:
            print(f"Error en playback: {e}")

    def apply_effect(self, tipo):
        pos_donde_estaba = self.get_posicion_actual_ms()
        
        pila = self.pilas_por_cancion[self.biblioteca[self.indice_actual]]
        current = pila.top()
        nuevo = None

        if tipo == "reverse":
            nuevo = current.reverse()
        elif tipo == "fast": 
            new_rate = int(current.frame_rate * 1.2)
            nuevo = current._spawn(current.raw_data, overrides={'frame_rate': new_rate}).set_frame_rate(current.frame_rate)
        elif tipo == "slow":
            new_rate = int(current.frame_rate * 0.8)
            nuevo = current._spawn(current.raw_data, overrides={'frame_rate': new_rate}).set_frame_rate(current.frame_rate)
        elif tipo == "boost":
            nuevo = current + 8

        if nuevo:
            pila.push(nuevo, label=tipo)  # guardamos el nombre del efecto
            self.play_current(desde_ms=pos_donde_estaba)

    def undo(self):
        pos_actual = self.get_posicion_actual_ms()
        pila = self.pilas_por_cancion[self.biblioteca[self.indice_actual]]
        if pila.size() > 1:
            pila.pop()
            self.play_current(desde_ms=pos_actual)