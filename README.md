

 DJ Stack Master Pro
1. Descripción General
DJ Stack Master Pro es un software de procesamiento de audio en tiempo real que utiliza el concepto de Edición No Destructiva. El programa permite cargar una biblioteca de música, aplicar múltiples efectos de sonido (reversa, velocidad, distorsión) y deshacer cambios de forma jerárquica.

El proyecto demuestra la implementación práctica de una Estructura de Datos Lineal (Pila) aplicada al procesamiento multimedia.

2. Arquitectura del Sistema
El software sigue un modelo de tres capas para garantizar la modularidad:

Lógica de Estructura (logic_stack.py): Implementa el TDA Pila (Stack) con operaciones push, pop, top, e is_empty.

Controlador de Audio (main_control.py): Gestiona la biblioteca de música, el procesamiento de señales mediante Pydub y la reproducción sincronizada con Pygame.

Interfaz Gráfica (gui_app.py): Desarrollada con CustomTkinter, permite la interacción visual con la música y la visualización de la pila.

3. Implementación de la Pila (Stack)
La estructura de datos Pila (LIFO - Last In, First Out) es el núcleo del editor:

Push: Cada vez que se aplica un efecto, el nuevo estado del audio se apila sobre el anterior.

Pop (Undo): Al deshacer un cambio, se elimina el elemento del tope, regresando instantáneamente al estado anterior de la canción.

Persistencia: Cada canción en la biblioteca posee su propia instancia de pila, permitiendo mantener el historial de cambios de forma independiente.

4. Tecnologías y Librerías
Python 3.12: Lenguaje base.

CustomTkinter: Interfaz de usuario moderna con soporte para modo oscuro.

Pygame (Mixer): Motor de reproducción de audio y control de volumen.

Pydub: Manipulación de archivos de audio a nivel de muestreo (frames).

FFmpeg: Motor externo necesario para la codificación y decodificación de formatos MP3/WAV.

5. Manual de Uso Rápido
Carga: El programa lee automáticamente los archivos en assets/music/.

Navegación: Use los botones ⏮ y ⏭ para saltar entre canciones (Navegación Circular).

Efectos: Seleccione cualquier efecto en el panel central. Estos se aplicarán sobre el punto actual de reproducción.

Búsqueda (Seek): Use la barra de progreso para saltar a cualquier punto de la canción.

Deshacer: Presione el botón rojo DESHACER para remover el último efecto aplicado desde la pila.
