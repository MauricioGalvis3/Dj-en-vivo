class EffectStack:
    def __init__(self):
        # La pila almacenará las rutas de los archivos generados
        self.stack = []
    
    def push(self, audio_file_path):
        """Agrega un nuevo archivo (con efecto) a la pila."""
        self.stack.append(audio_file_path)
        print(f"-> Nuevo estado: {audio_file_path}")

    def pop(self):
        """Elimina el último efecto y devuelve el archivo anterior."""
        if len(self.stack) > 1:
            removed = self.stack.pop()
            print(f"<- Deshaciendo efecto: {removed}")
            return self.stack[-1] # El nuevo "tope" es el sonido anterior
        else:
            print("INFO: Ya estás en la canción original (Base).")
            return self.stack[0]

# Ejemplo de uso rápido:
if __name__ == "__main__":
    dj_pila = EffectStack()
    dj_pila.push("original.mp3")    # Estado 0
    dj_pila.push("con_eco.mp3")     # Estado 1
    dj_pila.push("en_reversa.mp3")  # Estado 2 (Tope de la pila)
    
    # Usuario presiona el botón "Deshacer"
    archivo_a_reproducir = dj_pila.pop() 
    print(f"Reproduciendo: {archivo_a_reproducir}") # Debería ser 'con_eco.mp3'