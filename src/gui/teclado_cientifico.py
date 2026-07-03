from typing import Callable, Optional
import customtkinter as ctk
from tkinter import Frame, Button, Toplevel, Label
import tkinter.font as tkfont


class Tooltip:
    """Simple tooltip for tkinter widgets."""
    def __init__(self, widget, text: str):
        self.widget = widget
        self.text = text
        self.tipwindow: Optional[Toplevel] = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, _event=None):
        if self.tipwindow or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = Label(tw, text=self.text, justify='left', background='#333', foreground='white', relief='solid', borderwidth=1, padx=4, pady=2)
        label.pack()

    def hide(self, _event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None


class TecladoCientifico(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTkFrame, callback: Callable[[str], None]) -> None:
        super().__init__(parent)
        self.callback = callback
        self.buttons = []
        self.btn_width = 56
        self.btn_height = 44
        self.font_size = 12
        self._crear_botones()

    def _crear_botones(self) -> None:
        # Buttons layout definition (label, insert_text, tooltip)
        botones = [
            ("sin", "sin(", "Seno"),("cos","cos(","Coseno"),("tan","tan(","Tangente"),("asin","asin(","Arco seno"),("acos","acos(","Arco coseno"),("atan","atan(","Arco tangente"),
        ]
        # Continue building buttons as tuples in rows
        botones_rows = [
            [ ("sin", "sin(", "Seno"),("cos","cos(","Coseno"),("tan","tan(","Tangente"),("asin","asin(","Arco seno"),("acos","acos(","Arco coseno"),("atan","atan(","Arco tangente") ],
            [ ("sinh","sinh(","Seno hip.") , ("cosh","cosh(","Coseno hip."), ("tanh","tanh(","Tang. hip."), ("ln","log(","Logaritmo natural"), ("log","log10(","Log base 10"), ("log2","log2(","Log base 2"), ("exp","exp(","Exponencial") ],
            [ ("sqrt","sqrt(","Raíz cuadrada"), ("x**2","x**2","Potencia cuadrada"), ("x**3","x**3","Potencia cúbica"), ("factorial","factorial(","Factorial"), ("1/x","1/(","Reciproco"), ("abs","abs(","Valor absoluto"), ("pi","pi","Pi") ],
            [ ("7","7","7"), ("8","8","8"), ("9","9","9"), ("/","/","División"), ("*","*","Multiplicación"), ("**","**","Potencia (**)"), ("+","+","Suma") ],
            [ ("4","4","4"), ("5","5","5"), ("6","6","6"), ("-","-","Resta"), ("(","(","Paréntesis apertura"), (")",")","Paréntesis cierre"), ("x","x","Variable x") ],
            [ ("1","1","1"), ("2","2","2"), ("3","3","3"), (".",".","Punto decimal"), ("0","0","0"), ("C","C","Limpiar campo"), ("⌫","\b","Borrar último") ],
        ]

        for r, row in enumerate(botones_rows):
            for c, (label, insert_text, tooltip) in enumerate(row):
                btn = ctk.CTkButton(self, text=label, width=self.btn_width, height=self.btn_height,
                                    command=lambda val=insert_text: self._on_press(val))
                btn.grid(row=r, column=c, padx=6, pady=6, sticky='nsew')
                Tooltip(btn, tooltip)
                self.buttons.append(btn)

        # Make grid cells expand equally
        for i in range(len(botones_rows)):
            self.grid_rowconfigure(i, weight=1)
        for j in range(len(botones_rows[0])):
            self.grid_columnconfigure(j, weight=1)

    def _on_press(self, val: str) -> None:
        if val == "C":
            self.callback("")
            return
        if val == "\b":
            self.callback("\b")
            return
        # Insert the given text (already python-friendly)
        self.callback(val)

    def set_button_size(self, width: int, height: int, font_size: int) -> None:
        self.btn_width = width
        self.btn_height = height
        self.font_size = font_size
        # Apply to existing buttons
        for b in self.buttons:
            try:
                b.configure(width=self.btn_width, height=self.btn_height)
                # customtkinter doesn't expose font directly on button in some versions; try config
                b.configure(font=(None, self.font_size))
            except Exception:
                pass
