class EffectStack:
    def __init__(self):
        self.__items = []
        self.__labels = []

    def push(self, audio_segment, label="base"):
        """Agrega un nuevo estado de audio al tope de la pila."""
        self.__items.append(audio_segment)
        self.__labels.append(label)

    def pop(self):
        """Elimina el efecto más reciente y retorna el estado anterior."""
        if len(self.__items) > 1:
            self.__labels.pop()
            return self.__items.pop()
        return None

    def top(self):
        """Muestra qué hay en el tope sin sacarlo."""
        if not self.is_empty():
            return self.__items[-1]
        return None

    def get_labels(self):
        """Retorna la lista de nombres de efectos aplicados (sin el audio)."""
        return list(self.__labels)

    def is_empty(self):
        return len(self.__items) == 0

    def size(self):
        return len(self.__items)
