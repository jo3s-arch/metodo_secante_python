import customtkinter as ctk
from typing import Callable


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

        # Panel de info del paso
        self.info = ctk.CTkLabel(self, text="Paso 0 / 0")
        self.info.pack(side="left", padx=8)
