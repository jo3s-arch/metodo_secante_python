from typing import Callable, Optional
import customtkinter as ctk
from tkinter import Frame, Button


class TecladoCientifico(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTkFrame, callback: Callable[[str], None]) -> None:
        super().__init__(parent)
        self.callback = callback
        self._crear_botones()

    def _crear_botones(self) -> None:
        botones = [
            "sin","cos","tan","asin","acos","atan",
            "sinh","cosh","tanh","ln","log","log2","exp","sqrt","^2","^3","fact","1/x","abs","pi","pi/2","2*pi","e",
            "7","8","9","/","*","^","+",
            "4","5","6","-","(",")","x",
            "1","2","3",".","0","C","⌫"
        ]

        # Crear en grid simple
        r = 0
        c = 0
        for i, b in enumerate(botones):
            btn = ctk.CTkButton(self, text=b, width=48, command=lambda val=b: self._on_press(val))
            btn.grid(row=r, column=c, padx=2, pady=2)
            c += 1
            if c >= 7:
                c = 0
                r += 1

    def _on_press(self, val: str) -> None:
        if val == "C":
            self.callback("")
            return
        if val == "⌫":
            # send backspace signal
            self.callback("\b")
            return
        # map some labels to texto insertable
        mapping = {
            "sqrt": "sqrt(",
            "^2": "**2",
            "^3": "**3",
            "fact": "factorial(",
            "pi": "pi",
            "pi/2": "pi/2",
            "2*pi": "2*pi",
            "ln": "log",
            "x": "x",
            "e": "E",
            "/": "/",
            "*": "*",
        }
        texto = mapping.get(val, val)
        self.callback(texto)
