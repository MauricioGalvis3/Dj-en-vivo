class EffectStack:
    def __init__(self):
        self.__items = []
        self.__labels = []  # 👈 guardamos el nombre de cada efecto

    def push(self, audio_segment, label="base"):  # 👈 label opcional
        self.__items.append(audio_segment)
        self.__labels.append(label)

    def pop(self):
        if len(self.__items) > 1:
            self.__labels.pop()
            return self.__items.pop()
        return None

    def top(self):
        if not self.is_empty():
            return self.__items[-1]
        return None

    def get_labels(self):  # 👈 método público para la GUI
        return list(self.__labels)

    def is_empty(self):
        return len(self.__items) == 0

    def size(self):
        return len(self.__items)