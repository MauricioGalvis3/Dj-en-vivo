import customtkinter as ctk
from main_control import DJProController
import pygame

class DJGui(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DJ STACK MASTER - V2 PRO")
        self.geometry("1000x650")
        self.dj = DJProController("assets/music")
        self.is_paused = False

        # --- UI SETUP ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar: Pila de Reproducción
        self.sidebar = ctk.CTkFrame(self, width=250)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        ctk.CTkLabel(self.sidebar, text="LISTA DE REPRODUCCIÓN", font=("Arial", 16, "bold")).pack(pady=10)
        self.playlist_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.playlist_frame.pack(fill="both", expand=True)

        # Main Panel
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.song_label = ctk.CTkLabel(self.main_frame, text="Song Name", font=("Arial", 22, "bold"), text_color="#1ABC9C")
        self.song_label.pack(pady=20)

        # BARRA DE PROGRESO INTERACTIVA
        self.progress_slider = ctk.CTkSlider(self.main_frame, from_=0, to=100, command=self.seek_audio)
        self.progress_slider.pack(pady=5, padx=30, fill="x")
        
        self.time_label = ctk.CTkLabel(self.main_frame, text="00:00 / 00:00", font=("Consolas", 14))
        self.time_label.pack()

        # CONTROLES
        self.controls = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.controls.pack(pady=20)
        ctk.CTkButton(self.controls, text="⏮", width=60, command=lambda: self.change_song(-1)).pack(side="left", padx=10)
        self.play_btn = ctk.CTkButton(self.controls, text="⏸", width=60, command=self.toggle_play)
        self.play_btn.pack(side="left", padx=10)
        ctk.CTkButton(self.controls, text="⏭", width=60, command=lambda: self.change_song(1)).pack(side="left", padx=10)

        # EFECTOS (Ahora todos presentes)
        self.eff_frame = ctk.CTkLabel(self.main_frame, text="EFECTOS DE PILA (STACK)", font=("Arial", 14, "bold"))
        self.eff_frame.pack(pady=(20, 5))
        
        self.btn_grid = ctk.CTkFrame(self.main_frame)
        self.btn_grid.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(self.btn_grid, text="🌀 Reversa", command=lambda: self.apply("reverse")).grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkButton(self.btn_grid, text="⏩ Rápido", command=lambda: self.apply("fast")).grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkButton(self.btn_grid, text="⏪ Lento", command=lambda: self.apply("slow")).grid(row=0, column=2, padx=10, pady=10)
        ctk.CTkButton(self.btn_grid, text="🔥 BOOST", command=lambda: self.apply("boost")).grid(row=0, column=3, padx=10, pady=10)

        ctk.CTkButton(self.main_frame, text="🔙 DESHACER ÚLTIMO CAMBIO (POP)", fg_color="#C0392B", command=self.undo).pack(pady=20)

        # Iniciar el bucle de actualización de la barra
        self.update_ui_loop()
        self.actualizar_lista_visual()

    def format_time(self, ms):
        seconds = int((ms / 1000) % 60)
        minutes = int((ms / (1000 * 60)) % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def update_ui_loop(self):
        # Obtener tiempos del controlador
        actual = self.dj.get_posicion_actual_ms()
        total = self.dj.duracion_total_ms
        
        # Actualizar barra y etiquetas
        if total > 0:
            porcentaje = (actual / total) * 100
            self.progress_slider.set(porcentaje)
            
            tiempo_restante = total - actual
            self.time_label.configure(text=f"{self.format_time(actual)} / -{self.format_time(tiempo_restante)}")

        # Cambiar nombre si es necesario
        self.song_label.configure(text=self.dj.biblioteca[self.indice_actual_check()])
        
        # Repetir cada 500ms
        self.after(500, self.update_ui_loop)

    def indice_actual_check(self): return self.dj.indice_actual

    def seek_audio(self, value):
        # value viene de 0 a 100 (porcentaje del slider)
        nuevo_ms = (value / 100) * self.dj.duracion_total_ms
        self.dj.play_current(desde_ms=nuevo_ms)

    def change_song(self, dir):
        self.dj.cambiar_cancion(dir)
        self.actualizar_lista_visual()

    def toggle_play(self):
        self.is_paused = not self.is_paused
        pygame.mixer.music.pause() if self.is_paused else pygame.mixer.music.unpause()
        self.play_btn.configure(text="▶" if self.is_paused else "⏸")

    def apply(self, t): self.dj.apply_effect(t)
    def undo(self): self.dj.undo()

    def actualizar_lista_visual(self):
        # Limpiamos el panel lateral
        for w in self.playlist_frame.winfo_children(): 
            w.destroy()
            
        nombre_actual = self.dj.biblioteca[self.dj.indice_actual]
        
        # 'reversed' hace que la última canción de la lista aparezca ARRIBA
        for c in reversed(self.dj.biblioteca):
            # Si es la que está sonando, le ponemos un color especial (El Tope)
            es_el_tope = (c == nombre_actual)
            color_bg = "#1ABC9C" if es_el_tope else "#2C3E50"
            texto = f"⭐ {c[:20]}" if es_el_tope else f"  {c[:20]}"
            
            label = ctk.CTkLabel(
                self.playlist_frame, 
                text=texto, 
                fg_color=color_bg, 
                corner_radius=8,
                height=35,
                font=("Arial", 13, "bold" if es_el_tope else "normal")
            )
            label.pack(pady=3, padx=10, fill="x")

if __name__ == "__main__":
    app = DJGui()
    app.mainloop()