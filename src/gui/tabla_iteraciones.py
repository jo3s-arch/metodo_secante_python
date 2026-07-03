from typing import List, Any
import tkinter as tk
from tkinter import ttk
from src.utils.mathutils import create_math_label


class TablaIteraciones(ttk.Frame):
    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent)
        # Header frame with MathText labels
        self.header_frame = tk.Frame(self)
        self.header_frame.pack(fill='x', padx=4, pady=(4,0))

        headers = [r"i", r"x_{n-1}", r"x_n", r"x_{n+1}", r"f(x_{n-1})", r"f(x_n)", r"Error"]
        self.header_canvases = []
        for h in headers:
            frame = tk.Frame(self.header_frame)
            frame.pack(side='left', fill='x', expand=True, padx=2)
            canvas = create_math_label(frame, h, tamaño=12, dpi=80, color='white')
            widget = canvas.get_tk_widget()
            widget.pack(fill='both', expand=True)
            self.header_canvases.append(canvas)

        self.tree = ttk.Treeview(self, columns=("i","xn_1","xn","xn1","fxn_1","fxn","error"), show="headings")
        # Keep headings plain for accessibility, tree view will be below custom headers
        self.tree.heading("i", text="i")
        self.tree.heading("xn_1", text="x_{n-1}")
        self.tree.heading("xn", text="x_n")
        self.tree.heading("xn1", text="x_{n+1}")
        self.tree.heading("fxn_1", text="f(x_{n-1})")
        self.tree.heading("fxn", text="f(x_n)")
        self.tree.heading("error", text="Error")
        # Configure column widths and anchors
        self.tree.column("i", width=60, anchor='center')
        self.tree.column("xn_1", width=180, anchor='e')
        self.tree.column("xn", width=180, anchor='e')
        self.tree.column("xn1", width=180, anchor='e')
        self.tree.column("fxn_1", width=180, anchor='e')
        self.tree.column("fxn", width=180, anchor='e')
        self.tree.column("error", width=140, anchor='e')
        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side='right', fill='y')
        self.tree.pack(fill="both", expand=True)

    def cargar_datos(self, datos: List[dict]) -> None:
        self.limpiar()
        for fila in datos:
            self.tree.insert("", "end", values=(
                fila.get("i"),
                f"{fila.get('x_prev'):.8g}" if fila.get('x_prev') is not None else '',
                f"{fila.get('x_curr'):.8g}" if fila.get('x_curr') is not None else '',
                f"{fila.get('x_next'):.8g}" if fila.get('x_next') is not None else '',
                f"{fila.get('f_prev'):.8g}" if fila.get('f_prev') is not None else '',
                f"{fila.get('f_curr'):.8g}" if fila.get('f_curr') is not None else '',
                f"{fila.get('error'):.8g}" if fila.get('error') is not None else '',
            ))

    def limpiar(self) -> None:
        for i in self.tree.get_children():
            self.tree.delete(i)
