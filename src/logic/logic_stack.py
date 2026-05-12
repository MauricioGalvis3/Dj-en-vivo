class EffectStack:
    def __init__(self):
        # Usamos una lista 
        self.__items = []

    def push(self, audio_segment):
        """Agrega un nuevo estado de audio al tope de la pila."""
        self.__items.append(audio_segment)

    def pop(self):
        """Elimina el efecto más reciente y retorna el estado anterior."""
        if len(self.__items) > 1:
            return self.__items.pop()
        return None

    def top(self):
        """Muestra qué hay en el tope sin sacarlo."""
        if not self.is_empty():
            return self.__items[-1]
        return None

    def is_empty(self):
        return len(self.__items) == 0

    def size(self):
        return len(self.__items)