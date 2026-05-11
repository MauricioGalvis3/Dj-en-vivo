import os
from pydub import AudioSegment
from logic.logic_stack import EffectStack

class DJController:
    def __init__(self, archivo_base):
        # 1. Inicializamos la Pila
        self.pila_estados = EffectStack()
        
        # 2. Definimos la ruta de la canción original
        self.ruta_original = os.path.join("assets", "music", archivo_base)
        
        # Metemos el estado inicial a la pila
        self.pila_estados.push(self.ruta_original)
        
        # Contador para nombrar los archivos temporales de forma única
        self.contador_cambios = 0

    def aplicar_reversa(self):
        """Toma el audio actual, lo invierte y lo guarda en la pila."""
        print("\n--- Procesando Reversa ---")
        
        # A. Obtener el audio que está en el "Tope" de la pila actualmente
        ruta_actual = self.pila_estados.current_state()
        audio = AudioSegment.from_file(ruta_actual)
        
        # B. Aplicar el efecto (Lógica de Pydub)
        audio_invertido = audio.reverse()
        
        # C. Guardar el nuevo archivo temporal
        self.contador_cambios += 1
        nombre_temp = f"edit_rev_{self.contador_cambios}.wav"
        ruta_temp = os.path.join("assets", "temp", nombre_temp)
        
        audio_invertido.export(ruta_temp, format="wav")
        
        # D. REGISTRAR EN LA PILA (Paso clave del proyecto)
        self.pila_estados.push(ruta_temp)
        
        return ruta_temp

    def deshacer_cambio(self):
        """Ejecuta el POP de la pila y devuelve el audio anterior."""
        print("\n--- Deshaciendo último efecto ---")
        return self.pila_estados.pop()

# --- PRUEBA DE FUNCIONAMIENTO ---
if __name__ == "__main__":
    # IMPORTANTE: Asegúrate de tener 'track1.wav' en assets/music/
    mi_dj = DJController("track1.wav")
    
    # Aplicamos reversa una vez
    paso1 = mi_dj.aplicar_reversa()
    
    # Aplicamos reversa otra vez (volvería al estado original, pero en un nuevo archivo)
    paso2 = mi_dj.aplicar_reversa()
    
    # DESHACER: Volvemos al estado después del primer efecto
    volver_atrás = mi_dj.deshacer_cambio()
    print(f"Ahora el audio activo es: {volver_atrás}")