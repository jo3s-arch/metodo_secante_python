from typing import Callable, Optional
import customtkinter as ctk
import tkinter as tk
from tkinter import Frame
from src.utils.mathutils import create_math_label


class Tooltip:
    """Simple tooltip for tkinter widgets."""
    def __init__(self, widget, text: str):
        self.widget = widget
        self.text = text
        self.tipwindow: Optional[tk.Toplevel] = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, _event=None):
        if self.tipwindow or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left', background='#333', foreground='white', relief='solid', borderwidth=1, padx=4, pady=2)
        label.pack()

    def hide(self, _event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None


class TecladoCientifico(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTkFrame, callback: Callable[[str], None]) -> None:
        super().__init__(parent)
        self.callback = callback
        self.buttons = []  # list of dicts: {'frame': tk.Frame, 'canvas': FigureCanvasTkAgg, 'latex': str, 'insert': str}
        self.btn_width = 56
        self.btn_height = 44
        self.font_size = 12
        self._crear_botones()

    def _crear_botones(self) -> None:
        # Define buttons rows as tuples: (latex_display, insert_text, tooltip)
        botones_rows = [
            [(r"\sin", "sin(", "Seno"),(r"\cos","cos(","Coseno"),(r"\tan","tan(","Tangente"),(r"\arcsin","asin(","Arco seno"),(r"\arccos","acos(","Arco coseno"),(r"\arctan","atan(","Arco tangente")],
            [(r"\sinh","sinh(","Seno hip."),(r"\cosh","cosh(","Coseno hip."),(r"\tanh","tanh(","Tang. hip."),(r"\ln","log(","Logaritmo natural"),(r"\log","log10(","Log base 10"),(r"\log_2","log2(","Log base 2"),(r"e^{x}","exp(","Exponencial")],
            [(r"\sqrt{x}","sqrt(","Raíz cuadrada"),(r"x^{2}","x**2","Potencia cuadrada"),(r"x^{3}","x**3","Potencia cúbica"),(r"n!","factorial(","Factorial"),(r"\frac{1}{x}","1/(","Reciproco"),(r"|x|","abs(","Valor absoluto"),(r"\pi","pi","Pi")],
            [("7","7","7"),("8","8","8"),("9","9","9"),(r"\div","/","División"),(r"\times","*","Multiplicación"),("^{ }","**","Potencia (**)"),("+","+","Suma")],
            [("4","4","4"),("5","5","5"),("6","6","6"),("-","-","Resta"),("(","(","Paréntesis apertura"),(")",")","Paréntesis cierre"),("x","x","Variable x")],
            [("1","1","1"),("2","2","2"),("3","3","3"),(".",".","Punto decimal"),("0","0","0"),("C","C","Limpiar campo"),("⌫","\b","Borrar último")],
        ]

        for r, row in enumerate(botones_rows):
            for c, (latex_disp, insert_text, tooltip) in enumerate(row):
                # Create a small tk.Frame as container for the matplotlib canvas
                container = tk.Frame(self, bg='')
                container.grid(row=r, column=c, padx=6, pady=6, sticky='nsew')
                # Create math canvas inside container
                canvas = create_math_label(container, latex_disp, tamaño=self.font_size, dpi=80, color='white')
                widget = canvas.get_tk_widget()
                widget.pack(fill='both', expand=True)
                # Bind click on the tk widget
                widget.bind('<Button-1>', lambda ev, val=insert_text: self._on_press(val))
                Tooltip(widget, tooltip)
                self.buttons.append({'frame': container, 'canvas': canvas, 'latex': latex_disp, 'insert': insert_text})

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
        # Apply to existing button canvases by updating their font size
        for b in self.buttons:
            try:
                canvas = b['canvas']
                # call the attached math_update to update font size
                try:
                    canvas.math_update(b['latex'], tamaño_nuevo=self.font_size)
                except Exception:
                    # fallback: redraw with same latex
                    canvas.math_update(b['latex'])
            except Exception:
                pass
