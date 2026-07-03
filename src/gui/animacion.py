import customtkinter as ctk
from typing import Callable
import tkinter as tk
from src.utils.mathutils import create_math_label


class PanelAnimacion(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTkFrame) -> None:
        super().__init__(parent)
        self._crear_controles()

    def _crear_controles(self) -> None:
        btn_prev = ctk.CTkButton(self, text="Anterior")
        btn_prev.pack(side="left", padx=4, pady=6)
        btn_play = ctk.CTkButton(self, text="Play")
        btn_play.pack(side="left", padx=4, pady=6)
        btn_pause = ctk.CTkButton(self, text="Pausa")
        btn_pause.pack(side="left", padx=4, pady=6)
        btn_next = ctk.CTkButton(self, text="Siguiente")
        btn_next.pack(side="left", padx=4, pady=6)
        btn_reset = ctk.CTkButton(self, text="Reiniciar")
        btn_reset.pack(side="left", padx=4, pady=6)

        # Velocidad
        label_v = ctk.CTkLabel(self, text="Velocidad:")
        label_v.pack(side="left", padx=6)
        self.slider = ctk.CTkSlider(self, from_=0.1, to=2.0, number_of_steps=19)
        self.slider.set(1.0)
        self.slider.pack(side="left", padx=6)

        # Panel de info del paso -> use math text canvases
        self.info_frame = tk.Frame(self)
        self.info_frame.pack(side='left', padx=8)

        self.info_canvases = {}
        labels = [ (r"i", "Iteración"), (r"x_{n-1}", "x_{n-1}"), (r"f(x_{n-1})", "f(x_{n-1})"), (r"x_n", "x_n"), (r"f(x_n)", "f(x_n)"), (r"x_{n+1}", "x_{n+1}"), (r"Error", "Error") ]
        for latex, key in labels:
            frame = tk.Frame(self.info_frame)
            frame.pack(fill='x')
            canvas = create_math_label(frame, latex, tamaño=12, dpi=80, color='white')
            widget = canvas.get_tk_widget()
            widget.pack(fill='both', expand=True)
            self.info_canvases[key] = canvas

    def update_info(self, data: dict) -> None:
        # data expected keys: i, x_prev, f_prev, x_curr, f_curr, x_next, error
        try:
            self.info_canvases['Iteración'].math_update(str(data.get('i', '')))
            self.info_canvases['x_{n-1}'].math_update(rf"x_{{n-1}} = {data.get('x_prev', '')}")
            self.info_canvases['f(x_{n-1})'].math_update(rf"f(x_{{n-1}}) = {data.get('f_prev', '')}")
            self.info_canvases['x_n'].math_update(rf"x_n = {data.get('x_curr', '')}")
            self.info_canvases['f(x_n)'].math_update(rf"f(x_n) = {data.get('f_curr', '')}")
            self.info_canvases['x_{n+1}'].math_update(rf"x_{{n+1}} = {data.get('x_next', '')}")
            self.info_canvases['Error'].math_update(rf"Error = {data.get('error', '')}")
        except Exception:
            pass
